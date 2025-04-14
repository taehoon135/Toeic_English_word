import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple

# 데이터베이스 파일 경로 상수 정의
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'toeic_vocabulary.db')

class BaseDatabase:
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        """데이터베이스 연결 초기화"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """데이터베이스 연결"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # 결과를 딕셔너리로 반환하도록 설정
            self.cursor = self.conn.cursor()
            # 외래키 제약조건 활성화
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"데이터베이스 연결 오류: {e}")

    def create_user_table(self):
        """User 테이블 생성"""
        try:
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
            return True
        except Exception as e:
            print(f"User 테이블 생성 오류: {e}")
            return False

    def create_word_table(self):
        """Word 테이블 생성"""
        try:
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
            self.commit()
            return True
        except Exception as e:
            print(f"Word 테이블 생성 오류: {e}")
            return False

    def create_category_table(self):
        """Category 테이블 생성"""
        try:
            self.execute("""
                CREATE TABLE IF NOT EXISTS Category (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.commit()
            return True
        except Exception as e:
            print(f"Category 테이블 생성 오류: {e}")
            return False

    def create_word_category_table(self):
        """WordCategory 테이블 생성"""
        try:
            self.execute("""
                CREATE TABLE IF NOT EXISTS WordCategory (
                    word_id INTEGER,
                    category_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (word_id, category_id),
                    FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE
                )
            """)
            self.commit()
            return True
        except Exception as e:
            print(f"WordCategory 테이블 생성 오류: {e}")
            return False

    def create_game_score_table(self):
        """GameScore 테이블 생성"""
        try:
            self.execute("""
                CREATE TABLE IF NOT EXISTS GameScore (
                    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    game_type TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
                )
            """)
            self.commit()
            return True
        except Exception as e:
            print(f"GameScore 테이블 생성 오류: {e}")
            return False

    def execute(self, query: str, params: Tuple = ()) -> bool:
        """SQL 쿼리 실행"""
        try:
            if not self.cursor:
                self.connect()
            self.cursor.execute(query, params)
            self.commit()  # 자동으로 commit
            return True
        except Exception as e:
            print(f"쿼리 실행 오류: {e}")
            self.rollback()
            return False

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict]:
        """단일 결과 조회"""
        try:
            if not self.cursor:
                self.connect()
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict]:
        """다중 결과 조회"""
        try:
            if not self.cursor:
                self.connect()
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return []

    def commit(self):
        """변경사항 저장"""
        if self.conn:
            self.conn.commit()

    def rollback(self):
        """변경사항 취소"""
        if self.conn:
            self.conn.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.close()

    def close(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None 