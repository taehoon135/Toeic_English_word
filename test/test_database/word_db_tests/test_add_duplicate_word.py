import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_add_duplicate_word(word_db_instance):
    """Test Case: 중복 단어 추가 시 기존 ID 반환"""
    # Arrange
    english = "banana"
    meaning = "바나나"
    word_id1 = word_db_instance.add_word(english, meaning)
    
    # Act
    word_id2 = word_db_instance.add_word(english, "다른의미") # 영어 단어 기준 중복
    
    # Assert
    assert word_id1 == word_id2, "중복 단어 추가 시 기존 ID를 반환해야 합니다."
    # 의미가 업데이트되지 않는다는 것도 확인할 수 있음 (add_word는 업데이트 기능이 아님)
    retrieved_word = word_db_instance.fetch_one("SELECT meaning FROM Word WHERE word_id = ?", (word_id1,))
    assert retrieved_word['meaning'] == meaning 