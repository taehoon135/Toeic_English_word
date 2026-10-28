import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_update_wrong_count(word_db_instance):
    """Test Case: 단어 오답 횟수 증가"""
    # Arrange (틀린 횟수는 사용자별)
    from database.user_db import UserDB
    user_db = UserDB(word_db_instance.db_path)
    user_a = user_db.register_user("wrong_user_a", "pw", "A")
    user_b = user_db.register_user("wrong_user_b", "pw", "B")
    user_db.close()
    word_id = word_db_instance.add_word("wrong_test", "오답테스트")
    assert word_db_instance.get_wrong_count(word_id, user_a) == 0

    # Act
    success = word_db_instance.update_wrong_count(word_id, user_a)

    # Assert
    assert success is True
    assert word_db_instance.get_wrong_count(word_id, user_a) == 1
    assert word_db_instance.get_wrong_count(word_id, user_b) == 0, "다른 사용자의 틀린 횟수는 변하지 않아야 합니다."
    words_a = {w['word_id']: w for w in word_db_instance.get_all_words(user_a)}
    assert words_a[word_id]['wrong_count'] == 1 