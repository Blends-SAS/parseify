import requests
import json
import openai
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




class OpenAIService:


    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        

    def __call__(self, messages):

        client = openai.OpenAI(api_key = self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model = 'gpt-4o',
            messages = messages,
            temperature=0,
            max_tokens=3500,
            top_p=1,
            frequency_penalty=0, 
            presence_penalty =0
        )

        return response.choices[0].message.content
    
    def translate(self, results, language):
            
            ''' Takes results from Websiteanalizer and translates them into the desired language'''
            
            #print('##### Raw results from parsiefy #####', results)
            prompt = f"""
                        Below, I will provide a Python dictionary containing some information. The values of this dictionary may be in various languages.

                        Your task is to:

                        1. Translate only the values of the dictionary into {language}.
                        2. If a value is already in the desired language, leave it unchanged.
                        4. If the value to translate is an URL or a name, leave it unchanged.
                        2. Return the dictionary as a string  format that is JSON-compatible and can be directly parsed using json.loads in Python.
                        Ensure the output contains no additional text or formatting—only the JSON representation of the dictionary.

                        ### PYTHON DICTIONARY ###

                        {json.dumps(results)}
                        """
            messages = [{"role": "user","content": prompt}]
            # Call gpt and json loads the results
            translated_results = self.__call__(messages=messages)[7:-3]
            # print("##### Translated results ####", translated_results)
            results = json.loads(translated_results)

            return results