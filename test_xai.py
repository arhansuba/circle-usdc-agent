# test_xai.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_models():
    api_key = os.getenv("XAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try to list available models
    try:
        response = requests.get(
            "https://api.x.ai/v1/models",
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_models()