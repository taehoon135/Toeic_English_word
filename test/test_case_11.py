import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.four_choice_quiz import FourChoiceQuizModel


def test_four_choice_quiz_model_normal_db():
    """
    Test case 11: FourChoiceQuizModel with normal DB output
    Input: DB 정상 출력
    Expected output: (문제, 정답, 힌트) 의 pair
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"},
        {"english": "banana", "meaning": "바나나"},
        {"english": "orange", "meaning": "오렌지"},
        {"english": "grape", "meaning": "포도"}
    ]
    
    # Act
    model = FourChoiceQuizModel(normal_db)
    result = model.get()
    
    # Assert
    assert len(result) == 4
    assert isinstance(result, list)
    
    # Check first pair
    question1, answer1, hint1 = result[0]
    assert "사과" in question1
    assert "apple" in answer1  # answer should contain the correct answer
    assert "," in answer1  # answer should be comma-separated choices
    assert hint1 == "hint"
    
    # Verify that answer contains 4 choices
    choices = answer1.split(",")
    assert len(choices) == 4
    assert "apple" in choices  # correct answer should be in choices 