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
    user_id = user_db_for_category.register_user("cat_user_remove_word", "pw_remove", "Cat User RemoveWord")
    assert user_id is not None
    word_id1 = word_db_for_category.add_word("word_remove1", "단어_삭제될1")
    assert word_id1 is not None
    word_id2 = word_db_for_category.add_word("word_remove2", "단어_남아있을2")
    assert word_id2 is not None
    return user_id, word_id1, word_id2

def test_remove_word_from_category(category_db_instance, setup_user_and_word):
    """Test Case: 카테고리에서 단어 제거"""
    # Arrange
    user_id, word_id1, word_id2 = setup_user_and_word
    category_id = category_db_instance.create_category(user_id, "Temporary Words For Removal")
    category_db_instance.add_word_to_category(category_id, word_id1)
    category_db_instance.add_word_to_category(category_id, word_id2)
    
    # Act
    success = category_db_instance.remove_word_from_category(category_id, word_id1)
    
    # Assert
    assert success is True
    words_in_cat = category_db_instance.get_words_in_category(category_id)
    assert len(words_in_cat) == 1
    assert words_in_cat[0]['id'] == word_id2 