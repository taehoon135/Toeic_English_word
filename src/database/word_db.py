from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase, DB_PATH
import csv
import os

# 사용자별 틀린 횟수 SQL (word_db / quiz_db / category_db 공용)
# 단어 + 해당 사용자의 wrong_count. 파라미터: (user_id,) — user_id가 None이면 wrong_count는 0
WORD_WITH_WRONG_COUNT = """
    SELECT w.*, COALESCE(uw.wrong_count, 0) AS wrong_count
    FROM Word w
    LEFT JOIN UserWord uw ON uw.word_id = w.word_id AND uw.user_id = ?
"""
WRONG_COUNT_UP = """
    INSERT INTO UserWord (user_id, word_id, wrong_count) VALUES (?, ?, 1)
    ON CONFLICT(user_id, word_id) DO UPDATE SET wrong_count = wrong_count + 1
"""
WRONG_COUNT_DOWN = "UPDATE UserWord SET wrong_count = MAX(wrong_count - 1, 0) WHERE user_id = ? AND word_id = ?"

class WordDB(BaseDatabase):
    """
    단어 데이터베이스 관리 클래스
    - 단어 추가, 수정, 삭제, 조회 기능 제공
    - CSV 파일에서 단어 가져오기 기능 제공
    - 카테고리와 단어 연결 관리
    """
    def __init__(self, db_path: str = DB_PATH):
        super().__init__(db_path)
        self.initialize_tables()  # DB 테이블 초기화

    def initialize_tables(self):
        """실제 앱 DB가 비어 있으면 toeic_words.csv로 단어를 채웁니다. (테이블 생성은 BaseDatabase)"""
        # 실제 앱 DB가 비어있을 때만 CSV로 초기 단어를 채움 (테스트용 임시 DB는 비워둠)
        if self.db_path != DB_PATH:
            return
        word_count = self.fetch_one("SELECT COUNT(*) as count FROM Word")
        if word_count and word_count['count'] == 0:
            # CSV 파일 경로 설정
            csv_path = os.path.join(os.path.dirname(__file__), "toeic_words.csv")
            if os.path.exists(csv_path):
                print("[DEBUG] CSV 파일에서 단어를 가져옵니다...")
                self.import_from_csv(csv_path)
                print("[DEBUG] CSV 파일 가져오기 완료")
            else:
                print("[DEBUG] CSV 파일을 찾을 수 없습니다.")

    def add_word(self, english: str, meaning: str, part_of_speech: str = None, example_sentence: str = None) -> int:
        """
        새로운 단어를 추가하거나 기존 단어의 ID를 반환합니다.
        Args:
            english: 영어 단어
            meaning: 한글 의미
            part_of_speech: 품사 (선택)
            example_sentence: 예문 (선택)
        Returns:
            int: 단어 ID (성공 시) 또는 None (실패 시)
        """
        try:
            # 중복 단어 체크
            existing = self.fetch_one("SELECT word_id FROM Word WHERE english = ?", (english,))
            if existing:
                return existing['word_id']  # 기존 단어의 ID 반환
            
            # 새 단어 추가
            if not self.execute(
                "INSERT INTO Word (english, meaning, part_of_speech, example_sentence) VALUES (?, ?, ?, ?)",
                (english, meaning, part_of_speech, example_sentence)
            ):  # CHECK 위반 (빈 단어/뜻)
                self.rollback()
                return None
            self.commit()
            return self.cursor.lastrowid  # 새로 추가된 단어의 ID 반환
        except Exception as e:
            print(f"단어 추가 오류: {e}")
            self.rollback()
            return None

    def import_from_csv(self, csv_path: str) -> bool:
        """
        CSV 파일에서 단어를 가져옵니다.
        Args:
            csv_path: CSV 파일 경로
        Returns:
            bool: 성공 여부
        """
        try:
            processed_rows = 0
            added_words = 0
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    processed_rows += 1
                    english = row.get('english', '').strip()
                    meaning = row.get('meaning', '').strip()
                    
                    if not english or not meaning:
                        print(f"Skipping row due to empty english or meaning: {row}")
                        continue

                    part_of_speech = row.get('part_of_speech', '').strip()
                    example_sentence = row.get('example_sentence', '').strip()

                    # 단어 추가
                    word_id = self.add_word(english, meaning, part_of_speech, example_sentence)
                    
                    if word_id:
                        added_words += 1
                    else:
                        print(f"Failed to add word '{english}'.")
            
            print(f"CSV Import Summary: Processed {processed_rows} rows. Words added: {added_words}")
            return True
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_path}")
            return False
        except Exception as e:
            print(f"Error during CSV import: {e}")
            return False

    def get_all_words(self, user_id: Optional[int] = None) -> List[Dict]:
        """
        모든 단어 목록을 조회합니다.
        Returns:
            List[Dict]: 단어 목록 (모든 컬럼 + 해당 사용자의 wrong_count)
        """
        return self.fetch_all(WORD_WITH_WRONG_COUNT + " ORDER BY w.word_id", (user_id,))

    def search_words(self, keyword: str) -> List[Dict]:
        """
        단어를 검색합니다 (영어/한글).
        Args:
            keyword: 검색어
        Returns:
            List[Dict]: 검색된 단어 목록
        """
        keyword_param = f"%{keyword}%"
        return self.fetch_all(
            """
            SELECT * FROM Word
            WHERE english LIKE ? OR meaning LIKE ?
            ORDER BY english
            """,
            (keyword_param, keyword_param)
        )

    def update_word(self, word_id: int, word: str, meaning: str, part_of_speech: str, example: str) -> bool:
        """
        단어 정보를 수정합니다.
        Args:
            word_id: 수정할 단어 ID
            word: 영어 단어
            meaning: 한글 의미
            part_of_speech: 품사
            example: 예문
        Returns:
            bool: 성공 여부
        """
        try:
            self.execute(
                """
                UPDATE Word
                SET english = ?, meaning = ?, part_of_speech = ?, example_sentence = ?
                WHERE word_id = ?
                """,
                (word, meaning, part_of_speech, example, word_id)
            )
            self.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.rollback()
            print(f"단어 수정 오류: {e}")
            return False

    def delete_word(self, word_id: int) -> bool:
        """
        단어를 삭제합니다.
        Args:
            word_id: 삭제할 단어 ID
        Returns:
            bool: 성공 여부
        """
        try:
            self.execute("DELETE FROM Word WHERE word_id = ?", (word_id,))
            self.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.rollback()
            print(f"단어 삭제 오류: {e}")
            return False

    def update_wrong_count(self, word_id: int, user_id: int) -> bool:
        """해당 사용자의 단어 틀린 횟수를 1 증가시킵니다."""
        if not self.execute(WRONG_COUNT_UP, (user_id, word_id)):
            self.rollback()
            return False
        self.commit()
        return True

    def get_wrong_count(self, word_id: int, user_id: int) -> int:
        """해당 사용자의 단어 틀린 횟수 (기록이 없으면 0)."""
        row = self.fetch_one("SELECT wrong_count FROM UserWord WHERE user_id = ? AND word_id = ?", (user_id, word_id))
        return row['wrong_count'] if row else 0

# 모듈 레벨에서 인스턴스 생성 - 메인 프로그램에서 사용되는 전역 인스턴스
word_db = WordDB() 
