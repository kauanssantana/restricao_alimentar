// Selecionando elementos da interface
const codigoInput = document.getElementById('codigoInput');
const buscarBtn = document.getElementById('buscarBtn');
const resultadoDiv = document.getElementById('resultado');
const btnNome = document.getElementById('btnNome');
const btnCodigo = document.getElementById('btnCodigo');

// 🌐 Dicionário de tradução de alergênicos para português
const traduzirAlergeno = {
    "en:milk": "Leite / Lactose",
    "en:nuts": "Nozes / Castanhas",
    "en:soybeans": "Soja",
    "en:gluten": "Glúten",
    "en:peanuts": "Amendoim",
    "en:eggs": "Ovo",
    "en:fish": "Peixe",
    "en:sesame": "Gergelim",
    "en:sesame-seeds": "Gergelim",
    "en:crustaceans": "Crustáceos",
    "en:mustard": "Mostarda"
};

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
    codigoInput.placeholder = "Ex: 7898024394181";
    codigoInput.value = ""; 
});

// FUNÇÃO PARA DESENHAR O CARD NA TELA
function renderizarProdutoNaTela(dados) {
    if (dados.products && dados.products.length > 0) {
        const produto = dados.products[0];
        
        const nomeProduto = produto.product_name || "Nome desconhecido";
        const ingredientes = produto.ingredients_text_pt || produto.ingredients_text || "Sem informações de ingredientes.";
        const alergenicos = produto.allergens_tags || []; 
        
        // Traduzindo as tags antes de mostrar na tela
        const alergenicosTraduzidos = alergenicos.map(tag => traduzirAlergeno[tag] || tag);
        const alergenicosTexto = alergenicosTraduzidos.length > 0 ? alergenicosTraduzidos.join(', ') : "Nenhuma tag registada.";

        // Cruzamento de dados com as restrições selecionadas no HTML
        // (Buscamos apenas as restrições da tela principal)
        const checkboxes = document.querySelectorAll('.grid-restricoes input[type="checkbox"]:checked');
        const restricoesUsuario = Array.from(checkboxes).map(cb => cb.value);

        let alerta = false;
        let perigosEncontrados = [];

        restricoesUsuario.forEach(restricao => {
            if (alergenicos.includes(restricao)) {
                alerta = true;
                const labelElement = document.querySelector(`.grid-restricoes input[value="${restricao}"]`);
                if(labelElement) {
                    perigosEncontrados.push(labelElement.parentElement.textContent.trim());
                }
            }
        });

        // Cores e status baseados no cruzamento
        let corBorda = alerta ? "#ef4444" : "#10b981"; 
        let corFundo = alerta ? "rgba(254, 242, 242, 0.9)" : "rgba(236, 253, 245, 0.9)";
        let iconeStatus = alerta ? "⚠️" : "✅";
        let tituloStatus = alerta ? "ALERTA DE RESTRIÇÃO" : "PRODUTO SEGURO";
        let mensagemStatus = alerta 
            ? `Contém ingredientes que precisa evitar: <strong>${perigosEncontrados.join(', ')}</strong>` 
            : `Nenhuma das restrições marcadas foi encontrada neste produto.`;

        // Construção do Card de Resultado final
        resultadoDiv.innerHTML = `
            <div style="border: 2px solid ${corBorda}; background-color: ${corFundo}; padding: 20px; border-radius: 20px; max-width: 800px; width: 100%; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05); backdrop-filter: blur(10px);">
                <h3 style="color: ${corBorda}; margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
                    ${iconeStatus} ${tituloStatus}
                </h3>
                <p style="margin-bottom: 20px; font-size: 14px;">${mensagemStatus}</p>
                
                <hr style="border: none; border-top: 1px solid rgba(0,0,0,0.1); margin-bottom: 20px;">
                
                <h4 style="margin: 0 0 15px 0; font-size: 18px;">${nomeProduto}</h4>
                
                <div style="font-size: 14px; color: var(--texto-escuro);">
                    <p style="margin-bottom: 8px;"><strong>Alergénicos Mapeados:</strong> ${alergenicosTexto}</p>
                    <p style="margin: 0; line-height: 1.5;"><strong>Ingredientes:</strong> ${ingredientes}</p>
                </div>
            </div>
        `;
        
        // Etiqueta que mostra a origem dos dados
        if (dados.origem === 'local') {
            resultadoDiv.innerHTML += `<div style="margin-top: 15px; text-align: center; font-size: 13px; color: #008f51; font-weight: bold; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">⚡ Carregado do seu Banco Local (NutriCheck)</div>`;
        } else {
            resultadoDiv.innerHTML += `<div style="margin-top: 15px; text-align: center; font-size: 13px; color: #3b82f6; font-weight: bold; text-shadow: 1px 1px 2px rgba(255,255,255,0.8);">🌐 Transferido da Internet e guardado no Banco!</div>`;
        }
        
    } else {
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center; font-weight: bold;">❌ Nenhum produto encontrado com este nome exato.</p>';
    }
}

// Conexão com o Back-end
async function buscarProduto() {
    const termoBusca = codigoInput.value.trim();

    if (!termoBusca) {
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center; font-weight: bold;">Por favor, digite algo para pesquisar.</p>';
        return;
    }

    resultadoDiv.innerHTML = '<p style="text-align: center; color: var(--texto-escuro); font-weight: 500;">Pesquisando no servidor...</p>';

    const termoCodificado = encodeURIComponent(termoBusca);
    const url = `http://127.0.0.1:5000/api/buscar?alimento=${termoCodificado}&tipo=${tipoBuscaAtual}`;
    
    try {
        const resposta = await fetch(url);
        if (!resposta.ok) throw new Error('Erro no servidor');
        
        const dados = await resposta.json();
        renderizarProdutoNaTela(dados);
        
    } catch (erro) {
        console.error(erro);
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center; font-weight: bold;">❌ Falha de comunicação. Verifique se o terminal do Python está a rodar.</p>';
    }
}

buscarBtn.addEventListener('click', buscarProduto);
codigoInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') buscarProduto();
});


// --- LÓGICA DO MODAL DE LOGIN E CADASTRO ---
const modal = document.getElementById('modalLogin');
const abrirModalBtn = document.getElementById('abrirModalBtn');
const fecharModal = document.querySelector('.fechar-modal');
const tabLogin = document.getElementById('tabLogin');
const tabCadastro = document.getElementById('tabCadastro');
const formLogin = document.getElementById('formLogin');
const formCadastro = document.getElementById('formCadastro');

// Abrir e Fechar
abrirModalBtn.onclick = () => modal.style.display = 'flex';
fecharModal.onclick = () => modal.style.display = 'none';
window.onclick = (e) => { if(e.target == modal) modal.style.display = 'none'; }

// Alternar entre Login e Cadastro
tabLogin.onclick = () => {
    tabLogin.classList.add('active');
    tabCadastro.classList.remove('active');
    formLogin.classList.remove('hidden');
    formCadastro.classList.add('hidden');
};

tabCadastro.onclick = () => {
    tabCadastro.classList.add('active');
    tabLogin.classList.remove('active');
    formCadastro.classList.remove('hidden');
    formLogin.classList.add('hidden');
};

// Validação de confirmação de senha no cadastro (Adicionado aqui no final!)
formCadastro.addEventListener('submit', (e) => {
    const senha = document.getElementById('senhaCadastro').value;
    const confirma = document.getElementById('confirmaSenha').value;

    if (senha !== confirma) {
        e.preventDefault(); // Impede o envio do formulário
        alert("⚠️ As senhas digitadas não coincidem. Por favor, verifique.");
    }
});