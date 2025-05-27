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
    user_id = user_db_for_category.register_user("cat_user_add_dup_word", "pw_add_dup", "Cat User AddDupWord")
    assert user_id is not None
    word_id1 = word_db_for_category.add_word("word_add_dup1", "단어_애드중복1")
    assert word_id1 is not None
    return user_id, word_id1, None

def test_add_duplicate_word_to_category(category_db_instance, setup_user_and_word):
    """Test Case: 이미 카테고리에 있는 단어 중복 추가 시도"""
    # Arrange
    user_id, word_id, _ = setup_user_and_word
    category_id = category_db_instance.create_category(user_id, "Unique Words Only Test")
    category_db_instance.add_word_to_category(category_id, word_id) # 먼저 추가
    
    # Act
    success = category_db_instance.add_word_to_category(category_id, word_id) # 중복 추가
    
    # Assert
    assert success is False, "이미 카테고리에 있는 단어는 추가되지 않아야 합니다 (False 반환 예상)"
    words_in_cat = category_db_instance.get_words_in_category(category_id)
    assert len(words_in_cat) == 1 # 단어 수는 여전히 1이어야 함 