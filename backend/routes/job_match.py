from fastapi import APIRouter, HTTPException, Depends
from models.user import get_current_user
from utils.deepseek import analyze_job_match_with_deepseek
from main import supabase
from datetime import datetime

router = APIRouter()

@router.post("/analyze")
async def analyze_job_match(
    desired_role: str, 
    resume_content: str, 
    user: dict = Depends(get_current_user)
):
    try:
        # Analyze job match with DeepSeek
        analysis_result = await analyze_job_match_with_deepseek(resume_content, desired_role)
        
        # Save to database
        job_match_data = {
            "user_id": user["id"],
            "desired_role": desired_role,
            "matches_json": analysis_result.get("matches", []),
            "skill_gaps_json": analysis_result.get("skill_gaps", []),
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("job_matches").insert(job_match_data).execute()
        
        return {"success": True, "analysis": analysis_result, "job_match_id": result.data[0]["id"] if result.data else None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job match analysis failed: {str(e)}")