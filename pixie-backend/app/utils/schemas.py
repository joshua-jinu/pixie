from pydantic import BaseModel, Field
from typing import Optional

class ChatInput(BaseModel):
    query: str
    session_id: Optional[str] = None