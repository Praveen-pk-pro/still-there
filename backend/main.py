from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from supabase import create_client, Client
import os
from dotenv import load_dotenv

from routes import auth, resume, roadmap, cover_letter, job_match, ats_resume

load_dotenv()

app = FastAPI(title="Career Compass API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(roadmap.router, prefix="/roadmap", tags=["roadmap"])
app.include_router(cover_letter.router, prefix="/cover-letter", tags=["cover-letter"])
app.include_router(job_match.router, prefix="/job-match", tags=["job-match"])
app.include_router(ats_resume.router, prefix="/ats-resume", tags=["ats-resume"])

@app.get("/")
async def root():
    return {"message": "Career Compass API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}