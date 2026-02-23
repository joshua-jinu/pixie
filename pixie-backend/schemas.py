from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal, List

class ChatInput(BaseModel):
    query: str
    session_id: Optional[str] = None