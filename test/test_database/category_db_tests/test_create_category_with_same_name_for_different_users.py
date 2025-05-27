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
def word_db_for_category(db_path): # setup_user_and_word에서 사용될 수 있으므로 유지
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
    # 이 테스트는 user1_id만 필요, 단어는 불필요
    user1_id = user_db_for_category.register_user("cat_user_diff1", "pw_diff1", "Category User Diff 1")
    assert user1_id is not None
    return user1_id, None, None 

def test_create_category_with_same_name_for_different_users(db_path, category_db_instance, user_db_for_category, setup_user_and_word):
    """Test Case: 다른 사용자가 동일 이름의 카테고리 생성"""
    # Arrange
    user1_id, _, _ = setup_user_and_word
    category_name = "Shared Category Name by Diff Users"
    cat_id_user1 = category_db_instance.create_category(user1_id, category_name)
    assert cat_id_user1 is not None

    # 다른 사용자 생성 (user_db_for_category fixture 직접 사용)
    user2_id = user_db_for_category.register_user("cat_user_diff2", "pw_diff2", "Category User Diff 2")
    assert user2_id is not None
    assert user1_id != user2_id, "테스트를 위해 사용자 ID가 달라야 합니다."
    
    # Act
    cat_id_user2 = category_db_instance.create_category(user2_id, category_name)
    
    # Assert
    assert cat_id_user2 is not None
    assert cat_id_user1 != cat_id_user2, "다른 사용자는 동일 이름으로 별개의 카테고리를 생성할 수 있어야 합니다."
    retrieved_cat2 = category_db_instance.get_category(cat_id_user2)
    assert retrieved_cat2['user_id'] == user2_id 