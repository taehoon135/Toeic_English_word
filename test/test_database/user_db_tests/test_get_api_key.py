import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_get_api_key(user_db_instance):
    """Test Case: 사용자 API 키 조회"""
    # Arrange
    api_key = "test_api_key_value"
    user_id = user_db_instance.register_user("getapikeyuser", "pw", "Get API User", user_api=api_key)
    
    # Act
    retrieved_api_key = user_db_instance.get_api_key(user_id)
    
    # Assert
    assert retrieved_api_key == api_key 