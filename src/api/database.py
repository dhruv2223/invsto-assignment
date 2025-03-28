import psycopg2
from psycopg2.extras import RealDictCursor

DB_NAME = "invsto"
DB_USER = "postgres"
DB_PASSWORD = "Cdhruv@1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=RealDictCursor  # Ensures results are dictionaries
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None
