# Importações necessárias do Flask e bibliotecas auxiliares
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import mysql.connector
import os
from datetime import date, timedelta
from functools import wraps
 
# Instanciação do app Flask e configuração da chave secreta para sessões
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave-dev-local')

# --- CONSTANTES DA APLICAÇÃO ---
VALOR_MULTA_DIARIA = 0.50 # Define o valor da multa por dia de atraso

# Configuração do gerenciador de login do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça o login para acessar esta página."
login_manager.login_message_category = "info"

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def conectar():
    """Estabelece conexão com o banco de dados MySQL hospedado no Railway."""
    return mysql.connector.connect(
        host=os.environ.get('MYSQLHOST'),         # Endereço fornecido pelo Railway
        user=os.environ.get('MYSQLUSER'),         # Usuário (geralmente root)
        password=os.environ.get('MYSQLPASSWORD'), # Sua senha do Railway
        database=os.environ.get('MYSQLDATABASE'), # Nome do banco (geralmente railway)
        port=int(os.environ.get('MYSQLPORT', 3306)) # Porta de conexão
    )