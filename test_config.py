# test_config.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def test_xai_connection():
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1"
    )
    
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{
                "role": "user",
                "content": "Hello! Can you hear me?"
            }]
        )
        print("Connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_xai_connection()