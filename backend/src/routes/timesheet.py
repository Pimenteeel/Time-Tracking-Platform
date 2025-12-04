from flask import Blueprint, request, jsonify
from database import get_db_connection
from datetime import datetime, timedelta

timesheet_bp = Blueprint('timesheet', __name__)

@timesheet_bp.route('/pilares', methods=['GET'])
def get_pilares():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Pilar, NomePilar FROM apt_pilares WHERE IsAtivo = 1")
        pilares = cursor.fetchall()

        lista = [{'id': row[0], 'nome': row[1]} for row in pilares]
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()

@timesheet_bp.route('/projetos/<int:pilar_id>', methods=['GET'])
def get_projetos(pilar_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT ID_Projeto, NomeProjeto FROM apt_projetos WHERE fk_ID_Pilar = ? AND IsAtivo = 1"
        cursor.execute(query, (pilar_id,))
        projetos = cursor.fetchall()

        lista = [{'id': row[0], 'nome': row[1]} for row in projetos]
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        conn.close()

@timesheet_bp.route('/salvar', methods=['POST'])
def salvar_apontamento():
    data = request.get_json()

    user_id = data.get('user_id')
    projeto_id = data.get('projeto_id')
    descricao = data.get('observacao')
    inicio_iso = data.get('inicio')
    fim_iso = data.get('fim')

    if not user_id or not projeto_id or not inicio_iso or not fim_iso:
        return jsonify({"erro": "Dados incompletos."}), 400
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        dt_inicio_utc = datetime.fromisoformat(inicio_iso.replace('Z', ''))
        dt_fim_utc = datetime.fromisoformat(fim_iso.replace('Z', ''))

        dt_inicio = dt_inicio_utc - timedelta(hours=3)
        dt_fim = dt_fim_utc - timedelta(hours=3)

        query = """
            INSERT INTO apt_apontamentos 
            (Descricao, Data_Inicio, Data_Fim, fk_ID_Usuario, fk_ID_Projeto)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (descricao, dt_inicio, dt_fim, user_id, projeto_id))
        conn.commit()

        return jsonify({"Mensagem": "Apontamento salvo!"}), 201
    except Exception as e:
        print(e)
        return jsonify({"Erro": f"Erro no banco: {str(e)}"}), 500
    finally:
        conn.close()
