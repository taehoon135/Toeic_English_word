import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_update_api_key(user_db_instance):
    """Test Case: 사용자 API 키 변경"""
    # Arrange
    user_id = user_db_instance.register_user("apikeyuser", "pw", "API User", user_api="old_api_key")
    new_api_key = "new_api_key_12345"
    
    # Act
    update_success = user_db_instance.update_api_key(user_id, new_api_key)
    
    # Assert
    assert update_success is True
    updated_user = user_db_instance.get_user_by_id(user_id)
    assert updated_user['user_api'] == new_api_key 