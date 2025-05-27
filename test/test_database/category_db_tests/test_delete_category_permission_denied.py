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
    user1_id = user_db_for_category.register_user("cat_user_del_perm1", "pw_del_perm1", "Cat User DelPerm1")
    assert user1_id is not None
    # 단어는 이 테스트에서 직접 사용되지 않음
    return user1_id, None, None 

def test_delete_category_permission_denied(category_db_instance, user_db_for_category, setup_user_and_word):
    """Test Case: 다른 사용자의 카테고리 삭제 시도 (실패해야 함)"""
    # Arrange
    user1_id, _, _ = setup_user_and_word
    category_name = "User1s Category For PermTest"
    cat_id_user1 = category_db_instance.create_category(user1_id, category_name)
    assert cat_id_user1 is not None

    # 다른 사용자 생성 (user_db_for_category fixture 직접 사용)
    user2_id = user_db_for_category.register_user("cat_user_del_perm2_attacker", "pw_del_perm2", "Cat User DelPerm2 Attacker")
    assert user2_id is not None
    assert user1_id != user2_id

    # Act: user2가 user1의 카테고리 삭제 시도
    success = category_db_instance.delete_category(cat_id_user1, user2_id)

    # Assert
    assert success is False, "다른 사용자의 카테고리는 삭제할 수 없어야 합니다."
    assert category_db_instance.get_category(cat_id_user1) is not None, "삭제 시도 후에도 카테고리는 남아있어야 합니다." 