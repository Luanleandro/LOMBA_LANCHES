import psycopg2
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
import sys

# Conecta a um banco de dados padrão para poder criar ou apagar outro
def get_admin_connection():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database="postgres", # Conecta ao banco de dados 'postgres' padrão
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_PORT
        )
        conn.autocommit = True
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        sys.exit(1)

# Conecta ao seu banco de dados específico
def get_app_connection():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro: O banco de dados '{POSTGRES_DB}' não existe. Por favor, rode este script com a opção --create.")
        sys.exit(1)

def drop_database():
    print(f"Removendo o banco de dados '{POSTGRES_DB}'...")
    conn = get_admin_connection()
    cursor = conn.cursor()
    try:
        # Encerra todas as conexões ativas com o banco de dados
        cursor.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{POSTGRES_DB}' AND pid <> pg_backend_pid();")
        cursor.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB};")
        print("Banco de dados removido com sucesso.")
    except Exception as e:
        print(f"Erro ao remover o banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

def create_database():
    print(f"Criando o banco de dados '{POSTGRES_DB}'...")
    conn = get_admin_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB};")
        print("Banco de dados criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

def create_tables():
    print("Criando a tabela 'users'...")
    conn = get_app_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE NOT NULL,
                login_code VARCHAR(6),
                code_expires_at TIMESTAMP
            );
        """)
        conn.commit()
        print("Tabela 'users' criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            drop_database()
            create_database()
            create_tables()
            print("Processo de reinicialização concluído.")
        elif sys.argv[1] == "--create":
            create_database()
            create_tables()
            print("Processo de criação concluído.")
        elif sys.argv[1] == "--drop":
            drop_database()
            print("Banco de dados removido.")
        else:
            print("Comando inválido. Use --create, --reset ou --drop.")
    else:
        print("Nenhum argumento fornecido. Use --create, --reset ou --drop.")