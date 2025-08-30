from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class User(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # This is a placeholder. In a real implementation, you would:
    # 1. Verify the JWT token
    # 2. Extract user information from the token
    # 3. Return the user object
    
    # For now, we'll return a mock user
    return {"id": "user_id", "email": "user@example.com"}