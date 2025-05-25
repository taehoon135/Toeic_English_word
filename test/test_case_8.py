import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.rain_quiz import RainQuizModel


def test_rain_quiz_model_normal_db():
    """
    Test case 8: RainQuizModel with normal DB output
    Input: DB 정상 출력
    Expected output: (문제, 정답, 힌트) 의 pair
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"},
        {"english": "banana", "meaning": "바나나"}
    ]
    
    # Act
    model = RainQuizModel(normal_db)
    result = model.get()
    
    # Assert
    assert len(result) == 2
    assert isinstance(result, list)
    
    # Check first pair
    question1, answer1, hint1 = result[0]
    assert question1 == "apple"
    assert answer1 == "사과"
    assert hint1 == "hint"
    
    # Check second pair
    question2, answer2, hint2 = result[1]
    assert question2 == "banana"
    assert answer2 == "바나나"
    assert hint2 == "hint" 