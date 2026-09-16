from pydantic import BaseModel

class RegisterRequest(BaseModel):
    role_id: int
    username: str
    email: str
    password: str
    full_name: str
