import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_delete_word_existing(word_db_instance):
    """Test Case: 존재하는 단어 삭제"""
    # Arrange
    word_id = word_db_instance.add_word("to_delete", "삭제될 단어")
    assert word_db_instance.fetch_one("SELECT * FROM Word WHERE word_id = ?", (word_id,)) is not None

    # Act
    success = word_db_instance.delete_word(word_id)
    
    # Assert
    assert success is True
    assert word_db_instance.fetch_one("SELECT * FROM Word WHERE word_id = ?", (word_id,)) is None 