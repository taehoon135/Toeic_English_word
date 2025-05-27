import pytest
from database.word_db import WordDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

def test_import_from_csv_file_not_found(word_db_instance):
    """Test Case: 존재하지 않는 CSV 파일에서 가져오기 시도"""
    # Arrange
    non_existent_csv = "non_existent_file.csv"
    # Act
    success = word_db_instance.import_from_csv(non_existent_csv)
    # Assert
    assert success is False 