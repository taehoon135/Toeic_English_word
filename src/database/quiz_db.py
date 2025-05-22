from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase, DB_PATH
import random

class QuizDB(BaseDatabase):
    def __init__(self, db_path: str = DB_PATH):
        super().__init__(db_path)
        self.initialize_tables()

    def initialize_tables(self):
        self.execute("DROP TABLE IF EXISTS quiz")
        self.execute("DROP TABLE IF EXISTS quiz_question")
        self.execute("""
        CREATE TABLE IF NOT EXISTS quiz (
            quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_type TEXT NOT NULL,
            category_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES Category(category_id)
        )
        """)
        self.execute("""
        CREATE TABLE IF NOT EXISTS quiz_question (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            options TEXT,
            hint TEXT,
            word_id INTEGER,
            FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id),
            FOREIGN KEY (word_id) REFERENCES Word(word_id)
        )
        """)
        self.commit()

    def create_quiz(self, quiz_type: str, category_id: Optional[int] = None) -> int:
        """
        새로운 퀴즈를 생성합니다.
        Args:
            quiz_type: 퀴즈 타입 ('short_answer_ek', 'short_answer_ke', 'cloze', 'four_choice', 'rain')
            category_id: 선택된 카테고리 ID (선택사항)
        Returns:
            int: 생성된 퀴즈 ID
        """
        try:
            self.execute(
                "INSERT INTO quiz (quiz_type, category_id) VALUES (?, ?)",
                (quiz_type, category_id)
            )
            self.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"퀴즈 생성 오류: {e}")
            self.rollback()
            return None

    def add_quiz_question(self, quiz_id: int, question: str, correct_answer: str, 
                         options: Optional[str] = None, hint: Optional[str] = None,
                         word_id: Optional[int] = None) -> int:
        """
        퀴즈에 문제를 추가합니다.
        Args:
            quiz_id: 퀴즈 ID
            question: 문제 내용
            correct_answer: 정답
            options: 선택지 (4지선다형의 경우)
            hint: 힌트
            word_id: 관련 단어 ID
        Returns:
            int: 생성된 문제 ID
        """
        try:
            self.execute(
                """
                INSERT INTO quiz_question 
                (quiz_id, question, correct_answer, options, hint, word_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (quiz_id, question, correct_answer, options, hint, word_id)
            )
            self.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"문제 추가 오류: {e}")
            self.rollback()
            return None

    def get_random_words_for_quiz(self, count: int = 5, category_id: Optional[int] = None) -> List[Dict]:
        """
        퀴즈용 랜덤 단어 목록을 조회합니다.
        """
        query = """
            SELECT w.*, c.name as category_name
            FROM Word w
            LEFT JOIN Category c ON w.category_id = c.category_id
        """
        params = []
        
        if category_id:
            query += " WHERE w.category_id = ?"
            params.append(category_id)
            
        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(count)
        
        return self.fetch_all(query, tuple(params))

    def record_quiz_result(self, user_id: int, word_id: int, is_correct: bool) -> bool:
        """
        퀴즈 결과를 기록합니다.
        """
        try:
            # 퀴즈 결과 기록
            self.execute(
                """
                INSERT INTO WordHistory (
                    user_id, word_id, is_correct, study_type
                ) VALUES (?, ?, ?, 'quiz')
                """,
                (user_id, word_id, 1 if is_correct else 0)
            )
            
            # 틀린 경우 wrong_count 증가
            if not is_correct:
                self.execute(
                    "UPDATE Word SET wrong_count = wrong_count + 1 WHERE word_id = ?",
                    (word_id,)
                )
                
            self.commit()
            return True
        except Exception as e:
            print(f"퀴즈 결과 기록 오류: {e}")
            self.rollback()
            return False

# 모듈 레벨에서 인스턴스 생성
quiz_db = QuizDB() 
