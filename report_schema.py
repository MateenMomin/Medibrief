from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    extracted_text: str
    language: Optional[str] = "en"


class ReportResponse(BaseModel):
    id: int
    extracted_text: str
    summarized_text: Optional[str] = None
    language: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True