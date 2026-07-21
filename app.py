from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='templates')

# ==========================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLite)
# ==========================================================================
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'escola.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================================================
# MODELOS DO BANCO DE DADOS (TABELAS)
# ==========================================================================
class Comunicado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    badge_classe = db.Column(db.String(50), nullable=False)
    badge_texto = db.Column(db.String(50), nullable=False)
    tempo = db.Column(db.String(20), default="Agora")
    titulo = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

class LancheSemana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segunda = db.Column(db.String(200), default="Suco de maracujá e biscoito integral")
    terca = db.Column(db.String(200), default="Fruta (banana/maçã) e iogurte")
    quarta = db.Column(db.String(200), default="Arroz doce com canela")
    quinta = db.Column(db.String(200), default="Sopa de legumes com frango")
    sexta = db.Column(db.String(200), default="Suco de uva e bolo de cenoura")

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disciplina = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data = db.Column(db.String(20), nullable=False)

def obter_ou_criar_lanche():
    lanche = LancheSemana.query.first()
    if not lanche:
        lanche = LancheSemana()
        db.session.add(lanche)
        db.session.commit()
    return lanche

# ==========================================================================
# 0. ARQUIVOS ESTÁTICOS
# ==========================================================================
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# ==========================================================================
# 1. FLUXO DE AUTENTICAÇÃO (LOGIN)
# ==========================================================================
@app.route('/')
def login():
    erro = request.args.get('erro')
    return render_template('login.html', erro=erro)

@app.route('/login_processo', methods=['POST'])
def login_processo():
    perfil = request.form.get('perfil')
    usuario = request.form.get('username')
    senha = request.form.get('password')

    if perfil == 'diretor' and usuario == 'diretor@escola.com' and senha == '1234':
        return redirect('/dashboard_diretor')
    elif perfil == 'professor' and usuario == 'professor@escola.com' and senha == '1234':
        return redirect('/dashboard_professor')
    elif perfil == 'responsavel':
        return redirect('/dashboard')
    else:
        return redirect(url_for('login', erro=1))

# ==========================================================================
# 2. DASHBOARDS PRINCIPAIS
# ==========================================================================
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard_professor')
def dashboard_professor():
    lista_provas = Prova.query.order_by(Prova.id.desc()).all()
    return render_template('dashboard_professor.html', lista_provas=lista_provas)

@app.route('/dashboard_diretor')
def dashboard_diretor():
    lista_comunicados = Comunicado.query.order_by(Comunicado.id.desc()).all()
    lanche_registro = obter_ou_criar_lanche()
    lista_eventos = Evento.query.all()
    lista_provas = Prova.query.all()

    lanche_dict = {
        "segunda": lanche_registro.segunda,
        "terca": lanche_registro.terca,
        "quarta": lanche_registro.quarta,
        "quinta": lanche_registro.quinta,
        "sexta": lanche_registro.sexta
    }

    return render_template(
        'dashboard_diretor.html', 
        lista_comunicados=lista_comunicados,
        lanche=lanche_dict,
        lista_eventos=lista_eventos,
        lista_provas=lista_provas
    )

# ==========================================================================
# 3. AÇÕES DO DIRETOR E PROFESSOR (GERENCIAMENTO VIA AJAX / FORM)
# ==========================================================================
@app.route('/criar_comunicado', methods=['POST'])
def criar_comunicado():
    tipo = request.form.get('tipo')
    titulo = request.form.get('titulo')
    mensagem = request.form.get('conteudo') 

    badge_classe = "tipo-aviso"
    badge_texto = "Aviso Geral"
    if tipo == "reuniao":
        badge_classe = "tipo-reuniao"
        badge_texto = "Reunião de Pais"
    elif tipo == "urgente":
        badge_classe = "tipo-urgente"
        badge_texto = "Urgente / Alerta"
    elif tipo == "evento":
        badge_classe = "tipo-evento"
        badge_texto = "Evento / Festa"

    novo_comunicado = Comunicado(
        tipo=tipo,
        badge_classe=badge_classe,
        badge_texto=badge_texto,
        titulo=titulo,
        mensagem=mensagem
    )
    db.session.add(novo_comunicado)
    db.session.commit()
    
    return jsonify({'status': 'sucesso', 'mensagem': 'Comunicado postado com sucesso!', 'id': novo_comunicado.id})

@app.route('/deletar_comunicado/<int:id>')
def deletar_comunicado(id):
    comunicado = Comunicado.query.get(id)
    if comunicado:
        db.session.delete(comunicado)
        db.session.commit()
    return redirect('/dashboard_diretor')

@app.route('/atualizar_cardapio', methods=['POST'])
def atualizar_cardapio():
    lanche_registro = obter_ou_criar_lanche()
    lanche_registro.segunda = request.form.get("segunda")
    lanche_registro.terca = request.form.get("terca")
    lanche_registro.quarta = request.form.get("quarta")
    lanche_registro.quinta = request.form.get("quinta")
    lanche_registro.sexta = request.form.get("sexta")
    db.session.commit()
    return redirect('/dashboard_diretor')

@app.route('/criar_evento', methods=['POST'])
def criar_evento():
    data = request.form.get('data')
    titulo = request.form.get('titulo')

    novo_evento = Evento(data=data, titulo=titulo)
    db.session.add(novo_evento)
    db.session.commit()
    
    return jsonify({'status': 'sucesso', 'mensagem': 'Evento adicionado ao calendário!', 'id': novo_evento.id})

@app.route('/deletar_evento/<int:id>')
def deletar_evento(id):
    evento = Evento.query.get(id)
    if evento:
        db.session.delete(evento)
        db.session.commit()
    return redirect('/dashboard_diretor')

@app.route('/criar_prova', methods=['POST'])
def criar_prova():
    disciplina = request.form.get('disciplina')
    conteudo = request.form.get('conteudo')
    data = request.form.get('data')

    nova_prova = Prova(disciplina=disciplina, conteudo=conteudo, data=data)
    db.session.add(nova_prova)
    db.session.commit()
    
    return jsonify({'status': 'sucesso', 'mensagem': 'Prova agendada com sucesso!', 'id': nova_prova.id})

@app.route('/deletar_prova/<int:id>')
def deletar_prova(id):
    prova = Prova.query.get(id)
    if prova:
        db.session.delete(prova)
        db.session.commit()
    return redirect('/dashboard_professor')

# ==========================================================================
# 4. ROTAS DO TOPO & CONTEÚDO DINÂMICO DOS PAIS (RESPONSÁVEIS)
# ==========================================================================
@app.route('/mais')
def mais(): return render_template('mais.html')
@app.route('/notificacoes')
def notificacoes(): return render_template('notificacoes.html')

@app.route('/comunicados')
def comunicados():
    lista_comunicados = Comunicado.query.order_by(Comunicado.id.desc()).all()
    return render_template('comunicados.html', lista_comunicados=lista_comunicados)

@app.route('/calendario')
def calendario():
    lista_eventos = Evento.query.all()
    return render_template('calendario.html', lista_eventos=lista_eventos)

@app.route('/avaliacoes')
def avaliacoes():
    lista_provas = Prova.query.order_by(Prova.id.desc()).all()
    return render_template('avaliacoes.html', lista_provas=lista_provas)

@app.route('/lanche')
def lanche():
    lanche_registro = obter_ou_criar_lanche()
    lanche_dict = {
        "segunda": lanche_registro.segunda,
        "terca": lanche_registro.terca,
        "quarta": lanche_registro.quarta,
        "quinta": lanche_registro.quinta,
        "sexta": lanche_registro.sexta
    }
    return render_template('lanche.html', lanche=lanche_dict)

@app.route('/boletim')
def boletim(): return render_template('boletim.html')

# ==========================================================================
# 5. OUTRAS ROTAS PADRÃO
# ==========================================================================
@app.route('/entrada_saida')
def entrada_saida(): return render_template('entrada_saida.html')
@app.route('/entrada_saida_historico')
def entrada_saida_historico(): return render_template('entrada_saida_historico.html')
@app.route('/qrcode')
def qrcode(): return render_template('qrcode.html')
@app.route('/perfil')
def perfil(): return render_template('perfil.html')
@app.route('/perfil_responsavel')
def perfil_responsavel(): return render_template('perfil_responsavel.html')
@app.route('/notas')
def notas(): return render_template('notas.html')
@app.route('/faltas')
def faltas(): return render_template('faltas.html')

# ==========================================================================
# 6. ROTAS DE ARQUIVOS DE MÍDIA / IMAGENS
# ==========================================================================
@app.route('/img/<path:filename>')
def serve_img(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'img'), filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco de dados verificado/criado com sucesso!")
    app.run(debug=True, port=5000)