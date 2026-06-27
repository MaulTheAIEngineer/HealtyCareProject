import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings
import logging

logger = logging.getLogger("TreeHealthyAI")

def get_db_connection():
    """
    Buka koneksi ke PostgreSQL. 
    Menggunakan RealDictCursor agar hasil query otomatis berbentuk dictionary (JSON-ready).
    """
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error(f"Gagal koneksi ke database PostgreSQL: {e}")
        return None