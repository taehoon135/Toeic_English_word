import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple

# 데이터베이스 파일의 절대 경로 지정
DB_PATH = os.path.join(os.path.dirname(__file__), 'toeic_vocabulary.db')

# 전체 스키마 (부모 테이블 → 자식 테이블 순). 어떤 DB 클래스로 열어도 모든 테이블이 생겨 FK가 항상 유효함
# 스키마를 바꾸면 SCHEMA_VERSION을 올릴 것 → 기존 DB는 _migrate()가 데이터를 옮기며 재구성
SCHEMA_VERSION = 1
SCHEMA = [
    """CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_login_id TEXT UNIQUE NOT NULL CHECK (trim(user_login_id) <> ''),
        user_pw TEXT NOT NULL,
        user_name TEXT NOT NULL,
        user_phone TEXT,
        is_admin INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0, 1)),
        user_api TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS Word (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        english TEXT UNIQUE NOT NULL CHECK (trim(english) <> ''),
        meaning TEXT NOT NULL CHECK (trim(meaning) <> ''),
        part_of_speech TEXT,
        example_sentence TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS UserWord (
        user_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        wrong_count INTEGER NOT NULL DEFAULT 0 CHECK (wrong_count >= 0),
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS Category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK (trim(name) <> '' AND name <> '전체'),  -- '전체'는 UI 필터 예약어
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id, name),
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS WordCategory (
        category_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        PRIMARY KEY (category_id, word_id),
        FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS Rain_Game_Score (
        score_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL DEFAULT 0 CHECK (score >= 0),
        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS quiz (
        quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_type TEXT NOT NULL,
        user_id INTEGER,
        category_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE SET NULL
    )""",
    """CREATE TABLE IF NOT EXISTS quiz_question (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        options TEXT,
        hint TEXT,
        word_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS quiz_result (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        is_correct INTEGER NOT NULL CHECK (is_correct IN (0, 1)),
        answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES Word(word_id) ON DELETE CASCADE
    )""",
]
TABLES = [s.split()[5] for s in SCHEMA]  # CREATE TABLE IF NOT EXISTS <name>


def _migrate(db_path: str):
    """
    user_version이 SCHEMA_VERSION보다 낮으면 모든 테이블을 현재 스키마로 재구성합니다.
    - 공통 컬럼만 옮김 (예: 예전 Word.wrong_count는 버려짐)
    - 제약(NOT NULL/CHECK/UNIQUE) 위반 행과, 부모가 없는 고아 행은 삭제
    """
    con = sqlite3.connect(db_path, isolation_level=None)  # 트랜잭션을 직접 제어
    try:
        if con.execute("PRAGMA user_version").fetchone()[0] >= SCHEMA_VERSION:
            return
        con.execute("PRAGMA foreign_keys = OFF")
        con.execute("PRAGMA legacy_alter_table = ON")  # RENAME 시 다른 테이블의 FK 참조를 바꾸지 않음
        con.execute("BEGIN")
        existing = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        old = [t for t in TABLES if t in existing]
        for t in old:
            con.execute(f'ALTER TABLE "{t}" RENAME TO "_old_{t}"')
        for stmt in SCHEMA:
            con.execute(stmt)
        for t in old:
            new_cols = {r[1] for r in con.execute(f'PRAGMA table_info("{t}")')}
            cols = ", ".join(r[1] for r in con.execute(f'PRAGMA table_info("_old_{t}")') if r[1] in new_cols)
            con.execute(f'INSERT OR IGNORE INTO "{t}" ({cols}) SELECT {cols} FROM "_old_{t}"')
            con.execute(f'DROP TABLE "_old_{t}"')
        # 고아 행 제거 (부모 삭제가 자식에게 연쇄되도록 위반이 없어질 때까지 반복)
        while bad := con.execute("PRAGMA foreign_key_check").fetchall():
            for table, rowid, _, _ in bad:
                con.execute(f'DELETE FROM "{table}" WHERE rowid = ?', (rowid,))
        con.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
        con.execute("COMMIT")
    except Exception:
        if con.in_transaction:
            con.execute("ROLLBACK")
        raise
    finally:
        con.close()


class BaseDatabase:
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
        _migrate(db_path)  # 모든 테이블 생성/스키마 갱신 (최신이면 즉시 반환)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # SQLite는 연결마다 FK를 켜야 ON DELETE CASCADE가 동작함
        self.conn.execute("PRAGMA foreign_keys = ON")

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

    def initialize_tables(self):
        """각 DB 클래스에서 자신의 테이블을 생성하도록 오버라이드합니다."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 