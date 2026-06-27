from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import settings

def dapatkan_analisis_dan_plan(scores: dict, total_score: int, risk_status: str, database_guidelines: str) -> dict:
    """
    Menembak Gemini API untuk mengunci keluaran JSON murni 
    berbasis kombinasi data ML dan rangkuman teks guideline dari Postgres.
    """
    raw_template = """You are the core AI Health Intelligence Engine for 'TreeHealthy'.
    Generate a professional medical synthesis and a highly tailored 7-day action plan based on these metrics:

    [PATIENT RISK PROFILE]
    - Overall Risk: {total_score}% ({risk_status})
    - Cardiovascular Risk: {tensi_score}%
    - Diabetes Risk: {gula_score}%
    - Stress & Physical Risk: {stress_score}%

    [POSTGRESQL INTERNAL GUIDELINES CONTEXT]
    {guidelines}

    STRICT OUTPUT RULES:
    Return ONLY a raw JSON object matching the keys below. Do not include markdown code block syntax (like ```json).

    REQUIRED SCHEMA:
    {{
    "ai_explanation": "Provide a 2-paragraph professional analysis in fluent medical English explaining WHY their risk factors are at these levels using the guidelines context.",
    "action_plan_7_days": [
        {{
        "hari": 1,
        "tasks": ["task 1", "task 2", "task 3", "task 4"]
        }}
    ]
    }}

    *CRITICAL*: Prioritize the highest risk factor. Since Cardiovascular risk is the highest at {tensi_score}%, ensure 60% of the daily tasks in 'action_plan_7_days' target blood pressure reduction, salt control, and stress relief."""

    prompt = PromptTemplate(
            template=raw_template,
            input_variables=["total_score", "risk_status", "tensi_score", "gula_score", "stress_score", "guidelines"]
        )

    llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2
        )

        # Rantai pipa LCEL
    chain = prompt | llm | JsonOutputParser()
        
    hasil_json = chain.invoke({
            "total_score": total_score,
            "risk_status": risk_status,
            "tensi_score": scores["tensi"],
            "gula_score": scores["gula"],
            "stress_score": scores["stress"],
            "guidelines": database_guidelines
        })
        
    return hasil_json