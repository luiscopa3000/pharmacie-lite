from pydantic import BaseModel
from typing import Optional, Dict

class ErrorData(BaseModel):
    type: str
    code: Optional[str] = None
    details: Optional[Dict] = None

class ErrorResponse(BaseModel):
    message: str
    data: ErrorData