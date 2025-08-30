from fastapi import APIRouter, HTTPException, Depends
from models.user import get_current_user
from utils.deepseek import generate_ats_resume_with_deepseek
from utils.pdf_generator import create_ats_resume_pdf
from main import supabase
from datetime import datetime

router = APIRouter()

@router.post("/generate")
async def generate_ats_resume(
    resume_data: dict, 
    domain: str, 
    user: dict = Depends(get_current_user)
):
    try:
        # Generate ATS resume with DeepSeek
        ats_resume = await generate_ats_resume_with_deepseek(resume_data, domain)
        
        # Generate PDF
        pdf_path = create_ats_resume_pdf(ats_resume)
        
        # Save to database
        ats_resume_data = {
            "user_id": user["id"],
            "resume_data": resume_data,
            "generated_resume_url": pdf_path,
            "domain": domain,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("ats_resumes").insert(ats_resume_data).execute()
        
        return {"success": True, "resume_url": pdf_path, "ats_resume_id": result.data[0]["id"] if result.data else None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ATS resume generation failed: {str(e)}")

@router.get("/download/{ats_resume_id}")
async def download_ats_resume(ats_resume_id: str, user: dict = Depends(get_current_user)):
    try:
        from main import supabase
        result = supabase.table("ats_resumes").select("generated_resume_url").eq("id", ats_resume_id).eq("user_id", user["id"]).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Resume not found")
            
        file_path = result.data[0]["generated_resume_url"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            file_path, 
            media_type="application/pdf",
            filename=f"ats_resume_{ats_resume_id}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")