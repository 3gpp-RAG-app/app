import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenAI configuration
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Set the OPENAI_API_KEY environment variable.")

client = OpenAI()
client.api_key = openai_api_key
