from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase
import csv
import os
import sqlite3

class WordDB(BaseDatabase):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)
        self.create_word_table()
        self.create_category_table()
        self.create_word_category_table()

    def create_word_table(self) -> None:
        """Word 테이블 생성"""
        self.execute("""
            CREATE TABLE IF NOT EXISTS Word (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                english TEXT NOT NULL,
                meaning TEXT NOT NULL,
                part_of_speech TEXT,
                example_sentence TEXT,
                pronunciation_audio TEXT,
                wrong_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def create_category_table(self) -> None:
        """Category 테이블 생성"""
        self.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def create_word_category_table(self) -> None:
        """WordCategory 테이블 생성"""
        self.execute("""
            CREATE TABLE IF NOT EXISTS WordCategory (
                word_id INTEGER,
                category_id INTEGER,
                PRIMARY KEY (word_id, category_id),
                FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE
            )
        """)

    def import_from_csv(self, csv_path: str) -> bool:
        """CSV 파일에서 단어 데이터 가져오기"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # 이미 존재하는 단어인지 확인
                    existing_word = self.fetch_one(
                        "SELECT word_id FROM Word WHERE english = ? AND meaning = ?",
                        (row['english'], row['meaning'])
                    )
                    
                    if existing_word:
                        continue  # 이미 존재하는 단어는 건너뜀
                    
                    # 단어 추가
                    self.execute(
                        """
                        INSERT INTO Word (
                            english, meaning, part_of_speech,
                            example_sentence
                        ) VALUES (?, ?, ?, ?)
                        """,
                        (
                            row['english'],
                            row['meaning'],
                            row.get('part_of_speech', ''),
                            row.get('example_sentence', '')
                        )
                    )
                    
                    # 카테고리 연결
                    if 'category' in row and row['category']:
                        word_id = self.cursor.lastrowid
                        category_id = self._get_or_create_category(row['category'])
                        if category_id:
                            self.execute(
                                """
                                INSERT INTO WordCategory (word_id, category_id)
                                VALUES (?, ?)
                                """,
                                (word_id, category_id)
                            )
            self.commit()
            print("단어 데이터가 성공적으로 가져와졌습니다.")
            return True
        except Exception as e:
            print(f"CSV 파일 가져오기 오류: {e}")
            self.rollback()
            return False

    def _get_or_create_category(self, name: str) -> Optional[int]:
        """카테고리 이름으로 ID 조회 또는 생성"""
        category = self.fetch_one(
            "SELECT category_id FROM Category WHERE name = ?",
            (name,)
        )
        
        if category:
            return category['category_id']
        else:
            self.execute(
                "INSERT INTO Category (name) VALUES (?)",
                (name,)
            )
            self.commit()
            return self.cursor.lastrowid

    def get_all_words(self) -> List[Dict]:
        """모든 단어 목록 조회"""
        return self.fetch_all(
            """
            SELECT 
                word_id as id,
                english,
                meaning,
                part_of_speech,
                example_sentence as example,
                pronunciation_audio as pronunciation_file,
                wrong_count,
                created_at
            FROM Word
            ORDER BY english
            """
        )

    def get_words(self, category_id: Optional[int] = None) -> List[Dict]:
        """단어 목록 조회"""
        if category_id is None:
            return self.fetch_all(
                """
                SELECT 
                    w.word_id as id,
                    w.english,
                    w.meaning,
                    w.part_of_speech,
                    w.example_sentence as example,
                    w.pronunciation_audio as pronunciation_file,
                    w.wrong_count,
                    w.created_at,
                    GROUP_CONCAT(c.name) as categories
                FROM Word w
                LEFT JOIN WordCategory wc ON w.word_id = wc.word_id
                LEFT JOIN Category c ON wc.category_id = c.category_id
                GROUP BY w.word_id
                ORDER BY w.english
                """
            )
        else:
            return self.fetch_all(
                """
                SELECT 
                    w.word_id as id,
                    w.english,
                    w.meaning,
                    w.part_of_speech,
                    w.example_sentence as example,
                    w.pronunciation_audio as pronunciation_file,
                    w.wrong_count,
                    w.created_at,
                    GROUP_CONCAT(c.name) as categories
                FROM Word w
                JOIN WordCategory wc ON w.word_id = wc.word_id
                JOIN Category c ON wc.category_id = c.category_id
                WHERE wc.category_id = ?
                GROUP BY w.word_id
                ORDER BY w.english
                """,
                (category_id,)
            )

    def get_word_details(self, word_id: int) -> Optional[Dict]:
        """단어 상세 정보 조회"""
        return self.fetch_one(
            """
            SELECT w.*, GROUP_CONCAT(c.name) as categories
            FROM Word w
            LEFT JOIN WordCategory wc ON w.word_id = wc.word_id
            LEFT JOIN Category c ON wc.category_id = c.category_id
            WHERE w.word_id = ?
            GROUP BY w.word_id
            """,
            (word_id,)
        )

    def update_wrong_count(self, word_id: int) -> bool:
        """틀린 횟수 증가"""
        return self.execute(
            """
            UPDATE Word 
            SET wrong_count = wrong_count + 1
            WHERE word_id = ?
            """,
            (word_id,)
        )

    def add_word(self, english: str, meaning: str, 
                part_of_speech: str = '', example_sentence: str = '', 
                pronunciation_audio: str = '', category_ids: List[int] = None) -> bool:
        """새로운 단어 추가"""
        try:
            self.execute(
                """
                INSERT INTO Word (
                    english, meaning, part_of_speech,
                    example_sentence, pronunciation_audio
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (english, meaning, part_of_speech, example_sentence, pronunciation_audio)
            )
            
            # 카테고리 연결
            if category_ids:
                word_id = self.cursor.lastrowid
                for category_id in category_ids:
                    self.execute(
                        """
                        INSERT INTO WordCategory (word_id, category_id)
                        VALUES (?, ?)
                        """,
                        (word_id, category_id)
                    )
            
            self.commit()
            return True
        except Exception as e:
            print(f"단어 추가 오류: {e}")
            self.rollback()
            return False

    def add_category(self, name: str) -> bool:
        """카테고리 추가"""
        try:
            self.execute(
                "INSERT INTO Category (name) VALUES (?)",
                (name,)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"카테고리 추가 오류: {e}")
            self.rollback()
            return False

    def get_categories(self) -> List[Dict]:
        """카테고리 목록 조회"""
        return self.fetch_all(
            """
            SELECT 
                c.category_id,
                c.name,
                COUNT(wc.word_id) as word_count
            FROM Category c
            LEFT JOIN WordCategory wc ON c.category_id = wc.category_id
            GROUP BY c.category_id
            ORDER BY c.name
            """
        )

    def add_word_to_category(self, word_id: int, category_id: int) -> bool:
        """단어를 카테고리에 추가"""
        return self.execute(
            """
            INSERT INTO WordCategory (word_id, category_id)
            VALUES (?, ?)
            """,
            (word_id, category_id)
        )

    def remove_word_from_category(self, word_id: int, category_id: int) -> bool:
        """카테고리에서 단어 제거"""
        return self.execute(
            """
            DELETE FROM WordCategory
            WHERE word_id = ? AND category_id = ?
            """,
            (word_id, category_id)
        )

    def delete_category(self, category_id: int) -> bool:
        """카테고리 삭제"""
        try:
            self.execute(
                "DELETE FROM Category WHERE category_id = ?",
                (category_id,)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"카테고리 삭제 오류: {e}")
            self.rollback()
            return False

# WordDB 인스턴스 생성
word_db = WordDB()

# CSV 파일이 존재하면 자동으로 데이터 임포트
csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_words.csv")
if os.path.exists(csv_file):
    # 단어가 없을 때만 임포트
    if not word_db.get_all_words():
        if word_db.import_from_csv(csv_file):
            print("단어 데이터가 성공적으로 가져와졌습니다.")
        else:
            print("단어 데이터 가져오기에 실패했습니다.") 