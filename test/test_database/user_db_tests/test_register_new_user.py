import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_register_new_user(user_db_instance):
    """Test Case: 새 사용자 등록 성공"""
    # Arrange
    user_login_id = "testuser1"
    user_pw = "password123"
    user_name = "Test User One"
    
    # Act
    user_id = user_db_instance.register_user(user_login_id, user_pw, user_name)
    
    # Assert
    assert user_id is not None, "사용자 등록 시 ID가 반환되어야 합니다."
    assert isinstance(user_id, int), "사용자 ID는 정수여야 합니다."
    
    registered_user = user_db_instance.get_user_by_id(user_id)
    assert registered_user is not None, "등록된 사용자를 ID로 조회할 수 있어야 합니다."
    assert registered_user['user_login_id'] == user_login_id
    assert registered_user['user_name'] == user_name 