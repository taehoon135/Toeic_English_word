"""
UserDB API 명세서

- 회원가입, 로그인, 사용자 정보 수정, 비밀번호 변경 등 사용자 관련 DB 함수 명세
"""

# 회원가입
# 새로운 사용자를 등록합니다.
def register_user(user_login_id, user_pw, user_name, is_admin=0, user_api=None):
    """
    Args:
        user_login_id (str): 로그인용 ID
        user_pw (str): 비밀번호
        user_name (str): 이름
        is_admin (int): 관리자 여부(0/1)
        user_api (str): API KEY(선택)
    Returns:
        int: 생성된 user_id
    Example:
        user_id = user_db.register_user('test1', 'pw123', '홍길동')
    """
    pass

# 로그인
# 로그인 ID, 비밀번호로 사용자 정보 반환
def login_user(user_login_id, user_pw):
    """
    Args:
        user_login_id (str): 로그인용 ID
        user_pw (str): 비밀번호
    Returns:
        dict: 사용자 정보
    Example:
        user = user_db.login_user('test1', 'pw123')
    """
    pass

# 사용자 정보(이름 등) 수정
def update_user_info(user_id, **kwargs):
    """
    Args:
        user_id (int): 사용자 PK
        kwargs: 변경할 필드명=값
    Returns:
        None
    Example:
        user_db.update_user_info(1, user_name='김철수')
    """
    pass

# API KEY 수정
def update_api_key(user_id, new_api_key):
    """
    Args:
        user_id (int): 사용자 PK
        new_api_key (str): 새 API KEY
    Returns:
        None
    Example:
        user_db.update_api_key(1, 'NEWKEY123')
    """
    pass

# user_id로 사용자 정보 조회
def get_user(user_id):
    """
    Args:
        user_id (int): 사용자 PK
    Returns:
        dict: 사용자 정보
    Example:
        user = user_db.get_user(1)
    """
    pass

# 비밀번호 변경
def change_password(user_id, old_password, new_password):
    """
    Args:
        user_id (int): 사용자 PK
        old_password (str): 기존 비밀번호
        new_password (str): 새 비밀번호
    Returns:
        bool: 성공 여부
    Example:
        user_db.change_password(1, 'oldpw', 'newpw')
    """
    pass 