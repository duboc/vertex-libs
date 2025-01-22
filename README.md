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

## Installation

```bash
pip install vertex-libs
```

Or install from source:

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

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=vertex_libs --cov-report=term-missing
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

[Apache 2.0](LICENSE)

## Roadmap

- [ ] Async support
- [ ] Batch processing
- [ ] Response parsing helpers
- [ ] Token counting utilities
- [ ] Rate limiting
- [ ] Context management
- [ ] Response caching
- [ ] Additional Vertex AI integrations