import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_login_user_invalid_password(user_db_instance):
    """Test Case: 잘못된 비밀번호로 로그인 시도"""
    # Arrange
    user_login_id = "loginuser2"
    user_pw = "correctpassword"
    user_name = "Login User Two"
    user_db_instance.register_user(user_login_id, user_pw, user_name)
    
    # Act
    logged_in_user = user_db_instance.login_user(user_login_id, "wrongpassword")
    
    # Assert
    assert logged_in_user is None, "잘못된 비밀번호로 로그인 시 None이 반환되어야 합니다." 