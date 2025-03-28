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

### 3. Token Counting and Usage Tracking

The client provides token counting capabilities using the native Google Generative AI SDK methods for accurate token counting. This can be used independently or combined with content generation.

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

Note: Token counting uses the native Gemini model tokenizer for precise token counts.

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

## Advanced Features

### 5. Asynchronous API Support

The GeminiClient provides asynchronous methods for non-blocking API calls. This is particularly useful in web applications and other environments where you want to maintain responsiveness.

```python
import asyncio
from vertex_libs import GeminiClient
from google.genai import types

async def example():
    client = GeminiClient()
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("What is quantum computing?")]
        )
    ]
    
    # Async API call
    response = await client.generate_content_async(contents)
    return response

# Run the async function
result = asyncio.run(example())
print(result)
```

For more details and advanced async examples, see the [Async Support Documentation](docs/features/async-support.md).

### 6. Batch Processing

The GeminiClient includes batch processing capabilities for efficiently handling multiple prompts:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Process multiple prompts at once
prompts = ["What is Python?", "What is JavaScript?", "What is Rust?"]

# Convert to contents format
contents_list = [
    [types.Content(
        role="user",
        parts=[types.Part.from_text(prompt)]
    )]
    for prompt in prompts
]

# Process in batch with concurrent requests (max 3 at a time)
results = client.batch_generate_content(
    contents_list=contents_list,
    max_concurrency=3
)

# Template-based batch processing
topics = ["Python", "JavaScript", "Rust"]
template = "What makes {item} unique compared to other programming languages?"

map_results = client.map_generate(
    template=template,
    items=topics,
    max_concurrency=3
)
```

For more details and advanced batch processing examples, see the [Batch Processing Documentation](docs/features/batch-processing.md).

### 7. Response Parsing Helpers

The GeminiClient provides helpers for extracting structured information from responses:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Extract lists from responses
list_contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("List 5 programming best practices.")]
    )
]
response = client.generate_content(list_contents)
best_practices = client.extract_list(response)

# Extract JSON data
json_contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("Provide information about three programming languages in JSON format.")]
    )
]
response = client.generate_content(json_contents)
data = client.extract_json(response)

# Extract key-value pairs
kv_contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Provide information about Python in this format:
            Name: 
            Creator: 
            Year: 
            Paradigm: 
        """)]
    )
]
response = client.generate_content(kv_contents)
python_info = client.parse_key_value_pairs(response)

# Extract text chunks
chunk_contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("Write three paragraphs about AI. Separate with blank lines.")]
    )
]
response = client.generate_content(chunk_contents)
paragraphs = client.extract_text_chunks(response)
```

For more details and advanced parsing examples, see the [Response Parsing Documentation](docs/features/response-parsing.md).

## Improvement Suggestions

1. **Model Selection**: Add model validation and available model listing
2. **Rate Limiting**: Implement rate limiting to prevent API quota issues
3. **Context Management**: Implement context manager protocol for better resource management
4. **Caching**: Add optional response caching for frequently used prompts

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
