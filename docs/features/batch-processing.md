# Batch Processing

The GeminiClient provides batch processing capabilities for efficiently handling multiple prompts with controlled concurrency. This feature is particularly useful for scenarios where you need to process a large number of similar requests or apply the same analysis to different inputs.

## Overview

Batch processing in GeminiClient offers two main approaches:
1. Direct batch processing using `batch_generate_content` and its async variant
2. Template-based batch processing using `map_generate` and its async variant

These methods automatically manage concurrency to prevent overwhelming the API service and provide a streamlined interface for processing collections of prompts.

## Available Batch Methods

### batch_generate_content

```python
def batch_generate_content(self, 
                         contents_list: List[List[types.Content]],
                         generation_config: Optional[types.GenerateContentConfig] = None,
                         model: str = "gemini-2.0-flash-exp",
                         return_json: bool = False,
                         json_schema: Optional[Dict] = None,
                         count_tokens: bool = False,
                         max_concurrency: int = 5)
```

This method processes multiple prompts in batch mode with configurable concurrency. Each prompt is processed individually, but the method manages the overall concurrency to prevent overwhelming the API service.

### map_generate

```python
def map_generate(self, 
               template: str,
               items: List[Any],
               map_function: Optional[Callable[[Any], str]] = None,
               generation_config: Optional[types.GenerateContentConfig] = None,
               model: str = "gemini-2.0-flash-exp",
               return_json: bool = False,
               json_schema: Optional[Dict] = None,
               count_tokens: bool = False,
               max_concurrency: int = 5)
```

This method applies a template across a list of items, generating content for each. It's a higher-level abstraction that handles the creation of prompts from a template and a list of items, then processes them in batch.

## Basic Usage

### Processing Multiple Prompts

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Prepare multiple prompts
prompts = [
    "What is Python?",
    "What is JavaScript?",
    "What is Rust?"
]

# Convert to contents format
contents_list = [
    [types.Content(
        role="user",
        parts=[types.Part.from_text(prompt)]
    )]
    for prompt in prompts
]

# Process in batch
results = client.batch_generate_content(
    contents_list=contents_list,
    max_concurrency=3
)

# Process results
for prompt, result in zip(prompts, results):
    print(f"Prompt: {prompt}")
    print(f"Response: {result[:100]}...")  # Show first 100 chars
    print()
```

### Using Templates with map_generate

```python
from vertex_libs import GeminiClient

client = GeminiClient()

# Define items and template
languages = ["Python", "JavaScript", "Rust"]
template = "What makes {item} unique compared to other programming languages?"

# Process with template
results = client.map_generate(
    template=template,
    items=languages,
    max_concurrency=3
)

# Process results
for language, result in zip(languages, results):
    print(f"Language: {language}")
    print(f"Response: {result[:100]}...")  # Show first 100 chars
    print()
```

## Advanced Usage

### Custom Mapping Function

You can provide a custom function to transform items before inserting them into the template:

```python
from vertex_libs import GeminiClient

client = GeminiClient()

# Custom mapping function
def format_topic(topic):
    return f"the {topic} programming language in 2025"

# Define items and template
languages = ["Python", "JavaScript", "Rust"]
template = "What will be the most important developments for {item}?"

# Process with custom mapping
results = client.map_generate(
    template=template,
    items=languages,
    map_function=format_topic,
    max_concurrency=3
)

# Process results
for language, result in zip(languages, results):
    print(f"Language: {language}")
    print(f"Response: {result[:100]}...")
    print()
```

### Batch Processing with JSON Responses

You can combine batch processing with structured JSON responses:

```python
from vertex_libs import GeminiClient
from google.genai import types
import json

client = GeminiClient()

# Define JSON schema
json_schema = {
    "type": "OBJECT",
    "properties": {
        "name": {"type": "STRING"},
        "created_year": {"type": "NUMBER"},
        "key_features": {"type": "ARRAY", "items": {"type": "STRING"}},
        "popularity_score": {"type": "NUMBER"}
    }
}

# Define languages to process
languages = ["Python", "JavaScript", "Rust"]

# Prepare template
template = """
Provide information about {item} in a structured format including:
- When it was created
- Key features (at least 3)
- A popularity score from 1-10
"""

# Process batch with JSON responses
results = client.map_generate(
    template=template,
    items=languages,
    json_schema=json_schema,
    return_json=True,
    max_concurrency=3
)

# Process structured results
for language, result in zip(languages, results):
    print(f"== {language} Information ==")
    
    # Results should be already parsed as dictionaries
    if isinstance(result, dict) and "key_features" in result:
        print(f"Created: {result['created_year']}")
        print(f"Popularity: {result['popularity_score']}/10")
        print("Key Features:")
        for feature in result['key_features']:
            print(f"- {feature}")
    else:
        print("Response format unexpected:", result)
    
    print()
```

### Error Handling in Batch Processing

Batch processing methods include built-in error handling. If a request fails, the error is logged and the corresponding result will contain error information instead of failing the entire batch:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Some prompts that might cause issues
prompts = [
    "What is Python?",
    "",  # Empty prompt might cause an error
    "What is JavaScript?",
    "Write an extremely long response that exceeds token limits"  # Might hit token limits
]

# Convert to contents format
contents_list = [
    [types.Content(
        role="user",
        parts=[types.Part.from_text(prompt)]
    )]
    for prompt in prompts
]

# Process batch with error handling
results = client.batch_generate_content(
    contents_list=contents_list,
    max_concurrency=2
)

# Process results, handling potential errors
for prompt, result in zip(prompts, results):
    print(f"Prompt: {prompt}")
    
    # Check if result contains error information
    if isinstance(result, dict) and "error" in result:
        print(f"ERROR: {result['error']}")
    else:
        print(f"Response: {result[:100]}...")
    
    print()
```

## Best Practices

### Concurrency Management

1. **Adjust `max_concurrency` based on your needs**:
   - Higher values process more requests in parallel but may hit rate limits
   - Lower values are more conservative but take longer
   - Start with the default of 5 and adjust based on performance

```python
# Conservative approach (fewer parallel requests)
results = client.batch_generate_content(
    contents_list=contents_list,
    max_concurrency=3  # Lower concurrency
)

# More aggressive approach (more parallel requests)
results = client.batch_generate_content(
    contents_list=contents_list,
    max_concurrency=10  # Higher concurrency
)
```

### Resource Management

2. **Process large batches in chunks**:
   - For very large collections, consider breaking them into smaller batches
   - This helps manage memory usage and provides better progress reporting

```python
from vertex_libs import GeminiClient
import time

client = GeminiClient()

# Large collection of items
all_items = ["item1", "item2", ..., "item10000"]  # Large list
template = "Describe {item} briefly."

# Process in chunks of 100
chunk_size = 100
all_results = []

for i in range(0, len(all_items), chunk_size):
    chunk = all_items[i:i+chunk_size]
    
    print(f"Processing chunk {i//chunk_size + 1}/{(len(all_items) + chunk_size - 1)//chunk_size}")
    
    # Process this chunk
    chunk_results = client.map_generate(
        template=template,
        items=chunk,
        max_concurrency=5
    )
    
    all_results.extend(chunk_results)
    
    # Optional: add a small delay between chunks
    time.sleep(1)

print(f"Processed {len(all_results)} items total")
```

### Error Recovery

3. **Implement retry logic for failed items**:
   - Collect items that failed and retry them with different parameters

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Initial list of prompts
prompts = ["prompt1", "prompt2", "prompt3", "prompt4", "prompt5"]

# Convert to contents format
contents_list = [
    [types.Content(
        role="user",
        parts=[types.Part.from_text(prompt)]
    )]
    for prompt in prompts
]

# First attempt
results = client.batch_generate_content(
    contents_list=contents_list,
    max_concurrency=5
)

# Collect failed items
failed_prompts = []
failed_indices = []

for i, (prompt, result) in enumerate(zip(prompts, results)):
    if isinstance(result, dict) and "error" in result:
        failed_prompts.append(prompt)
        failed_indices.append(i)

# If there are failed items, retry with more conservative settings
if failed_prompts:
    print(f"Retrying {len(failed_prompts)} failed prompts with more conservative settings...")
    
    # Convert failed prompts to contents
    failed_contents_list = [
        [types.Content(
            role="user",
            parts=[types.Part.from_text(prompt)]
        )]
        for prompt in failed_prompts
    ]
    
    # Retry with more conservative settings
    retry_results = client.batch_generate_content(
        contents_list=failed_contents_list,
        max_concurrency=1,  # More conservative
        model="gemini-1.0-pro"  # Fallback to a different model
    )
    
    # Update original results with retry results
    for i, retry_result in zip(failed_indices, retry_results):
        results[i] = retry_result

# Now results contains the best available response for each prompt
```

## Performance Considerations

- **API Quotas**: Batch processing still consumes API quotas for each individual request
- **Rate Limiting**: If you hit rate limits, decrease `max_concurrency`
- **Cost Management**: Each request in a batch incurs separate API costs
- **Latency vs. Throughput**: Higher concurrency increases throughput but may increase latency for individual requests

## When to Use Batch Processing

Batch processing is ideal for:
- Processing datasets with similar prompts
- Analyzing multiple documents or items
- Generating variations of content
- Creating consistent content across multiple topics
- Parallel processing of independent requests

## References

- [Google Vertex AI Quotas and Limits](https://cloud.google.com/vertex-ai/docs/quotas)
- [Python Concurrency Guidelines](https://docs.python.org/3/library/concurrent.futures.html)
