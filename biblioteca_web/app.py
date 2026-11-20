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

# --- MODELOS DE USUÁRIO E AUTENTICAÇÃO ---
class FuncionarioUser(UserMixin):
    def __init__(self, id_funcionario, nome):
        self.id = id_funcionario
        self.nome = nome
        self.role = 'admin' # Adiciona o perfil de admin

    def get_id(self):
        return f"funcionario-{self.id}"

class UsuarioUser(UserMixin):
    def __init__(self, cpf, nome):
        self.id = cpf
        self.nome = nome
        self.role = 'usuario' # Adiciona o perfil de usuário

    def get_id(self):
        return f"usuario-{self.id}"

@login_manager.user_loader
def load_user(user_id_str):
    try:
        tipo, user_id = user_id_str.split('-', 1)
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        if tipo == 'funcionario':
            cursor.execute("SELECT ID_funcionario, nome FROM Funcionario WHERE ID_funcionario = %s", (user_id,))
            func = cursor.fetchone()
            if func:
                return FuncionarioUser(func['ID_funcionario'], func['nome'])
        elif tipo == 'usuario':
            cursor.execute("SELECT CPF, nome FROM Usuario WHERE CPF = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return UsuarioUser(user['CPF'], user['nome'])
    except Exception as e:
        print(f"Erro ao carregar usuário: {e}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
    return None

# --- DECORADOR PARA VERIFICAR PERMISSÃO DE ADMIN ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Acesso negado. Esta área é restrita para administradores.", "danger")
            return redirect(url_for('portal_acervo_publico'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROTAS DE AUTENTICAÇÃO E PÚBLICAS ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        # Tenta fazer login como funcionário
        cursor.execute("SELECT * FROM Funcionario WHERE email = %s", (email,))
        func = cursor.fetchone()
        if func and func['senha'] == senha:
            user = FuncionarioUser(func['ID_funcionario'], func['nome'])
            login_user(user)
            conn.close()
            return redirect(url_for('index'))

        # Se não for funcionário, tenta como usuário
        cursor.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
        user_comum = cursor.fetchone()
        conn.close()
        if user_comum and user_comum['senha'] == senha:
            user = UsuarioUser(user_comum['CPF'], user_comum['nome'])
            login_user(user)
            return redirect(url_for('portal_acervo_publico'))

        flash('Credenciais inválidas. Verifique seu e-mail e senha.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# --- ROTAS DO PAINEL DE ADMIN ---
@app.route('/')
@login_required
@admin_required
def index():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) as total FROM Usuario")
        total_usuarios = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM Item_acervo")
        total_itens = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM Emprestimo WHERE status = 'Ativo'")
        emprestimos_ativos = cursor.fetchone()['total']
        return render_template('index.html', total_usuarios=total_usuarios, total_itens=total_itens, emprestimos_ativos=emprestimos_ativos)
    except Exception as e:
        flash(f"Erro ao carregar estatísticas: {str(e)}", "danger")
        return render_template('index.html')
    finally:
        conn.close()

# --- ROTAS DO PORTAL DO USUÁRIO ---
@app.route('/portal/acervo')
@login_required
def portal_acervo_publico():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        termo_busca = request.args.get('busca', '')
        query = "SELECT * FROM Item_acervo WHERE titulo LIKE %s"
        cursor.execute(query, (f'%{termo_busca}%',))
        itens = cursor.fetchall()
        return render_template('portal_acervo.html', itens=itens, termo_busca=termo_busca)
    except Exception as e:
        flash(f"Erro ao carregar o acervo: {e}", "danger")
        return render_template('portal_acervo.html', itens=[])
    finally:
        conn.close()

@app.route('/portal/meus_emprestimos')
@login_required
def portal_meus_emprestimos():
    if current_user.role != 'usuario':
        return abort(403)
    
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT E.data_emprest, E.data_dev, E.status, E.multa, I.titulo
            FROM Emprestimo E
            JOIN Movimentacao M ON E.ID_emprestimo = M.ID_emprestimo
            JOIN Item_acervo I ON M.ID_item = I.ID_item
            WHERE E.CPF = %s AND M.tipo = 'Emprestado'
            ORDER BY E.data_emprest DESC
        """
        cursor.execute(query, (current_user.id,))
        emprestimos = cursor.fetchall()
        return render_template('portal_meus_emprestimos.html', emprestimos=emprestimos)
    except Exception as e:
        flash(f"Erro ao carregar seus empréstimos: {e}", "danger")
        return render_template('portal_meus_emprestimos.html', emprestimos=[])
    finally:
        conn.close()