import pytest
from database.word_db import WordDB
import os
import csv

# conftest.py 의 db_path fixture 를 사용합니다.

TEMP_CSV_FILE = "temp_test_words_import_successful.csv" # 파일 이름 충돌 방지

@pytest.fixture
def word_db_instance(db_path):
    """WordDB 인스턴스를 제공하고 테스트 후 정리합니다."""
    db = WordDB(db_path)
    yield db
    db.close()

@pytest.fixture
def create_temp_csv_file_for_import_successful():
    """import_from_csv 테스트를 위한 임시 CSV 파일을 생성합니다."""
    csv_data = [
        ["english", "meaning", "part_of_speech", "example_sentence"],
        ["csv_word1", "CSV단어1", "noun", "Example for CSV word1"],
        ["csv_word2", "CSV단어2", "verb", ""],
        ["", "의미만있음", "", ""], # 영어 단어 누락 케이스
        ["영어만있음", "", "", ""]  # 의미 누락 케이스
    ]
    with open(TEMP_CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
    yield TEMP_CSV_FILE
    if os.path.exists(TEMP_CSV_FILE):
        os.remove(TEMP_CSV_FILE) # 테스트 후 파일 삭제

def test_import_from_csv_successful(word_db_instance, create_temp_csv_file_for_import_successful):
    """Test Case: CSV 파일에서 단어 가져오기 성공 (정상 데이터)"""
    # Arrange
    csv_file_path = create_temp_csv_file_for_import_successful
    
    # Act
    success = word_db_instance.import_from_csv(csv_file_path)
    
    # Assert
    assert success is True
    imported_word1 = word_db_instance.search_words("csv_word1")
    assert len(imported_word1) == 1
    assert imported_word1[0]['meaning'] == "CSV단어1"
    
    imported_word2 = word_db_instance.search_words("csv_word2")
    assert len(imported_word2) == 1
    assert imported_word2[0]['meaning'] == "CSV단어2"

    # 영어 또는 의미가 없는 단어는 추가되지 않아야 함 (WordDB 로직에 따라)
    assert not word_db_instance.search_words("의미만있음")
    assert not word_db_instance.search_words("영어만있음") 