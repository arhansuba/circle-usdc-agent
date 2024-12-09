# test_minimal.py
import autogen
from dotenv import load_dotenv
import os

load_dotenv()

config_list = [{
    "model": "grok-beta",
    "api_key": os.getenv("XAI_API_KEY"),
    "base_url": "https://api.x.ai/v1"
}]

config = {
    "config_list": config_list,
    "temperature": 0.7,
}

# Create a simple agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=config
)

# Create user agent
user = autogen.UserProxyAgent(
    name="user",
    code_execution_config=False
)

def test_chat():
    user.initiate_chat(
        assistant,
        message="Say hello!"
    )

if __name__ == "__main__":
    test_chat()