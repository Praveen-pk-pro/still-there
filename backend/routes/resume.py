from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
import uuid
import os
from datetime import datetime
from typing import Optional

from utils.deepseek import analyze_resume_with_deepseek
from utils.file_processing import save_uploaded_file, create_improved_resume_pdf
from utils.resume_parser import parse_resume
from models.user import get_current_user

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    try:
        # Save uploaded file
        file_path = save_uploaded_file(file)
        
        # Parse resume content
        resume_content = parse_resume(file_path)
        
        # Analyze with DeepSeek
        analysis_result = await analyze_resume_with_deepseek(resume_content)
        
        # Generate improved resume
        improved_resume_path = create_improved_resume_pdf(
            resume_content, 
            analysis_result["improvements"]
        )
        
        # Save to database
        from main import supabase
        resume_data = {
            "user_id": user["id"],
            "original_filename": file.filename,
            "resume_url": file_path,
            "improved_resume_url": improved_resume_path,
            "score": analysis_result["score"],
            "analysis_json": analysis_result,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("resumes").insert(resume_data).execute()
        
        return JSONResponse({
            "success": True,
            "score": analysis_result["score"],
            "analysis": analysis_result["analysis"],
            "improvements": analysis_result["improvements"],
            "improved_resume_url": improved_resume_path,
            "resume_id": result.data[0]["id"] if result.data else None
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(e)}")

@router.get("/download-improved/{resume_id}")
async def download_improved_resume(resume_id: str, user: dict = Depends(get_current_user)):
    try:
        from main import supabase
        result = supabase.table("resumes").select("improved_resume_url").eq("id", resume_id).eq("user_id", user["id"]).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")
            
        file_path = result.data[0]["improved_resume_url"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            file_path, 
            media_type="application/pdf",
            filename=f"improved_resume_{resume_id}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")