import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.quiz_generation.cloze_quiz import ClozeQuizModel


def test_cloze_quiz_model_normal_db_with_valid_api_key():
    """
    Test case 16: ClozeQuizModel with normal DB and valid API KEY
    Input: DB 정상 출력, Valid API KEY
    Expected output: (문제, 정답, 힌트) 의 pair
    """
    # Arrange
    normal_db = [
        {"english": "apple", "meaning": "사과"}
    ]
    valid_api_key = "valid_api_key"
    
    # Mock the LLM response and translation
    mock_llm_response = "Q:The fruit is red and sweet ______;A:apple"
    mock_translation = [MagicMock(text="과일은 빨갛고 달콤합니다 ______")]
    
    # Act & Assert
    with patch('src.LLM.LLMResponse.get_response', return_value=mock_llm_response), \
         patch('googletrans.Translator.translate', return_value=mock_translation), \
         patch('asyncio.get_event_loop') as mock_loop:
        
        mock_loop.return_value.run_until_complete.return_value = mock_translation
        
        model = ClozeQuizModel(normal_db, APIKEY=valid_api_key)
        result = model.get()
        
        # Assert
        assert len(result) == 1
        assert isinstance(result, list)
        
        question, answer, hint = result[0]
        assert isinstance(question, str)
        assert answer == "apple"
        assert isinstance(hint, str) 