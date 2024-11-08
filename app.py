from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imc.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class UserIMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peso = db.Column(db.Float, nullable=False)
    altura = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    classificacao = db.Column(db.String(50), nullable=False)

# Função para calcular IMC
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return imc

# Função para classificar o IMC
def classificar_imc(imc):
    if imc < 18.5:
        return 'Abaixo do peso'
    elif 18.5 <= imc < 24.9:
        return 'Peso normal'
    elif 25 <= imc < 29.9:
        return 'Acima do peso'
    else:
        return 'Obesidade'

# Função para salvar os dados no banco de dados SQLite
def salvar_no_banco(nome, peso, altura, imc, classificacao):
    conn = SQLAlchemy.connect('imc.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imc_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            peso REAL,
            altura REAL,
            imc REAL,
            classificacao TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO imc_data (nome, peso, altura, imc, classificacao)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, peso, altura, imc, classificacao))
    conn.commit()
    conn.close()

# Rota principal - Formulário para inserir dados
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        
        imc = calcular_imc(peso, altura)
        classificacao = classificar_imc(imc)
        
        salvar_no_banco(nome, peso, altura, imc, classificacao)
        
        return render_template('result.html', nome=nome, imc=imc, classificacao=classificacao)
    
    return render_template('index.html')

# Rota para exibir os dados armazenados no banco de dados
@app.route('/data')
def data():
    conn = SQLAlchemy.connect('imc.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM imc_data')
    dados = cursor.fetchall()
    conn.close()
    from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserIMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        weight = request.form.get('weight')
        height = request.form.get('height')

        if name and weight and height:
            try:
                weight = float(weight)
                height = float(height)

                imc = weight / (height ** 2)
                if imc < 18.5:
                    status = "Abaixo do peso"
                elif 18.5 <= imc <= 24.9:
                    status = "Peso normal"
                elif 25 <= imc <= 29.9:
                    status = "Sobrepeso"
                else:
                    status = "Obesidade"

                new_entry = UserIMC(name=name, weight=weight, height=height, imc=imc, status=status)
                db.session.add(new_entry)
                db.session.commit()

                return redirect(url_for('results'))
            except ValueError:
                print("Erro na conversão de peso ou altura.")
                return "Erro: Peso ou altura inválidos."
        else:
            print("Erro: Campos não preenchidos corretamente.")
            return "Erro: Campos não preenchidos corretamente."
    return render_template('index.html')

@app.route('/results')
def results():
    imc_records = UserIMC.query.all()
    return render_template('results.html', imc_records=imc_records)

if __name__== '_main_':
    app.run(port=5000, debug=True)
