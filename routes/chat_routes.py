from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ai_service import ask_gemini
from auth import get_current_user
from database import get_db
from models import ChatMessage, Conversation, User
from schemas import (
    AIRequest,
    ConversationRequest,
    UpdateConversationRequest,
)

router = APIRouter()


# =====================================
# AI APIs
# =====================================

@router.post("/ask-ai")
def ask_ai(
    request: AIRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate Conversation
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # Fetch Previous Chat History
    chats = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == current_user.id,
            ChatMessage.conversation_id == request.conversation_id,
        )
        .order_by(ChatMessage.id.desc())
        .limit(10)
        .all()
    )

    # Build Prompt
    history_lines = [
        f"{chat.role}: {chat.message}"
        for chat in reversed(chats)
    ]

    history_lines.append(
        f"User: {request.question}"
    )

    prompt = "\n".join(history_lines)

    # Call Gemini
    try:
        answer = ask_gemini(prompt)

    except Exception as e:
        error_message = str(e)

        if "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        raise HTTPException(
            status_code=500,
            detail="Something went wrong with AI response.",
        )

    # Save User Message
    user_msg = ChatMessage(
        conversation_id=request.conversation_id,
        user_id=current_user.id,
        role="User",
        message=request.question,
    )

    # Save AI Response
    ai_msg = ChatMessage(
        conversation_id=request.conversation_id,
        user_id=current_user.id,
        role="AI",
        message=answer,
    )

    db.add_all([user_msg, ai_msg])
    db.commit()

    return {
        "email": current_user.email,
        "answer": answer,
    }


# =====================================
# Chat History APIs
# =====================================

@router.get("/chat-history/{conversation_id}")
def get_chat_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chats = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == current_user.id,
            ChatMessage.conversation_id == conversation_id,
        )
        .order_by(ChatMessage.id.asc())
        .all()
    )

    return chats


@router.delete("/chat-history/{chat_id}")
def delete_single_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.id == chat_id,
            ChatMessage.user_id == current_user.id,
        )
        .first()
    )

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    db.delete(chat)
    db.commit()

    return {
        "message": "Chat deleted successfully",
    }


# =====================================
# Conversation APIs
# =====================================

@router.post("/conversation")
def create_conversation(
    request: ConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = Conversation(
        user_id=current_user.id,
        title=request.title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
    }


@router.get("/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == current_user.id
        )
        .order_by(Conversation.id.desc())
        .all()
    )

    return conversations


@router.get("/conversation/{conversation_id}")
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation


@router.put("/conversation/{conversation_id}")
def update_conversation(
    conversation_id: int,
    request: UpdateConversationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    conversation.title = request.title

    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
        "message": "Conversation updated successfully",
    }


@router.delete("/conversation/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # If cascade delete is configured in models.py,
    # this will automatically remove all related messages.
    db.delete(conversation)
    db.commit()

    return {
        "message": "Conversation deleted successfully",
    }