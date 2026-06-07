from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import User, ChatMessage
from schemas import AIRequest
from database import get_db
from auth import get_current_user
from ai_service import ask_gemini
router = APIRouter()

# =====================================
# AI API
# =====================================    

@router.post("/ask-ai")
def ask_ai(
    request: AIRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # 1. Fetch previous history BEFORE adding the incoming question
    chats = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.id.desc())
        .limit(10)
        .all()
    )    

    # 2. Build conversational history payload
    history_lines = [f"{chat.role}: {chat.message}" for chat in reversed(chats)]
    history_lines.append(f"User: {request.question}")
    prompt = "\n".join(history_lines)

    # 3. Call external AI Service
    try:
        answer = ask_gemini(prompt)
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Too many requests 😄 Please wait a little and try again."
            )
        raise HTTPException(
            status_code=500,
            detail="Something went wrong with AI response."
        ) 

    # 4. Batch database writes to a single commit transaction
    user_msg = ChatMessage(user_id=current_user.id, role="User", message=request.question)
    ai_msg = ChatMessage(user_id=current_user.id, role="AI", message=answer)
    
    db.add_all([user_msg, ai_msg])
    db.commit()
    
    return {
        "email": current_user.email,
        "answer": answer
    }


# =====================================
# Chat History APIs
# =====================================        

@router.get("/chat-history")
def chat_history(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).all()    


@router.delete("/chat-history/{chat_id}")
def delete_single_chat(
    chat_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    chat = db.query(ChatMessage).filter(
        ChatMessage.id == chat_id, 
        ChatMessage.user_id == current_user.id
    ).first()    

    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )

    db.delete(chat)
    db.commit()

    return {"message": "Chat deleted successfully"}


@router.delete("/chat-history")
def delete_all_chat(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).delete()
    db.commit()     

    return {"message": "Chats deleted successfully"}