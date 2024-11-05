from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('imc.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS imc_data (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Altura REAL NOT NULL,
            Peso REAL NOT NULL,
            Imc REAL NOT NULL,
            Categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


    init_db()

def calcular_imc(altura, peso):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        categoria = 'Abaixo do Peso'
    elif 18.5 <= imc < 24.9:
        categoria = 'Normal'
    else:
        categoria = 'Acima do Peso'
    return round(imc, 2), categoria


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    Nome = request.form['nome']
    Altura = float(request.form['altura'])
    Peso = float(request.form['peso'])

    imc, categoria = calcular_imc(Altura, Peso)

    conn = get_db_connection()
    conn.execute('INSERT INTO imc_data (Nome, Altura, Peso, Imc, Categoria) VALUES (?, ?, ?, ?, ?)',
                (Nome, Altura, Peso, imc, categoria))
    conn.commit()
    conn.close()

    return render_template('result.html', nome=Nome, imc=imc, categoria=categoria,)


@app.route('/dados')
def dados():
    conn = get_db_connection()
    dados = conn.execute('SELECT * FROM imc_data').fetchall()
    conn.close()
    return render_template('data.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)
    