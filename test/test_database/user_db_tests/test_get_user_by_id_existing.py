import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_get_user_by_id_existing(user_db_instance):
    """Test Case: 존재하는 사용자 ID로 정보 조회"""
    # Arrange
    user_id = user_db_instance.register_user("getuser", "pw", "GetUser")
    
    # Act
    found_user = user_db_instance.get_user_by_id(user_id)
    
    # Assert
    assert found_user is not None
    assert found_user['user_id'] == user_id
    assert found_user['user_login_id'] == "getuser" 