from flask import Flask, request, jsonify
import pyodbc
import os
from dotenv import load_dotenv

app = Flask(__name__)
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

        #Criação do cursor p/ teste:
        cursor = conexao.cursor()

        #Teste com consulta:
        cursor.execute("SELECT * FROM apt_usuario")

        #Printar os resultados:
        linhas = cursor.fetchall()
        for linha in linhas:
            print(linha)

    except Exception as e:
        print(f"Erro ao conectar ou consultar: {e}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()
            print("Conexão fechada")

if __name__ == "__main__":
    get_db_connection()
    app.run(debug=True)