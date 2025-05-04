"""
WordDB API 명세서

- 단어 추가, 조회, 수정, 삭제, 카테고리 관리 등 단어 관련 DB 함수 명세
"""

# 단어 추가 (카테고리 선택 가능)
def add_word(word, meaning, part_of_speech, example, category_id=None):
    """
    Args:
        word (str): 영어 단어
        meaning (str): 한글 뜻
        part_of_speech (str): 품사
        example (str): 예문
        category_id (int): 카테고리 PK(선택)
    Returns:
        int: 생성된 word_id
    Example:
        word_id = word_db.add_word('apple', '사과', 'noun', 'I like apples.', 1)
    """
    pass

# 전체 단어 목록 조회
def get_all_words():
    """
    Returns:
        list: 단어 리스트
    Example:
        words = word_db.get_all_words()
    """
    pass

# 단어 상세 정보 조회
def get_word_details(word_id):
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        dict: 단어 정보
    Example:
        word = word_db.get_word_details(1)
    """
    pass

# 오답 횟수 1 증가
def update_wrong_count(word_id):
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        word_db.update_wrong_count(1)
    """
    pass

# 단어 검색 (영어/한글)
def search_words(keyword):
    """
    Args:
        keyword (str): 검색어
    Returns:
        list: 검색 결과 리스트
    Example:
        result = word_db.search_words('apple')
    """
    pass

# 단어 정보 수정
def update_word(word_id, word, meaning, part_of_speech, example, category_id=None):
    """
    Args:
        word_id (int): 단어 PK
        word (str): 영어 단어
        meaning (str): 한글 뜻
        part_of_speech (str): 품사
        example (str): 예문
        category_id (int): 카테고리 PK(선택)
    Returns:
        bool: 성공 여부
    Example:
        word_db.update_word(1, 'apple', '사과', 'noun', 'I like apples.', 1)
    """
    pass

# 단어 삭제
def delete_word(word_id):
    """
    Args:
        word_id (int): 단어 PK
    Returns:
        bool: 성공 여부
    Example:
        word_db.delete_word(1)
    """
    pass 