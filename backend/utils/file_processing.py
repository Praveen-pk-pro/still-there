import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

def save_uploaded_file(file: UploadFile) -> str:
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    return file_path