from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/buscar', methods=['GET'])
def buscar_produto():
    termo = request.args.get('alimento')
    
    if not termo:
        return jsonify({"erro": "Nenhum alimento informado"}), 400

    # Usando o servidor global para testar se o BR está instável
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={termo}&search_simple=1&action=process&json=1"
    
    headers = {
        "User-Agent": "ScannerGuardiao/1.0 (contato: seuemail@exemplo.com)"
    }
    
    try:
        print(f"🔍 Tentando buscar: {termo}")
        resposta = requests.get(url, headers=headers, timeout=10)
        
        # Imprime o código de status no terminal (ex: 200, 403, 500)
        print(f"📡 Status da API: {resposta.status_code}")
        
        dados = resposta.json()
        
        # Verifica se a API retornou produtos
        if 'products' in dados:
            print(f"✅ Encontrados {len(dados['products'])} produtos.")
            return jsonify(dados)
        else:
            print("⚠️ API respondeu, mas não encontrou a chave 'products'.")
            return jsonify({"products": []})
            
    except Exception as e:
        # ISSO AQUI VAI NOS DAR A RESPOSTA DEFINITIVA NO TERMINAL
        print("❌ ERRO NO SERVIDOR:")
        print(str(e))
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)