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
    user_id = user_db_for_category.register_user("cat_user_delete_succ", "pw_del_succ", "Cat User DelSucc")
    assert user_id is not None
    word_id1 = word_db_for_category.add_word("word_del_succ1", "단어_삭제성공카테1")
    assert word_id1 is not None
    return user_id, word_id1, None 

def test_delete_category_successful(category_db_instance, setup_user_and_word):
    """Test Case: 카테고리 삭제 (연관된 WordCategory 레코드도 삭제 확인)"""
    # Arrange
    user_id, word_id, _ = setup_user_and_word
    category_id = category_db_instance.create_category(user_id, "To Be Deleted Category")
    category_db_instance.add_word_to_category(category_id, word_id)
    assert category_db_instance.get_category(category_id) is not None
    assert len(category_db_instance.get_words_in_category(category_id)) == 1

    # Act
    success = category_db_instance.delete_category(category_id, user_id)
    
    # Assert
    assert success is True
    assert category_db_instance.get_category(category_id) is None, "삭제된 카테고리는 조회되지 않아야 합니다."
    wc_entry = category_db_instance.fetch_one("SELECT * FROM WordCategory WHERE category_id = ?", (category_id,))
    assert wc_entry is None, "카테고리 삭제 시 WordCategory의 연관 레코드도 삭제되어야 합니다." 