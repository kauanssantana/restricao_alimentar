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

    # 🚀 O SEGREDO: Usando a API V2 oficial, que não bloqueia aplicações!
    url = f"https://world.openfoodfacts.org/api/v2/search?search_terms={termo}"
    
    headers = {
        "User-Agent": "NutriCheckApp/1.0 - Projeto Academico"
    }
    
    try:
        print(f"🔍 Tentando buscar na API V2: {termo}")
        resposta = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 Status da API: {resposta.status_code}")
        
        if resposta.status_code != 200:
            return jsonify({"erro": "A base de dados oficial está indisponível no momento."}), 503
            
        dados = resposta.json()
        
        if 'products' in dados and len(dados['products']) > 0:
            print(f"✅ Encontrados {len(dados['products'])} produtos.")
            return jsonify(dados)
        else:
            print("⚠️ API respondeu, mas não encontrou produtos.")
            return jsonify({"products": []})
            
    except Exception as e:
        print("❌ ERRO NO SERVIDOR:")
        print(str(e))
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)