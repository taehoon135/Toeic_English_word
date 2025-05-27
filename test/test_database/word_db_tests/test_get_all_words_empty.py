import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_get_all_words_empty(word_db_instance):
    """Test Case: 단어가 없을 때 모든 단어 조회"""
    # Arrange (DB는 비어있음)
    # Act
    words = word_db_instance.get_all_words()
    # Assert
    assert words == [] 