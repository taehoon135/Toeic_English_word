import sqlite3
import os
from typing import Optional, Dict, Any, List, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'toeic_vocabulary.db')

class BaseDatabase:
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.initialize_tables()

    def disable_foreign_keys(self):
        self.execute("PRAGMA foreign_keys = OFF")
        self.commit()

    def enable_foreign_keys(self):
        self.execute("PRAGMA foreign_keys = ON")
        self.commit()

    def execute(self, query: str, params: Tuple = ()) -> bool:
        try:
            self.cursor.execute(query, params)
            return True
        except Exception as e:
            return False

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict]:
        try:
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            return None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict]:
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            return []

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def initialize_tables(self):
        pass

    def create_user_table(self):
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
            return False

    def create_word_table(self):
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
            return False

    def create_category_table(self):
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
            return False

    def create_word_category_table(self):
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
            return False

    def create_game_score_table(self):
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
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 