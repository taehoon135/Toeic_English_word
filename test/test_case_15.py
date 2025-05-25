import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.cloze_quiz import ClozeQuizModel


def test_cloze_quiz_model_none_db_with_api_key():
    """
    Test case 15: ClozeQuizModel with None DB and any API KEY
    Input: DB 결과가 None, Any API KEY
    Expected output: Raise exception (db error)
    """
    # Arrange
    none_db = None
    api_key = "test_api_key"
    
    # Act & Assert
    with pytest.raises(Exception):
        model = ClozeQuizModel(none_db, APIKEY=api_key)
        result = model.get() 