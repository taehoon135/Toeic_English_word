from typing import Dict, List, Optional
from .base_db import BaseDatabase, DB_PATH
from .word_db import WORD_WITH_WRONG_COUNT, WRONG_COUNT_UP, WRONG_COUNT_DOWN
import random

class QuizDB(BaseDatabase):
    def __init__(self, db_path: str = DB_PATH):
        super().__init__(db_path)

    def create_quiz(self, quiz_type: str, user_id: Optional[int] = None, category_id: Optional[int] = None) -> Optional[int]:
        """
        새로운 퀴즈(1회 풀이 세션)를 생성합니다.
        Args:
            quiz_type: 'short_answer_ek', 'short_answer_ke', 'cloze', 'four_choice', 'rain'
            user_id: 푸는 사용자 ID
            category_id: 선택된 카테고리 ID (전체면 None)
        Returns:
            생성된 퀴즈 ID 또는 None
        """
        if not self.execute(
            "INSERT INTO quiz (quiz_type, user_id, category_id) VALUES (?, ?, ?)",
            (quiz_type, user_id, category_id)
        ):
            self.rollback()
            return None
        self.commit()
        return self.cursor.lastrowid

    def add_quiz_question(self, quiz_id: int, question: str, correct_answer: str,
                         options: Optional[str] = None, hint: Optional[str] = None,
                         word_id: Optional[int] = None) -> Optional[int]:
        """퀴즈에 문제를 추가하고 문제 ID를 반환합니다."""
        if not self.execute(
            """
            INSERT INTO quiz_question
            (quiz_id, question, correct_answer, options, hint, word_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (quiz_id, question, correct_answer, options, hint, word_id)
        ):
            self.rollback()
            return None
        self.commit()
        return self.cursor.lastrowid

    def get_random_words_for_quiz(self, count: Optional[int] = None, category_id: Optional[int] = None,
                                  user_id: Optional[int] = None) -> List[Dict]:
        """
        퀴즈용 단어를 뽑습니다. 해당 사용자가 많이 틀린 단어일수록 뽑힐 확률이 높습니다 (가중치 = wrong_count + 1).
        Args:
            count: 뽑을 개수 (None이면 전부, 순서만 섞음)
            category_id: 카테고리 ID (None이면 전체 단어)
            user_id: 틀린 횟수 기준 사용자 (None이면 균등 추출)
        """
        if category_id is None:
            words = self.fetch_all(WORD_WITH_WRONG_COUNT, (user_id,))
            for w in words:
                w['category_name'] = None
        else:
            words = self.fetch_all(f"""
                SELECT t.*, c.name AS category_name
                FROM ({WORD_WITH_WRONG_COUNT}) t
                JOIN WordCategory wc ON t.word_id = wc.word_id
                JOIN Category c ON c.category_id = wc.category_id
                WHERE wc.category_id = ?
            """, (user_id, category_id))
        # 가중 비복원 추출 (Efraimidis-Spirakis): key = U^(1/w) 상위 count개
        words.sort(key=lambda w: random.random() ** (1 / ((w['wrong_count'] or 0) + 1)), reverse=True)
        return words if count is None else words[:count]

    def record_quiz_result(self, user_id: int, quiz_id: int, word_id: int, is_correct: bool) -> bool:
        """
        문제 1개의 풀이 결과를 기록합니다.
        해당 사용자의 wrong_count: 오답이면 +1, 정답이면 -1 (0 미만으로는 내려가지 않음).
        """
        if not self.execute(
            "INSERT INTO quiz_result (quiz_id, user_id, word_id, is_correct) VALUES (?, ?, ?, ?)",
            (quiz_id, user_id, word_id, 1 if is_correct else 0)
        ):
            self.rollback()  # 존재하지 않는 quiz/user/word (FK 위반)
            return False
        self.execute(WRONG_COUNT_DOWN if is_correct else WRONG_COUNT_UP, (user_id, word_id))
        self.commit()
        return True

# 모듈 레벨에서 인스턴스 생성
quiz_db = QuizDB()
