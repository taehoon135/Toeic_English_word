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
    user_id = user_db_for_category.register_user("cat_user_add_nonword", "pw_add_nonword", "Cat User AddNonWord")
    assert user_id is not None
    # 이 테스트는 존재하지 않는 단어를 사용하므로, 단어 생성 불필요
    return user_id, None, None 

def test_add_word_to_category_non_existent_word(category_db_instance, setup_user_and_word):
    """Test Case: 존재하지 않는 단어를 카테고리에 추가 시도"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    category_id = category_db_instance.create_category(user_id, "Words Collection For NonExistWord")
    non_existent_word_id = 99998 # 존재하지 않을 가능성이 매우 높은 ID
    # Act
    success = category_db_instance.add_word_to_category(category_id, non_existent_word_id)
    # Assert
    assert success is False 