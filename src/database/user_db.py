from typing import Dict, Optional, Tuple
from .base_db import BaseDatabase, DB_PATH

class UserDB(BaseDatabase):
    """
    사용자 데이터베이스 관리 클래스
    - 사용자 등록, 로그인, 정보 수정 기능 제공
    - 관리자/일반 사용자 구분 관리
    """
    def __init__(self, db_path: str = DB_PATH):
        super().__init__(db_path)
        self.initialize_tables()

    def initialize_tables(self):
        """
        User 테이블 생성 및 초기화
        - 테이블이 없으면 새로 생성
        """
        self.execute("PRAGMA foreign_keys = OFF")
        self.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login_id TEXT UNIQUE NOT NULL,
            user_pw TEXT NOT NULL,
            user_name TEXT NOT NULL,
            user_phone TEXT,
            is_admin BOOLEAN DEFAULT 0,
            user_api TEXT
        )
        """)
        self.execute("PRAGMA foreign_keys = ON")
        self.commit()

    def register_user(self, user_login_id: str, user_pw: str, user_name: str, 
                     user_phone: str = None, is_admin: bool = False, user_api: str = None) -> int:
        """
        새로운 사용자를 등록합니다.
        Args:
            user_login_id: 로그인 ID
            user_pw: 비밀번호
            user_name: 사용자 이름
            user_phone: 전화번호 (선택)
            is_admin: 관리자 여부 (기본값: False)
            user_api: API 키 (선택)
        Returns:
            int: 사용자 ID (성공 시) 또는 None (실패 시)
        """
        try:
            self.execute(
                """
                INSERT INTO User 
                (user_login_id, user_pw, user_name, user_phone, is_admin, user_api) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_login_id, user_pw, user_name, user_phone, is_admin, user_api)
            )
            self.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"사용자 등록 오류: {e}")
            self.rollback()
            return None

    def login_user(self, user_login_id: str, user_pw: str) -> Optional[Dict]:
        """
        사용자 로그인을 처리합니다.
        Args:
            user_login_id: 로그인 ID
            user_pw: 비밀번호
        Returns:
            Optional[Dict]: 사용자 정보 또는 None (실패 시)
        """
        return self.fetch_one(
            "SELECT * FROM User WHERE user_login_id = ? AND user_pw = ?",
            (user_login_id, user_pw)
        )

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        사용자 ID로 사용자 정보를 조회합니다.
        Args:
            user_id: 사용자 ID
        Returns:
            Optional[Dict]: 사용자 정보 또는 None (실패 시)
        """
        return self.fetch_one(
            "SELECT * FROM User WHERE user_id = ?",
            (user_id,)
        )

    def update_user(self, user_id: int, user_name: str, user_pw: str = None) -> bool:
        """
        사용자 정보를 수정합니다.
        Args:
            user_id: 사용자 ID
            user_name: 새 사용자 이름
            user_pw: 새 비밀번호 (선택)
        Returns:
            bool: 성공 여부
        """
        try:
            if user_pw:
                self.execute(
                    "UPDATE User SET user_name = ?, user_pw = ? WHERE user_id = ?",
                    (user_name, user_pw, user_id)
                )
            else:
                self.execute(
                    "UPDATE User SET user_name = ? WHERE user_id = ?",
                    (user_name, user_id)
                )
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 정보 수정 오류: {e}")
            self.rollback()
            return False

    def update_api_key(self, user_id: int, new_api_key: str) -> bool:
        """
        사용자의 API 키를 수정합니다.
        Args:
            user_id: 사용자 ID
            new_api_key: 새 API 키
        Returns:
            bool: 성공 여부
        """
        try:
            self.execute(
                "UPDATE User SET user_api = ? WHERE user_id = ?",
                (new_api_key, user_id)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"API 키 수정 오류: {e}")
            self.rollback()
            return False

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        사용자의 비밀번호를 변경합니다.
        Args:
            user_id: 사용자 ID
            old_password: 현재 비밀번호
            new_password: 새 비밀번호
        Returns:
            bool: 성공 여부
        """
        try:
            user = self.fetch_one(
                "SELECT user_id FROM User WHERE user_id = ? AND user_pw = ?",
                (user_id, old_password)
            )
            if not user:
                print("현재 비밀번호가 일치하지 않습니다.")
                return False

            self.execute(
                "UPDATE User SET user_pw = ? WHERE user_id = ?",
                (new_password, user_id)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"비밀번호 변경 오류: {e}")
            self.rollback()
            return False

# 전역 인스턴스 생성
user_db = UserDB() 