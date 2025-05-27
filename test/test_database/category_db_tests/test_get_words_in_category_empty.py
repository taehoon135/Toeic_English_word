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
    user_id = user_db_for_category.register_user("cat_user_get_empty", "pw_get_empty", "Cat User GetEmpty")
    assert user_id is not None
    # 이 테스트는 단어가 없는 카테고리를 다루므로 단어 생성 불필요
    return user_id, None, None

def test_get_words_in_category_empty(category_db_instance, setup_user_and_word):
    """Test Case: 단어가 없는 카테고리에서 단어 조회"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    category_id = category_db_instance.create_category(user_id, "Empty Words Cat For Test")
    # Act
    words = category_db_instance.get_words_in_category(category_id)
    # Assert
    assert words == [] 