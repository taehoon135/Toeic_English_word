"""
GameDB API 명세서

- 게임 점수 저장, 랭킹, 통계 등 게임 관련 DB 함수 명세
"""

# 게임 점수 저장
def save_score(user_id, game_type, score):
    """
    Args:
        user_id (int): 사용자 PK
        game_type (str): 게임 종류
        score (int): 점수
    Returns:
        bool: 성공 여부
    Example:
        game_db.save_score(1, 'word_quiz', 100)
    """
    pass

# 사용자별 게임 점수 목록 조회
def get_user_scores(user_id, game_type=None):
    """
    Args:
        user_id (int): 사용자 PK
        game_type (str): 게임 종류(선택)
    Returns:
        list: 점수 리스트
    Example:
        scores = game_db.get_user_scores(1)
    """
    pass

# 게임별 최고 점수(랭킹) 조회
def get_high_scores(game_type, limit=10):
    """
    Args:
        game_type (str): 게임 종류
        limit (int): 상위 N개(기본 10)
    Returns:
        list: 랭킹 리스트
    Example:
        ranking = game_db.get_high_scores('word_quiz', 5)
    """
    pass

# 사용자별 게임 통계 조회
def get_user_statistics(user_id):
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        dict: 통계 정보
    Example:
        stats = game_db.get_user_statistics(1)
    """
    pass 