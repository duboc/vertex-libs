"""
 Copyright 2024 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import pytest
import os
from unittest.mock import Mock, patch
from google.genai import types
from vertex_libs import GeminiClient
from vertex_libs.gemini_client import TokenCount
from tenacity import RetryError

@pytest.fixture
def mock_genai():
    with patch('vertex_libs.gemini_client.genai') as mock:
        yield mock

@pytest.fixture
def client():
    os.environ['GCP_PROJECT'] = 'test-project'
    return GeminiClient()

def test_init_with_project_id():
    client = GeminiClient(project_id="test-project")
    assert client.project_id == "test-project"

def test_init_with_env_var():
    os.environ['GCP_PROJECT'] = 'env-project'
    client = GeminiClient()
    assert client.project_id == "env-project"

def test_init_without_project_id():
    if 'GCP_PROJECT' in os.environ:
        del os.environ['GCP_PROJECT']
    with pytest.raises(ValueError):
        GeminiClient()

def test_generate_content_success(mock_genai, client):
    # Mock successful response
    mock_response = Mock()
    mock_response.text = "Test response"
    mock_genai.Client().models.generate_content.return_value = mock_response

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    response = client.generate_content(contents)
    assert response == "Test response"

def test_generate_content_stream(mock_genai, client):
    # Mock streaming response
    mock_chunks = [Mock(text="chunk1"), Mock(text="chunk2")]
    mock_genai.Client().models.generate_content_stream.return_value = mock_chunks

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    stream = client.generate_content(contents, stream=True)
    assert list(stream) == mock_chunks

def test_generate_content_region_fallback(mock_genai, client):
    # Make first region fail, second succeed
    def mock_generate(*args, **kwargs):
        if mock_generate.calls == 0:
            mock_generate.calls += 1
            raise Exception("First region failed")
        mock_response = Mock()
        mock_response.text = "Success from second region"
        return mock_response
    
    mock_generate.calls = 0
    mock_genai.Client().models.generate_content.side_effect = mock_generate

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    response = client.generate_content(contents)
    assert response == "Success from second region"
    assert mock_generate.calls == 1

def test_custom_generation_config(mock_genai, client):
    mock_response = Mock()
    mock_response.text = "Test response"
    mock_genai.Client().models.generate_content.return_value = mock_response

    custom_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.8,
        max_output_tokens=2000
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    response = client.generate_content(
        contents,
        generation_config=custom_config
    )
    
    assert response == "Test response"
    
    # Verify the config was passed correctly
    called_config = mock_genai.Client().models.generate_content.call_args[1]['config']
    assert called_config.temperature == 0.7
    assert called_config.top_p == 0.8
    assert called_config.max_output_tokens == 2000

def test_all_regions_fail(mock_genai, client):
    # Make all regions fail
    mock_genai.Client().models.generate_content.side_effect = Exception("All regions failed")

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    with pytest.raises(RetryError):
        client.generate_content(contents)

def test_custom_logger(caplog):
    import logging
    logger = logging.getLogger("test_logger")
    client = GeminiClient(project_id="test-project", logger=logger)
    
    # Mock generate_content to fail
    with patch('vertex_libs.gemini_client.genai') as mock_genai:
        mock_genai.Client().models.generate_content.side_effect = Exception("Test error")
        
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text("Test prompt")]
            )
        ]
        
        with pytest.raises(Exception):
            client.generate_content(contents)
    
    # Verify warning was logged
    assert any("Test error" in record.message for record in caplog.records)

def test_count_tokens(mock_genai, client):
    # Mock token counting response
    mock_count = Mock()
    mock_count.total_tokens = 10
    mock_genai.Client().count_tokens.return_value = mock_count

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    token_count = client.count_tokens(contents)
    assert isinstance(token_count, TokenCount)
    assert token_count.prompt_tokens == 10
    assert token_count.completion_tokens == 0
    assert token_count.total_tokens == 10

def test_generate_content_with_token_count(mock_genai, client):
    # Mock response
    mock_response = Mock()
    mock_response.text = "Test response with five tokens"
    mock_genai.Client().models.generate_content.return_value = mock_response

    # Mock token count
    mock_count = Mock()
    mock_count.total_tokens = 10
    mock_genai.Client().count_tokens.return_value = mock_count

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    response, token_count = client.generate_content(contents, count_tokens=True)
    assert response == "Test response with five tokens"
    assert isinstance(token_count, TokenCount)
    assert token_count.prompt_tokens == 10
    assert token_count.completion_tokens == 5
    assert token_count.total_tokens == 15

def test_generate_content_json_response(mock_genai, client):
    # Mock JSON response
    mock_response = Mock()
    mock_response.text = '{"key": "value", "number": 42}'
    mock_genai.Client().models.generate_content.return_value = mock_response

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Return JSON")]
        )
    ]

    response = client.generate_content(contents, return_json=True)
    assert isinstance(response, dict)
    assert response["key"] == "value"
    assert response["number"] == 42

def test_generate_content_non_json_response(mock_genai, client):
    # Mock non-JSON response
    mock_response = Mock()
    mock_response.text = "Plain text response"
    mock_genai.Client().models.generate_content.return_value = mock_response

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Return text")]
        )
    ]

    response = client.generate_content(contents, return_json=True)
    assert isinstance(response, dict)
    assert response["text"] == "Plain text response"

def test_generate_content_json_with_token_count(mock_genai, client):
    # Mock JSON response
    mock_response = Mock()
    mock_response.text = '{"result": "success"}'
    mock_genai.Client().models.generate_content.return_value = mock_response

    # Mock token count
    mock_count = Mock()
    mock_count.total_tokens = 5
    mock_genai.Client().count_tokens.return_value = mock_count

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Return JSON")]
        )
    ]

    response, token_count = client.generate_content(
        contents,
        return_json=True,
        count_tokens=True
    )
    
    assert isinstance(response, dict)
    assert response["result"] == "success"
    assert isinstance(token_count, TokenCount)
    assert token_count.prompt_tokens == 5
    assert token_count.completion_tokens == 1  # One JSON object
    assert token_count.total_tokens == 6

def test_count_tokens_error(mock_genai, client):
    # Mock token counting error
    mock_genai.Client().count_tokens.side_effect = Exception("Token counting failed")

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Test prompt")]
        )
    ]

    with pytest.raises(Exception) as exc_info:
        client.count_tokens(contents)
    assert "Token counting failed" in str(exc_info.value) 