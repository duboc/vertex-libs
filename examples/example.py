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