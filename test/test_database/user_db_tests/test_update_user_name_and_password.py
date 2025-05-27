import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_update_user_name_and_password(user_db_instance):
    """Test Case: 사용자 이름 및 비밀번호 변경"""
    # Arrange
    user_id = user_db_instance.register_user("updateuser2", "oldpw", "Old Name 2")
    new_name = "New Name 2"
    new_pw = "newpw123"
    
    # Act
    update_success = user_db_instance.update_user(user_id, new_name, new_pw)
    
    # Assert
    assert update_success is True
    # 변경된 비밀번호로 로그인 시도
    logged_in_user = user_db_instance.login_user("updateuser2", new_pw)
    assert logged_in_user is not None
    assert logged_in_user['user_name'] == new_name 