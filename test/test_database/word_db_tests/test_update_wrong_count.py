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
    # Arrange
    word_id = word_db_instance.add_word("wrong_test", "오답테스트")
    initial_word = word_db_instance.fetch_one("SELECT wrong_count FROM Word WHERE word_id = ?", (word_id,))
    initial_wrong_count = initial_word['wrong_count']
    
    # Act
    success = word_db_instance.update_wrong_count(word_id)
    
    # Assert
    assert success is True
    updated_word = word_db_instance.fetch_one("SELECT wrong_count FROM Word WHERE word_id = ?", (word_id,))
    assert updated_word['wrong_count'] == initial_wrong_count + 1 