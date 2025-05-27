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
    user_id = user_db_for_category.register_user("cat_user_update_exist", "pw_upd_exist", "Cat User UpdateExistName")
    assert user_id is not None
    return user_id, None, None

def test_update_category_name_to_existing_for_same_user(category_db_instance, setup_user_and_word):
    """Test Case: 동일 사용자에게 이미 있는 다른 카테고리 이름으로 변경 시도 (실패)"""
    # Arrange
    user_id, _, _ = setup_user_and_word
    cat_name1 = "CategoryToUpdate"
    cat_name2 = "ExistingOtherCategory"
    cat_id1 = category_db_instance.create_category(user_id, cat_name1)
    category_db_instance.create_category(user_id, cat_name2) # 이 이름으로 변경 시도
    
    # Act
    success = category_db_instance.update_category_name(cat_id1, user_id, cat_name2)
    
    # Assert
    assert success is False, "이미 사용 중인 이름으로 변경 시 False를 반환해야 합니다."
    original_cat = category_db_instance.get_category(cat_id1)
    assert original_cat['name'] == cat_name1, "카테고리 이름이 변경되지 않았어야 합니다." 