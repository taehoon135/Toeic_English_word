import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.four_choice_quiz import FourChoiceQuizModel


def test_four_choice_quiz_model_empty_db():
    """
    Test case 9: FourChoiceQuizModel with empty DB result
    Input: DB 결과가 [] (빈 리스트)
    Expected output: 빈 리스트
    """
    # Arrange
    empty_db = []
    
    # Act
    model = FourChoiceQuizModel(empty_db)
    result = model.get()
    
    # Assert
    assert result == []
    assert len(result) == 0 