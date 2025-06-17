from flask import Flask, request, session, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Permitir CORS com cookies

app.secret_key = 'chave_secreta_segura'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('ecobud.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Rota principal
@app.route('/')
def index():
    return 'API do EcoBud está rodando corretamente!'

# Registrar usuário
@app.route('/register', methods=['POST'])
def register():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha'].encode('utf-8')
    hashed = bcrypt.hashpw(senha, bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuario (nome, email, senha) VALUES (?, ?)', (nome, email, hashed))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return 'Email já cadastrado!', 400

    conn.close()
    return 'Cadastro realizado com sucesso!', 200

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha'].encode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(senha, user['senha']):
        session['usuario_id'] = user['id']
        return 'Login realizado com sucesso!', 200
    else:
        return 'Email ou senha inválidos!', 401

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return 'Logout realizado com sucesso!'

# Criar consumo
@app.route('/registrar_consumo', methods=['POST'])
def registrar_consumo():
    if 'usuario_id' not in session:
        return 'Não autorizado', 401

    usuario_id = session['usuario_id']
    mes = request.form['mes']
    ano = request.form['ano']
    energia = request.form['energia']
    agua = request.form['agua']
    plastico = request.form['plastico']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consumo (usuario_id, mes, ano, energia_kwh, agua_litros, plastico_kg)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (usuario_id, mes, ano, energia, agua, plastico))
    conn.commit()
    conn.close()

    return 'Consumo registrado com sucesso!'

# Visualizar consumo
@app.route('/monitoramento')
def monitoramento():
    if 'usuario_id' not in session:
        return 'Não autorizado', 401

    usuario_id = session['usuario_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM consumo WHERE usuario_id = ?', (usuario_id,))
    registros = cursor.fetchall()
    conn.close()

    return jsonify([dict(ix) for ix in registros])

# Registrar pontuação do quiz
@app.route('/registrar_quiz', methods=['POST'])
def registrar_quiz():
    if 'usuario_id' not in session:
        return 'Não autorizado', 401

    usuario_id = session['usuario_id']
    pontuacao = request.form['pontuacao']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz (usuario_id, pontuacao)
        VALUES (?, ?)
    ''', (usuario_id, pontuacao))
    conn.commit()
    conn.close()

    return 'Pontuação registrada com sucesso!'

# Ver pontuação do quiz
@app.route('/quiz')
def visualizar_quiz():
    if 'usuario_id' not in session:
        return 'Não autorizado', 401

    usuario_id = session['usuario_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quiz WHERE usuario_id = ?', (usuario_id,))
    registros = cursor.fetchall()
    conn.close()

    return jsonify([dict(ix) for ix in registros])

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
