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

import asyncio
from vertex_libs import GeminiClient
from google.genai import types
import json

def demonstrate_response_parsing():
    """
    Example showing various response parsing helpers.
    """
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
    json_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("""
                Provide information about three programming languages in JSON format.
                Include name, creator, and year created for each.
            """)]
        )
    ]
    
    print("\nExtracting JSON from response...")
    response = client.generate_content(json_contents)
    
    # Extract JSON (works with direct JSON, code blocks, etc.)
    languages_data = client.extract_json(response)
    
    if languages_data:
        print("\nExtracted JSON data:")
        print(json.dumps(languages_data, indent=2))
    
    # 3. Example with key-value pair extraction
    kv_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("""
                Provide information about Python in this format:
                Name: 
                Creator: 
                Year: 
                Paradigm: 
                Latest Version: 
            """)]
        )
    ]
    
    print("\nExtracting key-value pairs from response...")
    response = client.generate_content(kv_contents)
    
    # Extract key-value pairs
    python_info = client.parse_key_value_pairs(response)
    
    print("\nExtracted key-value pairs:")
    for key, value in python_info.items():
        print(f"{key}: {value}")
    
    # 4. Example with text chunk extraction
    chunk_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("""
                Write three short paragraphs about artificial intelligence.
                Separate each paragraph with a blank line.
            """)]
        )
    ]
    
    print("\nExtracting text chunks from response...")
    response = client.generate_content(chunk_contents)
    
    # Extract paragraphs/chunks
    paragraphs = client.extract_text_chunks(response)
    
    print("\nExtracted paragraphs:")
    for i, para in enumerate(paragraphs, 1):
        print(f"\nParagraph {i}:")
        print(para)

def demonstrate_batch_processing():
    """
    Example showing batch processing functionality.
    """
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
    print("\nBatch results:")
    for i, (prompt, result) in enumerate(zip(prompts, results), 1):
        print(f"\n--- Result {i}: {prompt} ---")
        print(result[:150] + "..." if len(result) > 150 else result)
    
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
    print("\nMap results:")
    for i, (topic, result) in enumerate(zip(topics, map_results), 1):
        print(f"\n--- Map Result {i}: {topic} ---")
        print(result[:150] + "..." if len(result) > 150 else result)

async def demonstrate_async_support():
    """
    Example showing async support functionality.
    """
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
    
    print("\nMaking multiple asynchronous requests concurrently...")
    async_results = await client.batch_generate_content_async(
        contents_list=contents_list,
        max_concurrency=3
    )
    
    # Display results
    print("\nAsync batch results:")
    for i, (prompt, result) in enumerate(zip(prompts, async_results), 1):
        print(f"\n--- Async Result {i}: {prompt} ---")
        print(result[:150] + "..." if len(result) > 150 else result)
    
    # Example using map_generate_async
    print("\nUsing map_generate_async...")
    
    frameworks = ["TensorFlow", "PyTorch", "scikit-learn"]
    template = "What are the main features of {item}?"
    
    async_map_results = await client.map_generate_async(
        template=template,
        items=frameworks,
        max_concurrency=3
    )
    
    # Display map results
    print("\nAsync map results:")
    for i, (framework, result) in enumerate(zip(frameworks, async_map_results), 1):
        print(f"\n--- Async Map Result {i}: {framework} ---")
        print(result[:150] + "..." if len(result) > 150 else result)

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
