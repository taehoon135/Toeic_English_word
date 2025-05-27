import pytest
from database.word_db import WordDB
from database.category_db import CategoryDB
from database.user_db import UserDB # category_db_instance_for_word 에서 사용

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

@pytest.fixture
def category_db_instance_for_word(db_path):
    """WordDB 테스트에서 Category 관련 상호작용이 필요할 때 사용합니다."""
    # UserDB 테이블도 CategoryDB가 의존하므로 UserDB도 초기화 필요
    UserDB(db_path).initialize_tables() # User 테이블 생성

    db = CategoryDB(db_path)
    # 테스트용 사용자 생성 (CategoryDB는 user_id를 요구)
    user_db_conn = UserDB(db_path) # 별도 연결 사용 또는 db_path로 새 인스턴스
    test_user_id = user_db_conn.register_user("word_test_user_for_category", "pw", "Word Test User Cat")
    user_db_conn.close()
    
    yield db, test_user_id 
    db.close()

def test_delete_word_also_deletes_from_word_category(db_path, word_db_instance, category_db_instance_for_word):
    """Test Case: 단어 삭제 시 WordCategory의 연관 레코드도 삭제되는지 확인 (CASCADE)"""
    # Arrange
    category_db, test_user_id = category_db_instance_for_word
    
    # 테스트용 카테고리 생성
    category_id = category_db.create_category(test_user_id, "Test Category for Word Deletion")
    assert category_id is not None and category_id > 0

    # 테스트용 단어 생성
    word_id = word_db_instance.add_word("cascade_word", "연쇄삭제단어")
    assert word_id is not None

    add_to_category_success = category_db.add_word_to_category(category_id, word_id)
    assert add_to_category_success is True
    
    linked_entry = category_db.fetch_one("SELECT * FROM WordCategory WHERE category_id = ? AND word_id = ?", (category_id, word_id))
    assert linked_entry is not None

    # Act: 단어 삭제
    delete_success = word_db_instance.delete_word(word_id)
    
    # Assert
    assert delete_success is True
    assert word_db_instance.fetch_one("SELECT * FROM Word WHERE word_id = ?", (word_id,)) is None
    linked_entry_after_delete = category_db.fetch_one("SELECT * FROM WordCategory WHERE category_id = ? AND word_id = ?", (category_id, word_id))
    assert linked_entry_after_delete is None, "Word 삭제 시 WordCategory의 연관 레코드가 삭제되지 않았습니다." 