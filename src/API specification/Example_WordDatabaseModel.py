from typing import List, Dict, Optional
from database.word_db import word_db

class Example_WordDatabaseModel:
    """
    단어 데이터베이스 모델
    
    이 클래스는 단어 관련 데이터베이스 작업을 처리합니다.
    실제 사용되는 핵심 기능만 포함되어 있습니다.
    """
    
    def __init__(self):
        """
        단어 데이터베이스 모델 초기화
        """
        self.word_db = word_db

    def get_all_words(self) -> List[Dict]:
        """
        모든 단어 목록을 조회합니다.
        
        Returns:
            List[Dict]: 단어 정보를 담은 딕셔너리 리스트
                각 딕셔너리는 다음 키를 포함합니다:
                - word_id: 단어 ID
                - english: 영어 단어
                - meaning: 한글 의미
                - part_of_speech: 품사
                - example_sentence: 예문
                - wrong_count: 틀린 횟수
        """
        return self.word_db.get_all_words()

    def search_words(self, keyword: str) -> List[Dict]:
        """
        단어를 검색합니다 (영어/한글).
        
        Args:
            keyword (str): 검색어
        
        Returns:
            List[Dict]: 검색된 단어 목록
                각 딕셔너리는 다음 키를 포함합니다:
                - word_id: 단어 ID
                - english: 영어 단어
                - meaning: 한글 의미
                - part_of_speech: 품사
                - example_sentence: 예문
                - wrong_count: 틀린 횟수
        """
        return self.word_db.search_words(keyword)

    def add_word(self, english: str, meaning: str, part_of_speech: str = None, example_sentence: str = None) -> int:
        """
        새로운 단어를 추가합니다.
        
        Args:
            english (str): 영어 단어
            meaning (str): 한글 의미
            part_of_speech (str, optional): 품사
            example_sentence (str, optional): 예문
        
        Returns:
            int: 추가된 단어의 ID (실패 시 None)
        """
        return self.word_db.add_word(english, meaning, part_of_speech, example_sentence)

    def update_word(self, word_id: int, word: str, meaning: str, part_of_speech: str, example: str) -> bool:
        """
        단어 정보를 수정합니다.
        
        Args:
            word_id (int): 수정할 단어 ID
            word (str): 영어 단어
            meaning (str): 한글 의미
            part_of_speech (str): 품사
            example (str): 예문
        
        Returns:
            bool: 수정 성공 여부
        """
        return self.word_db.update_word(word_id, word, meaning, part_of_speech, example)

    def delete_word(self, word_id: int) -> bool:
        """
        단어를 삭제합니다.
        
        Args:
            word_id (int): 삭제할 단어 ID
        
        Returns:
            bool: 삭제 성공 여부
        """
        return self.word_db.delete_word(word_id)

    def update_wrong_count(self, word_id: int) -> bool:
        """
        단어의 틀린 횟수를 1 증가시킵니다.
        
        Args:
            word_id (int): 수정할 단어 ID
        
        Returns:
            bool: 수정 성공 여부
        """
        return self.word_db.update_wrong_count(word_id) 
