import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.cloze_quiz import ClozeQuizModel


def test_cloze_quiz_model_missing_api_key():
    """
    Test case 12: ClozeQuizModel with missing API KEY
    Input: Any DB, API KEY 누락
    Expected output: Raise exception (api key 누락)
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"}
    ]
    
    # Act & Assert
    with pytest.raises(Exception):
        model = ClozeQuizModel(normal_db, APIKEY=None)
        result = model.get() 