// Selecionando elementos da interface
const codigoInput = document.getElementById('codigoInput');
const buscarBtn = document.getElementById('buscarBtn');
const resultadoDiv = document.getElementById('resultado');
const btnNome = document.getElementById('btnNome');
const btnCodigo = document.getElementById('btnCodigo');

// Variável para saber qual tipo de busca o utilizador quer fazer
let tipoBuscaAtual = 'nome';

// Lógica de troca do Toggle (Nome vs Código de Barras)
btnNome.addEventListener('click', () => {
    tipoBuscaAtual = 'nome';
    btnNome.classList.add('ativo');
    btnCodigo.classList.remove('ativo');
    codigoInput.placeholder = "Ex: biscoito recheado";
    codigoInput.value = ""; 
});

btnCodigo.addEventListener('click', () => {
    tipoBuscaAtual = 'codigo';
    btnCodigo.classList.add('ativo');
    btnNome.classList.remove('ativo');
    codigoInput.placeholder = "Ex: 7622300990732";
    codigoInput.value = ""; 
});

// FUNÇÃO PARA DESENHAR O CARD NA TELA (AGORA SEM IMAGENS)
function renderizarProdutoNaTela(dados) {
    if (dados.products && dados.products.length > 0) {
        const produto = dados.products[0];
        
        const nomeProduto = produto.product_name || "Nome desconhecido";
        const ingredientes = produto.ingredients_text_pt || produto.ingredients_text || "Sem informações de ingredientes.";
        const alergenicos = produto.allergens_tags || []; 
        const alergenicosTexto = alergenicos.length > 0 ? alergenicos.join(', ') : "Nenhuma tag registada.";

        // Cruzamento de dados com as restrições selecionadas no HTML
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        const restricoesUsuario = Array.from(checkboxes).map(cb => cb.value);

        let alerta = false;
        let perigosEncontrados = [];

        restricoesUsuario.forEach(restricao => {
            if (alergenicos.includes(restricao)) {
                alerta = true;
                const label = document.querySelector(`input[value="${restricao}"]`).parentElement.textContent.trim();
                perigosEncontrados.push(label);
            }
        });

        // Cores e status baseados no cruzamento
        let corBorda = alerta ? "#ef4444" : "#10b981"; 
        let corFundo = alerta ? "#fef2f2" : "#ecfdf5";
        let iconeStatus = alerta ? "⚠️" : "✅";
        let tituloStatus = alerta ? "ALERTA DE RESTRIÇÃO" : "PRODUTO SEGURO";
        let mensagemStatus = alerta 
            ? `Contém ingredientes que precisa evitar: <strong>${perigosEncontrados.join(', ')}</strong>` 
            : `Nenhuma das restrições marcadas foi encontrada neste produto.`;

        // Construção do Card de Resultado final (Mais limpo e direto ao ponto)
        resultadoDiv.innerHTML = `
            <div style="border: 2px solid ${corBorda}; background-color: ${corFundo}; padding: 20px; border-radius: 12px; max-width: 600px; width: 100%;">
                <h3 style="color: ${corBorda}; margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                    ${iconeStatus} ${tituloStatus}
                </h3>
                <p style="margin-bottom: 20px; font-size: 14px;">${mensagemStatus}</p>
                
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin-bottom: 20px;">
                
                <h4 style="margin: 0 0 15px 0; font-size: 18px;">${nomeProduto}</h4>
                
                <div style="font-size: 14px; color: var(--texto-escuro);">
                    <p style="margin-bottom: 8px;"><strong>Alergénicos Mapeados:</strong> ${alergenicosTexto}</p>
                    <p style="margin: 0; line-height: 1.5;"><strong>Ingredientes:</strong> ${ingredientes}</p>
                </div>
            </div>
        `;
        
        // Etiqueta que mostra se o Python foi à internet ou se já tinha no banco local
        if (dados.origem === 'local') {
            resultadoDiv.innerHTML += `<div style="margin-top: 15px; text-align: center; font-size: 13px; color: #10b981; font-weight: bold;">⚡ Carregado do seu Banco Local (NutriCheck)</div>`;
        } else {
            resultadoDiv.innerHTML += `<div style="margin-top: 15px; text-align: center; font-size: 13px; color: #3b82f6; font-weight: bold;">🌐 Transferido da Internet e guardado no Banco!</div>`;
        }
        
    } else {
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center;">❌ Nenhum produto encontrado com este nome exato.</p>';
    }
}

// O JavaScript agora APENAS fala com o Python.
async function buscarProduto() {
    const termoBusca = codigoInput.value.trim();

    if (!termoBusca) {
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center;">Por favor, digite algo para pesquisar.</p>';
        return;
    }

    resultadoDiv.innerHTML = '<p style="text-align: center; color: var(--texto-claro);">Pesquisando no servidor...</p>';

    const termoCodificado = encodeURIComponent(termoBusca);
    
    // Bate na porta do nosso Back-end Python
    const url = `http://127.0.0.1:5000/api/buscar?alimento=${termoCodificado}&tipo=${tipoBuscaAtual}`;
    
    try {
        const resposta = await fetch(url);
        if (!resposta.ok) throw new Error('Erro no servidor');
        
        const dados = await resposta.json();
        renderizarProdutoNaTela(dados);
        
    } catch (erro) {
        console.error(erro);
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center;">❌ Falha de comunicação. Verifique se o terminal do Python está a rodar.</p>';
    }
}

buscarBtn.addEventListener('click', buscarProduto);
codigoInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') buscarProduto();
});