from flask import Flask, jsonify, Blueprint, request
from database import get_db_connection
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    senha_digitada = data.get('Senha')

    if not email or not senha_digitada:
        return jsonify({"Erro": "Email e senha são obrigatórios"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"Erro": "Erro ao conectar ao banco de dados"}), 500
    
    try:
        cursor = conn.cursor()

        query = "SELECT Email, Senha from apt_usuario WHERE Email = ? AND IsAtivo = 1"
        cursor.execute(query, (email,))

        usuario_encontrado = cursor.fetchone()

        if usuario_encontrado:
            senha_hash_banco = usuario_encontrado[1]

            if bcrypt.check_password_hash(senha_hash_banco, senha_digitada):
                return jsonify({"Mensagem": "Login com sucesso!", "user": usuario_encontrado[0]}), 200         
        return jsonify({"Mensagem": "Email ou senha incorretos"}), 401
    
    except Exception as e:
        return jsonify({"erro": f"Erro interno {str(e)}"}), 500
    
    finally:
        conn.close()