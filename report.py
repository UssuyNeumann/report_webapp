from flask import Flask, render_template, request, redirect, session, flash


class Report:
    def __init__(self, nome, area, descricao=None):
        self.nome = nome
        self.area = area
        self.descricao = descricao


relatorio1 = Report('Relatório da Millenium Falcon', 'Star Wars', 'cargueira leve do modelo YT-1300f')
relatorio2 = Report('Relatório da Galactica', 'Battlestar Galactica', 'nave de guerra do modelo Jupiter')
relatorio3 = Report('Relatório da USS Enterprise', ' Star Trek', 'nave de exploração do modelo Constitution')
lista_relatorios = [relatorio1, relatorio2, relatorio3]   

app = Flask(__name__)
app.secret_key = 'secreto' #chave_secreta_para_sessao

@app.route('/')
def report():
    return render_template('report.html', titulo='Relatórios de Naves', relatorios=lista_relatorios)


@app.route('/novo')
def novo():
    return render_template('form_novo.html', titulo='Novo Relatório')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    area = request.form['area']
    objeto_report = Report(nome, area)
    lista_relatorios.append(objeto_report)
    return redirect('/') 

@app.route('/login')
def login():
    return render_template('login.html', titulo='Login')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if senha == 'admin':
        session['usuario_logado'] = usuario
        flash('Login realizado com sucesso!')
        return redirect('/')
    else:
        flash('Usuário ou senha inválidos!')
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Logout realizado com sucesso!')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
