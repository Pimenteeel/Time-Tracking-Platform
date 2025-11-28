import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    SERVIDOR = os.getenv('DB_SERVER')
    BANCO = os.getenv('DB_NAME')
    USUARIO_SQL = os.getenv('DB_USER')
    SENHA_SQL = os.getenv('DB_PASSWORD')

    str_conexao = f"DRIVER={DRIVER};SERVER={SERVIDOR};DATABASE={BANCO};UID={USUARIO_SQL};PWD={SENHA_SQL};"

    try:
        #Conexão com o banco: 
        conexao = pyodbc.connect(str_conexao)
        print("Conexão bem sucedida (Autenticação Windows)")
        return conexao

    except Exception as e:
        print(f"Erro ao conectar ou consultar: {e}")