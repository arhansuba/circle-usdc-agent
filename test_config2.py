# test_config.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def test_config():
    try:
        client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        
        print("Test successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_config()