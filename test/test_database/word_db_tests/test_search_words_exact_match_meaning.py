import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_search_words_exact_match_meaning(word_db_instance):
    """Test Case: 한글 의미 정확히 검색"""
    # Arrange
    word_db_instance.add_word("house", "집")
    word_db_instance.add_word("car", "자동차")
    
    # Act
    results = word_db_instance.search_words("집")
    
    # Assert
    assert len(results) == 1
    assert results[0]['meaning'] == "집" 