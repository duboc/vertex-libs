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

from vertex_libs import GeminiClient
from google.genai import types
import json

def demonstrate_token_counting():
    """Example of token counting functionality."""
    client = GeminiClient()
    
    # Simple prompt
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("What is quantum computing?")]
        )
    ]
    
    # Count tokens before generation
    token_count = client.count_tokens(contents)
    print("\n=== Token Count Before Generation ===")
    print(f"Prompt tokens: {token_count.prompt_tokens}")
    
    # Generate with token counting
    print("\n=== Generate with Token Counting ===")
    response, usage = client.generate_content(contents, count_tokens=True)
    print(f"Response: {response}")
    print(f"\nToken Usage:")
    print(f"- Total tokens: {usage.total_tokens}")
    print(f"- Prompt tokens: {usage.prompt_tokens}")
    print(f"- Completion tokens: {usage.completion_tokens}")

def demonstrate_json_responses():
    """Example of JSON response parsing."""
    client = GeminiClient()
    
    # Request structured data
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("""
                Return a JSON object with information about three programming languages.
                Include for each: name, year_created, main_use_case, and popularity_rank.
                Format as a list of objects.
            """)]
        )
    ]
    
    print("\n=== JSON Response Example ===")
    # Get parsed JSON response
    response = client.generate_content(contents, return_json=True)
    
    # Process structured data
    if isinstance(response, list):
        for lang in response:
            print(f"\nLanguage: {lang['name']}")
            print(f"Created: {lang['year_created']}")
            print(f"Use Case: {lang['main_use_case']}")
            print(f"Rank: {lang['popularity_rank']}")
    else:
        print("Response:", response)

def demonstrate_combined_features():
    """Example combining JSON responses and token counting."""
    client = GeminiClient()
    
    # Define JSON schema for quantum computing response
    json_schema = {
        "type": "OBJECT",
        "properties": {
            "basic_definition": {"type": "STRING"},
            "key_concepts": {"type": "ARRAY", "items": {"type": "STRING"}},
            "practical_applications": {"type": "ARRAY", "items": {"type": "STRING"}},
            "current_limitations": {"type": "ARRAY", "items": {"type": "STRING"}}
        }
    }
    
    # Request structured data about quantum computing
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("""
                Provide information about quantum computing with:
                - A basic definition
                - Key concepts
                - Practical applications
                - Current limitations
            """)]
        )
    ]
    
    print("\n=== Combined JSON and Token Counting Example ===")
    # Get both structured response and token usage
    response, usage = client.generate_content(
        contents,
        return_json=True,
        json_schema=json_schema,
        count_tokens=True
    )
    
    print("\nStructured Response:")
    try:
        data = json.loads(response)
        if 'basic_definition' in data:
            print(f"\nDefinition:")
            print(data['basic_definition'])
        
        if 'key_concepts' in data:
            print("\nKey Concepts:")
            for concept in data['key_concepts']:
                print(f"- {concept}")
        
        if 'practical_applications' in data:
            print("\nPractical Applications:")
            for app in data['practical_applications']:
                print(f"- {app}")
        
        if 'current_limitations' in data:
            print("\nCurrent Limitations:")
            for limit in data['current_limitations']:
                print(f"- {limit}")
    except json.JSONDecodeError:
        print("Raw response:", response)
    
    print("\nToken Usage Statistics:")
    print(f"- Total tokens: {usage.total_tokens}")
    print(f"- Prompt tokens: {usage.prompt_tokens}")
    print(f"- Response tokens: {usage.completion_tokens}")

def demonstrate_dynamic_response():
    """Example showing how to get either text or JSON responses based on user input."""
    client = GeminiClient()
    
    # Example with text response
    text_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("What is quantum computing?")]
        )
    ]
    
    print("\n=== Text Response Example ===")
    text_response = client.generate_content(text_contents)
    print(f"Text Response: {text_response}")
    
    # Example with JSON response
    json_schema = {
        "type": "OBJECT",
        "properties": {
            "definition": {"type": "STRING"},
            "advantages": {"type": "ARRAY", "items": {"type": "STRING"}}
        }
    }
    
    json_contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("""
                Explain quantum computing in a structured format with:
                - A brief definition
                - Key advantages
            """)]
        )
    ]
    
    print("\n=== JSON Response Example ===")
    json_response = client.generate_content(
        json_contents,
        return_json=True,
        json_schema=json_schema
    )
    
    try:
        data = json.loads(json_response)
        print("\nStructured Data:")
        print(f"Definition: {data['definition']}")
        print("\nAdvantages:")
        for advantage in data['advantages']:
            print(f"- {advantage}")
    except json.JSONDecodeError:
        print("Raw response:", json_response)

def main():
    """Run all demonstrations."""
    try:
        demonstrate_token_counting()
        demonstrate_json_responses()
        demonstrate_combined_features()
        demonstrate_dynamic_response()
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 