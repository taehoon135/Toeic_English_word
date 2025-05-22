from typing import List, Dict, Optional
from database.quiz_db import quiz_db

class Example_QuizDatabaseModel:
    """
    퀴즈 데이터베이스 모델
    
    이 클래스는 퀴즈 관련 데이터베이스 작업을 처리합니다.
    실제 사용되는 핵심 기능만 포함되어 있습니다.
    """
    
    def __init__(self):
        """
        퀴즈 데이터베이스 모델 초기화
        """
        self.quiz_db = quiz_db

    def get_random_words_for_quiz(self, count: int = 5, category_id: Optional[int] = None) -> List[Dict]:
        """
        퀴즈용 랜덤 단어 목록을 조회합니다.
        
        Args:
            count (int, optional): 조회할 단어 수. 기본값은 5입니다.
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
            >>> model = Example_QuizDatabaseModel()
            >>> words = model.get_random_words_for_quiz(count=5, category_id=1)
            >>> print(words)
            [
                {'word_id': 1, 'word': 'apple', 'meaning': '사과', 'category_id': 1, 'category_name': '과일'},
                ...
            ]
        """
        return self.quiz_db.get_random_words_for_quiz(count, category_id)

    def record_quiz_result(self, user_id: int, word_id: int, is_correct: bool) -> bool:
        """
        퀴즈 결과를 기록합니다.
        
        Args:
            user_id (int): 사용자 ID
            word_id (int): 단어 ID
            is_correct (bool): 정답 여부 (True: 정답, False: 오답)
        
        Returns:
            bool: 기록 성공 여부 (True: 성공, False: 실패)
        
        Example:
            >>> model = Example_QuizDatabaseModel()
            >>> success = model.record_quiz_result(user_id=1, word_id=1, is_correct=True)
            >>> print(success)
            True
        """
        return self.quiz_db.record_quiz_result(user_id, word_id, is_correct) 
