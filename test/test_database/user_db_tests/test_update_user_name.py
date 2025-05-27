import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_update_user_name(user_db_instance):
    """Test Case: 사용자 이름 변경"""
    # Arrange
    user_id = user_db_instance.register_user("updateuser", "pw", "Old Name")
    new_name = "New Name"
    
    # Act
    update_success = user_db_instance.update_user(user_id, new_name)
    
    # Assert
    assert update_success is True, "사용자 정보 수정은 True를 반환해야 합니다."
    updated_user = user_db_instance.get_user_by_id(user_id)
    assert updated_user['user_name'] == new_name 