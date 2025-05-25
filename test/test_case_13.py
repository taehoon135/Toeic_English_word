import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.cloze_quiz import ClozeQuizModel


def test_cloze_quiz_model_invalid_api_key():
    """
    Test case 13: ClozeQuizModel with invalid API KEY format
    Input: Any DB, API KEY 형식 잘못됨
    Expected output: Raise exception (api key 형식 오류)
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"}
    ]
    invalid_api_key = "invalid_key_format"
    
    # Act & Assert
    with pytest.raises(Exception):
        model = ClozeQuizModel(normal_db, APIKEY=invalid_api_key)
        result = model.get() 