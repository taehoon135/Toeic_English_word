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
def setup_user_and_words_for_get_cat(db_path, user_db_for_category, word_db_for_category):
    user_id = user_db_for_category.register_user("cat_user_getlist", "pw_getlist", "Cat User GetList")
    assert user_id is not None
    word_id1 = word_db_for_category.add_word("word_getcat1", "단어_겟카테1")
    assert word_id1 is not None
    word_id2 = word_db_for_category.add_word("word_getcat2", "단어_겟카테2")
    assert word_id2 is not None
    return user_id, word_id1, word_id2

def test_get_categories_by_user(category_db_instance, user_db_for_category, setup_user_and_words_for_get_cat):
    """Test Case: 특정 사용자의 카테고리 목록 조회 (단어 수 포함)"""
    # Arrange
    user_id, word_id1, word_id2 = setup_user_and_words_for_get_cat
    cat1_name = "Tech Books GetList"
    cat2_name = "Cooking Recipes GetList"
    cat3_name = "Empty Category GetList"

    cat1_id = category_db_instance.create_category(user_id, cat1_name)
    cat2_id = category_db_instance.create_category(user_id, cat2_name)
    category_db_instance.create_category(user_id, cat3_name) # 단어 없는 카테고리

    category_db_instance.add_word_to_category(cat1_id, word_id1)
    category_db_instance.add_word_to_category(cat1_id, word_id2)
    category_db_instance.add_word_to_category(cat2_id, word_id1)

    # 다른 사용자의 카테고리 (조회되면 안됨)
    # user_db_for_category fixture를 사용하여 user_id가 중복되지 않도록 주의
    other_user_id = user_db_for_category.register_user("other_cat_user_getlist", "pw_other", "Other GetList") 
    category_db_instance.create_category(other_user_id, "Others Category GetList")

    # Act
    user_categories = category_db_instance.get_categories_by_user(user_id)
    
    # Assert
    assert len(user_categories) == 3 
    
    tech_books_cat = next((c for c in user_categories if c['name'] == cat1_name), None)
    assert tech_books_cat is not None
    assert tech_books_cat['word_count'] == 2
    
    cooking_cat = next((c for c in user_categories if c['name'] == cat2_name), None)
    assert cooking_cat is not None
    assert cooking_cat['word_count'] == 1

    empty_cat = next((c for c in user_categories if c['name'] == cat3_name), None)
    assert empty_cat is not None
    assert empty_cat['word_count'] == 0 