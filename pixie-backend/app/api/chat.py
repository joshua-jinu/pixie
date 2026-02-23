import uuid
from fastapi import APIRouter, HTTPException
from app.utils.schemas import ChatInput
from app.agent.agent import agent

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(payload: ChatInput):

    try:
        session_id = payload.session_id or str(uuid.uuid4())  # Generate a new session ID if not provided

        response = await agent.run(
            session_id=session_id,
            query=payload.query
        )

        return {"response": response, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))