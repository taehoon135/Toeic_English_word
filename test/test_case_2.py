import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.short_answer_quiz import ShortAnswerEKQuizModel


def test_short_answer_ek_quiz_model_normal_db():
    """
    Test case 2: ShortAnswerEKQuizModel with normal DB output
    Input: DB 정상 출력
    Expected output: (문제, 정답, 힌트) 의 pair
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"},
        {"english": "banana", "meaning": "바나나"}
    ]
    
    # Act
    model = ShortAnswerEKQuizModel(normal_db)
    result = model.get()
    
    # Assert
    assert len(result) == 2
    assert isinstance(result, list)
    
    # Check first pair
    question1, answer1, hint1 = result[0]
    assert "apple" in question1
    assert answer1 == "사과"
    assert isinstance(hint1, str)  # hint should be string (초성)
    
    # Check second pair
    question2, answer2, hint2 = result[1]
    assert "banana" in question2
    assert answer2 == "바나나"
    assert isinstance(hint2, str)  # hint should be string (초성) 