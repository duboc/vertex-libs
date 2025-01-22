import os
import logging
from typing import Optional, List
from tenacity import retry, stop_after_attempt, wait_exponential
from google import genai
from google.genai import types

class GeminiClient:
    """A client for interacting with Gemini API with region fallback capabilities."""
    
    def __init__(self, project_id: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize the GeminiClient.
        
        Args:
            project_id (str, optional): Google Cloud Project ID. If None, will try to get from environment.
            logger (logging.Logger, optional): Custom logger instance. If None, will create a new one.
        """
        self.project_id = project_id or os.environ.get("GCP_PROJECT")
        if not self.project_id:
            raise ValueError("Project ID must be provided or set in GCP_PROJECT environment variable")
            
        self.logger = logger or logging.getLogger(__name__)
        
        # List of regions to try
        self.regions = [
            "us-central1",
            "europe-west2",
            "europe-west3", 
            "asia-northeast1",
            "australia-southeast1",
            "asia-south1"
        ]
        
        # Default safety settings
        self.safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ]
        
        # Default generation config
        self.default_generation_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
            safety_settings=self.safety_settings
        )

    def _initialize_client(self, region: str):
        """Initialize Gemini client with the specified region."""
        return genai.Client(
            vertexai=True,
            project=self.project_id,
            location=region
        )

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    def generate_content(self, 
                        contents: List[types.Content],
                        stream: bool = False,
                        generation_config: Optional[types.GenerateContentConfig] = None,
                        model: str = "gemini-2.0-flash-exp") -> str:
        """
        Generate content using Gemini model with region fallback.
        
        Args:
            contents: List of Content objects containing the prompt
            stream: Whether to stream the response
            generation_config: Optional custom generation config
            model: Model name to use
            
        Returns:
            str: Generated content
            
        Raises:
            Exception: If all regions fail
        """
        last_error = None
        gen_config = generation_config or self.default_generation_config

        for region in self.regions:
            try:
                client = self._initialize_client(region)
                
                if stream:
                    response = client.models.generate_content_stream(
                        model=model,
                        contents=contents,
                        config=gen_config
                    )
                    return response
                else:
                    response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=gen_config
                    )
                    return response.text
                    
            except Exception as e:
                self.logger.warning(f"Error with region {region}: {str(e)}")
                last_error = e
                continue
        
        raise Exception(f"All regions failed. Last error: {str(last_error)}") from last_error

def example_usage():
    """Example usage of the GeminiClient"""
    client = GeminiClient()
    
    # Prepare the prompt
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text("Tell me a short story about a robot.")]
        )
    ]
    
    # Generate content
    try:
        # Non-streaming response
        response = client.generate_content(contents)
        print("Regular response:", response)
        
        # Streaming response
        stream = client.generate_content(contents, stream=True)
        print("\nStreaming response:")
        for chunk in stream:
            print(chunk, end="")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    example_usage()