"""
단어 관리를 위한 데이터베이스 클래스
단어의 CRUD 작업과 카테고리 관리를 담당합니다.

주요 기능:
- 단어 추가/수정/삭제/조회
- 카테고리 관리
- CSV 파일 임포트

사용 예시:
    >>> word_db = WordDB()
    >>> word_db.add_word("apple", "사과", "noun")
    >>> words = word_db.get_all_words()
"""

from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase
import csv
import os
import sqlite3

class WordDB(BaseDatabase):
    """
    단어 관리를 위한 데이터베이스 클래스
    
    Attributes:
        db_path (str): 데이터베이스 파일 경로
    """
    
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        """
        WordDB 초기화
        
        Args:
            db_path (str): 데이터베이스 파일 경로 (기본값: 'toeic_vocabulary.db')
        """
        super().__init__(db_path)

    def import_from_csv(self, csv_path: str) -> bool:
        """
        CSV 파일에서 단어 데이터를 가져옵니다.
        
        CSV 파일 형식:
        - 필수 컬럼: english, meaning
        - 선택 컬럼: part_of_speech, example_sentence, category
        
        Args:
            csv_path (str): CSV 파일 경로
            
        Returns:
            bool: 임포트 성공 여부
            
        Example:
            >>> word_db.import_from_csv("words.csv")
            True
        """
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
        """
        카테고리를 조회하거나 생성합니다.
        
        Args:
            name (str): 카테고리 이름
            
        Returns:
            Optional[int]: 카테고리 ID, 실패 시 None
        """
        try:
            # 기존 카테고리 조회
            category = self.fetch_one(
                "SELECT category_id FROM Category WHERE name = ?",
                (name,)
            )
            
            if category:
                return category['category_id']
            
            # 새 카테고리 생성
            self.execute(
                "INSERT INTO Category (name) VALUES (?)",
                (name,)
            )
            self.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"카테고리 생성 오류: {e}")
            self.rollback()
            return None

    def get_all_words(self) -> List[Dict]:
        """
        모든 단어를 조회합니다.
        
        Returns:
            List[Dict]: 단어 목록
            
        Example:
            >>> words = word_db.get_all_words()
            >>> for word in words:
            ...     print(f"{word['english']}: {word['meaning']}")
        """
        try:
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
                LEFT JOIN WordCategory wc ON w.word_id = wc.word_id
                LEFT JOIN Category c ON wc.category_id = c.category_id
                GROUP BY w.word_id
                ORDER BY w.word_id
            """)
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return []

    def get_words(self, category_id: Optional[int] = None) -> List[Dict]:
        """
        카테고리별 단어를 조회합니다.
        
        Args:
            category_id (Optional[int]): 카테고리 ID (기본값: None, 모든 단어 조회)
            
        Returns:
            List[Dict]: 단어 목록
            
        Example:
            >>> words = word_db.get_words(category_id=1)
            >>> for word in words:
            ...     print(f"{word['english']}: {word['meaning']}")
        """
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
            print(f"데이터 조회 오류: {e}")
            return []

    def get_word_details(self, word_id: int) -> Optional[Dict]:
        """
        단어의 상세 정보를 조회합니다.
        
        Args:
            word_id (int): 조회할 단어 ID
            
        Returns:
            Optional[Dict]: {
                'id': int,
                'english': str,
                'meaning': str,
                'part_of_speech': str,
                'example': str,
                'wrong_count': int,
                'categories': str
            }
            
        Example:
            >>> word = word_db.get_word_details(1)
            >>> print(f"{word['english']}: {word['meaning']}")
        """
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
            print(f"데이터 조회 오류: {e}")
            return None

    def update_wrong_count(self, word_id: int) -> bool:
        """
        단어의 틀린 횟수를 증가시킵니다.
        
        Args:
            word_id (int): 단어 ID
            
        Returns:
            bool: 업데이트 성공 여부
        """
        try:
            self.execute("""
                UPDATE Word
                SET wrong_count = wrong_count + 1
                WHERE word_id = ?
            """, (word_id,))
            self.commit()
            return True
        except Exception as e:
            print(f"데이터 업데이트 오류: {e}")
            self.rollback()
            return False

    def add_word(self, english: str, meaning: str, 
                part_of_speech: str = '', example_sentence: str = '', 
                pronunciation_audio: str = '', category_ids: List[int] = None) -> bool:
        """
        새 단어를 추가합니다.
        
        Args:
            english (str): 영어 단어
            meaning (str): 단어 의미
            part_of_speech (str): 품사 (기본값: '')
            example_sentence (str): 예문 (기본값: '')
            pronunciation_audio (str): 발음 파일 경로 (기본값: '')
            category_ids (List[int]): 카테고리 ID 목록 (기본값: None)
            
        Returns:
            bool: 추가 성공 여부
            
        Example:
            >>> word_db.add_word("apple", "사과", "noun", "I eat an apple.")
            True
        """
        try:
            self.execute("""
                INSERT INTO Word (
                    english, meaning, part_of_speech,
                    example_sentence, pronunciation_audio
                ) VALUES (?, ?, ?, ?, ?)
            """, (english, meaning, part_of_speech, 
                 example_sentence, pronunciation_audio))
            
            if category_ids:
                word_id = self.cursor.lastrowid
                for category_id in category_ids:
                    self.execute("""
                        INSERT INTO WordCategory (word_id, category_id)
                        VALUES (?, ?)
                    """, (word_id, category_id))
            
            self.commit()
            return True
        except Exception as e:
            print(f"데이터 추가 오류: {e}")
            self.rollback()
            return False

    def add_category(self, name: str) -> bool:
        """
        새 카테고리를 추가합니다.
        
        Args:
            name (str): 카테고리 이름
            
        Returns:
            bool: 추가 성공 여부
            
        Example:
            >>> word_db.add_category("동사")
            True
        """
        try:
            self.execute("""
                INSERT INTO Category (name)
                VALUES (?)
            """, (name,))
            self.commit()
            return True
        except Exception as e:
            print(f"데이터 추가 오류: {e}")
            self.rollback()
            return False

    def get_categories(self) -> List[Dict]:
        """
        모든 카테고리를 조회합니다.
        
        Returns:
            List[Dict]: 카테고리 목록
            
        Example:
            >>> categories = word_db.get_categories()
            >>> for category in categories:
            ...     print(f"{category['name']}")
        """
        try:
            return self.fetch_all("""
                SELECT c.*, COUNT(wc.word_id) as word_count
                FROM Category c
                LEFT JOIN WordCategory wc ON c.category_id = wc.category_id
                GROUP BY c.category_id
                ORDER BY c.category_id
            """)
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return []

    def add_word_to_category(self, word_id: int, category_id: int) -> bool:
        """
        단어를 카테고리에 추가합니다.
        
        Args:
            word_id (int): 단어 ID
            category_id (int): 카테고리 ID
            
        Returns:
            bool: 추가 성공 여부
            
        Example:
            >>> word_db.add_word_to_category(1, 1)
            True
        """
        try:
            self.execute("""
                INSERT INTO WordCategory (word_id, category_id)
                VALUES (?, ?)
            """, (word_id, category_id))
            self.commit()
            return True
        except Exception as e:
            print(f"데이터 추가 오류: {e}")
            self.rollback()
            return False

    def remove_word_from_category(self, word_id: int, category_id: int) -> bool:
        """
        단어를 카테고리에서 제거합니다.
        
        Args:
            word_id (int): 단어 ID
            category_id (int): 카테고리 ID
            
        Returns:
            bool: 제거 성공 여부
        """
        try:
            self.execute("""
                DELETE FROM WordCategory
                WHERE word_id = ? AND category_id = ?
            """, (word_id, category_id))
            self.commit()
            return True
        except Exception as e:
            print(f"데이터 삭제 오류: {e}")
            self.rollback()
            return False

    def delete_category(self, category_id: int) -> bool:
        """
        카테고리를 삭제합니다.
        
        Args:
            category_id (int): 카테고리 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        try:
            self.execute("""
                DELETE FROM Category
                WHERE category_id = ?
            """, (category_id,))
            self.commit()
            return True
        except Exception as e:
            print(f"데이터 삭제 오류: {e}")
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