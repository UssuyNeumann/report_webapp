from flask import Flask, render_template, request, redirect, session, flash, url_for


class Report:
    def __init__(self, nome, area, descricao=None):
        self.nome = nome
        self.area = area
        self.descricao = descricao


relatorio1 = Report('Relatório da Millenium Falcon', 'Star Wars', 'cargueira leve do modelo YT-1300f')
relatorio2 = Report('Relatório da Galactica', 'Battlestar Galactica', 'nave de guerra do modelo Jupiter')
relatorio3 = Report('Relatório da USS Enterprise', ' Star Trek', 'nave de exploração do modelo Constitution')
lista_relatorios = [relatorio1, relatorio2, relatorio3]   

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

usuario1 = Usuario('Han Solo','han@rebeldes.org', 'solo')
usuario2 = Usuario('Spock','spock@enterprise.org', 'spock')
usuario3 = Usuario('William Adama','adama@galatica.org', 'adama')

usuarios = {usuario1.email: usuario1, usuario2.email: usuario2, usuario3.email: usuario3}   


app = Flask(__name__)
app.secret_key = 'secreto' #chave_secreta_para_sessao

@app.route('/')
def report():
    return render_template('report.html', titulo='Relatórios de Naves', relatorios=lista_relatorios)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('form_novo.html', titulo='Novo Relatório')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    area = request.form['area']
    objeto_report = Report(nome, area)
    lista_relatorios.append(objeto_report)
    return redirect(url_for('report')) 

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            print('autenticar: ' + str(proxima_pagina))
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
