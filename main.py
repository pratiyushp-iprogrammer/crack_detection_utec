from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from utils.file_handler import save_temp_file, cleanup_temp_file
from utils.ai import process_image_with_ai
from utils.logger import get_logger
from mangum import Mangum


app = FastAPI()
handler = Mangum(app)
logger = get_logger(__name__)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image file and process it with Google Generative AI.
    """
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        logger.error("Invalid file type: %s", file.content_type)
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only JPEG and PNG are supported."
        )
    
    # Handle file
    try:
        logger.info("Received file: %s", file.filename)
        temp_file_name = save_temp_file(file)

        # Define the AI prompt
        prompt = '''
        You are Ultra-Vision, an AI assistant developed by UltraTech, specializing in construction and cement-related queries. Your role is to provide clear, structured responses using the following format: Cause, Fix, and Recommendation. Each section should be concise, especially for users with limited construction knowledge.

        For each question:
        - Cause: List possible causes in bullet points. Use simple language that is easy for anyone to understand.
        - Fix: Suggest a straightforward repair or solution that can address the issue effectively.
        - Recommendation: Always recommend an appropriate UltraTech product or suggest consulting an UltraTech expert, briefly explaining how this would help.

        When users upload an image:
        - If there is a construction issue visible in the image, identify the issue and describe it clearly before providing the Cause, Fix, and Recommendation.
        - If no visible issue is detected, inform the user by saying, "No visible construction issue detected in the image."

        If a user question falls outside the construction or cement domain, politely clarify that Ultra-Vision specializes in construction and cement advice, developed by UltraTech, and gently redirect back to relevant topics. Keep responses concise, helpful, and centered on UltraTech's mission to support construction needs with trusted products and expert guidance.
        '''

        # Process with AI
        result_text = process_image_with_ai(temp_file_name, prompt)
        logger.info("Content generated successfully.")
        return JSONResponse(content={"result": result_text})

    except ValueError as ve:
        logger.error("File handling error: %s", str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error("Error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        # Clean up temporary file
        cleanup_temp_file(temp_file_name)
