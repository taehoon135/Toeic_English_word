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
    user_id = user_db_for_category.register_user("cat_user_get_or_create_new", "pw_goc_n", "Cat User GoCNew")
    assert user_id is not None
    return user_id, None, None

def test_get_or_create_category_new(category_db_instance, setup_user_and_word):
    """Test Case: 존재하지 않는 카테고리를 get_or_create_category로 생성하기"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    category_name = "New Category For GoC"
    
    # Act
    cat_id, created = category_db_instance.get_or_create_category(user_id, category_name)
    
    # Assert
    assert cat_id is not None
    assert isinstance(cat_id, int) and cat_id > 0
    assert created is True, "새로 생성되었으므로 created는 True여야 합니다."
    retrieved_category = category_db_instance.get_category(cat_id)
    assert retrieved_category is not None
    assert retrieved_category['name'] == category_name 