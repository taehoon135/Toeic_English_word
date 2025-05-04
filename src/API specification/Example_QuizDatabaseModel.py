"""
QuizDB API 명세서

- 퀴즈 생성, 문제 추가, 퀴즈 조회, 결과 기록 등 퀴즈 관련 DB 함수 명세
"""

# 퀴즈 생성
def create_quiz(quiz_type, category_id=None):
    """
    Args:
        quiz_type (str): 퀴즈 유형
        category_id (int): 카테고리 PK(선택)
    Returns:
        int: 생성된 quiz_id
    Example:
        quiz_id = quiz_db.create_quiz('multiple_choice', 1)
    """
    pass

# 퀴즈에 문제 추가
def add_quiz_question(quiz_id, question, correct_answer, options=None, hint=None):
    """
    Args:
        quiz_id (int): 퀴즈 PK
        question (str): 문제 내용
        correct_answer (str): 정답
        options (str): 객관식 선택지(쉼표 구분, 선택)
        hint (str): 힌트(선택)
    Returns:
        int: 생성된 question_id
    Example:
        qid = quiz_db.add_quiz_question(1, '사과는?', 'apple', 'apple,banana,orange', 'a로 시작')
    """
    pass

# 퀴즈 상세 정보(문제 포함) 조회
def get_quiz(quiz_id):
    """
    Args:
        quiz_id (int): 퀴즈 PK
    Returns:
        dict: 퀴즈 정보 및 문제 리스트
    Example:
        quiz = quiz_db.get_quiz(1)
    """
    pass

# 퀴즈 결과 기록
def record_quiz_result(user_id, word_id, is_correct):
    """
    Args:
        user_id (int): 사용자 PK
        word_id (int): 단어 PK
        is_correct (bool): 정답 여부
    Returns:
        bool: 성공 여부
    Example:
        quiz_db.record_quiz_result(1, 10, True)
    """
    pass 