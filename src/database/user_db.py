"""
사용자 관리를 위한 데이터베이스 클래스
사용자의 회원가입, 로그인, 정보 수정 등을 담당합니다.

주요 기능:
- 사용자 등록/로그인/정보 수정
- 사용자 정보 조회
- 비밀번호 검증

사용 예시:
    >>> user_db = UserDB()
    >>> user_db.register("user1", "password123", "홍길동")
    >>> user = user_db.login("user1", "password123")
"""

from typing import Dict, Optional, Tuple
from .base_db import BaseDatabase
import sqlite3
import hashlib

class UserDB(BaseDatabase):
    """
    사용자 관리를 위한 데이터베이스 클래스
    
    Attributes:
        db_path (str): 데이터베이스 파일 경로
    """
    
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        """
        UserDB 초기화
        
        Args:
            db_path (str): 데이터베이스 파일 경로 (기본값: 'toeic_vocabulary.db')
        """
        super().__init__(db_path)

    def _hash_password(self, password: str) -> str:
        """
        비밀번호를 해시화합니다.
        
        Args:
            password (str): 원본 비밀번호
            
        Returns:
            str: 해시화된 비밀번호
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str, name: str) -> bool:
        """
        새로운 사용자를 등록합니다.
        
        Args:
            username (str): 사용자명
            password (str): 비밀번호
            name (str): 사용자 이름
            
        Returns:
            bool: 등록 성공 여부
            
        Example:
            >>> user_db.register("user1", "password123", "홍길동")
            True
        """
        try:
            # 비밀번호 해시화
            hashed_password = self._hash_password(password)
            
            # 사용자 추가
            self.execute("""
                INSERT INTO User (username, password, name)
                VALUES (?, ?, ?)
            """, (username, hashed_password, name))
            
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 등록 오류: {e}")
            self.rollback()
            return False

    def login(self, username: str, password: str) -> Optional[Dict]:
        """
        사용자 로그인을 처리합니다.
        
        Args:
            username (str): 사용자명
            password (str): 비밀번호
            
        Returns:
            Optional[Dict]: {
                'user_id': int,
                'username': str,
                'name': str
            }
            
        Example:
            >>> user = user_db.login("user1", "password123")
            >>> if user:
            ...     print(f"환영합니다, {user['name']}님!")
        """
        try:
            # 비밀번호 해시화
            hashed_password = self._hash_password(password)
            
            # 사용자 조회
            return self.fetch_one("""
                SELECT user_id, username, name
                FROM User
                WHERE username = ? AND password = ?
            """, (username, hashed_password))
        except Exception as e:
            print(f"로그인 오류: {e}")
            return None

    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """
        사용자 정보를 조회합니다.
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            Optional[Dict]: {
                'user_id': int,
                'username': str,
                'name': str,
                'created_at': str
            }
            
        Example:
            >>> user_info = user_db.get_user_info(1)
            >>> print(f"사용자명: {user_info['username']}")
        """
        try:
            return self.fetch_one("""
                SELECT user_id, username, name, created_at
                FROM User
                WHERE user_id = ?
            """, (user_id,))
        except Exception as e:
            print(f"사용자 정보 조회 오류: {e}")
            return None

    def update_user_info(self, user_id: int, name: str) -> bool:
        """
        사용자 정보를 수정합니다.
        
        Args:
            user_id (int): 사용자 ID
            name (str): 새로운 이름
            
        Returns:
            bool: 수정 성공 여부
            
        Example:
            >>> user_db.update_user_info(1, "김철수")
            True
        """
        try:
            self.execute("""
                UPDATE User
                SET name = ?
                WHERE user_id = ?
            """, (name, user_id))
            
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 정보 수정 오류: {e}")
            self.rollback()
            return False

    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        사용자 비밀번호를 변경합니다.
        
        Args:
            user_id (int): 사용자 ID
            old_password (str): 현재 비밀번호
            new_password (str): 새로운 비밀번호
            
        Returns:
            bool: 변경 성공 여부
            
        Example:
            >>> user_db.change_password(1, "old123", "new123")
            True
        """
        try:
            # 현재 비밀번호 확인
            hashed_old_password = self._hash_password(old_password)
            user = self.fetch_one("""
                SELECT user_id
                FROM User
                WHERE user_id = ? AND password = ?
            """, (user_id, hashed_old_password))
            
            if not user:
                print("현재 비밀번호가 일치하지 않습니다.")
                return False
            
            # 새 비밀번호 설정
            hashed_new_password = self._hash_password(new_password)
            self.execute("""
                UPDATE User
                SET password = ?
                WHERE user_id = ?
            """, (hashed_new_password, user_id))
            
            self.commit()
            return True
        except Exception as e:
            print(f"비밀번호 변경 오류: {e}")
            self.rollback()
            return False

    def delete_user(self, user_id: int) -> bool:
        """
        사용자 계정을 삭제합니다.
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            bool: 삭제 성공 여부
            
        Example:
            >>> user_db.delete_user(1)
            True
        """
        try:
            self.execute("""
                DELETE FROM User
                WHERE user_id = ?
            """, (user_id,))
            
            self.commit()
            return True
        except Exception as e:
            print(f"사용자 삭제 오류: {e}")
            self.rollback()
            return False

# UserDB 인스턴스 생성
user_db = UserDB() 