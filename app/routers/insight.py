from fastapi import APIRouter, HTTPException
from database import get_db_connection
from typing import List
from sxhemas import ComplianceLog

router = APIRouter(prefix="/api/v1/insight", tags=["Dashboard Insights"])

@router.get("/compliance-history/{user_id}", response_model=List[ComplianceLog])
async def dapatkan_riwayat_grafik(user_id: int):
    """
    Mengambil data riwayat penyelesaian tugas harian dari tabel PostgreSQL 
    untuk disuplai ke komponen Recharts di frontend.
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Gagal menyambung ke database internal.")
        
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT to_char(logged_date, 'YYYY-MM-DD') as tanggal, total_tasks, completed_tasks, compliance_rate 
                   FROM user_compliance_logs WHERE user_id = %s ORDER BY logged_date ASC LIMIT 7;""",
                (user_id,)
            )
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()