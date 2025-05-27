import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_search_words_exact_match_english(word_db_instance):
    """Test Case: 영어 단어 정확히 검색"""
    # Arrange
    word_db_instance.add_word("unique_word", "특별한 단어")
    word_db_instance.add_word("another_unique", "또 다른 특별함")

    # Act
    results = word_db_instance.search_words("unique_word")

    # Assert
    assert len(results) == 1
    assert results[0]['english'] == "unique_word" 