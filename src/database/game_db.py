from typing import List, Dict
from .base_db import BaseDatabase, DB_PATH

class GameDB(BaseDatabase):
    # GameDB 인스턴스 초기화
    def __init__(self, db_path: str = DB_PATH):
        super().__init__(db_path)
        self.initialize_tables()

    def initialize_tables(self):
        # Rain Game 점수 테이블 생성
        self.execute("""
        CREATE TABLE IF NOT EXISTS Rain_Game_Score (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
        """)
        self.commit()

    def save_rain_game_score(self, user_id: int, score: int) -> bool:
        """
        Rain Game 점수를 저장합니다.
        Args:
            user_id: 사용자 ID
            score: 획득한 점수
        Returns:
            bool: 성공 여부
        """
        try:
            self.execute(
                "INSERT INTO Rain_Game_Score (user_id, score) VALUES (?, ?)",
                (user_id, score)
            )
            self.commit()
            return True
        except Exception as e:
            print(f"Rain Game 점수 저장 오류: {e}")
            self.rollback()
            return False

    def get_user_high_score(self, user_id: int) -> int:
        """
        사용자의 최고 점수를 조회합니다.
        Args:
            user_id: 사용자 ID
        Returns:
            int: 최고 점수
        """
        result = self.fetch_one(
            "SELECT MAX(score) as high_score FROM Rain_Game_Score WHERE user_id = ?",
            (user_id,)
        )
        return result['high_score'] if result and result['high_score'] is not None else 0

    def get_rain_game_ranking(self, limit: int = 10) -> List[Dict]:
        """
        Rain Game 랭킹을 조회합니다.
        Args:
            limit: 조회할 상위 랭킹 수
        Returns:
            List[Dict]: 랭킹 목록 (사용자 정보와 최고 점수 포함)
        """
        return self.fetch_all("""
            SELECT u.user_id, u.user_name, MAX(rgs.score) as high_score
            FROM User u
            JOIN Rain_Game_Score rgs ON u.user_id = rgs.user_id
            GROUP BY u.user_id, u.user_name
            ORDER BY high_score DESC
            LIMIT ?
        """, (limit,))

    def get_user_recent_scores(self, user_id: int, limit: int = 5) -> List[Dict]:
        """
        사용자의 최근 점수 기록을 조회합니다.
        Args:
            user_id: 사용자 ID
            limit: 조회할 기록 수
        Returns:
            List[Dict]: 최근 점수 기록
        """
        return self.fetch_all("""
            SELECT score, played_at
            FROM Rain_Game_Score
            WHERE user_id = ?
            ORDER BY played_at DESC
            LIMIT ?
        """, (user_id, limit))

# GameDB 인스턴스 생성
game_db = GameDB() 
