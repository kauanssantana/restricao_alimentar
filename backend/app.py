from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, requests, json

app = Flask(__name__)
app.secret_key = "nutricheck_secret_2026"

# Configuração CORS permitindo envio de credenciais (cookies de sessão)
CORS(app, supports_credentials=True)
DB_PATH = 'nutricheck.db'

# --- UTILITÁRIOS DE BANCO DE DADOS ---
def query_db(query, args=(), one=False, commit=False):
    with sqlite3.connect(DB_PATH) as conn:
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

# --- ROTAS DE AUTENTICAÇÃO E PERFIL ---
@app.route('/api/cadastro', methods=['POST', 'OPTIONS'], strict_slashes=False)
def cadastrar():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    d = request.json or {}
    
    # FORÇANDO OS TIPOS (STR) PARA EVITAR O INTERFACE ERROR DO SQLITE
    nome = str(d.get('nome', '')).strip()
    email = str(d.get('email', '')).lower().strip()
    senha = str(d.get('senha', ''))
    confirm = str(d.get('confirmarSenha', ''))
    telefone = str(d.get('telefone', '') or '').strip()
    
    if not (nome and email and senha): 
        return jsonify({"erro": "Campos obrigatórios em falta."}), 400
    if senha != confirm: 
        return jsonify({"erro": "As senhas não coincidem."}), 400
    if len(senha) < 6: 
        return jsonify({"erro": "Senha muito curta."}), 400

    try:
        # Garantindo que as restrições sejam uma lista antes do JSON Dumps
        restricoes_lista = d.get('restricoes', [])
        if not isinstance(restricoes_lista, list):
            restricoes_lista = []
            
        senha_hash = generate_password_hash(senha)
        restricoes_json = json.dumps(restricoes_lista)
        
        # Agora a injeção é 100% segura
        query_db("INSERT INTO usuarios (nome, email, telefone, senha, restricoes) VALUES (?,?,?,?,?)",
                 (nome, email, telefone, senha_hash, restricoes_json), commit=True)
        
        user = query_db("SELECT id, nome FROM usuarios WHERE email = ?", (email,), one=True)
        session['user_id'] = user['id']
        session['user_nome'] = user['nome']
        
        return jsonify({"mensagem": "Conta criada!", "usuario": {"id": user['id'], "nome": nome, "email": email, "restricoes": restricoes_lista}}), 201
    
    except sqlite3.IntegrityError: 
        return jsonify({"erro": "E-mail já registado."}), 409
    except Exception as e:
        print("Erro interno na hora de cadastrar:", e)
        return jsonify({"erro": "Erro interno no servidor."}), 500

@app.route('/api/login', methods=['POST', 'OPTIONS'], strict_slashes=False)
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    d = request.json or {}
    email = str(d.get('email', '')).lower().strip()
    senha = str(d.get('senha', ''))

    u = query_db("SELECT * FROM usuarios WHERE email = ?", (email,), one=True)
    
    if u and check_password_hash(u['senha'], senha):
        session['user_id'] = u['id']
        session['user_nome'] = u['nome']
        return jsonify({"mensagem": "Sucesso!", "usuario": {"id": u['id'], "nome": u['nome'], "restricoes": json.loads(u['restricoes'])}})
    
    return jsonify({"erro": "Credenciais inválidas."}), 401

@app.route('/api/logout', methods=['POST', 'OPTIONS'], strict_slashes=False)
def logout():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    session.clear()
    return jsonify({"mensagem": "Logout efetuado."})

@app.route('/api/perfil', methods=['GET', 'PUT', 'OPTIONS'], strict_slashes=False)
def gerenciar_perfil():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    uid = session.get('user_id')
    if not uid: return jsonify({"erro": "Não autenticado."}), 401
    
    if request.method == 'GET':
        u = query_db("SELECT id, nome, email, restricoes FROM usuarios WHERE id = ?", (uid,), one=True)
        return jsonify({"id": u['id'], "nome": u['nome'], "restricoes": json.loads(u['restricoes'])})
    
    restricoes_lista = request.json.get('restricoes', [])
    if not isinstance(restricoes_lista, list):
        restricoes_lista = []
        
    restricoes_json = json.dumps(restricoes_lista)
    query_db("UPDATE usuarios SET restricoes = ? WHERE id = ?", (restricoes_json, uid), commit=True)
    return jsonify({"mensagem": "Atualizado!"})

# --- MOTOR DE BUSCA (LOCAL + API) ---
@app.route('/api/buscar', methods=['GET', 'OPTIONS'], strict_slashes=False)
def buscar():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    termo = request.args.get('alimento')
    tipo = request.args.get('tipo', 'nome')
    if not termo: return jsonify({"erro": "Sem termo"}), 400

    # 1. Busca Local Otimizada
    sql = "SELECT * FROM alimentos WHERE codigo_barras = ?" if tipo == 'codigo' else \
          "SELECT * FROM alimentos WHERE nome COLLATE NOCASE = ? OR nome LIKE ? LIMIT 1"
    args = (termo,) if tipo == 'codigo' else (termo, f"%{termo}%")
    res = query_db(sql, args, one=True)

    if res:
        return jsonify({"origem": "local", "products": [{
            "code": res['codigo_barras'], "product_name": res['nome'], "ingredients_text_pt": res['ingredientes'],
            "allergens_tags": res['alergenicos'].split(', ') if res['alergenicos'] else [], "image_url": res['imagem_url']
        }]})

    # 2. Busca API Externa
    try:
        url = f"https://br.openfoodfacts.org/api/v2/product/{termo}" if tipo == 'codigo' else \
              f"https://br.openfoodfacts.org/api/v2/search?search_terms={termo.replace(' ', '%20')}"
        r = requests.get(url, headers={"User-Agent": "NutriCheck/1.0"}, timeout=10).json()
        prod = r.get('product') if tipo == 'codigo' else (r.get('products', [{}])[0])
        
        if prod and prod.get('product_name'):
            tags = prod.get('allergens_tags', [])
            query_db("INSERT OR IGNORE INTO alimentos VALUES (?,?,?,?,?)",
                     (prod.get('code'), prod.get('product_name'), prod.get('ingredients_text_pt', 'N/A'), ', '.join(tags), prod.get('image_url', '')), commit=True)
            return jsonify({"origem": "api", "products": [prod]})
    except Exception as e:
        # A IDENTAÇÃO FOI CORRIGIDA AQUI!
        print(f"🔴 Erro na API externa: {e}")

    # E O RETURN FOI CORRIGIDO AQUI!
    return jsonify({"products": []})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)