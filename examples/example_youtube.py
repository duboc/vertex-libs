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
        for chunk in stream:
            print(chunk, end="")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 