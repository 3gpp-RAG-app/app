import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Set the OPENAI_API_KEY environment variable.")

client = OpenAI()
client.api_key = openai_api_key

search_endpoint = 'http://127.0.0.1:5000/milvus/search'
logs_endpoint = 'http://127.0.0.1:5000/milvus/logs'
secrect_key = 'thisShouldBeBetterPasswordLatee'