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
def setup_users_for_permission_test(db_path, user_db_for_category):
    user1_id = user_db_for_category.register_user("cat_user_upd_perm1", "pw_upd_p1", "Cat User UpdPerm1_Owner")
    assert user1_id is not None
    user2_id = user_db_for_category.register_user("cat_user_upd_perm2_other", "pw_upd_p2", "Cat User UpdPerm2_Other")
    assert user2_id is not None
    assert user1_id != user2_id
    return user1_id, user2_id

def test_update_category_permission_denied(category_db_instance, setup_users_for_permission_test):
    """Test Case: 다른 사용자의 카테고리 이름 변경 시도 (실패)"""
    # Arrange
    user1_id, user2_id = setup_users_for_permission_test
    original_name = "User1s Category For UpdatePermTest"
    cat_id_user1 = category_db_instance.create_category(user1_id, original_name)
    assert cat_id_user1 is not None
    
    new_name_by_other = "Attempted Update By Other"

    # Act: user2가 user1의 카테고리 이름 변경 시도
    success = category_db_instance.update_category_name(cat_id_user1, user2_id, new_name_by_other)
    
    # Assert
    assert success is False, "다른 사용자의 카테고리 이름은 변경할 수 없어야 합니다."
    category_after_attempt = category_db_instance.get_category(cat_id_user1)
    assert category_after_attempt['name'] == original_name, "카테고리 이름이 변경되지 않았어야 합니다." 