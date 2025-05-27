import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_add_new_word(word_db_instance):
    """Test Case: 새 단어 추가 성공"""
    # Arrange
    english = "apple"
    meaning = "사과"
    part_of_speech = "noun"
    example = "An apple a day keeps the doctor away."
    
    # Act
    word_id = word_db_instance.add_word(english, meaning, part_of_speech, example)
    
    # Assert
    assert word_id is not None
    assert isinstance(word_id, int)
    retrieved_word = word_db_instance.fetch_one("SELECT * FROM Word WHERE word_id = ?", (word_id,))
    assert retrieved_word['english'] == english
    assert retrieved_word['meaning'] == meaning 