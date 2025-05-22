"""
CategoryDB API 명세서 (실제 구현 기준)

- 카테고리 생성, 조회, 수정, 삭제, 단어-카테고리 관계 등 카테고리 관련 DB 함수 명세
"""

from typing import List, Dict, Optional
from database.category_db import category_db

class Example_CategoryDatabaseModel:
    """
    카테고리 데이터베이스 모델
    
    이 클래스는 카테고리 관련 데이터베이스 작업을 처리합니다.
    실제 사용되는 핵심 기능만 포함되어 있습니다.
    """
    
    def __init__(self):
        """
        카테고리 데이터베이스 모델 초기화
        """
        self.category_db = category_db

    def create_category(self, user_id: int, category_name: str) -> int:
        """
        새 카테고리를 생성합니다.
        
        Args:
            user_id (int): 카테고리를 생성할 사용자 ID
            category_name (str): 카테고리 이름
        
        Returns:
            int: 생성된 카테고리의 ID (실패 시 0)
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> category_id = model.create_category(user_id=1, category_name="동물")
            >>> print(category_id)
            1
        """
        return self.category_db.create_category(user_id, category_name)

    def get_categories_by_user(self, user_id: int) -> List[Dict]:
        """
        사용자별 카테고리 목록을 조회합니다.
        
        Args:
            user_id (int): 카테고리를 조회할 사용자 ID
        
        Returns:
            List[Dict]: 카테고리 정보를 담은 딕셔너리 리스트
                각 딕셔너리는 다음 키를 포함합니다:
                - category_id: 카테고리 ID
                - name: 카테고리 이름
                - created_at: 생성 시간
                - word_count: 포함된 단어 수
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> categories = model.get_categories_by_user(user_id=1)
            >>> print(categories)
            [
                {
                    "category_id": 1,
                    "name": "동물",
                    "created_at": "2024-03-15 14:30:00",
                    "word_count": 10
                },
                ...
            ]
        """
        return self.category_db.get_categories_by_user(user_id)

    def delete_category(self, category_id: int, user_id: int) -> bool:
        """
        카테고리를 삭제합니다.
        
        Args:
            category_id (int): 삭제할 카테고리 ID
            user_id (int): 카테고리 소유자 ID (권한 확인용)
        
        Returns:
            bool: 삭제 성공 여부
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> success = model.delete_category(category_id=1, user_id=1)
            >>> print(success)
            True
        """
        return self.category_db.delete_category(category_id, user_id)

    def update_category(self, category_id: int, category_name: str, user_id: int) -> bool:
        """
        카테고리 이름을 수정합니다.
        
        Args:
            category_id (int): 수정할 카테고리 ID
            category_name (str): 새로운 카테고리 이름
            user_id (int): 카테고리 소유자 ID (권한 확인용)
        
        Returns:
            bool: 수정 성공 여부
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> success = model.update_category(category_id=1, category_name="새 이름", user_id=1)
            >>> print(success)
            True
        """
        return self.category_db.update_category(category_id, category_name, user_id)

    def add_word_to_category(self, category_id: int, word_id: int) -> bool:
        """
        단어를 카테고리에 추가합니다.
        
        Args:
            category_id (int): 카테고리 ID
            word_id (int): 추가할 단어 ID
        
        Returns:
            bool: 추가 성공 여부
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> success = model.add_word_to_category(category_id=1, word_id=1)
            >>> print(success)
            True
        """
        return self.category_db.add_word_to_category(category_id, word_id)

    def remove_word_from_category(self, category_id: int, word_id: int) -> bool:
        """
        카테고리에서 단어를 제거합니다.
        
        Args:
            category_id (int): 카테고리 ID
            word_id (int): 제거할 단어 ID
        
        Returns:
            bool: 제거 성공 여부
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> success = model.remove_word_from_category(category_id=1, word_id=1)
            >>> print(success)
            True
        """
        return self.category_db.remove_word_from_category(category_id, word_id)

    def get_words_in_category(self, category_id: int) -> List[Dict]:
        """
        카테고리에 속한 단어 목록을 조회합니다.
        
        Args:
            category_id (int): 조회할 카테고리 ID
        
        Returns:
            List[Dict]: 단어 정보를 담은 딕셔너리 리스트
                각 딕셔너리는 다음 키를 포함합니다:
                - id: 단어 ID
                - english: 영어 단어
                - meaning: 한글 의미
                - part_of_speech: 품사
                - example: 예문
                - wrong_count: 틀린 횟수
        
        Example:
            >>> model = Example_CategoryDatabaseModel()
            >>> words = model.get_words_in_category(category_id=1)
            >>> print(words)
            [
                {
                    "id": 1,
                    "english": "apple",
                    "meaning": "사과",
                    "part_of_speech": "noun",
                    "example": "I like apples.",
                    "wrong_count": 0
                },
                ...
            ]
        """
        return self.category_db.get_words_in_category(category_id)

# 단어가 속한 카테고리 목록 조회
def get_word_categories(word_id: int) -> list:
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        list[dict]: 해당 단어가 속한 카테고리 정보 리스트
    Example:
        categories = category_db.get_word_categories(1)
    """
    pass

# 전체 카테고리 목록 조회 (단어 수 포함)
def get_all_categories() -> list:
    """
    Returns:
        list[dict]: 전체 카테고리 정보 리스트 (단어 수 포함)
    Example:
        categories = category_db.get_all_categories()
    """
    pass 
