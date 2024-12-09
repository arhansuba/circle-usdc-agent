# test_groq.py
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def test_groq_connection():
    api_key = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": "Say hello!"}]
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print("Connection successful!")
            result = response.json()
            print("Response:", result['choices'][0]['message']['content'])
            return True
        else:
            print(f"Error status code: {response.status_code}")
            print(f"Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error connecting to Groq: {str(e)}")
        return False

if __name__ == "__main__":
    test_groq_connection()