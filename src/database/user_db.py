from typing import Dict, Optional
from .base_db import BaseDatabase
import sqlite3

class UserDB(BaseDatabase):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)
        self.create_user_table()

    def create_user_table(self):
        """사용자 테이블 초기화"""
        self.execute("""
            CREATE TABLE IF NOT EXISTS User (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.commit()

    def register(self, username: str, password: str, name: str) -> bool:
        """새 사용자 등록"""
        try:
            self.execute(
                "INSERT INTO User (username, password, name) VALUES (?, ?, ?)",
                (username, password, name)
            )
            self.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username: str, password: str) -> Optional[Dict]:
        """사용자 로그인"""
        user = self.fetch_one(
            "SELECT * FROM User WHERE username = ? AND password = ?",
            (username, password)
        )
        return user if user else None

    def add_user(self, username: str, password: str, is_admin: bool = False) -> bool:
        """새로운 사용자 추가"""
        try:
            self.execute(
                """
                INSERT INTO User (username, password, is_admin)
                VALUES (?, ?, ?)
                """,
                (username, password, 1 if is_admin else 0)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 추가 오류: {e}")
            self.rollback()
            return False

    def get_user(self, username: str) -> Optional[Dict]:
        """사용자 정보 조회"""
        return self.fetch_one(
            "SELECT * FROM User WHERE username = ?",
            (username,)
        )

    def update_user(self, user_id: int, **kwargs) -> bool:
        """사용자 정보 수정"""
        try:
            set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
            query = f"UPDATE User SET {set_clause} WHERE user_id = ?"
            params = list(kwargs.values()) + [user_id]
            
            self.execute(query, params)
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 정보 수정 오류: {e}")
            self.rollback()
            return False

# UserDB 인스턴스 생성
user_db = UserDB() 