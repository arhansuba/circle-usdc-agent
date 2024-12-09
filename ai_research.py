# ai_research.py
import autogen
from dotenv import load_dotenv
import os
import json
import logging
import httpx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Basic configuration
config_list = [{
    "model": "grok-beta",
    "api_key": os.getenv("XAI_API_KEY"),
    "base_url": "https://api.x.ai/v1"
}]

config = {
    "config_list": config_list,
    "temperature": 0.7,
}

# Create agents
user_proxy = autogen.UserProxyAgent(
    name="user",
    system_message="A human user. Interact with the planner to discuss the plan.",
    code_execution_config=False
)

planner = autogen.AssistantAgent(
    name="planner",
    llm_config=config,
    system_message="""Plan research tasks and coordinate between team members."""
)

engineer = autogen.AssistantAgent(
    name="engineer",
    llm_config=config,
    system_message="""Write code to solve tasks."""
)

scientist = autogen.AssistantAgent(
    name="scientist",
    llm_config=config,
    system_message="""Analyze research papers and provide insights."""
)

executor = autogen.UserProxyAgent(
    name="executor",
    system_message="Execute code and report results.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": False,
    }
)

critic = autogen.AssistantAgent(
    name="critic",
    llm_config=config,
    system_message="""Review and provide feedback on plans and results."""
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, planner, engineer, scientist, executor, critic],
    messages=[],
    max_round=50
)

# Create manager
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=config)

def run_research(topic):
    """Run research on a given topic"""
    try:
        initial_message = {
            "role": "user",
            "content": f"Research the following topic, check the arxiv website for interesting papers to support your result and create a markdown table of different domains: {topic}"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",  # Ensure the model field is included
            "messages": [
                {"role": "system", "content": "You are a research assistant."},
                initial_message
            ],
            "temperature": 0
        }
        
        response = httpx.post(f"{os.getenv('OPENAI_API_BASE')}/chat/completions", headers=headers, json=data)
        
        if response.status_code != 200:
            logger.error(f"Error in research execution: {response.status_code} - {response.text}")
            return None
        
        result = response.json()
        logger.info("Research completed successfully.")
        
        return {
            "engineer": 1,
            "scientist": 1,
            "planner": 1,
            "executor": 1,
            "critic": 1
        }
    except Exception as e:
        logger.error(f"Error in research execution: {str(e)}")
        raise

if __name__ == "__main__":
    topic = "Artificial intelligence and employment trends"
    contributions = run_research(topic)
    print(json.dumps(contributions))