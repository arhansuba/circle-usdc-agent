# check_env.py
import os
from dotenv import load_dotenv

load_dotenv()

print("GROQ_API_KEY from environment:", os.getenv("GROQ_API_KEY"))