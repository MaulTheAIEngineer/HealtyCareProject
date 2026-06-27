import joblib
import numpy as np
import logging

logger = logging.getLogger("TreeHealthyAI")

try:
    # Memuat model Random Forest Multi-Output
    model_random_forest = joblib.load("./model_rf.pkl")
except Exception as e:
    logger.warning(f"File model_rf.pkl tidak ditemukan, memakai fallback simulasi. Error: {e}")
    model_random_forest = None

def prediksi_risk_scores(request_data) -> dict:
    """
    Ekstrak 11 jawaban kuis, ubah jadi matriks, 
    lalu hitung nilai probabilitas desimal untuk 3 label target.
    """
    if model_random_forest is not None:
        try:
            # Contoh manipulasi array input berdasarkan skema fitur kalian
            # Gabungkan variabel demografi (usia, gender, bmi) + 11 jawaban kuis
            fitur_lengkap = [request_data.usia, request_data.jenis_kelamin, request_data.bmi] + request_data.jawaban_kuis
            input_matrix = np.array([fitur_lengkap])
            
            # Prediksi Multi-Output menghasilkan list array probabilitas per kelas
            prob = model_random_forest.predict_proba(input_matrix)
            
            tensi = int(round(prob[0][0][1] * 100))
            gula = int(round(prob[1][0][1] * 100))
            stress = int(round(prob[2][0][1] * 100))
            
            return {"tensi": tensi, "gula": gula, "stress": stress}
        except Exception as e:
            logger.error(f"Gagal kalkulasi model ML .pkl: {e}")
            
    # Fallback angka simulasi agar Dzikri tetap bisa testing UI frontend
    return {"tensi": 67, "gula": 38, "stress": 14}