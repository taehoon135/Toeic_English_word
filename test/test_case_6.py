import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.rain_quiz import RainQuizModel


def test_rain_quiz_model_empty_db():
    """
    Test case 6: RainQuizModel with empty DB result
    Input: DB 결과가 [] (빈 리스트)
    Expected output: 빈 리스트
    """
    # Arrange
    empty_db = []
    
    # Act
    model = RainQuizModel(empty_db)
    result = model.get()
    
    # Assert
    assert result == []
    assert len(result) == 0 