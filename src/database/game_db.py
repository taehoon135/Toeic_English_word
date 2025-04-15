"""
게임 관련 데이터를 관리하는 데이터베이스 클래스
게임 점수, 진행 상황, 통계 등을 관리합니다.

주요 기능:
- 게임 점수 기록 및 조회
- 게임 통계 관리
- 사용자별 게임 기록 조회

사용 예시:
    >>> game_db = GameDB()
    >>> game_db.save_score(1, "word_quiz", 100)
    >>> scores = game_db.get_user_scores(1)
"""

from typing import Dict, List, Optional, Tuple
from .base_db import BaseDatabase

class GameDB(BaseDatabase):
    """
    게임 관련 데이터를 관리하는 데이터베이스 클래스
    
    Attributes:
        db_path (str): 데이터베이스 파일 경로
    """
    
    def __init__(self, db_path: str = 'toeic_vocabulary.db'):
        """
        GameDB 초기화
        
        Args:
            db_path (str): 데이터베이스 파일 경로 (기본값: 'toeic_vocabulary.db')
        """
        super().__init__(db_path)

    def save_score(self, user_id: int, game_type: str, score: int) -> bool:
        """
        게임 점수를 저장합니다.
        
        Args:
            user_id (int): 사용자 ID
            game_type (str): 게임 종류 ('word_quiz', 'memory_game' 등)
            score (int): 획득한 점수
            
        Returns:
            bool: 저장 성공 여부
            
        Example:
            >>> game_db.save_score(1, "word_quiz", 100)
            True
        """
        try:
            self.execute("""
                INSERT INTO GameScore (user_id, game_type, score)
                VALUES (?, ?, ?)
            """, (user_id, game_type, score))
            
            self.commit()
            return True
        except Exception as e:
            print(f"점수 저장 오류: {e}")
            self.rollback()
            return False

    def get_user_scores(self, user_id: int, game_type: Optional[str] = None) -> List[Dict]:
        """
        사용자의 게임 점수를 조회합니다.
        
        Args:
            user_id (int): 사용자 ID
            game_type (Optional[str]): 게임 종류 (기본값: None, 모든 게임)
            
        Returns:
            List[Dict]: {
                'score_id': int,
                'game_type': str,
                'score': int,
                'created_at': str
            }
            
        Example:
            >>> scores = game_db.get_user_scores(1)
            >>> for score in scores:
            ...     print(f"{score['game_type']}: {score['score']}점")
        """
        try:
            if game_type:
                return self.fetch_all("""
                    SELECT score_id, game_type, score, created_at
                    FROM GameScore
                    WHERE user_id = ? AND game_type = ?
                    ORDER BY created_at DESC
                """, (user_id, game_type))
            else:
                return self.fetch_all("""
                    SELECT score_id, game_type, score, created_at
                    FROM GameScore
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                """, (user_id,))
        except Exception as e:
            print(f"점수 조회 오류: {e}")
            return []

    def get_high_scores(self, game_type: str, limit: int = 10) -> List[Dict]:
        """
        게임별 최고 점수를 조회합니다.
        
        Args:
            game_type (str): 게임 종류
            limit (int): 조회할 상위 점수 개수 (기본값: 10)
            
        Returns:
            List[Dict]: {
                'user_id': int,
                'username': str,
                'score': int,
                'created_at': str
            }
            
        Example:
            >>> high_scores = game_db.get_high_scores("word_quiz")
            >>> for score in high_scores:
            ...     print(f"{score['username']}: {score['score']}점")
        """
        try:
            return self.fetch_all("""
                SELECT gs.user_id, u.username, gs.score, gs.created_at
                FROM GameScore gs
                JOIN User u ON gs.user_id = u.user_id
                WHERE gs.game_type = ?
                ORDER BY gs.score DESC
                LIMIT ?
            """, (game_type, limit))
        except Exception as e:
            print(f"최고 점수 조회 오류: {e}")
            return []

    def get_user_statistics(self, user_id: int) -> Dict:
        """
        사용자의 게임 통계를 조회합니다.
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            Dict: {
                'total_games': int,
                'average_score': float,
                'highest_score': int,
                'game_types': Dict[str, Dict]
            }
            
        Example:
            >>> stats = game_db.get_user_statistics(1)
            >>> print(f"총 게임 수: {stats['total_games']}")
        """
        try:
            # 전체 통계
            total_stats = self.fetch_one("""
                SELECT 
                    COUNT(*) as total_games,
                    AVG(score) as average_score,
                    MAX(score) as highest_score
                FROM GameScore
                WHERE user_id = ?
            """, (user_id,))
            
            # 게임 종류별 통계
            game_type_stats = self.fetch_all("""
                SELECT 
                    game_type,
                    COUNT(*) as game_count,
                    AVG(score) as average_score,
                    MAX(score) as highest_score
                FROM GameScore
                WHERE user_id = ?
                GROUP BY game_type
            """, (user_id,))
            
            # 결과 구성
            result = {
                'total_games': total_stats['total_games'],
                'average_score': round(total_stats['average_score'], 2),
                'highest_score': total_stats['highest_score'],
                'game_types': {}
            }
            
            for stat in game_type_stats:
                result['game_types'][stat['game_type']] = {
                    'game_count': stat['game_count'],
                    'average_score': round(stat['average_score'], 2),
                    'highest_score': stat['highest_score']
                }
            
            return result
        except Exception as e:
            print(f"통계 조회 오류: {e}")
            return {
                'total_games': 0,
                'average_score': 0.0,
                'highest_score': 0,
                'game_types': {}
            }

    def delete_user_scores(self, user_id: int) -> bool:
        """
        사용자의 모든 게임 점수를 삭제합니다.
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            bool: 삭제 성공 여부
            
        Example:
            >>> game_db.delete_user_scores(1)
            True
        """
        try:
            self.execute("""
                DELETE FROM GameScore
                WHERE user_id = ?
            """, (user_id,))
            
            self.commit()
            return True
        except Exception as e:
            print(f"점수 삭제 오류: {e}")
            self.rollback()
            return False

# GameDB 인스턴스 생성
game_db = GameDB() 