import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.cloze_quiz import ClozeQuizModel


def test_cloze_quiz_model_empty_db_with_api_key():
    """
    Test case 14: ClozeQuizModel with empty DB and any API KEY
    Input: DB 결과가 [] (빈 리스트), Any API KEY
    Expected output: 빈 리스트
    """
    # Arrange
    empty_db = []
    api_key = "test_api_key"
    
    # Act
    model = ClozeQuizModel(empty_db, APIKEY=api_key)
    result = model.get()
    
    # Assert
    assert result == []
    assert len(result) == 0 