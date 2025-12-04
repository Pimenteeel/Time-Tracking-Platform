from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
import os

from routes.auth import auth_bp
from routes.timesheet import timesheet_bp

load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'minha_chave_secreta')

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(timesheet_bp, url_prefix='/api')

@app.route("/login-page")
def login_page():
    return render_template('login.html')

@app.route("/")
def home():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)