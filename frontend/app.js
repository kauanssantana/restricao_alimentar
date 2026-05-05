// Selecionando elementos da interface
const codigoInput = document.getElementById('codigoInput');
const buscarBtn = document.getElementById('buscarBtn');
const resultadoDiv = document.getElementById('resultado');
const btnNome = document.getElementById('btnNome');
const btnCodigo = document.getElementById('btnCodigo');

// Variável para saber qual tipo de busca o usuário quer fazer
let tipoBuscaAtual = 'nome'; // Pode ser 'nome' ou 'codigo'

// Lógica de troca do Toggle (Nome vs Código de Barras)
btnNome.addEventListener('click', () => {
    tipoBuscaAtual = 'nome';
    btnNome.classList.add('ativo');
    btnCodigo.classList.remove('ativo');
    codigoInput.placeholder = "Ex: biscoito recheado";
    codigoInput.value = ""; // Limpa o campo
});

btnCodigo.addEventListener('click', () => {
    tipoBuscaAtual = 'codigo';
    btnCodigo.classList.add('ativo');
    btnNome.classList.remove('ativo');
    codigoInput.placeholder = "Ex: 7622300990732";
    codigoInput.value = ""; // Limpa o campo
});

// Lógica principal de busca conectada ao nosso Back-end (Flask)
async function buscarProduto() {
    const termoBusca = codigoInput.value.trim();

    if (!termoBusca) {
        resultadoDiv.innerHTML = '<p style="color: red; text-align: center;">Por favor, digite algo para buscar.</p>';
        return;
    }

    resultadoDiv.innerHTML = '<p style="text-align: center;">Buscando na base de dados...</p>';

    // Por enquanto, nosso back-end atende tudo na mesma rota.
    // Futuramente, podemos separar a lógica de código vs nome lá no Python.
    const termoCodificado = encodeURIComponent(termoBusca);
    const apiUrl = `http://127.0.0.1:5000/api/buscar?alimento=${termoCodificado}`;

    try {
        const resposta = await fetch(apiUrl);
        const dados = await resposta.json();

        if (dados.products && dados.products.length > 0) {
            const produto = dados.products[0];
            
            const nomeProduto = produto.product_name || "Nome desconhecido";
            const ingredientes = produto.ingredients_text_pt || produto.ingredients_text || "Sem informações de ingredientes.";
            const imagem = produto.image_url || ""; 
            const alergenicos = produto.allergens_tags || []; 
            const alergenicosTexto = alergenicos.length > 0 ? alergenicos.join(', ') : "Nenhuma tag registrada.";

            // Cruzamento de dados com as restrições selecionadas no HTML
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            const restricoesUsuario = Array.from(checkboxes).map(cb => cb.value);

            let alerta = false;
            let perigosEncontrados = [];

            restricoesUsuario.forEach(restricao => {
                if (alergenicos.includes(restricao)) {
                    alerta = true;
                    // Procura o nome da label amigável (ex: pega "Lactose" em vez de "en:milk")
                    const label = document.querySelector(`input[value="${restricao}"]`).parentElement.textContent.trim();
                    perigosEncontrados.push(label);
                }
            });

            // Cores e status baseados no cruzamento de dados
            let corBorda = alerta ? "#ef4444" : "#10b981"; // Vermelho ou Verde da paleta atual
            let corFundo = alerta ? "#fef2f2" : "#ecfdf5";
            let iconeStatus = alerta ? "⚠️" : "✅";
            let tituloStatus = alerta ? "ALERTA DE RESTRIÇÃO" : "PRODUTO SEGURO";
            let mensagemStatus = alerta 
                ? `Contém ingredientes que você marcou: <strong>${perigosEncontrados.join(', ')}</strong>` 
                : `Nenhuma das restrições marcadas foi encontrada neste produto.`;

            // Construção do Card de Resultado final
            resultadoDiv.innerHTML = `
                <div style="border: 2px solid ${corBorda}; background-color: ${corFundo}; padding: 20px; border-radius: 12px;">
                    <h3 style="color: ${corBorda}; margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                        ${iconeStatus} ${tituloStatus}
                    </h3>
                    <p style="margin-bottom: 20px; font-size: 14px;">${mensagemStatus}</p>
                    
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin-bottom: 20px;">
                    
                    <h4 style="margin: 0 0 15px 0; font-size: 18px;">${nomeProduto}</h4>
                    ${imagem ? `<img src="${imagem}" alt="${nomeProduto}" style="max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 15px;">` : ''}
                    
                    <div style="font-size: 14px; color: var(--texto-escuro);">
                        <p style="margin-bottom: 8px;"><strong>Alergênicos Mapeados:</strong> ${alergenicosTexto}</p>
                        <p style="margin: 0; line-height: 1.5;"><strong>Ingredientes:</strong> ${ingredientes}</p>
                    </div>
                </div>
            `;
            
        } else {
            resultadoDiv.innerHTML = '<p style="color: red; text-align: center;">❌ Nenhum produto encontrado.</p>';
        }
        
    } catch (erro) {
        console.error("Erro de conexão:", erro);
        resultadoDiv.innerHTML = '<p style="color: red; text-align: center;">❌ Erro ao conectar com o servidor.</p>';
    }
}

// Escutadores de eventos
buscarBtn.addEventListener('click', buscarProduto);

// Permite buscar apertando o "Enter" no teclado
codigoInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        buscarProduto();
    }
});