from typing import Dict, List, Optional
from .base_db import BaseDatabase

class GameDB(BaseDatabase):
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        super().__init__(db_path)
        self.create_game_score_table()

    def add_score(self, user_id: int, game_type: str, score: int) -> bool:
        """게임 점수 추가"""
        try:
            self.execute(
                """
                INSERT INTO GameScore (user_id, game_type, score)
                VALUES (?, ?, ?)
                """,
                (user_id, game_type, score)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"점수 추가 오류: {e}")
            self.rollback()
            return False

    def get_user_scores(self, user_id: int) -> List[Dict]:
        """사용자의 게임 점수 조회"""
        return self.fetch_all(
            """
            SELECT * FROM GameScore
            WHERE user_id = ?
            ORDER BY played_at DESC
            """,
            (user_id,)
        )

    def get_high_scores(self, game_type: str, limit: int = 10) -> List[Dict]:
        """게임별 최고 점수 조회"""
        return self.fetch_all(
            """
            SELECT g.*, u.username
            FROM GameScore g
            JOIN User u ON g.user_id = u.user_id
            WHERE g.game_type = ?
            ORDER BY g.score DESC
            LIMIT ?
            """,
            (game_type, limit)
        )

    def get_user_ranking(self, user_id: int, game_type: str) -> Optional[int]:
        """사용자의 게임 랭킹 조회"""
        result = self.fetch_one(
            """
            WITH RankedScores AS (
                SELECT user_id, score,
                       RANK() OVER (ORDER BY score DESC) as rank
                FROM GameScore
                WHERE game_type = ?
                GROUP BY user_id
                HAVING score = MAX(score)
            )
            SELECT rank
            FROM RankedScores
            WHERE user_id = ?
            """,
            (game_type, user_id)
        )
        return result['rank'] if result else None

# GameDB 인스턴스 생성
game_db = GameDB() 