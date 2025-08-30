from fastapi import APIRouter, HTTPException, Depends
from models.user import get_current_user
from utils.deepseek import generate_cover_letter_with_deepseek
from utils.pdf_generator import create_cover_letter_pdf
from main import supabase
from datetime import datetime

router = APIRouter()

@router.post("/generate")
async def generate_cover_letter(
    job_title: str, 
    company_name: str, 
    resume_content: str, 
    user: dict = Depends(get_current_user)
):
    try:
        # Generate cover letter with DeepSeek
        cover_letter = await generate_cover_letter_with_deepseek(resume_content, f"Job Title: {job_title}, Company: {company_name}")
        
        # Generate PDF
        pdf_path = create_cover_letter_pdf(cover_letter)
        
        # Save to database
        cover_letter_data = {
            "user_id": user["id"],
            "job_title": job_title,
            "company_name": company_name,
            "cover_letter_text": cover_letter,
            "letter_url": pdf_path,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("cover_letters").insert(cover_letter_data).execute()
        
        return {"success": True, "cover_letter": cover_letter, "cover_letter_url": pdf_path, "cover_letter_id": result.data[0]["id"] if result.data else None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")

@router.get("/download/{cover_letter_id}")
async def download_cover_letter(cover_letter_id: str, user: dict = Depends(get_current_user)):
    try:
        from main import supabase
        result = supabase.table("cover_letters").select("letter_url").eq("id", cover_letter_id).eq("user_id", user["id"]).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Cover letter not found")
            
        file_path = result.data[0]["letter_url"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            file_path, 
            media_type="application/pdf",
            filename=f"cover_letter_{cover_letter_id}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")