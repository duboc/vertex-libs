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

def main():
    client = GeminiClient()

    # Create video part from YouTube URL
    video_part = types.Part.from_uri(
        file_uri="https://www.youtube.com/watch?v=h7RgCa-ooQU&t=29s",
        mime_type="video/*"
    )

    # Create content with video and text prompt
    contents = [
        types.Content(
            role="user",
            parts=[
                video_part,
                types.Part(text="Please describe this video in detail.")
            ]
        )
    ]

    try:
        # Get streaming response
        print("Analyzing video...")
        stream = client.generate_content(
            contents=contents,
            stream=True  # Enable streaming for longer responses
        )
        
        print("\nResponse:")
        full_text = ""
        for chunk in stream:
            # Extract just the text content from the chunk
            try:
                if hasattr(chunk, 'candidates') and chunk.candidates:
                    # Get the first candidate
                    candidate = chunk.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        # Get the text from the first part
                        text = candidate.content.parts[0].text
                        if text:
                            full_text += text
                            print(text, end="")
            except Exception as e:
                print(f"Error processing chunk: {e}")
        
        # Print a newline at the end
        print()

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
