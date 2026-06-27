from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import scoring, insight, rag
import uvicorn

app = FastAPI(
    title="HealthyCare AI Backend - Monolithic Version",
    description="Core Engine AI untuk Platform TreeHealthy (Dicoding Capstone)",
    version="1.0.0"
)

# Set-up CORS agar aman ditembak lintas server oleh React/Express
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Satukan semua jalur pipa router ke dalam aplikasi utama
app.include_router(scoring.router)
app.include_router(insight.router)
app.include_router(rag.router)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to TreeHealthy AI Core API. All pipelines operating successfully."
    }

if __name__ == "__main__":
    # Jalankan server lokal di port 8000 dengan fitur auto-reload aktif
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)