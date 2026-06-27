from fastapi import APIRouter, HTTPException
from sxhemas import ChatRequest, ChatResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

router = APIRouter(prefix="/api/v1/assistant", tags=["Chatbot Konsultasi"])

@router.post("/chat", response_model=ChatResponse)
async def obrolan_asisten_kesehatan(payload: ChatRequest):
    """
    Direct Chatbot menggunakan memori internal Gemini 
    untuk menjawab pertanyaan konsultasi bebas seputar PTM dari pengguna.
    """
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY)
        prompt_chat = f"You are a friendly medical assistant at TreeHealthy. Answer this query clearly and encouragement: {payload.pesan_user}"
        
        response = llm.invoke(prompt_chat)
        return {"jawaban_ai": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))