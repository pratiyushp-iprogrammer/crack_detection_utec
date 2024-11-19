import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise Exception("Google Generative AI API key not found in .env file.")
