# Async Support

The GeminiClient provides asynchronous methods that allow non-blocking API calls for improved application responsiveness. This is particularly useful in web applications, API services, or any environment where you want to maintain responsiveness while making multiple API calls.

## Overview

Asynchronous methods in GeminiClient use Python's `asyncio` library to provide non-blocking API call capabilities. Since the Google Vertex AI APIs themselves don't yet have native async support, these methods use a thread pool executor to run the synchronous operations in the background.

## Available Async Methods

### generate_content_async

```python
async def generate_content_async(self, 
                           contents: List[types.Content],
                           stream: bool = False,
                           generation_config: Optional[types.GenerateContentConfig] = None,
                           model: str = "gemini-2.0-flash-exp",
                           return_json: bool = False,
                           json_schema: Optional[Dict] = None,
                           count_tokens: bool = False)
```

This is the async version of the main `generate_content` method. It has the same parameters and return types but can be awaited in an async context.

### batch_generate_content_async

```python
async def batch_generate_content_async(self, 
                                contents_list: List[List[types.Content]],
                                generation_config: Optional[types.GenerateContentConfig] = None,
                                model: str = "gemini-2.0-flash-exp",
                                return_json: bool = False,
                                json_schema: Optional[Dict] = None,
                                count_tokens: bool = False,
                                max_concurrency: int = 5)
```

Processes multiple prompts in batch mode asynchronously, with a configurable concurrency level.

### map_generate_async

```python
async def map_generate_async(self, 
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

Asynchronously applies a template across a list of items, generating content for each.

## Basic Usage

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
    
    # Simple async call
    response = await client.generate_content_async(contents)
    print(response)

# Run the async function
asyncio.run(example())
```

## Advanced Usage

### Concurrent API Calls

```python
import asyncio
from vertex_libs import GeminiClient
from google.genai import types

async def make_multiple_requests():
    client = GeminiClient()
    
    # Prepare multiple prompts
    prompts = [
        "What is machine learning?",
        "What is deep learning?",
        "What is reinforcement learning?"
    ]
    
    # Convert to contents format
    contents_list = [
        [types.Content(
            role="user",
            parts=[types.Part.from_text(prompt)]
        )]
        for prompt in prompts
    ]
    
    # Process all prompts concurrently with a limit of 3 concurrent requests
    results = await client.batch_generate_content_async(
        contents_list=contents_list,
        max_concurrency=3
    )
    
    # Process results
    for prompt, result in zip(prompts, results):
        print(f"Prompt: {prompt}")
        print(f"Response: {result[:100]}...")  # Show first 100 chars
        print()

# Run the async function
asyncio.run(make_multiple_requests())
```

### Using map_generate_async with a Template

```python
import asyncio
from vertex_libs import GeminiClient

async def process_with_template():
    client = GeminiClient()
    
    # Define items and template
    frameworks = ["TensorFlow", "PyTorch", "scikit-learn"]
    template = "What are the main features of {item}?"
    
    # Process all items concurrently
    results = await client.map_generate_async(
        template=template,
        items=frameworks,
        max_concurrency=3
    )
    
    # Process results
    for framework, result in zip(frameworks, results):
        print(f"Framework: {framework}")
        print(f"Response: {result[:100]}...")  # Show first 100 chars
        print()

# Run the async function
asyncio.run(process_with_template())
```

### Custom Map Function

```python
import asyncio
from vertex_libs import GeminiClient

async def process_with_map_function():
    client = GeminiClient()
    
    # Custom mapping function
    def format_language(language):
        return f"the {language} programming language"
    
    # Define items and template
    languages = ["Python", "JavaScript", "Rust"]
    template = "What are the unique features of {item}?"
    
    # Process all items concurrently with custom mapping
    results = await client.map_generate_async(
        template=template,
        items=languages,
        map_function=format_language,
        max_concurrency=3
    )
    
    # Process results
    for language, result in zip(languages, results):
        print(f"Language: {language}")
        print(f"Response: {result[:100]}...")  # Show first 100 chars
        print()

# Run the async function
asyncio.run(process_with_map_function())
```

## Best Practices

1. **Error Handling**: Always use try/except blocks around async operations:

```python
async def safe_generate():
    try:
        response = await client.generate_content_async(contents)
        return response
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None
```

2. **Concurrency Control**: Be mindful of the `max_concurrency` parameter to avoid overloading:

```python
# Limit to 5 concurrent requests
results = await client.batch_generate_content_async(
    contents_list=contents_list,
    max_concurrency=5  # Adjust based on your application's needs
)
```

3. **Timeout Handling**: Consider implementing timeouts for async operations:

```python
import asyncio

async def with_timeout():
    try:
        # Set a timeout of 30 seconds
        response = await asyncio.wait_for(
            client.generate_content_async(contents),
            timeout=30.0
        )
        return response
    except asyncio.TimeoutError:
        print("The operation timed out")
        return None
```

4. **Integration with Web Frameworks**: The async methods integrate well with async web frameworks like FastAPI:

```python
from fastapi import FastAPI
from vertex_libs import GeminiClient
from google.genai import types

app = FastAPI()
client = GeminiClient()

@app.get("/generate")
async def generate(prompt: str):
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(prompt)]
        )
    ]
    
    response = await client.generate_content_async(contents)
    return {"response": response}
```

## Performance Considerations

- Async operations still consume API quotas and resources
- Using high concurrency may lead to rate limiting
- For very high throughput, consider implementing your own rate limiting
- Monitor memory usage when processing large batches

## Advanced Example: Multiple Operations in Parallel

```python
import asyncio
from vertex_libs import GeminiClient
from google.genai import types

async def complex_workflow():
    client = GeminiClient()
    
    # Define several different tasks
    async def task1():
        contents = [types.Content(
            role="user",
            parts=[types.Part.from_text("What is machine learning?")]
        )]
        return await client.generate_content_async(contents)
    
    async def task2():
        languages = ["Python", "JavaScript", "Rust"]
        template = "What is {item} used for?"
        return await client.map_generate_async(template=template, items=languages)
    
    async def task3():
        contents = [types.Content(
            role="user",
            parts=[types.Part.from_text("Write a short poem about technology.")]
        )]
        return await client.generate_content_async(contents)
    
    # Run all tasks concurrently
    result1, result2, result3 = await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
    
    # Process results
    print("Task 1 Result:", result1[:50], "...")
    print("Task 2 Results:", [r[:20] + "..." for r in result2])
    print("Task 3 Result:", result3[:50], "...")

# Run the complex workflow
asyncio.run(complex_workflow())
```

## References

- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
