import google.generativeai as genai
from config import GENAI_API_KEY

# Configure Google Generative AI
genai.configure(api_key=GENAI_API_KEY)

# Define the generative AI model
model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

def process_image_with_ai(file_path: str, prompt: str) -> str:
    """
    Processes the given image using Google Generative AI with the specified prompt.
    """
    uploaded_file = genai.upload_file(file_path)
    result = model.generate_content([uploaded_file, "\n\n", prompt])
    return result.text
