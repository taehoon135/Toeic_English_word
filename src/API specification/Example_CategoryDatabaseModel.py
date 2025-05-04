"""
CategoryDB API 명세서

- 카테고리 생성, 단어-카테고리 연결, 카테고리별 단어 조회 등 카테고리 관련 DB 함수 명세
"""

# 카테고리 생성
def create_category(user_id, category_name):
    """
    Args:
        user_id (int): 사용자 PK
        category_name (str): 카테고리명
    Returns:
        int: 생성된 category_id
    Example:
        category_id = category_db.create_category(1, '동물')
    """
    pass

# 사용자별 카테고리 목록 조회
def get_user_categories(user_id):
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        list: 카테고리 리스트
    Example:
        categories = category_db.get_user_categories(1)
    """
    pass

# 단어를 카테고리에 추가
def add_word_to_category(category_id, word_id):
    """
    Args:
        category_id (int): 카테고리 PK
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        category_db.add_word_to_category(1, 10)
    """
    pass

# 카테고리에서 단어 제거
def remove_word_from_category(category_id, word_id):
    """
    Args:
        category_id (int): 카테고리 PK
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        category_db.remove_word_from_category(1, 10)
    """
    pass

# 카테고리 삭제
def delete_category(category_id):
    """
    Args:
        category_id (int): 카테고리 PK
    Returns:
        bool: 성공 여부
    Example:
        category_db.delete_category(1)
    """
    pass 