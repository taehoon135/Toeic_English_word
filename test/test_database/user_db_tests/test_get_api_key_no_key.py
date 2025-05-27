import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_get_api_key_no_key(user_db_instance):
    """Test Case: API 키가 없는 사용자 조회"""
    # Arrange
    user_id = user_db_instance.register_user("noapikeyuser", "pw", "No API User")
    
    # Act
    retrieved_api_key = user_db_instance.get_api_key(user_id)
    
    # Assert
    assert retrieved_api_key is None 