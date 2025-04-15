"""
데이터베이스 기본 클래스
모든 데이터베이스 작업의 기반이 되는 클래스입니다.

주요 기능:
- 데이터베이스 연결 관리
- 테이블 생성 및 초기화
- 기본적인 CRUD 작업 지원
- 트랜잭션 관리

사용 예시:
    >>> db = BaseDatabase()
    >>> db.execute("SELECT * FROM User")
    >>> result = db.fetch_one("SELECT * FROM User WHERE user_id = ?", (1,))
"""

import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple

# 데이터베이스 파일 경로 상수 정의
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'toeic_vocabulary.db')

class BaseDatabase:
    """
    데이터베이스 기본 클래스
    
    Attributes:
        db_path (str): 데이터베이스 파일 경로
        conn (sqlite3.Connection): 데이터베이스 연결 객체
        cursor (sqlite3.Cursor): 데이터베이스 커서 객체
    """
    
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        """
        데이터베이스 연결 초기화
        
        Args:
            db_path (str): 데이터베이스 파일 경로 (기본값: 'toeic_vocabulary.db')
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        
        # 테이블 생성
        self.create_user_table()
        self.create_word_table()
        self.create_category_table()
        self.create_word_category_table()
        self.create_game_score_table()

    def connect(self):
        """
        데이터베이스 연결을 설정합니다.
        외래 키 제약 조건을 활성화합니다.
        
        Raises:
            sqlite3.Error: 데이터베이스 연결 실패 시
        """
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
        """
        User 테이블을 생성합니다.
        
        테이블 구조:
        - user_id (INTEGER): 기본 키, 자동 증가
        - username (TEXT): 사용자명, 유니크
        - password (TEXT): 비밀번호
        - name (TEXT): 사용자 이름
        - created_at (TIMESTAMP): 생성 시간
        
        Returns:
            bool: 테이블 생성 성공 여부
        """
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
        """
        Word 테이블을 생성합니다.
        
        테이블 구조:
        - word_id (INTEGER): 기본 키, 자동 증가
        - english (TEXT): 영어 단어
        - meaning (TEXT): 단어 의미
        - part_of_speech (TEXT): 품사
        - example_sentence (TEXT): 예문
        - pronunciation_audio (TEXT): 발음 파일 경로
        - wrong_count (INTEGER): 틀린 횟수
        - created_at (TIMESTAMP): 생성 시간
        
        Returns:
            bool: 테이블 생성 성공 여부
        """
        try:
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
            self.commit()
            return True
        except Exception as e:
            print(f"Word 테이블 생성 오류: {e}")
            return False

    def create_category_table(self):
        """
        Category 테이블을 생성합니다.
        
        테이블 구조:
        - category_id (INTEGER): 기본 키, 자동 증가
        - name (TEXT): 카테고리 이름, 유니크
        - created_at (TIMESTAMP): 생성 시간
        
        Returns:
            bool: 테이블 생성 성공 여부
        """
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
        """
        WordCategory 테이블을 생성합니다.
        단어와 카테고리의 다대다 관계를 관리합니다.
        
        테이블 구조:
        - word_id (INTEGER): 외래 키, Word 테이블 참조
        - category_id (INTEGER): 외래 키, Category 테이블 참조
        - created_at (TIMESTAMP): 생성 시간
        
        Returns:
            bool: 테이블 생성 성공 여부
        """
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
        """
        GameScore 테이블을 생성합니다.
        
        테이블 구조:
        - score_id (INTEGER): 기본 키, 자동 증가
        - user_id (INTEGER): 외래 키, User 테이블 참조
        - game_type (TEXT): 게임 종류
        - score (INTEGER): 게임 점수
        - played_at (TIMESTAMP): 게임 플레이 시간
        
        Returns:
            bool: 테이블 생성 성공 여부
        """
        try:
            self.execute("""
                CREATE TABLE IF NOT EXISTS GameScore (
                    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
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
        """
        SQL 쿼리를 실행합니다.
        
        Args:
            query (str): 실행할 SQL 쿼리문
            params (Tuple): 쿼리 파라미터 (기본값: 빈 튜플)
            
        Returns:
            bool: 쿼리 실행 성공 여부
            
        Raises:
            Exception: 쿼리 실행 중 오류 발생 시
        """
        try:
            self.cursor.execute(query, params)
            return True
        except Exception as e:
            print(f"쿼리 실행 오류: {e}")
            return False

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict]:
        """
        단일 결과를 조회합니다.
        
        Args:
            query (str): 실행할 SQL 쿼리문
            params (Tuple): 쿼리 파라미터
            
        Returns:
            Optional[Dict]: 조회 결과를 딕셔너리로 반환, 결과가 없으면 None 반환
        """
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict]:
        """
        모든 결과를 조회합니다.
        
        Args:
            query (str): 실행할 SQL 쿼리문
            params (Tuple): 쿼리 파라미터
            
        Returns:
            List[Dict]: 조회 결과를 딕셔너리 리스트로 반환
        """
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"데이터 조회 오류: {e}")
            return []

    def commit(self):
        """변경사항을 데이터베이스에 저장합니다."""
        try:
            self.conn.commit()
        except Exception as e:
            print(f"커밋 오류: {e}")

    def rollback(self):
        """마지막 커밋 이후의 변경사항을 취소합니다."""
        try:
            self.conn.rollback()
        except Exception as e:
            print(f"롤백 오류: {e}")

    def __enter__(self):
        """컨텍스트 매니저 진입"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.close()

    def close(self):
        """데이터베이스 연결을 종료합니다."""
        if self.conn:
            self.conn.close() 