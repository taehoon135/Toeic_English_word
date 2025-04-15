from typing import List, Dict, Optional
from .base_db import BaseDatabase

class CategoryDB(BaseDatabase):
    def initialize_tables(self):
        """카테고리 관련 테이블 생성"""
        try:
            # 카테고리 테이블 생성
            self.execute("""
                CREATE TABLE IF NOT EXISTS Category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES User(id),
                    UNIQUE(user_id, name)
                )
            """)
            
            # 단어-카테고리 연결 테이블 생성
            self.execute("""
                CREATE TABLE IF NOT EXISTS WordCategory (
                    word_id INTEGER,
                    category_id INTEGER,
                    PRIMARY KEY (word_id, category_id),
                    FOREIGN KEY (word_id) REFERENCES Word(id),
                    FOREIGN KEY (category_id) REFERENCES Category(id)
                )
            """)
            self.commit()
            return True
        except Exception as e:
            print(f"테이블 생성 오류: {e}")
            return False

    def create_category(self, user_id: int, name: str) -> bool:
        """새로운 카테고리 생성"""
        try:
            self.execute(
                "INSERT INTO Category (user_id, name) VALUES (?, ?)",
                (user_id, name)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"카테고리 생성 오류: {e}")
            return False
    
    def get_user_categories(self, user_id: int) -> List[Dict]:
        """사용자의 모든 카테고리 조회"""
        try:
            categories = self.fetch_all(
                "SELECT id, name FROM Category WHERE user_id = ?",
                (user_id,)
            )
            return categories
        except Exception as e:
            print(f"카테고리 조회 오류: {e}")
            return []

    def add_word_to_category(self, word_id: int, category_id: int) -> bool:
        """단어를 카테고리에 추가"""
        try:
            self.execute(
                "INSERT INTO WordCategory (word_id, category_id) VALUES (?, ?)",
                (word_id, category_id)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"단어 카테고리 추가 오류: {e}")
            return False
    
    def remove_word_from_category(self, word_id: int, category_id: int) -> bool:
        """카테고리에서 단어 제거"""
        try:
            self.execute(
                "DELETE FROM WordCategory WHERE word_id = ? AND category_id = ?",
                (word_id, category_id)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"단어 카테고리 제거 오류: {e}")
            return False
    
    def get_words_by_categories(self, category_ids: List[int]) -> List[Dict]:
        """선택된 카테고리들의 단어 조회"""
        try:
            placeholders = ','.join(['?'] * len(category_ids))
            query = f"""
                SELECT DISTINCT w.* 
                FROM Word w
                JOIN WordCategory wc ON w.id = wc.word_id
                WHERE wc.category_id IN ({placeholders})
            """
            return self.fetch_all(query, category_ids)
        except Exception as e:
            print(f"카테고리별 단어 조회 오류: {e}")
            return []
    
    def delete_category(self, category_id: int) -> bool:
        """카테고리 삭제"""
        try:
            # 먼저 WordCategory 테이블에서 관련된 레코드 삭제
            self.execute(
                "DELETE FROM WordCategory WHERE category_id = ?",
                (category_id,)
            )
            # 그 다음 Category 테이블에서 카테고리 삭제
            self.execute(
                "DELETE FROM Category WHERE id = ?",
                (category_id,)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"카테고리 삭제 오류: {e}")
            return False
    
    def get_word_categories(self, word_id: int) -> List[Dict]:
        """단어가 속한 카테고리 조회"""
        try:
            query = """
                SELECT c.id, c.name
                FROM Category c
                JOIN WordCategory wc ON c.id = wc.category_id
                WHERE wc.word_id = ?
            """
            return self.fetch_all(query, (word_id,))
        except Exception as e:
            print(f"단어 카테고리 조회 오류: {e}")
            return []

    def add_category(self, name: str, created_by: int) -> bool:
        """새로운 카테고리 추가"""
        return self.execute(
            """
            INSERT INTO Category (name, created_by)
            VALUES (?, ?)
            """,
            (name, created_by)
        )

    def get_category_by_id(self, category_id: int) -> Optional[Dict]:
        """카테고리 ID로 조회"""
        return self.fetch_one(
            """
            SELECT c.*, u.username as creator_name
            FROM Category c
            JOIN User u ON c.created_by = u.user_id
            WHERE c.category_id = ?
            """,
            (category_id,)
        )

    def get_categories_by_user(self, user_id: int) -> List[Dict]:
        """사용자가 생성한 카테고리 목록 조회"""
        return self.fetch_all(
            """
            SELECT c.*, COUNT(w.word_id) as word_count
            FROM Category c
            LEFT JOIN Word w ON c.category_id = w.category_id
            WHERE c.created_by = ?
            GROUP BY c.category_id
            ORDER BY c.created_at DESC
            """,
            (user_id,)
        )

    def get_all_categories(self) -> List[Dict]:
        """모든 카테고리 목록 조회"""
        return self.fetch_all(
            """
            SELECT c.*, u.username as creator_name, COUNT(w.word_id) as word_count
            FROM Category c
            JOIN User u ON c.created_by = u.user_id
            LEFT JOIN Word w ON c.category_id = w.category_id
            GROUP BY c.category_id
            ORDER BY c.name
            """
        )

    def update_category(self, category_id: int, name: str) -> bool:
        """카테고리 정보 수정"""
        return self.execute(
            """
            UPDATE Category
            SET name = ?
            WHERE category_id = ?
            """,
            (name, category_id)
        )

    def delete_category(self, category_id: int) -> bool:
        """카테고리 삭제 (연관된 단어들의 category_id는 NULL로 설정됨)"""
        return self.execute(
            "DELETE FROM Category WHERE category_id = ?",
            (category_id,)
        )

    def get_words_in_category(self, category_id: int) -> List[Dict]:
        """카테고리에 속한 단어 목록 조회"""
        return self.fetch_all(
            """
            SELECT w.*, u.username as added_by_name
            FROM Word w
            JOIN User u ON w.added_by = u.user_id
            WHERE w.category_id = ?
            ORDER BY w.word
            """,
            (category_id,)
        )

    def add_word_to_category(self, word_id: int, category_id: int) -> bool:
        """단어를 카테고리에 추가"""
        return self.execute(
            """
            UPDATE Word
            SET category_id = ?
            WHERE word_id = ?
            """,
            (category_id, word_id)
        )

    def remove_word_from_category(self, word_id: int) -> bool:
        """단어를 카테고리에서 제거"""
        return self.execute(
            """
            UPDATE Word
            SET category_id = NULL
            WHERE word_id = ?
            """,
            (word_id,)
        )

# CategoryDB 인스턴스 생성
category_db = CategoryDB('category.db') 