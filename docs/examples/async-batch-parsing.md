# Async, Batch, and Parsing Example

This document explains the async, batch, and parsing example (`example_async_batch_parsing.py`) provided in the examples directory. This example demonstrates the three newly implemented features of the GeminiClient:

1. Asynchronous API support
2. Batch processing capabilities
3. Response parsing helpers

## Overview

The example shows how to use these powerful features individually and in combination. It's structured into three main demonstration functions, each focusing on one of the new features, plus a main function that runs them all.

## Example Code

Here's an overview of the structure of `example_async_batch_parsing.py`:

```python
import asyncio
from vertex_libs import GeminiClient
from google.genai import types
import json

def demonstrate_response_parsing():
    """Example showing various response parsing helpers."""
    # ...

def demonstrate_batch_processing():
    """Example showing batch processing functionality."""
    # ...

async def demonstrate_async_support():
    """Example showing async support functionality."""
    # ...

async def main():
    """Run all examples."""
    try:
        # Demonstrate response parsing helpers
        demonstrate_response_parsing()
        
        # Demonstrate batch processing
        demonstrate_batch_processing()
        
        # Demonstrate async support
        await demonstrate_async_support()
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
```

## Walkthrough

Let's examine each section of the example in detail:

### 1. Response Parsing Helpers

The `demonstrate_response_parsing` function shows how to use the various response parsing helpers to extract structured information from model responses:

```python
def demonstrate_response_parsing():
    """Example showing various response parsing helpers."""
    client = GeminiClient()
    
    print("\n=== Response Parsing Helpers Example ===\n")
    
    # 1. Example with list extraction
    list_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("List 5 programming best practices.")]
        )
    ]
    
    print("Extracting list from response...")
    response = client.generate_content(list_contents)
    
    # Extract list items (works with markdown lists, JSON lists, etc.)
    best_practices = client.extract_list(response)
    
    print("\nExtracted list items:")
    for i, practice in enumerate(best_practices, 1):
        print(f"{i}. {practice}")
    
    # 2. Example with JSON extraction
    # ...
    
    # 3. Example with key-value pair extraction
    # ...
    
    # 4. Example with text chunk extraction
    # ...
```

This function demonstrates four parsing helpers:

#### List Extraction

The `extract_list` method identifies and extracts lists from responses, regardless of whether they're formatted as markdown bullet points, numbered lists, or JSON arrays.

#### JSON Extraction

The `extract_json` method extracts structured JSON data from responses, even if it's wrapped in code blocks or embedded in other text.

#### Key-Value Pair Extraction

The `parse_key_value_pairs` method extracts key-value pairs from text formatted like "Key: Value" on separate lines.

#### Text Chunk Extraction

The `extract_text_chunks` method splits responses into separate chunks using a specified separator (default is double newline).

### 2. Batch Processing

The `demonstrate_batch_processing` function shows how to process multiple prompts efficiently:

```python
def demonstrate_batch_processing():
    """Example showing batch processing functionality."""
    client = GeminiClient()
    
    print("\n=== Batch Processing Example ===\n")
    
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
    
    # Process in batch (synchronously)
    print("Processing batch synchronously...")
    results = client.batch_generate_content(
        contents_list=contents_list,
        max_concurrency=3
    )
    
    # Display results
    # ...
    
    # Example using map_generate
    print("\nUsing map_generate for processing a list of items...")
    
    topics = ["Python", "JavaScript", "Rust"]
    template = "What makes {item} unique compared to other programming languages?"
    
    map_results = client.map_generate(
        template=template,
        items=topics,
        max_concurrency=3
    )
    
    # Display map results
    # ...
```

This function demonstrates two batch processing approaches:

#### Direct Batch Processing

The `batch_generate_content` method processes multiple prompts with controlled concurrency. Each prompt is processed as a separate request, but the method handles the concurrency to prevent overwhelming the API.

#### Template-Based Batch Processing

The `map_generate` method applies a template to a list of items, generating content for each. This is a higher-level abstraction that simplifies working with collections of similar prompts.

### 3. Async Support

The `demonstrate_async_support` function shows how to use the asynchronous API for non-blocking operations:

```python
async def demonstrate_async_support():
    """Example showing async support functionality."""
    client = GeminiClient()
    
    print("\n=== Async Support Example ===\n")
    
    # Single async request
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Explain quantum computing briefly.")]
        )
    ]
    
    print("Making asynchronous request...")
    response = await client.generate_content_async(contents)
    
    print("\nAsync response:")
    print(response[:150] + "..." if len(response) > 150 else response)
    
    # Multiple concurrent async requests
    # ...
    
    # Example using map_generate_async
    # ...
```

This function demonstrates three async approaches:

#### Single Async Request

The `generate_content_async` method is the async version of the main `generate_content` method. It has the same parameters but can be awaited in an async context.

#### Concurrent Async Requests

The `batch_generate_content_async` method processes multiple prompts concurrently in an asynchronous manner.

#### Async Template Processing

The `map_generate_async` method combines template-based batch processing with async capabilities.

### 4. Main Function

The `main` function orchestrates the execution of all the demonstrations:

```python
async def main():
    """Run all examples."""
    try:
        # Demonstrate response parsing helpers
        demonstrate_response_parsing()
        
        # Demonstrate batch processing
        demonstrate_batch_processing()
        
        # Demonstrate async support
        await demonstrate_async_support()
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
```

This pattern shows how to:
- Use both synchronous and asynchronous functions together
- Handle exceptions gracefully
- Launch an async entry point with `asyncio.run()`

## Running the Example

To run this example:

```bash
# From the repository root
python -m examples.example_async_batch_parsing
```

## Expected Output

The output will show results from all three demonstrations:

1. Extracted lists, JSON data, key-value pairs, and text chunks
2. Results from batch processing with both direct and template approaches
3. Results from async operations, including single and concurrent requests

## Key Takeaways

### Response Parsing

- Use the right parser for the right job
- Parsers handle various formats and are robust to minor variations
- Parsers can be combined for complex responses

### Batch Processing

- Batch processing is efficient for multiple similar prompts
- Templates simplify working with collections of items
- Concurrency controls help balance performance and API limits

### Async Support

- Async methods improve responsiveness in applications
- Multiple requests can run concurrently
- Async batch methods combine concurrency with efficient processing

## Next Steps

After understanding these advanced features, you can:

- Combine them in your own applications
- Explore customizing the parameters for your specific use cases
- Integrate them with web applications or data processing pipelines

For more information, see the detailed feature documentation:
- [Async Support](../features/async-support.md)
- [Batch Processing](../features/batch-processing.md)
- [Response Parsing Helpers](../features/response-parsing.md)
