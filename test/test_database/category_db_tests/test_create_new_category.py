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
    user_id = user_db_for_category.register_user("cat_user_create_new", "pw_new", "Category User New")
    assert user_id is not None
    word_id1 = word_db_for_category.add_word("test_word_new1", "테스트단어_새거1")
    assert word_id1 is not None
    word_id2 = word_db_for_category.add_word("test_word_new2", "테스트단어_새거2")
    assert word_id2 is not None
    return user_id, word_id1, word_id2

def test_create_new_category(category_db_instance, setup_user_and_word):
    """Test Case: 새 카테고리 생성 성공"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    category_name = "My First New Category"
    
    # Act
    category_id = category_db_instance.create_category(user_id, category_name)
    
    # Assert
    assert category_id is not None
    assert isinstance(category_id, int) and category_id > 0
    retrieved_category = category_db_instance.get_category(category_id)
    assert retrieved_category is not None
    assert retrieved_category['name'] == category_name
    assert retrieved_category['user_id'] == user_id 