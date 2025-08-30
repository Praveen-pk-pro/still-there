from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from models.user import User, UserCreate
from utils.auth import get_password_hash, verify_password, create_access_token
from main import supabase

router = APIRouter()
security = HTTPBearer()

@router.post("/register")
async def register(user: UserCreate):
    # Check if user already exists
    existing_user = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    # Create user in Supabase
    new_user = {
        "email": user.email,
        "password_hash": hashed_password,
        "full_name": user.full_name
    }
    result = supabase.table("users").insert(new_user).execute()
    
    # Create JWT token
    token = create_access_token({"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(user: UserCreate):
    # Check if user exists
    result = supabase.table("users").select("*").eq("email", user.email).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    db_user = result.data[0]
    
    # Verify password
    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Create JWT token
    token = create_access_token({"sub": user.email})
    
    return {"access_token": token, "token_type": "bearer"}