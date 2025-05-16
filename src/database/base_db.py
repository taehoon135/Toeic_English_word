import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple
from abc import ABC, abstractmethod

# 데이터베이스 파일의 절대 경로 지정
DB_PATH = os.path.join(os.path.dirname(__file__), 'toeic_vocabulary.db')
print(f"DB_PATH 전역 변수 설정됨: {DB_PATH}")

class BaseDatabase(ABC):
    """
    기본 데이터베이스 연결 및 쿼리 실행을 위한 추상 클래스
    모든 데이터베이스 모델의 기본이 되는 클래스입니다.
    """
    def __init__(self, db_path: str = DB_PATH):
        """
        데이터베이스 연결을 초기화합니다.
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        print(f"BaseDatabase 인스턴스가 {self.db_path} 경로로 초기화됨")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # self.initialize_tables()

    def disable_foreign_keys(self):
        self.execute("PRAGMA foreign_keys = OFF")
        self.commit()

    def enable_foreign_keys(self):
        self.execute("PRAGMA foreign_keys = ON")
        self.commit()

    def execute(self, query: str, params: Tuple = ()) -> bool:
        """
        SQL 쿼리를 실행합니다.
        Args:
            query: SQL 쿼리문
            params: 쿼리 파라미터
        Returns:
            bool: 실행 성공 여부
        """
        try:
            self.cursor.execute(query, params)
            return True
        except Exception as e:
            print(f"쿼리 실행 오류: {e}")
            return False

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict]:
        """
        단일 행을 조회합니다.
        Args:
            query: SQL 쿼리문
            params: 쿼리 파라미터
        Returns:
            Optional[Dict]: 조회된 행 데이터
        """
        try:
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict]:
        """
        모든 행을 조회합니다.
        Args:
            query: SQL 쿼리문
            params: 쿼리 파라미터
        Returns:
            List[Dict]: 조회된 모든 행 데이터
        """
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return []

    def commit(self):
        """트랜잭션을 커밋합니다."""
        self.conn.commit()

    def rollback(self):
        """트랜잭션을 롤백합니다."""
        self.conn.rollback()

    def close(self):
        """데이터베이스 연결을 종료합니다."""
        self.conn.close()

    @abstractmethod
    def initialize_tables(self):
        """
        각 DB 클래스에서 구현해야 하는 테이블 초기화 메서드
        """
        raise NotImplementedError("하위 클래스에서 이 메서드를 구현해야 합니다.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 