import pytest
from database.category_db import CategoryDB
from database.user_db import UserDB
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_for_category(db_path):
    db = UserDB(db_path)
    yield db
    db.close()

@pytest.fixture
def word_db_for_category(db_path):
    db = WordDB(db_path)
    yield db
    db.close()

@pytest.fixture
def category_db_instance(db_path, user_db_for_category):
    db = CategoryDB(db_path)
    yield db
    db.close()

@pytest.fixture
def setup_user_and_word(db_path, user_db_for_category, word_db_for_category):
    user_id = user_db_for_category.register_user("cat_user_dup_same", "pw_dup_s", "Category User Dup Same")
    assert user_id is not None
    # 이 테스트에서는 단어 ID가 직접 필요하지 않음
    return user_id, None, None 

def test_create_duplicate_category_for_same_user(category_db_instance, setup_user_and_word):
    """Test Case: 동일 사용자가 중복된 이름의 카테고리 생성 시도 (기존 ID 반환)"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    category_name = "Duplicate Category Same User"
    category_id1 = category_db_instance.create_category(user_id, category_name)
    
    # Act
    category_id2 = category_db_instance.create_category(user_id, category_name)
    
    # Assert
    assert category_id1 == category_id2, "중복 카테고리 생성 시 기존 ID를 반환해야 합니다." 