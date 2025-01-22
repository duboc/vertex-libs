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

    # Example with different media sources
    contents = [
        types.Content(
            role="user",
            parts=[
                # GCS bucket image
                types.Part.from_uri(
                    file_uri="gs://your-bucket/image.jpg",
                    mime_type="image/jpeg"
                ),
                # GCS bucket video
                types.Part.from_uri(
                    file_uri="gs://your-bucket/video.mp4",
                    mime_type="video/mp4"
                ),
                # GCS bucket audio
                types.Part.from_uri(
                    file_uri="gs://your-bucket/audio.mp3",
                    mime_type="audio/mpeg"
                ),
                # YouTube video
                types.Part.from_uri(
                    file_uri="https://www.youtube.com/watch?v=your-video-id",
                    mime_type="video/*"
                ),
                # Text prompt
                types.Part(text="Please analyze all these media files and describe what you see and hear.")
            ]
        )
    ]

    try:
        print("Analyzing media...")
        stream = client.generate_content(
            contents=contents,
            stream=True
        )
        
        print("\nResponse:")
        for chunk in stream:
            print(chunk, end="")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 