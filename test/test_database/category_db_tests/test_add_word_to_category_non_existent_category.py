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
    # 이 테스트는 사용자 ID가 직접 필요하지 않음, 단어 ID만 필요
    user_id = user_db_for_category.register_user("cat_user_add_noncat", "pw_add_noncat", "Cat User AddNonCat") 
    word_id1 = word_db_for_category.add_word("word_add_noncat1", "단어_애드논캣1")
    assert word_id1 is not None
    return user_id, word_id1, None

def test_add_word_to_category_non_existent_category(category_db_instance, setup_user_and_word):
    """Test Case: 존재하지 않는 카테고리에 단어 추가 시도"""
    # Arrange
    _, word_id, _ = setup_user_and_word # 사용자 ID는 이 테스트에서 직접 사용되지 않음
    non_existent_category_id = 99999 # 존재하지 않을 가능성이 매우 높은 ID
    # Act
    success = category_db_instance.add_word_to_category(non_existent_category_id, word_id)
    # Assert
    assert success is False 