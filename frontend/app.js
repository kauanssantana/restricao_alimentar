const codigoInput = document.getElementById('codigoInput');
const buscarBtn = document.getElementById('buscarBtn');
const resultadoDiv = document.getElementById('resultado');

async function buscarProduto() {
    const termoBusca = codigoInput.value.trim();

    if (!termoBusca) {
        resultadoDiv.innerHTML = '<p style="color: red;">Por favor, digite o nome de um alimento.</p>';
        return;
    }

    resultadoDiv.innerHTML = '<p>Buscando na base de dados...</p>';

    // Prepara o texto digitado para virar formato de link com segurança
    const termoCodificado = encodeURIComponent(termoBusca);

    
    // A URL agora aponta para o seu servidor local na porta 5000
    const apiUrl = `http://127.0.0.1:5000/api/buscar?alimento=${termoCodificado}`;

    try {
        const resposta = await fetch(apiUrl);
        const dados = await resposta.json();

        // Verifica se a API retornou a lista de produtos e se ela não está vazia
        if (dados.products && dados.products.length > 0) {
            
            // Pegamos apenas o PRIMEIRO produto da lista (índice 0)
            const produto = dados.products[0];
            
            const nomeProduto = produto.product_name || "Nome desconhecido";
            const ingredientes = produto.ingredients_text_pt || produto.ingredients_text || "Sem informações de ingredientes.";
            const imagem = produto.image_url || ""; 
            
            const alergenicos = produto.allergens_tags && produto.allergens_tags.length > 0 
                ? produto.allergens_tags.join(', ') 
                : "Nenhuma tag de alergênico registrada.";

            resultadoDiv.innerHTML = `
                <h3>✅ ${nomeProduto}</h3>
                ${imagem ? `<img src="${imagem}" alt="${nomeProduto}" style="max-width: 150px; border-radius: 8px;">` : ''}
                <p><strong>⚠️ Alergênicos Mapeados:</strong> ${alergenicos}</p>
                <p><strong>🔍 Ingredientes:</strong> ${ingredientes}</p>
            `;
            
        } else {
            resultadoDiv.innerHTML = '<p style="color: red;">❌ Nenhum produto encontrado com esse nome.</p>';
        }
        
    } catch (erro) {
        console.error("Erro de conexão com a API:", erro);
        resultadoDiv.innerHTML = '<p style="color: red;">❌ Erro ao conectar com o servidor. Verifique o console (F12).</p>';
    }
}

buscarBtn.addEventListener('click', buscarProduto);