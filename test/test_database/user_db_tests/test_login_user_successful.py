import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_login_user_successful(user_db_instance):
    """Test Case: 성공적인 사용자 로그인"""
    # Arrange
    user_login_id = "loginuser"
    user_pw = "securepassword"
    user_name = "Login User"
    user_db_instance.register_user(user_login_id, user_pw, user_name)
    
    # Act
    logged_in_user = user_db_instance.login_user(user_login_id, user_pw)
    
    # Assert
    assert logged_in_user is not None, "로그인에 성공해야 합니다."
    assert logged_in_user['user_login_id'] == user_login_id
    assert logged_in_user['user_name'] == user_name 