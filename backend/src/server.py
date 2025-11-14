#from flask import Flask, request, jsonify
import pyodbc

#app = Flask(__name__)

def get_db_connection():
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    SERVIDOR = r'br02sqltc1.straumann.com\sql2019t'
    BANCO = 'pesq_desenv_test'

    str_conexao = f"{DRIVER}; SERVER = {SERVIDOR}; DATABASE = {BANCO}; Trust_Connection = yes;"

    try:
        #Conexão com o banco: 
        conexao = pyodbc.connect(str_conexao)
        print("Conexão bem sucedida (Autenticação Windows)")

        #Criação do cursor p/ teste:
        cursor = conexao.cursor()

        #Teste com consulta:
        cursor.execute("SELECT * FROM usuario")

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