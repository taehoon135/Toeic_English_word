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
    user_id = user_db_for_category.register_user("cat_user_get_or_create_exist", "pw_goc_e", "Cat User GoCExist")
    assert user_id is not None
    return user_id, None, None

def test_get_or_create_category_existing(category_db_instance, setup_user_and_word):
    """Test Case: 이미 존재하는 카테고리를 get_or_create_category로 가져오기"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    category_name = "Existing Category For GoC"
    existing_cat_id = category_db_instance.create_category(user_id, category_name)
    
    # Act
    cat_id, created = category_db_instance.get_or_create_category(user_id, category_name)
    
    # Assert
    assert cat_id == existing_cat_id
    assert created is False, "이미 존재하므로 created는 False여야 합니다." 