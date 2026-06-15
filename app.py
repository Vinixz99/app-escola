from flask import Flask, render_template, request, send_from_directory, redirect
import os

app = Flask(__name__, template_folder='templates')

# ==========================================================================
# BANCO DE DADOS TEMPORÁRIO (Memória do Servidor)
# ==========================================================================
comunicados_db = []
proximo_comunicado_id = 1

# Nova estrutura de Lanche (Segunda a Sexta) com dados padrão editáveis
lanche_db = {
    "segunda": "Suco de maracujá e biscoito integral",
    "terca": "Fruta (banana/maçã) e iogurte",
    "quarta": "Arroz doce com canela",
    "quinta": "Sopa de legumes com frango",
    "sexta": "Suco de uva e bolo de cenoura"
}

# Nova estrutura de Calendário de Eventos
calendario_db = []
proximo_evento_id = 1

# Nova estrutura de Avaliações/Provas
provas_db = []
proximo_prova_id = 1


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
    return render_template('login.html')

@app.route('/login_processo', methods=['POST'])
def login_processo():
    perfil = request.form.get('perfil')
    usuario = request.form.get('username')
    senha = request.form.get('password')

    if perfil == 'diretor' and usuario == 'diretor@escola.com' and senha == '1234':
        return redirect('/dashboard_diretor')
    elif perfil == 'responsavel':
        return redirect('/dashboard')
    else:
        return redirect('/')


# ==========================================================================
# 2. DASHBOARDS PRINCIPAIS
# ==========================================================================
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard_diretor')
def dashboard_diretor():
    # Enviamos absolutamente TODOS os dados reais para o painel do diretor gerenciar
    return render_template(
        'dashboard_diretor.html', 
        lista_comunicados=comunicados_db,
        lanche=lanche_db,
        lista_eventos=calendario_db,
        lista_provas=provas_db
    )


# ==========================================================================
# 3. AÇÕES DO DIRETOR (GERENCIAMENTO REAL)
# ==========================================================================

# --- GERENCIAR COMUNICADOS ---
@app.route('/criar_comunicado', methods=['POST'])
def criar_comunicado():
    global proximo_comunicado_id
    tipo = request.form.get('tipo')
    titulo = request.form.get('titulo')
    mensagem = request.form.get('mensagem')

    badge_classe = "tipo-aviso"
    badge_texto = "Aviso Geral"
    if tipo == "Reuniões":
        badge_classe = "tipo-reuniao"
        badge_texto = "Reunião de Pais"
    elif tipo == "Avaliações":
        badge_classe = "tipo-prova"
        badge_texto = "Avaliação / Prova"

    novo_comunicado = {
        "id": proximo_comunicado_id,
        "tipo": tipo,
        "badge_classe": badge_classe,
        "badge_texto": badge_texto,
        "tempo": "Agora",
        "titulo": titulo,
        "mensagem": mensagem
    }
    comunicados_db.insert(0, novo_comunicado)
    proximo_comunicado_id += 1
    return redirect('/dashboard_diretor')

@app.route('/deletar_comunicado/<int:id>', methods=['POST'])
def deletar_comunicado(id):
    global comunicados_db
    comunicados_db = [c for c in comunicados_db if c.get('id') != id]
    return redirect('/dashboard_diretor')


# --- GERENCIAR LANCHE ESCOLAR ---
@app.route('/atualizar_lanche', methods=['POST'])
def atualizar_lanche():
    global lanche_db
    # Substitui os lanches pelos valores digitados pelo diretor
    lanche_db["segunda"] = request.form.get("segunda")
    lanche_db["terca"] = request.form.get("terca")
    lanche_db["quarta"] = request.form.get("quarta")
    lanche_db["quinta"] = request.form.get("quinta")
    lanche_db["sexta"] = request.form.get("sexta")
    return redirect('/dashboard_diretor')


# --- GERENCIAR CALENDÁRIO ---
@app.route('/criar_evento', methods=['POST'])
def criar_evento():
    global proximo_evento_id
    data = request.form.get('data')
    titulo = request.form.get('titulo')
    
    # Inverte a data padrão do HTML (AAAA-MM-DD) para o formato BR (DD/MM)
    data_br = "/".join(data.split("-")[1:3][::-1]) if data else ""

    novo_evento = {
        "id": proximo_evento_id,
        "data": data_br,
        "titulo": titulo
    }
    calendario_db.append(novo_evento)
    proximo_evento_id += 1
    return redirect('/dashboard_diretor')

@app.route('/deletar_evento/<int:id>', methods=['POST'])
def deletar_evento(id):
    global calendario_db
    calendario_db = [e for e in calendario_db if e.get('id') != id]
    return redirect('/dashboard_diretor')


# --- GERENCIAR AVALIAÇÕES/PROVAS ---
@app.route('/criar_prova', methods=['POST'])
def criar_prova():
    global proximo_prova_id
    disciplina = request.form.get('disciplina')
    conteudo = request.form.get('conteudo')
    data = request.form.get('data')
    
    data_br = "/".join(data.split("-")[1:3][::-1]) if data else ""

    nova_prova = {
        "id": proximo_prova_id,
        "disciplina": disciplina,
        "conteudo": conteudo,
        "data": data_br
    }
    provas_db.append(nova_prova)
    proximo_prova_id += 1
    return redirect('/dashboard_diretor')

@app.route('/deletar_prova/<int:id>', methods=['POST'])
def deletar_prova(id):
    global provas_db
    provas_db = [p for p in provas_db if p.get('id') != id]
    return redirect('/dashboard_diretor')


# ==========================================================================
# 4. ROTAS DO TOPO & FUNCIONALIDADES GERENCIAIS (CONTEÚDO DINÂMICO DOS PAIS)
# ==========================================================================
@app.route('/mais')
def mais(): return render_template('mais.html')

@app.route('/notificacoes')
def notificacoes(): return render_template('notificacoes.html')

@app.route('/calendario')
def calendario():
    # Passa a lista dinâmica de eventos criados pelo diretor
    return render_template('calendario.html', lista_eventos=calendario_db)

@app.route('/avaliacoes')
def avaliacoes():
    # Passa a lista dinâmica de provas criadas pelo diretor
    return render_template('avaliacoes.html', lista_provas=provas_db)

@app.route('/lanche')
def lanche():
    # Passa o dicionário de cardápios dinâmicos para a tela
    return render_template('lanche.html', lanche=lanche_db)

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

@app.route('/comunicados')
def comunicados():
    return render_template('comunicados.html', lista_comunicados=comunicados_db)


if __name__ == '__main__':
    app.run(debug=True, port=5000)