// Selecionando elementos da interface
const codigoInput = document.getElementById('codigoInput');
const buscarBtn = document.getElementById('buscarBtn');
const resultadoDiv = document.getElementById('resultado');
const btnNome = document.getElementById('btnNome');
const btnCodigo = document.getElementById('btnCodigo');

// Variável para saber qual tipo de busca o usuário quer fazer
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

// FUNÇÃO PARA DESENHAR O CARD NA TELA (Deixa o código organizado)
function renderizarProdutoNaTela(dados) {
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
                const label = document.querySelector(`input[value="${restricao}"]`).parentElement.textContent.trim();
                perigosEncontrados.push(label);
            }
        });

        // Cores e status baseados no cruzamento de dados
        let corBorda = alerta ? "#ef4444" : "#10b981"; 
        let corFundo = alerta ? "#fef2f2" : "#ecfdf5";
        let iconeStatus = alerta ? "⚠️" : "✅";
        let tituloStatus = alerta ? "ALERTA DE RESTRIÇÃO" : "PRODUTO SEGURO";
        let mensagemStatus = alerta 
            ? `Contém ingredientes que você marcou: <strong>${perigosEncontrados.join(', ')}</strong>` 
            : `Nenhuma das restrições marcadas foi encontrada neste produto.`;

        // Construção do Card de Resultado final
        resultadoDiv.innerHTML = `
            <div style="border: 2px solid ${corBorda}; background-color: ${corFundo}; padding: 20px; border-radius: 12px; max-width: 600px; width: 100%;">
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
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center;">❌ Nenhum produto encontrado na base de dados.</p>';
    }
}

// Lógica principal de busca conectada com a API Real e o Modo de Simulação
async function buscarProduto() {
    const termoBusca = codigoInput.value.trim();

    if (!termoBusca) {
        resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center;">Por favor, digite algo para buscar.</p>';
        return;
    }

    resultadoDiv.innerHTML = '<p style="text-align: center; color: var(--texto-claro);">Buscando na base de dados...</p>';

    const termoCodificado = encodeURIComponent(termoBusca);
    let apiUrl = '';
    
    if (tipoBuscaAtual === 'nome') {
        apiUrl = `https://br.openfoodfacts.org/api/v2/search?search_terms=${termoCodificado}`;
    } else {
        apiUrl = `https://br.openfoodfacts.org/api/v2/product/${termoCodificado}`;
    }

    try {
        const resposta = await fetch(apiUrl);
        if (!resposta.ok) {
            throw new Error(`A API bloqueou o acesso com o status: ${resposta.status}`);
        }
        
        const dados = await resposta.json();
        let dadosTratados = { products: [] };
        
        if (tipoBuscaAtual === 'codigo') {
            // Busca por código é exata, retorna só 1 produto
            if (dados.product) dadosTratados.products.push(dados.product);
        } else {
            // 🧠 NOVA LÓGICA DE NOME: Vasculha a lista para achar o melhor resultado
            if (dados.products && dados.products.length > 0) {
                // Tenta achar o primeiro produto que tenha a palavra pesquisada no nome
                const melhorMatch = dados.products.find(p => 
                    p.product_name && p.product_name.toLowerCase().includes(termoBusca.toLowerCase())
                );
                
                // Se achou um que bate o nome, usa ele. Se não, usa o primeiro da lista como plano B.
                if (melhorMatch) {
                    dadosTratados.products.push(melhorMatch);
                } else {
                    dadosTratados.products.push(dados.products[0]);
                }
            }
        }
        
        renderizarProdutoNaTela(dadosTratados);
        
    } catch (erro) {
        console.warn("⚠️ API da Open Food Facts caiu ou falhou. Ativando o Modo Simulação (Mock).", erro);
        
        // 🚀 O MODO DE SIMULAÇÃO (MOCK)
        // Se falhar e a palavra for nutella, a gente desenha dados falsos para você poder continuar a testar.
        if (termoBusca.toLowerCase() === 'nutella') {
            const dadosDeEmergencia = {
                products: [{
                    product_name: "Nutella (Modo Simulação - API Offline)",
                    ingredients_text_pt: "Açúcar, óleo de palma, avelãs, cacau em pó, leite desnatado em pó, soro de leite em pó, emulsificante lecitinas (soja), aromatizante.",
                    image_url: "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_pt.450.400.jpg",
                    allergens_tags: ["en:milk", "en:nuts", "en:soybeans"]
                }]
            };
            
            renderizarProdutoNaTela(dadosDeEmergencia);
            
            // Aviso discreto para informar que os dados são simulados
            resultadoDiv.innerHTML += `
                <div style="margin-top: 15px; padding: 10px; background: #fff3cd; color: #856404; border: 1px solid #ffeeba; border-radius: 8px; text-align: center; max-width: 600px; width: 100%;">
                    ⚠️ <strong>Aviso de Sistema:</strong> A conexão com a base europeia falhou. Exibindo dados de simulação local.
                </div>
            `;
        } else {
            resultadoDiv.innerHTML = '<p style="color: #ef4444; text-align: center;">❌ Erro de conexão de rede. A API oficial está bloqueando acessos no momento. Tente novamente mais tarde.</p>';
        }
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