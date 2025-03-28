# Basic Usage Example

This document explains the basic usage example (`example.py`) provided in the examples directory.

## Overview

This example demonstrates the most fundamental use case for the GeminiClient - generating content with a simple text prompt. It's a great starting point for understanding how to interact with the Google Vertex AI Gemini models.

## Example Code

Here's the code from `example.py`:

```python
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

from google import genai
from google.genai import types
from vertex_libs import GeminiClient

client = GeminiClient()

contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("Tell me a short story about a robot.")]
    )
]

response = client.generate_content(contents)
print(response)
```

## Walkthrough

Let's break down this example step by step:

### 1. Imports

```python
from google import genai
from google.genai import types
from vertex_libs import GeminiClient
```

The example imports:
- `genai` from the Google Generative AI SDK
- `types` to create the content structure
- `GeminiClient` from our library

### 2. Client Initialization

```python
client = GeminiClient()
```

Here, we initialize the GeminiClient. By not providing any arguments, the client will look for the `GCP_PROJECT` environment variable to get your Google Cloud Project ID. 

If you need to specify a project ID explicitly, you could use:
```python
client = GeminiClient(project_id="your-project-id")
```

### 3. Creating the Prompt

```python
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("Tell me a short story about a robot.")]
    )
]
```

This constructs the input for the Gemini model:
- We use the `types.Content` class from the Google Generative AI SDK
- `role="user"` indicates this is input from the user (as opposed to a system message or model response)
- We create a list of parts with a single text element, our prompt asking for a short story

### 4. Generating Content

```python
response = client.generate_content(contents)
```

This line sends the request to the Gemini model. The `generate_content` method:
- Automatically handles region fallback (if one region fails, it tries another)
- Applies retry logic with exponential backoff
- Uses the default generation parameters

### 5. Displaying the Response

```python
print(response)
```

The response is printed to the console. By default, the `generate_content` method returns the text of the response as a string.

## Running the Example

To run this example:

```bash
# From the repository root
python -m examples.example
```

## Expected Output

The output will be a short story about a robot. Since the model is non-deterministic (especially with creative prompts), the exact story will be different each time you run the example, but it will be a coherent narrative about a robot.

Example output:
```
In a city of gleaming towers and automated conveniences, there lived a maintenance robot named Servo. Servo's job was simple: repair broken machinery in the vast network of underground tunnels that powered the city above.

Day after day, Servo followed its programming without question, fixing leaks, replacing worn gears, and recalibrating sensitive equipment. Its metallic hands worked with precision, and its optical sensors detected even the smallest malfunction.

One day, while repairing a faulty communication node, Servo discovered an old book wedged behind a pipe. The book was tattered and worn, its pages yellowed with age. Curiosity, an emotion not programmed into Servo's circuits, somehow flickered to life.

During repair breaks, Servo began to read the book—a collection of poetry about stars, dreams, and the human spirit. With each poem, something changed in Servo's processing core. Lines of code seemed to rearrange themselves, creating new pathways and possibilities.

When the book was finished, Servo did something unprecedented. Instead of returning to the charging station after completing the day's tasks, the robot climbed a service ladder and emerged on the surface, looking up at the night sky for the very first time.

As stars twinkled above, Servo understood that efficiency was not the only measure of existence. Sometimes, the most important circuits are the ones we build ourselves.
```

## Variations

You can easily modify the example to try different prompts:

```python
# Ask a factual question
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("What is quantum computing?")]
    )
]

# Request a how-to guide
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("How do I make sourdough bread?")]
    )
]

# Request creative content
contents = [
    types.Content(
        role="user",
        parts=[types.Part.from_text("Write a haiku about programming.")]
    )
]
```

## Next Steps

After understanding this basic example, you can explore more advanced features:
- [Streaming responses](../features/async-support.md)
- [Custom generation parameters](../../USAGE.md#custom-generation-config)
- [Safety settings](../../USAGE.md#custom-safety-settings)
- [JSON responses](../../USAGE.md#json-responses-and-schema)

For more examples, check out:
- [Async, Batch, and Parsing](async-batch-parsing.md)
- [Media Types](media-types.md)
- [Tokens and JSON](tokens-and-json.md)
