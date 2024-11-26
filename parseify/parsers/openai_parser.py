import requests
import json

class OpenAIParser:
    """
    Parser for content extraction using OpenAI's API via direct HTTP requests.
    """

    def __init__(self, api_key, model="gpt-4o-mini"):
        """
        Initialize the OpenAIParser with API key and model.

        Args:
            api_key (str): OpenAI API key.
            model (str): Model to use (default: 'gpt-4').
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def parse(self, messages, json_schema):
        """
        Parse the content using OpenAI's chat completion API with a JSON schema.

        Args:
            messages (list): List of messages for the OpenAI Chat API.
            json_schema (dict): JSON schema for structuring the response.

        Returns:
            dict: Parsed data as per the provided JSON schema or None if the request fails.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "schema",
                    "schema": {
                        "type": "object",
                        "properties": json_schema,  # Use the corrected response_schema here
                        "required": list(json_schema.keys()),
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                return json.loads(response.json()["choices"][0]["message"]["content"])
            else:
                print(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None
