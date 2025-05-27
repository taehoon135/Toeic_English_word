import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_update_word_info(word_db_instance):
    """Test Case: 단어 정보 수정"""
    # Arrange
    word_id = word_db_instance.add_word("old_english", "옛날의미", "old_pos", "old_example")
    new_english = "new_english"
    new_meaning = "새로운의미"
    new_pos = "new_pos"
    new_example = "new_example"
    
    # Act
    # word_db.py의 update_word 메서드 매개변수 순서: word_id, word, meaning, part_of_speech, example_sentence
    # 여기서 'word'는 영어단어를 의미합니다.
    success = word_db_instance.update_word(word_id, new_english, new_meaning, new_pos, new_example)
    
    # Assert
    assert success is True
    updated_word = word_db_instance.fetch_one("SELECT * FROM Word WHERE word_id = ?", (word_id,))
    assert updated_word['english'] == new_english
    assert updated_word['meaning'] == new_meaning
    assert updated_word['part_of_speech'] == new_pos
    assert updated_word['example_sentence'] == new_example 