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
import base64

def load_image_from_file(file_path: str) -> bytes:
    """Load image file as bytes."""
    with open(file_path, "rb") as image_file:
        return image_file.read()

def main():
    client = GeminiClient()

    # Load the image as bytes
    image_bytes = load_image_from_file("guardanapo.jpg")
    
    # Create content with both image and text
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    inline_data=types.Blob(
                        mime_type="image/jpeg",
                        data=image_bytes
                    )
                ),
                types.Part(text="What do you see in this image? Please describe it in detail.")
            ]
        )
    ]

    try:
        # Get non-streaming response
        print("Analyzing image...")
        response = client.generate_content(
            contents,
            model="gemini-2.0-flash-exp"  # Using the correct model name
        )
        print("\nResponse:", response)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 