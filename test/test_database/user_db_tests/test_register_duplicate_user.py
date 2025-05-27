import pytest
from database.user_db import UserDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_instance(db_path):
    """UserDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = UserDB(db_path)
    yield db
    db.close()

def test_register_duplicate_user(user_db_instance):
    """Test Case: 중복된 로그인 ID로 사용자 등록 시도"""
    # Arrange
    user_login_id = "duplicateuser"
    user_pw = "password123"
    user_name = "Duplicate User"
    user_db_instance.register_user(user_login_id, user_pw, user_name) # 먼저 등록
    
    # Act
    duplicate_user_id = user_db_instance.register_user(user_login_id, "anotherpassword", "Another Name")
    
    # Assert
    assert duplicate_user_id is None, "중복 사용자 등록 시 None이 반환되어야 합니다." 