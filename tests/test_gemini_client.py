import pytest
import os
from unittest.mock import Mock, patch
from google.genai import types
from vertex_libs import GeminiClient
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