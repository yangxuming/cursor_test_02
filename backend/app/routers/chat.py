import json

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from ..auth import get_current_user
from ..database import get_db, async_session
from ..models import User, Conversation, Message
from ..services.deepseek import stream_chat

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: int


@router.post("/stream")
async def chat_stream(
    req: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == req.conversation_id,
            Conversation.user_id == user.id,
        )
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    user_message = Message(conversation_id=conversation.id, role="user", content=req.message)
    db.add(user_message)
    await db.flush()

    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    )
    history = result.scalars().all()

    messages = [{"role": m.role, "content": m.content} for m in history]

    await db.commit()

    async def event_generator():
        full_response = ""
        stream_error = None
        try:
            async for chunk in stream_chat(messages):
                full_response += chunk
                yield {"event": "message", "data": json.dumps({"content": chunk})}
        except Exception as e:
            stream_error = e
            yield {"event": "error", "data": json.dumps({"error": str(e)})}
        finally:
            if full_response:
                try:
                    async with async_session() as save_db:
                        assistant_message = Message(
                            conversation_id=conversation.id,
                            role="assistant",
                            content=full_response,
                        )
                        save_db.add(assistant_message)
                        await save_db.commit()
                except Exception:
                    pass

        if stream_error is None:
            yield {"event": "done", "data": json.dumps({"content": full_response})}

    return EventSourceResponse(event_generator())
