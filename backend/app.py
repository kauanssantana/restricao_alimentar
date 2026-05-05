from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests

app = Flask(__name__)
CORS(app)

def salvar_no_banco(codigo, nome, ingredientes, alergenicos, imagem):
    try:
        conexao = sqlite3.connect('nutricheck.db')
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alimentos (
                codigo_barras TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                ingredientes TEXT,
                alergenicos TEXT,
                imagem_url TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO alimentos (codigo_barras, nome, ingredientes, alergenicos, imagem_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (codigo, nome, ingredientes, alergenicos, imagem))
        
        conexao.commit()
        conexao.close()
    except Exception as e:
        print("Erro ao guardar no banco:", e)

@app.route('/api/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('alimento')
    tipo = request.args.get('tipo', 'nome')
    
    if not termo:
        return jsonify({"erro": "Nenhum termo"}), 400

    # ==========================================
    # PASSO 1: BUSCA INTELIGENTE NO BANCO LOCAL
    # ==========================================
    try:
        conexao = sqlite3.connect('nutricheck.db')
        cursor = conexao.cursor()
        resultado = None

        if tipo == 'codigo':
            cursor.execute("SELECT * FROM alimentos WHERE codigo_barras = ?", (termo,))
            resultado = cursor.fetchone()
        else:
            # 🧠 1. Tenta achar EXATAMENTE o nome digitado
            cursor.execute("SELECT * FROM alimentos WHERE nome COLLATE NOCASE = ?", (termo,))
            resultado = cursor.fetchone()
            
            if not resultado:
                # 🧠 2. Tenta achar a palavra ISOLADA (Ex: "Bis" sem pegar "Biscoito")
                cursor.execute("SELECT * FROM alimentos WHERE nome LIKE ? OR nome LIKE ? OR nome LIKE ?", 
                               (f"{termo} %", f"% {termo} %", f"% {termo}"))
                resultado = cursor.fetchone()
                
            if not resultado:
                # 🧠 3. Fallback genérico (O que fazíamos antes)
                cursor.execute("SELECT * FROM alimentos WHERE nome LIKE ?", ('%' + termo + '%',))
                resultado = cursor.fetchone()

        conexao.close()

        if resultado:
            print(f"⚡ Encontrado no Banco Local: {resultado[1]}")
            return jsonify({
                "origem": "local",
                "products": [{
                    "code": resultado[0],
                    "product_name": resultado[1],
                    "ingredients_text_pt": resultado[2],
                    "allergens_tags": resultado[3].split(', ') if resultado[3] else [],
                    "image_url": resultado[4]
                }]
            })
    except sqlite3.OperationalError:
        pass 

    # ==========================================
    # PASSO 2: SE NÃO TEM LOCAL, O PYTHON VAI À INTERNET
    # ==========================================
    print(f"🌐 Não tem localmente. O Python vai pesquisar '{termo}' à Open Food Facts...")
    headers = {"User-Agent": "NutriCheckApp/1.0 - Projeto"}
    termo_formatado = termo.replace(" ", "%20")
    
    if tipo == 'codigo':
        url = f"https://br.openfoodfacts.org/api/v2/product/{termo_formatado}"
    else:
        url = f"https://br.openfoodfacts.org/api/v2/search?search_terms={termo_formatado}"

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code != 200:
            return jsonify({"erro": "API externa indisponível"}), 503
        
        dados = resposta.json()
        produto_escolhido = None

        if tipo == 'codigo':
            if 'product' in dados:
                produto_escolhido = dados['product']
        else:
            if 'products' in dados and len(dados['products']) > 0:
                termo_lower = termo.lower()
                for p in dados['products']:
                    nome_p = p.get('product_name', '').lower()
                    marca_p = p.get('brands', '').lower()
                    # Garante que não pega algo totalmente errado na API externa também
                    if termo_lower in nome_p or termo_lower in marca_p:
                        produto_escolhido = p
                        break
        
        if produto_escolhido:
            codigo = produto_escolhido.get('code', '000000')
            nome = produto_escolhido.get('product_name', 'Nome Desconhecido')
            ingredientes = produto_escolhido.get('ingredients_text_pt', produto_escolhido.get('ingredients_text', 'Sem informação detalhada'))
            
            alergenicos_lista = produto_escolhido.get('allergens_tags', [])
            alergenicos_str = ', '.join(alergenicos_lista)
            imagem = produto_escolhido.get('image_url', '')

            salvar_no_banco(codigo, nome, ingredientes, alergenicos_str, imagem)

            return jsonify({
                "origem": "api",
                "products": [{
                    "code": codigo,
                    "product_name": nome,
                    "ingredients_text_pt": ingredientes,
                    "allergens_tags": alergenicos_lista,
                    "image_url": imagem
                }]
            })
        else:
            return jsonify({"products": []}) 
            
    except Exception as e:
        print("Erro na API Externa:", e)
        return jsonify({"erro": "Falha na comunicação com a API externa"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)