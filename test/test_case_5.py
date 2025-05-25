import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.short_answer_quiz import ShortAnswerKEQuizModel


def test_short_answer_ke_quiz_model_normal_db():
    """
    Test case 5: ShortAnswerKEQuizModel with normal DB output
    Input: DB 정상 출력
    Expected output: (문제, 정답, 힌트) 의 pair
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"},
        {"english": "banana", "meaning": "바나나"}
    ]
    
    # Act
    model = ShortAnswerKEQuizModel(normal_db)
    result = model.get()
    
    # Assert
    assert len(result) == 2
    assert isinstance(result, list)
    
    # Check first pair
    question1, answer1, hint1 = result[0]
    assert "사과" in question1
    assert answer1 == "apple"
    assert isinstance(hint1, str)  # hint should be string (partial word)
    assert hint1.startswith("a")  # hint should start with first part of word
    
    # Check second pair
    question2, answer2, hint2 = result[1]
    assert "바나나" in question2
    assert answer2 == "banana"
    assert isinstance(hint2, str)  # hint should be string (partial word)
    assert hint2.startswith("b")  # hint should start with first part of word 