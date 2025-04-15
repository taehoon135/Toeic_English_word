from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase
import random

class QuizDB(BaseDatabase):
    def get_random_words_for_quiz(self, count: int = 10, category_id: Optional[int] = None) -> List[Dict]:
        """퀴즈용 랜덤 단어 목록 조회"""
        if category_id:
            return self.fetch_all(
                """
                SELECT w.*, c.name as category_name
                FROM Word w
                LEFT JOIN Category c ON w.category_id = c.category_id
                WHERE w.category_id = ?
                ORDER BY RANDOM()
                LIMIT ?
                """,
                (category_id, count)
            )
        else:
            return self.fetch_all(
                """
                SELECT w.*, c.name as category_name
                FROM Word w
                LEFT JOIN Category c ON w.category_id = c.category_id
                ORDER BY RANDOM()
                LIMIT ?
                """,
                (count,)
            )

    def get_words_by_difficulty(self, difficulty_level: int, count: int = 10) -> List[Dict]:
        """난이도별 단어 목록 조회 (wrong_count 기반)"""
        return self.fetch_all(
            """
            SELECT w.*, c.name as category_name
            FROM Word w
            LEFT JOIN Category c ON w.category_id = c.category_id
            WHERE w.wrong_count >= ?
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (difficulty_level, count)
        )

    def record_quiz_result(self, user_id: int, word_id: int, is_correct: bool) -> bool:
        """퀴즈 결과 기록"""
        try:
            # WordHistory에 기록 추가
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
                    """
                    UPDATE Word
                    SET wrong_count = wrong_count + 1
                    WHERE word_id = ?
                    """,
                    (word_id,)
                )
            
            return True
        except Exception as e:
            print(f"퀴즈 결과 기록 오류: {e}")
            return False

    def get_user_quiz_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """사용자의 퀴즈 이력 조회"""
        return self.fetch_all(
            """
            SELECT h.*, w.word, w.meaning, w.part_of_speech
            FROM WordHistory h
            JOIN Word w ON h.word_id = w.word_id
            WHERE h.user_id = ? AND h.study_type = 'quiz'
            ORDER BY h.studied_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        )

    def get_user_weak_words(self, user_id: int, limit: int = 10) -> List[Dict]:
        """사용자의 취약 단어 목록 조회"""
        return self.fetch_all(
            """
            SELECT w.*, 
                   COUNT(CASE WHEN h.is_correct = 0 THEN 1 END) as wrong_count,
                   COUNT(h.history_id) as total_attempts,
                   CAST(COUNT(CASE WHEN h.is_correct = 1 THEN 1 END) AS FLOAT) / 
                   COUNT(h.history_id) * 100 as accuracy_rate
            FROM Word w
            JOIN WordHistory h ON w.word_id = h.word_id
            WHERE h.user_id = ? AND h.study_type = 'quiz'
            GROUP BY w.word_id
            HAVING accuracy_rate < 70
            ORDER BY accuracy_rate ASC
            LIMIT ?
            """,
            (user_id, limit)
        )

    def get_quiz_statistics(self, user_id: int) -> Dict:
        """사용자의 퀴즈 통계 조회"""
        return self.fetch_one(
            """
            SELECT 
                COUNT(DISTINCT h.word_id) as total_words_studied,
                COUNT(h.history_id) as total_attempts,
                COUNT(CASE WHEN h.is_correct = 1 THEN 1 END) as correct_answers,
                CAST(COUNT(CASE WHEN h.is_correct = 1 THEN 1 END) AS FLOAT) / 
                COUNT(h.history_id) * 100 as overall_accuracy
            FROM WordHistory h
            WHERE h.user_id = ? AND h.study_type = 'quiz'
            """,
            (user_id,)
        )

# QuizDB 인스턴스 생성
quiz_db = QuizDB() 