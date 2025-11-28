from flask import Flask, jsonify, Blueprint, request, current_app
from database import get_db_connection
from flask_bcrypt import Bcrypt
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    senha_digitada = data.get('Senha')

    if not email or not senha_digitada:
        return jsonify({"Erro": "Email e senha são obrigatórios"}), 400
    
    ############Lógia de Mock para desenvolvimento########################

    print(f"Tentando logar com {email} e {senha_digitada}")

    if email == "rafael.leal@neodent.com":
        hash_falso = bcrypt.generate_password_hash("Supergelo1!").decode('utf-8')

        usuario_encontrado = (999, hash_falso)
    else:
        usuario_encontrado = None
    
    try:
        if usuario_encontrado:
            id_usuario = usuario_encontrado[0]
            senha_hash_banco = usuario_encontrado[1]

            if bcrypt.check_password_hash(senha_hash_banco, senha_digitada):

                payload = {
                    'user_id': id_usuario,
                    'email': email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
                }

                secret_key = current_app.config.get('SECRET_KEY')

                token = jwt.encode(payload, secret_key, algorithm="HS256")

                return jsonify({
                    "Mensagem": "Login com sucesso!",
                    "token": token, 
                    "user_id": id_usuario
                    }), 200
        
        return jsonify({"Mensagem": "Email ou senha incorretos"}), 401
    
    except Exception as e:
        return jsonify({"erro": f"Erro interno {str(e)}"}), 500
    

    #######################################################################

    # conn = get_db_connection()
    # if not conn:
    #     return jsonify({"Erro": "Erro ao conectar ao banco de dados"}), 500
    
    # try:
    #     cursor = conn.cursor()

    #     query = "SELECT ID, Senha from apt_usuario WHERE Email = ? AND IsAtivo = 1"
    #     cursor.execute(query, (email,))

    #     usuario_encontrado = cursor.fetchone()

    #     if usuario_encontrado:
    #         id_usuario = usuario_encontrado[0]
    #         senha_hash_banco = usuario_encontrado[1]

    #         if bcrypt.check_password_hash(senha_hash_banco, senha_digitada):

    #             payload = {
    #                 'user_id': id_usuario,
    #                 'email': email,
    #                 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    #             }

    #             secret_key = current_app.config.get('SECRET_KEY')
    #             token = jwt.encode(payload, secret_key, algorithm="HS256")

    #             return jsonify({
    #                 "Mensagem": "Login com sucesso!",
    #                 "token": token, 
    #                 "user_id": id_usuario
    #                 }), 200

    #     return jsonify({"Mensagem": "Email ou senha incorretos"}), 401
    
    # except Exception as e:
    #     return jsonify({"erro": f"Erro interno {str(e)}"}), 500
    
    # finally:
    #     conn.close()