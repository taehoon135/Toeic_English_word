from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase
import csv
import os
import sqlite3

class WordDB(BaseDatabase):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)

    # CSV 파일에서 단어 데이터 임포트
    def import_from_csv(self, csv_path: str) -> bool:
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_word = self.fetch_one(
                        "SELECT word_id FROM Word WHERE english = ? AND meaning = ?",
                        (row['english'], row['meaning'])
                    )
                    if existing_word:
                        continue
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
            return True
        except Exception as e:
            self.rollback()
            return False

    # 카테고리명으로 카테고리 조회 또는 생성
    def _get_or_create_category(self, name: str) -> Optional[int]:
        try:
            category = self.fetch_one(
                "SELECT category_id FROM Category WHERE name = ?",
                (name,)
            )
            if category:
                return category['category_id']
            self.execute(
                "INSERT INTO Category (name) VALUES (?)",
                (name,)
            )
            self.commit()
            return self.cursor.lastrowid
        except Exception as e:
            self.rollback()
            return None

    # 전체 단어 목록 조회
    def get_all_words(self) -> List[Dict]:
        try:
            return self.fetch_all("""
                SELECT 
                    w.word_id as id,
                    w.english,
                    w.meaning,
                    w.part_of_speech,
                    w.example_sentence as example,
                    w.wrong_count,
                    w.created_at,
                    GROUP_CONCAT(c.name) as categories
                FROM Word w
                LEFT JOIN WordCategory wc ON w.word_id = wc.word_id
                LEFT JOIN Category c ON wc.category_id = c.category_id
                GROUP BY w.word_id
                ORDER BY w.word_id
            """)
        except Exception as e:
            print(f"Error in get_all_words: {e}")
            return []

    # 카테고리별 단어 목록 조회
    def get_words(self, category_id: Optional[int] = None) -> List[Dict]:
        try:
            if category_id:
                return self.fetch_all("""
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
                    LEFT JOIN Category c ON wc.category_id = c.category_id
                    WHERE wc.category_id = ?
                    GROUP BY w.word_id
                    ORDER BY w.word_id
                """, (category_id,))
            else:
                return self.get_all_words()
        except Exception as e:
            return []

    # 단어 상세 정보 조회
    def get_word_details(self, word_id: int) -> Optional[Dict]:
        try:
            return self.fetch_one("""
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
                WHERE w.word_id = ?
                GROUP BY w.word_id
            """, (word_id,))
        except Exception as e:
            return None

    # 오답 횟수 1 증가
    def update_wrong_count(self, word_id: int) -> bool:
        try:
            self.execute("""
                UPDATE Word
                SET wrong_count = wrong_count + 1
                WHERE word_id = ?
            """, (word_id,))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # 단어 추가 (핵심 기능)
    def add_word(self, word: str, meaning: str, part_of_speech: str, example: str, category_id: Optional[int] = None) -> int:
        try:
            self.execute(
                """
                INSERT INTO Word (english, meaning, part_of_speech, example_sentence)
                VALUES (?, ?, ?, ?)
                """,
                (word, meaning, part_of_speech, example)
            )
            self.commit()
            new_word_id = self.cursor.lastrowid
            
            # 카테고리가 지정된 경우 WordCategory 테이블에도 추가
            if category_id:
                self.execute(
                    """
                    INSERT INTO WordCategory (word_id, category_id)
                    VALUES (?, ?)
                    """,
                    (new_word_id, category_id)
                )
                self.commit()
            
            return new_word_id  # 새로 생성된 단어의 ID 반환
        except Exception as e:
            self.rollback()
            print(f"Error in add_word: {e}")
            return -1  # 에러 발생 시 -1 반환

    # 카테고리 추가
    def add_category(self, name: str) -> bool:
        try:
            self.execute("""
                INSERT INTO Category (name)
                VALUES (?)
            """, (name,))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # 전체 카테고리 목록 조회
    def get_categories(self) -> List[Dict]:
        try:
            return self.fetch_all("""
                SELECT c.*, COUNT(wc.word_id) as word_count
                FROM Category c
                LEFT JOIN WordCategory wc ON c.category_id = wc.category_id
                GROUP BY c.category_id
                ORDER BY c.category_id
            """)
        except Exception as e:
            return []

    # 단어를 카테고리에 추가
    def add_word_to_category(self, word_id: int, category_id: int) -> bool:
        try:
            self.execute("""
                INSERT INTO WordCategory (word_id, category_id)
                VALUES (?, ?)
            """, (word_id, category_id))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # 단어를 카테고리에서 제거
    def remove_word_from_category(self, word_id: int, category_id: int) -> bool:
        try:
            self.execute("""
                DELETE FROM WordCategory
                WHERE word_id = ? AND category_id = ?
            """, (word_id, category_id))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # 카테고리 삭제
    def delete_category(self, category_id: int) -> bool:
        try:
            self.execute("""
                DELETE FROM Category
                WHERE category_id = ?
            """, (category_id,))
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            return False

    # Word, WordHistory 테이블 생성 및 초기화
    def initialize_tables(self):
        self.execute("DROP TABLE IF EXISTS WordHistory")
        self.execute("DROP TABLE IF EXISTS WordCategory")
        self.execute("DROP TABLE IF EXISTS Word")
        self.execute("DROP TABLE IF EXISTS Category")
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS Category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS Word (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            english TEXT NOT NULL,
            meaning TEXT NOT NULL,
            part_of_speech TEXT,
            example_sentence TEXT,
            wrong_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS WordCategory (
            word_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (word_id, category_id),
            FOREIGN KEY (word_id) REFERENCES Word(word_id),
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        )
        """)
        
        self.execute("""
        CREATE TABLE IF NOT EXISTS WordHistory (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            word_id INTEGER NOT NULL,
            is_correct INTEGER NOT NULL,
            study_type TEXT NOT NULL,
            studied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (word_id) REFERENCES Word(word_id)
        )
        """)
        self.commit()

    # 단어장 전체 리스트(영어, 해석, 품사)
    def get_word_list(self):
        return self.fetch_all("SELECT word_id, english, meaning, part_of_speech FROM Word")

    # 단어 상세정보(예문, 발음)
    def get_word_detail(self, word_id):
        return self.fetch_one("SELECT example_sentence, pronunciation FROM Word WHERE word_id = ?", (word_id,))

    # 단어 검색 (영어/한글)
    def search_words(self, keyword: str) -> List[Dict]:
        keyword = f"%{keyword}%"
        return self.fetch_all(
            """
            SELECT w.*, GROUP_CONCAT(c.name) as category_names
            FROM Word w
            LEFT JOIN WordCategory wc ON w.word_id = wc.word_id
            LEFT JOIN Category c ON wc.category_id = c.category_id
            WHERE w.english LIKE ? OR w.meaning LIKE ?
            GROUP BY w.word_id
            ORDER BY w.english
            """,
            (keyword, keyword)
        )

    # 단어 조회 (word_id)
    def get_word(self, word_id: int) -> Dict:
        return self.fetch_one(
            """
            SELECT w.*, c.name as category_name
            FROM Word w
            LEFT JOIN Category c ON w.category_id = c.category_id
            WHERE w.word_id = ?
            """,
            (word_id,)
        )

    # 카테고리별 단어 목록 조회
    def get_words_by_category(self, category_id: int) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT w.*, c.name as category_name
            FROM Word w
            LEFT JOIN Category c ON w.category_id = c.category_id
            WHERE w.category_id = ?
            ORDER BY w.english
            """,
            (category_id,)
        )

    # 단어 정보 수정
    def update_word(self, word_id: int, word: str, meaning: str, part_of_speech: str, example: str, category_id: Optional[int] = None) -> bool:
        try:
            # Word 테이블 업데이트
            self.execute(
                """
                UPDATE Word
                SET english = ?, meaning = ?, part_of_speech = ?, example_sentence = ?
                WHERE word_id = ?
                """,
                (word, meaning, part_of_speech, example, word_id)
            )
            
            # 카테고리 관계 업데이트
            if category_id is not None:
                # 기존 카테고리 관계 제거
                self.execute(
                    "DELETE FROM WordCategory WHERE word_id = ?",
                    (word_id,)
                )
                # 새로운 카테고리 관계 추가
                self.execute(
                    "INSERT INTO WordCategory (word_id, category_id) VALUES (?, ?)",
                    (word_id, category_id)
                )
            
            self.commit()
            return True
        except Exception as e:
            self.rollback()
            print(f"Error in update_word: {e}")
            return False

    # 단어 삭제
    def delete_word(self, word_id: int) -> bool:
        self.execute(
            "DELETE FROM Word WHERE word_id = ?",
            (word_id,)
        )
        self.commit()
        return True

    # 오답 횟수 기준 단어 목록 조회
    def get_words_by_wrong_count(self, min_wrong_count: int = 1) -> List[Dict]:
        return self.fetch_all(
            """
            SELECT w.*, c.name as category_name
            FROM Word w
            LEFT JOIN Category c ON w.category_id = c.category_id
            WHERE w.wrong_count >= ?
            ORDER BY w.wrong_count DESC
            """,
            (min_wrong_count,)
        ) 
