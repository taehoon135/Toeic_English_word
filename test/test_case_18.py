import pytest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.LLM.LLMResponse import get_response


def test_get_response_unsupported_model():
    """
    Test case 18: get_response with unsupported model name
    Input: model name 미지원 값
    Expected output: 빈 문자열 ("")
    """
    # Arrange
    prompt = "Hello, world!"
    unsupported_model = "unsupported_model"
    api_key = "test_api_key"
    
    # Act
    result = get_response(prompt, unsupported_model, api_key)
    
    # Assert
    assert result == "" 