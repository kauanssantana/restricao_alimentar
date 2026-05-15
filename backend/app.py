from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, requests, json, os

app = Flask(__name__)
app.secret_key = "nutricheck_secret_2026"
CORS(app, supports_credentials=True)
DB_PATH = 'nutricheck.db'

# --- UTILITÁRIOS DE BANCO DE DADOS ---
def query_db(query, args=(), one=False, commit=False):
    with sqlite3.connect(DB_PATH) as conn:
        # ATIVA O SUPORTE A CHAVES ESTRANGEIRAS (Obrigatório para o CASCADE funcionar na LGPD)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        if commit: conn.commit()
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv

def init_db():
    query_db('''CREATE TABLE IF NOT EXISTS alimentos (
        codigo_barras TEXT PRIMARY KEY, nome TEXT NOT NULL,
        ingredientes TEXT, alergenicos TEXT, imagem_url TEXT)''', commit=True)

    query_db('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL, telefone TEXT, senha TEXT NOT NULL,
        restricoes TEXT DEFAULT '[]', criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''', commit=True)

    # LGPD: ON DELETE CASCADE garante que se o usuário for deletado, o histórico vai junto
    query_db('''CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        produto_nome TEXT NOT NULL,
        produto_imagem TEXT,
        alergenicos TEXT DEFAULT '[]',
        seguro INTEGER DEFAULT 1,
        consultado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE)''', commit=True)
        
    # SEGURANÇA: Tabela de auditoria para mitigar Força Bruta
    query_db('''CREATE TABLE IF NOT EXISTS logs_login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_tentativa TEXT NOT NULL,
        ip_origem TEXT,
        sucesso INTEGER DEFAULT 0,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''', commit=True)

# --- ROTAS DE AUTENTICAÇÃO ---
@app.route('/api/cadastro', methods=['POST', 'OPTIONS'], strict_slashes=False)
def cadastrar():
    if request.method == 'OPTIONS': return jsonify({}), 200
    d        = request.json or {}
    nome     = str(d.get('nome', '')).strip()
    email    = str(d.get('email', '')).lower().strip()
    senha    = str(d.get('senha', ''))
    confirm  = str(d.get('confirmarSenha', ''))
    telefone = str(d.get('telefone', '') or '').strip()

    if not (nome and email and senha): return jsonify({"erro": "Campos obrigatórios em falta."}), 400
    if senha != confirm:               return jsonify({"erro": "As senhas não coincidem."}), 400
    if len(senha) < 8:                 return jsonify({"erro": "A senha deve ter pelo menos 8 caracteres."}), 400

    try:
        restricoes_lista = d.get('restricoes', [])
        if not isinstance(restricoes_lista, list): restricoes_lista = []
        query_db("INSERT INTO usuarios (nome, email, telefone, senha, restricoes) VALUES (?,?,?,?,?)",
                 (nome, email, telefone, generate_password_hash(senha), json.dumps(restricoes_lista)), commit=True)
        user = query_db("SELECT id, nome FROM usuarios WHERE email = ?", (email,), one=True)
        session['user_id']   = user['id']
        session['user_nome'] = user['nome']
        return jsonify({"mensagem": "Conta criada!", "usuario": {
            "id": user['id'], "nome": nome, "email": email, "restricoes": restricoes_lista
        }}), 201
    except sqlite3.IntegrityError:
        return jsonify({"erro": "E-mail já registado."}), 409
    except Exception as e:
        print("Erro no cadastro:", e)
        return jsonify({"erro": "Erro interno no servidor."}), 500

@app.route('/api/login', methods=['POST', 'OPTIONS'], strict_slashes=False)
def login():
    if request.method == 'OPTIONS': return jsonify({}), 200
    d     = request.json or {}
    email = str(d.get('email', '')).lower().strip()
    senha = str(d.get('senha', ''))
    ip    = request.remote_addr # Captura o IP de origem
    
    # 🛡️ DEFESA CONTRA FORÇA BRUTA: Verifica tentativas falhas nos últimos 15 min
    bloqueio = query_db('''SELECT COUNT(*) as tentativas FROM logs_login 
                           WHERE email_tentativa = ? AND sucesso = 0 
                           AND data_hora >= DATETIME('now', '-15 minutes')''', (email,), one=True)
                           
    if bloqueio and bloqueio['tentativas'] >= 5:
        return jsonify({"erro": "Muitas tentativas inválidas. Conta bloqueada por 15 minutos por segurança."}), 429

    u = query_db("SELECT * FROM usuarios WHERE email = ?", (email,), one=True)
    
    if u and check_password_hash(u['senha'], senha):
        # Registo de Sucesso
        query_db("INSERT INTO logs_login (email_tentativa, ip_origem, sucesso) VALUES (?, ?, 1)", (email, ip), commit=True)
        session['user_id']   = u['id']
        session['user_nome'] = u['nome']
        return jsonify({"mensagem": "Sucesso!", "usuario": {
            "id": u['id'], "nome": u['nome'], "email": u['email'],
            "telefone": u['telefone'], "restricoes": json.loads(u['restricoes'])
        }})
        
    # Registo de Falha
    query_db("INSERT INTO logs_login (email_tentativa, ip_origem, sucesso) VALUES (?, ?, 0)", (email, ip), commit=True)
    return jsonify({"erro": "Credenciais inválidas."}), 401

@app.route('/api/logout', methods=['POST', 'OPTIONS'], strict_slashes=False)
def logout():
    if request.method == 'OPTIONS': return jsonify({}), 200
    session.clear()
    return jsonify({"mensagem": "Logout efetuado."})

# --- ROTAS DE PERFIL E LGPD ---
@app.route('/api/perfil', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'], strict_slashes=False)
def gerenciar_perfil():
    if request.method == 'OPTIONS': return jsonify({}), 200
    uid = session.get('user_id')
    if not uid: return jsonify({"erro": "Não autenticado."}), 401

    if request.method == 'GET':
        u = query_db("SELECT id, nome, email, telefone, restricoes FROM usuarios WHERE id = ?", (uid,), one=True)
        return jsonify({"id": u['id'], "nome": u['nome'], "email": u['email'],
                        "telefone": u['telefone'], "restricoes": json.loads(u['restricoes'])})

    # 🛡️ ADEQUAÇÃO LGPD: Exclusão total de dados
    if request.method == 'DELETE':
        try:
            # 1. Apaga primeiro todo o histórico do utilizador (Garante a limpeza e contorna erro de FK)
            query_db("DELETE FROM historico WHERE usuario_id = ?", (uid,), commit=True)
            
            # 2. Depois, apaga o perfil do utilizador
            query_db("DELETE FROM usuarios WHERE id = ?", (uid,), commit=True)
            
            session.clear()
            return jsonify({"mensagem": "Conta e dados pessoais excluídos com sucesso."})
        except Exception as e:
            print("Erro ao excluir conta:", e)
            return jsonify({"erro": "Erro interno ao processar a exclusão."}), 500

    # Atualização de restrições (PUT)
    restricoes_lista = (request.json or {}).get('restricoes', [])
    if not isinstance(restricoes_lista, list): restricoes_lista = []
    query_db("UPDATE usuarios SET restricoes = ? WHERE id = ?", (json.dumps(restricoes_lista), uid), commit=True)
    return jsonify({"mensagem": "Restrições atualizadas!"})

@app.route('/api/perfil/dados', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def atualizar_dados():
    if request.method == 'OPTIONS': return jsonify({}), 200
    uid = session.get('user_id')
    if not uid: return jsonify({"erro": "Não autenticado."}), 401

    d        = request.json or {}
    nome     = str(d.get('nome', '')).strip()
    telefone = str(d.get('telefone', '') or '').strip()

    if not nome: return jsonify({"erro": "O nome não pode estar vazio."}), 400

    try:
        query_db("UPDATE usuarios SET nome = ?, telefone = ? WHERE id = ?", (nome, telefone, uid), commit=True)
        session['user_nome'] = nome
        return jsonify({"mensagem": "Dados atualizados!", "nome": nome, "telefone": telefone})
    except Exception as e:
        print("Erro ao atualizar dados:", e)
        return jsonify({"erro": "Erro interno."}), 500

@app.route('/api/perfil/senha', methods=['PUT', 'OPTIONS'], strict_slashes=False)
def atualizar_senha():
    if request.method == 'OPTIONS': return jsonify({}), 200
    uid = session.get('user_id')
    if not uid: return jsonify({"erro": "Não autenticado."}), 401

    d                = request.json or {}
    senha_atual      = str(d.get('senhaAtual', ''))
    nova_senha       = str(d.get('novaSenha', ''))
    confirmar        = str(d.get('confirmarNovaSenha', ''))

    if not (senha_atual and nova_senha): return jsonify({"erro": "Preencha todos os campos."}), 400
    if nova_senha != confirmar:          return jsonify({"erro": "As senhas não coincidem."}), 400
    if len(nova_senha) < 8:             return jsonify({"erro": "A nova senha deve ter pelo menos 8 caracteres."}), 400

    u = query_db("SELECT senha FROM usuarios WHERE id = ?", (uid,), one=True)
    if not check_password_hash(u['senha'], senha_atual):
        return jsonify({"erro": "Senha atual incorreta."}), 401

    try:
        query_db("UPDATE usuarios SET senha = ? WHERE id = ?", (generate_password_hash(nova_senha), uid), commit=True)
        return jsonify({"mensagem": "Senha alterada com sucesso!"})
    except Exception as e:
        print("Erro ao alterar senha:", e)
        return jsonify({"erro": "Erro interno."}), 500

# --- ROTAS DE HISTÓRICO ---
@app.route('/api/historico', methods=['GET', 'POST', 'OPTIONS'], strict_slashes=False)
def gerenciar_historico():
    if request.method == 'OPTIONS': return jsonify({}), 200
    uid = session.get('user_id')
    if not uid: return jsonify({"erro": "Não autenticado."}), 401

    if request.method == 'POST':
        d              = request.json or {}
        produto_nome   = str(d.get('produto_nome', '')).strip()
        produto_imagem = str(d.get('produto_imagem', '') or '')
        alergenicos    = json.dumps(d.get('alergenicos', []))
        seguro         = 1 if d.get('seguro', True) else 0

        if not produto_nome: return jsonify({"erro": "Nome do produto obrigatório."}), 400

        try:
            query_db("INSERT INTO historico (usuario_id, produto_nome, produto_imagem, alergenicos, seguro) VALUES (?,?,?,?,?)",
                     (uid, produto_nome, produto_imagem, alergenicos, seguro), commit=True)
            # Mantém apenas os últimos 10 por utilizador
            query_db('''DELETE FROM historico WHERE usuario_id = ? AND id NOT IN (
                        SELECT id FROM historico WHERE usuario_id = ?
                        ORDER BY consultado_em DESC LIMIT 10)''', (uid, uid), commit=True)
            return jsonify({"mensagem": "Consulta guardada!"}), 201
        except Exception as e:
            print("Erro ao salvar histórico:", e)
            return jsonify({"erro": "Erro interno."}), 500

    # GET — últimas 10 consultas
    registos = query_db('''SELECT produto_nome, produto_imagem, alergenicos, seguro, consultado_em
                           FROM historico WHERE usuario_id = ?
                           ORDER BY consultado_em DESC LIMIT 10''', (uid,))
    return jsonify([{
        "produto_nome":   r['produto_nome'],
        "produto_imagem": r['produto_imagem'],
        "alergenicos":    json.loads(r['alergenicos']),
        "seguro":         bool(r['seguro']),
        "consultado_em":  r['consultado_em']
    } for r in registos])

# --- MOTOR DE BUSCA ---
@app.route('/api/buscar', methods=['GET', 'OPTIONS'], strict_slashes=False)
def buscar():
    if request.method == 'OPTIONS': return jsonify({}), 200
    termo = request.args.get('alimento')
    tipo  = request.args.get('tipo', 'nome')
    if not termo: return jsonify({"erro": "Sem termo"}), 400

    # 1. Busca Local
    sql  = "SELECT * FROM alimentos WHERE codigo_barras = ?" if tipo == 'codigo' else \
           "SELECT * FROM alimentos WHERE nome COLLATE NOCASE = ? OR nome LIKE ? LIMIT 1"
    args = (termo,) if tipo == 'codigo' else (termo, f"%{termo}%")
    res  = query_db(sql, args, one=True)

    if res:
        return jsonify({"origem": "local", "products": [{
            "code": res['codigo_barras'], "product_name": res['nome'],
            "ingredients_text_pt": res['ingredientes'],
            "allergens_tags": res['alergenicos'].split(', ') if res['alergenicos'] else [],
            "image_url": res['imagem_url']
        }]})

    # 2. Busca API Externa
    try:
        url  = f"https://br.openfoodfacts.org/api/v2/product/{termo}" if tipo == 'codigo' else \
               f"https://br.openfoodfacts.org/api/v2/search?search_terms={termo.replace(' ', '%20')}"
        r    = requests.get(url, headers={"User-Agent": "NutriCheck/1.0"}, timeout=10).json()
        
        if tipo == 'codigo':
            prod = r.get('product')
        else:
            produtos_encontrados = r.get('products', [])
            prod = None
            termo_lower = termo.lower()
            for p in produtos_encontrados:
                nome_p = str(p.get('product_name', '')).lower()
                marca_p = str(p.get('brands', '')).lower()
                # Só aceita se o termo aparecer no nome ou na marca
                if termo_lower in nome_p or termo_lower in marca_p:
                    prod = p
                    break

        if prod and prod.get('product_name'):
            tags = prod.get('allergens_tags', [])
            query_db("INSERT OR IGNORE INTO alimentos VALUES (?,?,?,?,?)",
                     (prod.get('code'), prod.get('product_name'),
                      prod.get('ingredients_text_pt', 'N/A'),
                      ', '.join(tags), prod.get('image_url', '')), commit=True)
            return jsonify({"origem": "api", "products": [prod]})
    except Exception as e:
        print(f"🔴 Erro na API externa: {e}")

    return jsonify({"products": []})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))