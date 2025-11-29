from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from src.routes.auth import auth_bp

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(base_dir, 'src', 'templates')
static_dir = os.path.join(base_dir, 'src', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'minha_chave_secreta')

app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/login-page")
def login_page():
    return render_template('login.html')

@app.route("/")
def home():
    return "<h1>Vá para o login: /login-page<h1>"

if __name__ == "__main__":
    app.run(debug=True)