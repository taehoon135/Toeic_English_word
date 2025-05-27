import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_change_password_wrong_old_password(user_db_instance):
    """Test Case: 잘못된 현재 비밀번호로 변경 시도"""
    # Arrange
    user_login_id = "changepwuser2"
    old_pw = "correctOldPassword"
    new_pw = "newPassword789"
    user_id = user_db_instance.register_user(user_login_id, old_pw, "Change PW User 2")
    
    # Act
    change_success = user_db_instance.change_password(user_id, "incorrectOldPassword", new_pw)
    
    # Assert
    assert change_success is False, "잘못된 이전 비밀번호로 변경 시 False가 반환되어야 합니다."
    # 비밀번호가 변경되지 않았는지 확인 (이전 비밀번호로 로그인 성공)
    logged_in_user = user_db_instance.login_user(user_login_id, old_pw)
    assert logged_in_user is not None, "비밀번호 변경 실패 시 이전 비밀번호로 로그인이 가능해야 합니다." 