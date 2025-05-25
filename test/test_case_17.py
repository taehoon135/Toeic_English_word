import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.LLM.LLMResponse import get_response


def test_get_response_empty_prompt():
    """
    Test case 17: get_response with empty prompt
    Input: prompt=""
    Expected output: 빈 문자열 ("")
    """
    # Arrange
    empty_prompt = ""
    api_key = "test_api_key"
    
    # Act
    result = get_response(empty_prompt, "gemini-2.0-flash", api_key)
    
    # Assert
    assert result == "" 