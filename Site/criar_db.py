import sqlite3

conn = sqlite3.connect('ecobud.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS consumo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    energia_kwh REAL NOT NULL,
    agua_litros REAL NOT NULL,
    plastico_kg REAL NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    pontuacao INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
)
''')

conn.commit()
conn.close()

print("Banco de dados SQLite 'ecobud.db' criado com sucesso!")
