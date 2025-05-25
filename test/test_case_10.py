import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.four_choice_quiz import FourChoiceQuizModel


def test_four_choice_quiz_model_none_db():
    """
    Test case 10: FourChoiceQuizModel with None DB result
    Input: DB 결과가 None
    Expected output: Raise exception (db error)
    """
    # Arrange
    none_db = None
    
    # Act & Assert
    with pytest.raises(Exception):
        model = FourChoiceQuizModel(none_db)
        result = model.get() 