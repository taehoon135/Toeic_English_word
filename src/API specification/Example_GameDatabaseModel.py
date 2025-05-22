from typing import List, Dict, Optional
from database.game_db import game_db

class Example_GameDatabaseModel:
    """
    게임 데이터베이스 모델
    
    이 클래스는 게임 관련 데이터베이스 작업을 처리합니다.
    실제 사용되는 핵심 기능만 포함되어 있습니다.
    """
    
    def __init__(self):
        """
        게임 데이터베이스 모델 초기화
        """
        self.game_db = game_db

    def get_random_words(self, count: int = 10, category_id: Optional[int] = None) -> List[Dict]:
        """
        게임용 랜덤 단어 목록을 조회합니다.
        
        Args:
            count (int, optional): 조회할 단어 수. 기본값은 10입니다.
            category_id (int, optional): 특정 카테고리의 단어만 조회할 경우 카테고리 ID. 기본값은 None입니다.
        
        Returns:
            List[Dict]: 단어 정보를 담은 딕셔너리 리스트
                각 딕셔너리는 다음 키를 포함합니다:
                - word_id: 단어 ID
                - word: 영어 단어
                - meaning: 한글 의미
                - category_id: 카테고리 ID
                - category_name: 카테고리 이름
        
        Example:
            >>> model = Example_GameDatabaseModel()
            >>> words = model.get_random_words(count=10, category_id=1)
            >>> print(words)
            [
                {'word_id': 1, 'word': 'apple', 'meaning': '사과', 'category_id': 1, 'category_name': '과일'},
                ...
            ]
        """
        return self.game_db.get_random_words(count, category_id)

    def record_game_result(self, user_id: int, score: int, game_type: str = 'rain') -> bool:
        """
        게임 결과를 기록합니다.
        
        Args:
            user_id (int): 사용자 ID
            score (int): 획득한 점수
            game_type (str, optional): 게임 타입. 기본값은 'rain'입니다.
        
        Returns:
            bool: 기록 성공 여부 (True: 성공, False: 실패)
        
        Example:
            >>> model = Example_GameDatabaseModel()
            >>> success = model.record_game_result(user_id=1, score=100, game_type='rain')
            >>> print(success)
            True
        """
        return self.game_db.record_game_result(user_id, score, game_type)

    def get_high_scores(self, limit: int = 10, game_type: str = 'rain') -> List[Dict]:
        """
        최고 점수 목록을 조회합니다.
        Args:
            limit: 조회할 기록 수 (기본값: 10)
            game_type: 게임 타입 (기본값: 'rain')
        Returns:
            List[Dict]: 최고 점수 목록
        """
        return self.game_db.get_high_scores(limit, game_type) 
