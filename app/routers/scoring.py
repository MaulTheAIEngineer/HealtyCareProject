from fastapi import APIRouter, HTTPException
from sxhemas import ScoringRequest, CleanResponsePayload
from services.ml_service import prediksi_risk_scores
from services.gemini_service import dapatkan_analisis_dan_plan
from database import get_db_connection

router = APIRouter(prefix="/api/v1", tags=["Kuis & Scoring Engine"])

@router.post("/predict-risk-and-guidance", response_model=CleanResponsePayload)
async def hitung_dan_buat_planner(payload: ScoringRequest):
    # 1. Hitung skor via ML Service
    scores = prediksi_risk_scores(payload)
    
    total_score = int(round(sum(scores.values()) / 3))
    risk_status = "High Risk" if total_score >= 60 else "Moderate Risk" if total_score >= 30 else "Low Risk"
    
    # 2. Ambil teks regulasi penanganan dari PostgreSQL (Menggantikan fungsi RAG ChromaDB)
    guidelines_text = "Pedoman Umum Kemenkes: Jaga pola konsumsi pangan sehat, hindari rokok, batasi garam."
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Mengambil teks pedoman berdasarkan risiko tertinggi
                penyakit_target = "Hipertensi" if scores["tensi"] > scores["gula"] else "Diabetes"
                cursor.execute(
                    "SELECT content FROM medical_guidelines WHERE disease_type = %s LIMIT 1;", 
                    (penyakit_target,)
                )
                row = cursor.fetchone()
                if row:
                    guidelines_text = row["content"]
        finally:
            conn.close()

    # 3. Lempar ke Gemini untuk dapatkan payload penjelasan dan 7-day task checklist
    try:
        ai_result = dapatkan_analisis_dan_plan(scores, total_score, risk_status, guidelines_text)
        
        # Gabungkan data kalkulasi angka dan data teks dari AI
        response_ready = {
            "ptm_risk_score": total_score,
            "risk_status": risk_status,
            "tensi_pembuluh_darah": scores["tensi"],
            "gula_darah_diabetes": scores["gula"],
            "fisik_stress": scores["stress"],
            "ai_explanation": ai_result.get("ai_explanation", ""),
            "action_plan_7_days": ai_result.get("action_plan_7_days", [])
        }
        return response_ready
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")