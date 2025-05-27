import pytest
from database.category_db import CategoryDB
from database.user_db import UserDB
from database.word_db import WordDB # setup_user_and_word에서 사용될 수 있으므로 import 유지

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
    user_id = user_db_for_category.register_user("cat_user_update_name_succ", "pw_upd_succ", "Cat User UpdateNameSucc")
    assert user_id is not None
    return user_id, None, None

def test_update_category_name_successful(category_db_instance, setup_user_and_word):
    """Test Case: 카테고리 이름 변경 성공"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    original_name = "Original Category Name"
    new_name = "Updated Category Name"
    category_id = category_db_instance.create_category(user_id, original_name)
    
    # Act
    success = category_db_instance.update_category_name(category_id, user_id, new_name)
    
    # Assert
    assert success is True
    updated_category = category_db_instance.get_category(category_id)
    assert updated_category is not None
    assert updated_category['name'] == new_name
    assert updated_category['user_id'] == user_id
