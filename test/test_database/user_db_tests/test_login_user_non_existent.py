import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_login_user_non_existent(user_db_instance):
    """Test Case: 존재하지 않는 사용자로 로그인 시도"""
    # Arrange
    user_login_id = "nonexistentuser"
    user_pw = "anypassword"
    
    # Act
    logged_in_user = user_db_instance.login_user(user_login_id, user_pw)
    
    # Assert
    assert logged_in_user is None, "존재하지 않는 사용자로 로그인 시 None이 반환되어야 합니다." 