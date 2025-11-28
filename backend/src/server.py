from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from routes.auth import auth_bp

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'minha_chave_secreta')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/")
def home():
    return "<h1>Rota: /auth/login<h1>"

if __name__ == "__main__":
    app.run(debug=True)