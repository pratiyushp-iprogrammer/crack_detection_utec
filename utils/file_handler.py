from tempfile import NamedTemporaryFile
import os
import shutil
from PIL import Image

def save_temp_file(upload_file) -> str:
    """
    Saves the uploaded file to a temporary file and validates it.
    """
    with NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)
        temp_file_name = temp_file.name

    # Validate image
    try:
        Image.open(temp_file_name).verify()
    except Exception:
        os.remove(temp_file_name)
        raise ValueError("Invalid image content.")
    
    return temp_file_name

def cleanup_temp_file(file_path: str):
    """
    Removes the temporary file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
