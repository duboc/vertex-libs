# Vertex Libs

A collection of robust Python libraries for Google Cloud Vertex AI, starting with a production-ready Gemini client that features region fallback, comprehensive error handling, and configurable safety settings.

## Features

### GeminiClient

- 🌍 **Region Fallback**: Automatically tries different regions if one fails
- 🔄 **Retry Logic**: Built-in exponential backoff with configurable retry attempts
- 🛡️ **Safety Settings**: Configurable content safety thresholds
- 📝 **Streaming Support**: Efficient streaming responses for real-time applications
- 🎛️ **Custom Configurations**: Flexible generation parameters
- 📊 **Logging Integration**: Custom logger support for better monitoring
- ⚡ **Performance**: Optimized for production workloads
- 🔄 **Async Support**: Non-blocking API calls for improved application responsiveness
- 📦 **Batch Processing**: Efficiently process multiple prompts with controlled concurrency
- 🔍 **Response Parsing Helpers**: Extract structured data from LLM responses (lists, JSON, key-value pairs)

## Quick Start

```python
from vertex_libs import GeminiClient
from google.genai import types

# Initialize client (set GCP_PROJECT env var or pass project_id)
client = GeminiClient()

# Create a prompt
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("What is quantum computing?")]
    )
]

# Get response
response = client.generate_content(contents)
print(response)
```

### Advanced Features

```python
import asyncio
from vertex_libs import GeminiClient
from google.genai import types

async def example():
    client = GeminiClient()
    
    # Async API call
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("What is quantum computing?")]
        )
    ]
    response = await client.generate_content_async(contents)
    
    # Batch processing with a template
    topics = ["Python", "JavaScript", "Rust"]
    template = "What makes {item} unique compared to other programming languages?"
    
    results = client.map_generate(template=template, items=topics)
    
    # Response parsing
    list_response = client.generate_content([
        types.Content(
            role="user",
            parts=[types.Part.from_text("List 3 cloud providers.")]
        )
    ])
    providers = client.extract_list(list_response)
    print(f"Extracted providers: {providers}")

# Run the async example
asyncio.run(example())
```

## Installation

Install from source:

```bash
git clone https://github.com/duboc/vertex-libs.git
cd vertex-libs
pip install -e .
```

## Prerequisites

1. Google Cloud Project
2. Gemini API enabled
3. Authentication set up (service account or application default credentials)

## Documentation

For detailed usage instructions and examples, see [USAGE.md](USAGE.md).

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/duboc/vertex-libs.git
cd vertex-libs

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

We maintain a comprehensive test suite with 100% code coverage. The tests are written using pytest and include:

- Unit tests for all functionality
- Integration tests for API interactions
- Mock tests for external dependencies
- Error handling scenarios
- Configuration validation

To run the tests:

```bash
# Quick test run
pytest

# Detailed test output
pytest -v

# Run with coverage report
pytest --cov=vertex_libs --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=vertex_libs --cov-report=html
```

For more detailed information about testing and contributing, see our [Contributing Guide](CONTRIBUTING.md).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for:
- Development environment setup
- Coding standards
- Test writing guidelines
- Documentation requirements
- Pull request process

For major changes, please open an issue first to discuss what you would like to change.

## License

[Apache 2.0](LICENSE)

## Roadmap

- [x] Async support
- [x] Batch processing
- [x] Response parsing helpers
- [x] Token counting utilities (using native SDK methods)
- [ ] Rate limiting
- [ ] Context management
- [ ] Response caching
- [ ] Additional Vertex AI integrations
