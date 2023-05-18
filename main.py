from flask import Flask, render_template, request, redirect, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from deta import Deta

app = Flask(__name__)
app.secret_key = '@bru123'

# Inicializar o Deta com sua chave de projeto
deta = Deta('b0aa59j8_9vXzwoimCQe5GZ8LTL6FXS7DMXDX9d47')

# Obter uma referência para a coleção no Deta.Space
jobs_db = deta.Base('jobs')

# Definir a senha de administrador (substitua pela sua senha real)
admin_password = 'admin123'
hashed_password = generate_password_hash(admin_password)

@app.route('/')
def index():
    # Obter todas as vagas de emprego
    jobs = jobs_db.fetch().items

    return render_template('index.html', jobs=jobs)

@app.route('/add_job', methods=['POST'])
def add_job():
    # Verificar se o usuário é um administrador
    if not check_admin():
        return redirect('/')

    title = request.form['title']
    description = request.form['description']
    company = request.form['company']
    location = request.form['location']

    job = {
        'title': title,
        'description': description,
        'company': company,
        'location': location
    }

    # Adicionar a nova vaga de emprego ao banco de dados
    jobs_db.put(job)

    return redirect('/admin')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Verificar se o usuário é um administrador
    if not check_admin():
        return redirect('/')

    # Obter todas as vagas de emprego
    jobs = jobs_db.fetch().items

    if request.method == 'POST':
        password = request.form['password']
        
        # Verificar se a senha do administrador está correta
        if check_password_hash(hashed_password, password):
            session['admin'] = True
            return render_template('admin.html', jobs=jobs)
        else:
            return redirect('/')

    return render_template('login.html')

@app.route('/api/jobs', methods=['GET'])
def api_jobs():
    # Obter todas as vagas de emprego como um JSON
    jobs = jobs_db.fetch().items

    return jsonify(jobs)

def check_admin():
    # Verificar se o usuário está logado como administrador
    if 'admin' in session:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run()
