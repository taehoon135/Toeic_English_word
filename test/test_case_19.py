import pytest
import sys
import os
from unittest.mock import patch

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.LLM.LLMResponse import get_response


def test_get_response_timeout():
    """
    Test case 19: get_response with API call timeout over 60 seconds
    Input: API 호출 60 s 초과
    Expected output: TimeoutError Exception
    """
    # Arrange
    prompt = "Hello, world!"
    api_key = "test_api_key"
    
    # Mock the API call to raise a TimeoutError
    with patch('src.LLM.LLMResponse.generate_gemini_response') as mock_gemini:
        mock_gemini.side_effect = TimeoutError("API call timeout")
        
        # Act & Assert
        with pytest.raises(TimeoutError):
            result = get_response(prompt, "gemini-2.0-flash", api_key) 