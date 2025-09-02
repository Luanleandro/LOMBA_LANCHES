import psycopg2
from psycopg2.extras import RealDictCursor
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

def get_db_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        cursor_factory=RealDictCursor
    )
    return conn

# Inicializar tabela users
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE NOT NULL,
            login_code VARCHAR(6),
            code_expires_at TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()