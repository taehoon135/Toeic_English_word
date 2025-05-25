import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.rain_quiz import RainQuizModel


def test_rain_quiz_model_none_db():
    """
    Test case 7: RainQuizModel with None DB result
    Input: DB 결과가 None
    Expected output: Raise exception (db error)
    """
    # Arrange
    none_db = None
    
    # Act & Assert
    with pytest.raises(Exception):
        model = RainQuizModel(none_db)
        result = model.get() 