# Response Parsing Helpers

The GeminiClient provides a set of helper methods for extracting structured information from model responses. These tools make it easier to work with various output formats and convert unstructured text into usable data structures.

## Overview

Parsing LLM responses can be challenging due to their variability and free-form nature. The response parsing helpers offer standardized methods to extract common data structures like lists, JSON objects, key-value pairs, and text chunks from responses, regardless of the exact format provided by the model.

## Available Parsing Methods

### extract_list

```python
def extract_list(self, response: Union[str, Dict], key: Optional[str] = None) -> List[str]:
```

Extracts a list of items from a response, handling various formats including markdown lists, JSON arrays, and more.

### extract_json

```python
def extract_json(self, text: str) -> Optional[Dict]:
```

Extracts JSON from text, even if it's embedded within other content, wrapped in code blocks, or contains minor formatting issues.

### parse_key_value_pairs

```python
def parse_key_value_pairs(self, text: str) -> Dict[str, str]:
```

Extracts key-value pairs from text formatted with "Key: Value" patterns on separate lines.

### extract_text_chunks

```python
def extract_text_chunks(self, response, separator: str = '\n\n') -> List[str]:
```

Splits a response into separate chunks using a specified separator (default is double newline).

## Basic Usage

### Extracting Lists

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt asking for a list
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("List 5 best practices for Python programming.")]
    )
]

# Get response
response = client.generate_content(contents)

# Extract list items
best_practices = client.extract_list(response)

# Print the extracted list
print("Best Practices for Python Programming:")
for i, practice in enumerate(best_practices, 1):
    print(f"{i}. {practice}")
```

This works with various list formats:

- Markdown bullet points (`* Item` or `- Item`)
- Numbered lists (`1. Item`)
- JSON arrays in the response
- List items directly found in a dictionary key

### Extracting JSON

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt requesting JSON
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Provide information about three programming languages in JSON format.
            Include for each: name, creator, and year created.
        """)]
    )
]

# Get response
response = client.generate_content(contents)

# Extract and parse JSON
languages_data = client.extract_json(response)

if languages_data:
    # Process the structured data
    for language in languages_data:
        print(f"Language: {language.get('name', 'Unknown')}")
        print(f"Creator: {language.get('creator', 'Unknown')}")
        print(f"Year: {language.get('year', 'Unknown')}")
        print()
else:
    print("No valid JSON found in the response.")
    print(response)  # Show the raw response
```

### Parsing Key-Value Pairs

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt for key-value information
contents = [
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

# Get response
response = client.generate_content(contents)

# Extract key-value pairs
python_info = client.parse_key_value_pairs(response)

# Print the structured information
print("Python Information:")
for key, value in python_info.items():
    print(f"{key}: {value}")
```

### Extracting Text Chunks

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt for text with paragraphs
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Write three short paragraphs about artificial intelligence.
            Separate each paragraph with a blank line.
        """)]
    )
]

# Get response
response = client.generate_content(contents)

# Extract paragraphs
paragraphs = client.extract_text_chunks(response)

# Print each paragraph
print(f"Found {len(paragraphs)} paragraphs:")
for i, para in enumerate(paragraphs, 1):
    print(f"\nParagraph {i}:")
    print(para)
```

## Advanced Usage

### Combining Multiple Parsers

You can combine multiple parsing methods to handle complex responses:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt for mixed format response
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Provide information about Python:
            1. A brief description
            2. Key information in Key: Value format (Creator, Year, Latest Version)
            3. A JSON object with its main features
        """)]
    )
]

# Get response
response = client.generate_content(contents)

# Extract paragraphs to separate the sections
sections = client.extract_text_chunks(response)

if len(sections) >= 3:
    # First section: description
    description = sections[0]
    print("Description:")
    print(description)
    print()
    
    # Second section: key-value pairs
    key_values = client.parse_key_value_pairs(sections[1])
    print("Key Information:")
    for key, value in key_values.items():
        print(f"{key}: {value}")
    print()
    
    # Third section: JSON
    features = client.extract_json(sections[2])
    if features:
        print("Features:")
        for feature in features.get("features", []):
            print(f"- {feature}")
```

### Handling Nested Lists

The `extract_list` method can handle nested structures when you provide a key:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt for nested data
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Generate a JSON object with programming languages categorized by type.
            Include: compiled languages, interpreted languages, and hybrid languages.
        """)]
    )
]

# Get response
response = client.generate_content(contents)

# Extract JSON first
data = client.extract_json(response)

if data:
    # Extract lists for each category
    compiled = client.extract_list(data, key="compiled_languages")
    interpreted = client.extract_list(data, key="interpreted_languages")
    hybrid = client.extract_list(data, key="hybrid_languages")
    
    print("Compiled Languages:", compiled)
    print("Interpreted Languages:", interpreted)
    print("Hybrid Languages:", hybrid)
```

### Custom Separators for Text Chunks

You can specify custom separators for `extract_text_chunks`:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Create a prompt for sections with custom separators
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Write about three programming languages.
            Separate each language with a line of dashes (---).
        """)]
    )
]

# Get response
response = client.generate_content(contents)

# Extract sections with custom separator
languages = client.extract_text_chunks(response, separator="---")

# Print each section
for i, language in enumerate(languages, 1):
    print(f"Language {i}:")
    print(language.strip())
    print()
```

## Best Practices

### 1. Provide Clear Instructions in Prompts

For optimal results, give clear instructions in your prompts about the expected format:

```python
# Clear prompt for extracting lists
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            List exactly 5 features of Python.
            Format each feature as a bullet point starting with a dash (-).
        """)]
    )
]
```

### 2. Handle Parsing Failures Gracefully

Always implement proper error handling for cases where parsing might fail:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Get response
response = client.generate_content(contents)

# Try to extract JSON with fallback
try:
    data = client.extract_json(response)
    if data:
        # Process structured data
        print("Successfully parsed JSON:", data)
    else:
        # Fall back to treating as text
        print("No JSON found, raw response:", response)
except Exception as e:
    print(f"Error parsing response: {str(e)}")
    print("Raw response:", response)
```

### 3. Combine with JSON Schema for Reliable Structured Data

For the most reliable structured data, combine parsing helpers with the built-in JSON schema support:

```python
from vertex_libs import GeminiClient
from google.genai import types

client = GeminiClient()

# Define JSON schema
json_schema = {
    "type": "OBJECT",
    "properties": {
        "languages": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "name": {"type": "STRING"},
                    "year": {"type": "NUMBER"},
                    "features": {"type": "ARRAY", "items": {"type": "STRING"}}
                }
            }
        }
    }
}

# Create prompt for structured data
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("List 3 programming languages with their year of creation and key features.")]
    )
]

# Request JSON response directly
structured_response = client.generate_content(
    contents,
    return_json=True,
    json_schema=json_schema
)

# No parsing needed for the outer structure
if isinstance(structured_response, dict) and "languages" in structured_response:
    languages = structured_response["languages"]
    for lang in languages:
        print(f"Language: {lang['name']} ({lang['year']})")
        
        # For extracting the nested list, you can still use the helper
        features = client.extract_list(lang, key="features")
        for feature in features:
            print(f"- {feature}")
        print()
```

### 4. Chain Extractors for Complex Data

For complex responses, chain multiple extractors to break down the parsing:

```python
# First extract chunks
sections = client.extract_text_chunks(response)

# Process each section differently
for i, section in enumerate(sections):
    if i == 0:  # First section might be an introduction
        print("Introduction:", section)
    elif ":" in section:  # Sections with colons might be key-value pairs
        kv_pairs = client.parse_key_value_pairs(section)
        print("Key-value section:", kv_pairs)
    elif section.strip().startswith(("{", "[")):  # Section might contain JSON
        json_data = client.extract_json(section)
        if json_data:
            print("JSON section:", json_data)
    elif any(line.strip().startswith(("-", "*", "•")) for line in section.split("\n")):
        # Section might contain a list
        items = client.extract_list(section)
        print("List section:", items)
```

## Common Use Cases

### 1. Extracting Structured Information from Reports

```python
# Prompt for a financial report
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("""
            Generate a quarterly financial report for a fictional tech company.
            Include:
            - Executive summary
            - Key metrics (Revenue, Profit, Growth)
            - Recommendations (as a bulleted list)
        """)]
    )
]

response = client.generate_content(contents)

# Extract sections
sections = client.extract_text_chunks(response)

# Extract metrics as key-value pairs
metrics_section = next((s for s in sections if "Revenue" in s), "")
metrics = client.parse_key_value_pairs(metrics_section)

# Extract recommendations as a list
recommendations_section = next((s for s in sections if "Recommendations" in s), "")
recommendations = client.extract_list(recommendations_section)

print(f"Revenue: {metrics.get('Revenue', 'N/A')}")
print(f"Profit: {metrics.get('Profit', 'N/A')}")
print("\nRecommendations:")
for rec in recommendations:
    print(f"- {rec}")
```

### 2. Processing Survey Responses

```python
# Process multiple survey responses
survey_responses = [
    "I liked the product. Rating: 4/5. Pros: Easy to use, Fast, Reliable. Cons: Expensive.",
    "Rating: 3/5. Pros: Good design. Cons: Slow performance, Poor documentation.",
    "Great product overall! Rating: 5/5. Pros: Intuitive, Powerful, Well-designed. No cons to mention."
]

results = []
for response in survey_responses:
    # Extract rating
    kv = client.parse_key_value_pairs(response)
    rating = kv.get("Rating", "N/A")
    
    # Extract pros and cons
    pros_text = response.split("Pros:")[1].split("Cons:")[0] if "Pros:" in response else ""
    cons_text = response.split("Cons:")[1] if "Cons:" in response else ""
    
    pros = [p.strip() for p in pros_text.split(",") if p.strip()]
    cons = [c.strip() for c in cons_text.split(",") if c.strip()]
    
    results.append({
        "rating": rating,
        "pros": pros,
        "cons": cons
    })

# Analyze results
avg_rating = sum(float(r["rating"].split("/")[0]) for r in results) / len(results)
all_pros = [p for r in results for p in r["pros"]]
all_cons = [c for r in results for c in r["cons"]]

print(f"Average Rating: {avg_rating:.1f}/5")
print(f"Most common pros: {', '.join(set(all_pros))}")
print(f"Most common cons: {', '.join(set(all_cons))}")
```

## References

- [Regular Expressions in Python](https://docs.python.org/3/library/re.html)
- [JSON in Python](https://docs.python.org/3/library/json.html)
- [Working with Text in Python](https://docs.python.org/3/library/text.html)
