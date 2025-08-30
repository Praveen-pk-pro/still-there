import os
import aiohttp
import json
from typing import Dict, Any

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

async def analyze_resume_with_deepseek(resume_content: str) -> Dict[str, Any]:
    """Analyze resume using DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        raise Exception("DeepSeek API key not configured")
    
    prompt = f"""
    Analyze this resume and provide:
    1. A score from 0-100
    2. Detailed analysis of strengths and weaknesses
    3. Specific improvements for ATS optimization
    4. An improved version of the resume
    
    Resume Content:
    {resume_content}
    
    Respond in JSON format with keys: score, analysis, improvements, improved_resume.
    """
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional resume analyst and career advisor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(DEEPSEEK_API_URL, headers=headers, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"DeepSeek API error: {response.status}")
                
                result = await response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Parse the JSON response
                return json.loads(content)
                
    except Exception as e:
        raise Exception(f"DeepSeek API call failed: {str(e)}")

async def generate_roadmap_with_deepseek(domain: str) -> Dict[str, Any]:
    """Generate learning roadmap using DeepSeek API"""
    prompt = f"""
    Create a detailed, step-by-step learning roadmap for someone wanting to become a {domain}.
    Include:
    1. Foundational skills and knowledge
    2. Intermediate topics and projects
    3. Advanced specialization areas
    4. Recommended resources and timelines
    
    Respond in JSON format with keys: overview, steps (array of objects with title, description, duration, resources).
    """
    
    # Similar implementation to analyze_resume_with_deepseek
    # ...

async def generate_cover_letter_with_deepseek(resume_content: str, job_details: str) -> str:
    """Generate cover letter using DeepSeek API"""
    prompt = f"""
    Based on the following resume and job details, write a professional cover letter:
    
    Resume: {resume_content}
    
    Job Details: {job_details}
    
    Create a compelling cover letter that highlights relevant skills and experience.
    """
    
    # Similar implementation to analyze_resume_with_deepseek
    # ...

# Add these functions to backend/utils/deepseek.py

async def analyze_job_match_with_deepseek(resume_content: str, desired_role: str) -> Dict[str, Any]:
    """Analyze job match using DeepSeek API"""
    prompt = f"""
    Analyze this resume against the desired role and provide:
    1. Matching job opportunities
    2. Skill gaps between the resume and the desired role
    3. Recommendations to bridge the skill gaps
    
    Resume Content:
    {resume_content}
    
    Desired Role: {desired_role}
    
    Respond in JSON format with keys: matches, skill_gaps, recommendations.
    """
    
    # Similar implementation to analyze_resume_with_deepseek
    # ...

async def generate_ats_resume_with_deepseek(resume_data: dict, domain: str) -> Dict[str, Any]:
    """Generate ATS-optimized resume using DeepSeek API"""
    prompt = f"""
    Create an ATS-optimized resume based on the following data for a {domain} role:
    
    Resume Data:
    {resume_data}
    
    Create a resume that will perform well with Applicant Tracking Systems.
    Include relevant keywords for the {domain} domain.
    
    Respond in JSON format with a complete resume structure.
    """
    
    # Similar implementation to analyze_resume_with_deepseek
    # ...