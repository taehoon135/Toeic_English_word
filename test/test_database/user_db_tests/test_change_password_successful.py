import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_change_password_successful(user_db_instance):
    """Test Case: 비밀번호 변경 성공"""
    # Arrange
    user_login_id = "changepwuser"
    old_pw = "oldPassword123"
    new_pw = "newPassword456"
    user_id = user_db_instance.register_user(user_login_id, old_pw, "Change PW User")
    
    # Act
    change_success = user_db_instance.change_password(user_id, old_pw, new_pw)
    
    # Assert
    assert change_success is True
    # 새 비밀번호로 로그인 확인
    logged_in_user = user_db_instance.login_user(user_login_id, new_pw)
    assert logged_in_user is not None, "새 비밀번호로 로그인이 가능해야 합니다."
    # 이전 비밀번호로 로그인 실패 확인
    logged_in_user_old_pw = user_db_instance.login_user(user_login_id, old_pw)
    assert logged_in_user_old_pw is None, "이전 비밀번호로 로그인이 불가능해야 합니다." 