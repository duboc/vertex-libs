# GeminiClient Usage Guide

## Overview
The `GeminiClient` is a robust Python client for Google's Gemini API that provides region fallback capabilities, error handling, and configurable safety settings. This guide will help you get the most out of the client.

## Installation

### From Source
```bash
# Clone the repository
git clone https://github.com/duboc/vertex-libs.git
cd vertex-libs

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Dependencies
The package will automatically install the following dependencies:
- `google-cloud-aiplatform`: For Vertex AI integration
- `google-generativeai`: For Gemini API
- `tenacity`: For retry logic

## Prerequisites

1. A Google Cloud Project
2. Gemini API enabled in your project
3. Proper authentication set up (service account or application default credentials)

## Basic Usage

```python
from vertex_libs import GeminiClient
from google.genai import types

# Initialize the client
client = GeminiClient(project_id="your-project-id")  # or set GCP_PROJECT env var

# Create a simple text prompt
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("What is the capital of France?")]
    )
]

# Get a response
response = client.generate_content(contents)
print(response)
```

## Advanced Features

### 1. Streaming Responses

```python
# Get streaming response
stream = client.generate_content(contents, stream=True)
for chunk in stream:
    print(chunk, end="")
```

### 2. Custom Generation Config

```python
custom_config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.8,
    max_output_tokens=2000,
    response_modalities=["TEXT"],
)

response = client.generate_content(
    contents,
    generation_config=custom_config
)
```

### 3. Custom Safety Settings

```python
custom_safety = [
    types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="BLOCK_MEDIUM_AND_ABOVE"
    )
]

config = types.GenerateContentConfig(
    safety_settings=custom_safety
)

response = client.generate_content(
    contents,
    generation_config=config
)
```

## Error Handling

The client includes built-in retry logic with exponential backoff:
- Maximum of 3 retry attempts
- Exponential backoff starting at 2 seconds
- Region fallback if a region fails

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks
2. **Custom Logging**: Provide your own logger for better integration with your application
3. **Resource Management**: Close or cleanup client when done in long-running applications

```python
import logging

logger = logging.getLogger("my_app")
client = GeminiClient(logger=logger)
```

## Improvement Suggestions

1. **Async Support**: Consider adding async versions of the methods for better performance in async applications
2. **Batch Processing**: Add support for batch processing multiple prompts
3. **Response Parsing**: Add helper methods for common response parsing patterns
4. **Model Selection**: Add model validation and available model listing
5. **Token Counting**: Add methods to estimate token usage
6. **Rate Limiting**: Implement rate limiting to prevent API quota issues
7. **Context Management**: Implement context manager protocol for better resource management
8. **Caching**: Add optional response caching for frequently used prompts

## Environment Variables

- `GCP_PROJECT`: Your Google Cloud Project ID (optional if provided in constructor)

## Common Issues and Solutions

1. **Authentication Errors**
   - Ensure you have proper credentials set up
   - Verify project ID is correct
   - Check API is enabled

2. **Region Failures**
   - The client will automatically try different regions
   - Check your quota limits in each region
   - Monitor region health status

3. **Rate Limits**
   - Implement backoff strategy
   - Consider using quotas across multiple regions
   - Monitor usage patterns

## Contributing

Feel free to submit issues and enhancement requests!

## Development

### Running Tests
The package includes a comprehensive test suite. To run the tests:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run tests with coverage report
pytest tests/ --cov=vertex_libs --cov-report=term-missing
```

The test suite covers:
- Initialization with different project ID sources
- Content generation (regular and streaming)
- Region fallback functionality
- Custom configuration handling
- Error handling and retries
- Logging functionality

### Project Structure
```
vertex-libs/
├── vertex_libs/
│   ├── __init__.py
│   └── gemini_client.py
├── tests/
│   └── test_gemini_client.py
├── setup.py
├── requirements-dev.txt
├── USAGE.md
└── LICENSE
```

## License

[Apache 2.0](LICENSE)