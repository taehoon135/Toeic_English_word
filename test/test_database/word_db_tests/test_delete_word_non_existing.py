import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_delete_word_non_existing(word_db_instance):
    """Test Case: 존재하지 않는 단어 삭제 시도"""
    # Arrange
    non_existent_word_id = 9999
    # Act
    success = word_db_instance.delete_word(non_existent_word_id)
    # Assert
    assert success is False # 일반적으로 존재하지 않는 ID 삭제 시 False 또는 오류 없음 