from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase, DB_PATH
import csv
import os
# import sqlite3 # sqlite3 모듈이 직접 사용되지 않으면 삭제 가능
# from .category_db import CategoryDB # CategoryDB 임포트 (순환참조 주의하며 실제 경로로)
# 위 임포트가 순환 참조를 일으키면, category_db: 'CategoryDB' 타입 힌트 사용

# word_db.py 상단에 추가 (실제 CategoryDB 위치에 따라 경로 조정 필요)
# from ..category_db import CategoryDB # 만약 category_db가 database 폴더 밖에 있다면
# 여기서는 같은 폴더라 가정하고 from .category_db import CategoryDB

# 클래스 정의 전에 임포트하는 것이 일반적
# 이 예제에서는 CategoryDB가 같은 디렉토리에 있다고 가정합니다.
# 실제 프로젝트 구조에 따라 from src.database.category_db import CategoryDB 등이 될 수 있습니다.
# 순환 참조를 피하기 위해, 함수 시그니처에서 'CategoryDB' 문자열 힌트를 사용하는 것이 더 안전할 수 있습니다.
# 여기서는 직접 임포트를 시도합니다.

# from .category_db import CategoryDB # CategoryDB 임포트 (순환참조 주의하며 실제 경로로)

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
        """
        Word 테이블 생성 및 초기화
        - 테이블이 없으면 새로 생성
        - 테이블이 비어있으면 CSV 파일에서 단어 가져오기
        """
        self.execute("PRAGMA foreign_keys = OFF")  # 외래키 제약 조건 일시 해제
        self.execute("""
        CREATE TABLE IF NOT EXISTS Word (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 단어 고유 ID
            english TEXT UNIQUE NOT NULL,              -- 영어 단어 (중복 불가)
            meaning TEXT NOT NULL,                     -- 한글 의미
            part_of_speech TEXT,                       -- 품사
            example_sentence TEXT,                     -- 예문
            wrong_count INTEGER DEFAULT 0              -- 오답 횟수
        )
        """)
        self.execute("PRAGMA foreign_keys = ON")      # 외래키 제약 조건 다시 활성화
        self.commit()

        # Word 테이블이 비어있는지 확인
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
                print(f"이미 등록된 단어: {english}")
                return existing['word_id']  # 기존 단어의 ID 반환
            
            # 새 단어 추가
            print(f"[DEBUG] add_word: {english}, {meaning}, {part_of_speech}, {example_sentence}")
            self.execute(
                "INSERT INTO Word (english, meaning, part_of_speech, example_sentence) VALUES (?, ?, ?, ?)",
                (english, meaning, part_of_speech, example_sentence)
            )
            self.commit()
            print(f"[DEBUG] add_word 성공: {english}")
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

                    print(f"[DEBUG] import_from_csv: {english}, {meaning}, {part_of_speech}, {example_sentence}")
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

    def get_all_words(self) -> List[Dict]:
        """
        모든 단어 목록을 조회합니다.
        Returns:
            List[Dict]: 단어 목록 (각 단어는 모든 컬럼 포함)
        """
        return self.fetch_all("SELECT * FROM Word")

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

    def update_wrong_count(self, word_id: int) -> bool:
        """
        단어의 틀린 횟수를 1 증가시킵니다.
        Args:
            word_id: 수정할 단어 ID
        Returns:
            bool: 성공 여부
        """
        try:
            self.execute(
                """
                UPDATE Word
                SET wrong_count = wrong_count + 1
                WHERE word_id = ?
                """,
                (word_id,)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"틀린 횟수 업데이트 오류: {e}")
            self.rollback()
            return False

# 모듈 레벨에서 인스턴스 생성 - 메인 프로그램에서 사용되는 전역 인스턴스
word_db = WordDB() 
