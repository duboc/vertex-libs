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
- `tiktoken`: For token counting

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

### 3. Token Counting and Usage Tracking

The client provides token counting capabilities using OpenAI's `tiktoken` library, which provides a good approximation for Gemini's token usage. This can be used independently or combined with content generation.

#### Independent Token Counting
```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("What is quantum computing?")]
    )
]

# Count tokens before generation
token_count = client.count_tokens(contents)
print(f"Prompt tokens: {token_count.prompt_tokens}")
print(f"Total tokens: {token_count.total_tokens}")
```

Note: Token counting is an approximation using the GPT-4 tokenizer, which is similar to Gemini's tokenization. The actual token count may vary slightly.

#### Token Usage with Generation
```python
# Generate with token counting
response, usage = client.generate_content(contents, count_tokens=True)
print(f"Response: {response}")
print(f"Token Usage:")
print(f"- Total tokens: {usage.total_tokens}")
print(f"- Prompt tokens: {usage.prompt_tokens}")
print(f"- Completion tokens: {usage.completion_tokens}")
```

The `TokenCount` object provides:
- `prompt_tokens`: Number of tokens in the input prompt
- `completion_tokens`: Number of tokens in the generated response
- `total_tokens`: Total tokens used (prompt + completion)

### 4. JSON Responses and Schema

The client supports structured JSON responses using the Gemini SDK's built-in JSON capability. You can specify a schema to ensure the response follows a specific format.

#### Basic JSON Response
```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Define your JSON schema
json_schema = {
    "type": "OBJECT",
    "properties": {
        "response": {"type": "STRING"}  # Simple schema for text response
    }
}

# Create your prompt
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("Tell me a short story about a robot.")]
    )
]

# Get JSON response
response = client.generate_content(
    contents,
    return_json=True,
    json_schema=json_schema
)

# Parse and use the response
data = json.loads(response)
print(data["response"])
```

#### Structured JSON Response
```python
# Define a more complex schema
json_schema = {
    "type": "OBJECT",
    "properties": {
        "title": {"type": "STRING"},
        "points": {"type": "ARRAY", "items": {"type": "STRING"}},
        "summary": {"type": "STRING"},
        "rating": {"type": "NUMBER"}
    }
}

# Create a prompt that matches your schema
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Analyze the book '1984' by George Orwell.
            Include a title, key points, summary, and rating out of 10.
        """)]
    )
]

# Get structured JSON response
response = client.generate_content(
    contents,
    return_json=True,
    json_schema=json_schema
)

# Parse and use the structured data
data = json.loads(response)
print(f"Title: {data['title']}")
print("\nKey Points:")
for point in data['points']:
    print(f"- {point}")
print(f"\nSummary: {data['summary']}")
print(f"Rating: {data['rating']}/10")
```

#### Schema Types and Format
The schema supports various types and formats:
```python
json_schema = {
    "type": "OBJECT",
    "properties": {
        # Basic types
        "text_field": {"type": "STRING"},
        "number_field": {"type": "NUMBER"},
        "boolean_field": {"type": "BOOLEAN"},
        
        # Arrays
        "string_array": {
            "type": "ARRAY",
            "items": {"type": "STRING"}
        },
        
        # Nested objects
        "nested_object": {
            "type": "OBJECT",
            "properties": {
                "field1": {"type": "STRING"},
                "field2": {"type": "NUMBER"}
            }
        }
    }
}
```

#### Response Mime Type
When using JSON responses, the client automatically sets:
- `response_mime_type = "application/json"`
- `response_schema = your_schema` (or a default schema if none provided)

#### Best Practices
1. Always provide a schema that matches your prompt's expected output
2. Handle JSON parsing errors gracefully
3. Validate the response structure matches your expectations
4. Keep schemas as simple as possible while meeting your needs

```python
try:
    data = json.loads(response)
    if all(key in data for key in ["title", "summary", "rating"]):
        # Process the data
        pass
    else:
        print("Response missing required fields")
except json.JSONDecodeError:
    print("Failed to parse JSON response")
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