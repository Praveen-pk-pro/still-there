from fastapi import APIRouter, HTTPException, Depends
from models.user import get_current_user
from utils.deepseek import generate_roadmap_with_deepseek
from utils.pdf_generator import create_roadmap_pdf
from main import supabase
from datetime import datetime

router = APIRouter()

@router.post("/generate")
async def generate_roadmap(domain: str, user: dict = Depends(get_current_user)):
    try:
        # Generate roadmap with DeepSeek
        roadmap_result = await generate_roadmap_with_deepseek(domain)
        
        # Generate PDF
        pdf_path = create_roadmap_pdf(roadmap_result)
        
        # Save to database
        roadmap_data = {
            "user_id": user["id"],
            "domain": domain,
            "roadmap_json": roadmap_result,
            "roadmap_pdf_url": pdf_path,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("roadmaps").insert(roadmap_data).execute()
        
        return {"success": True, "roadmap": roadmap_result, "roadmap_pdf_url": pdf_path, "roadmap_id": result.data[0]["id"] if result.data else None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roadmap generation failed: {str(e)}")

@router.get("/download/{roadmap_id}")
async def download_roadmap(roadmap_id: str, user: dict = Depends(get_current_user)):
    try:
        from main import supabase
        result = supabase.table("roadmaps").select("roadmap_pdf_url").eq("id", roadmap_id).eq("user_id", user["id"]).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Roadmap not found")
            
        file_path = result.data[0]["roadmap_pdf_url"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
            
        return FileResponse(
            file_path, 
            media_type="application/pdf",
            filename=f"learning_roadmap_{roadmap_id}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")