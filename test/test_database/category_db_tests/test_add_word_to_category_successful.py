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
    user_id = user_db_for_category.register_user("cat_user_add_word_succ", "pw_add_succ", "Cat User AddWordSucc")
    assert user_id is not None
    word_id1 = word_db_for_category.add_word("word_add_succ1", "단어_애드성공1")
    assert word_id1 is not None
    return user_id, word_id1, None # word_id2는 이 테스트에서 불필요

def test_add_word_to_category_successful(category_db_instance, setup_user_and_word):
    """Test Case: 카테고리에 단어 추가 성공"""
    # Arrange
    user_id, word_id, _ = setup_user_and_word
    category_id = category_db_instance.create_category(user_id, "My Words For Add Test")
    
    # Act
    success = category_db_instance.add_word_to_category(category_id, word_id)
    
    # Assert
    assert success is True
    words_in_cat = category_db_instance.get_words_in_category(category_id)
    assert len(words_in_cat) == 1
    assert words_in_cat[0]['id'] == word_id # get_words_in_category는 word_id를 id로 반환 