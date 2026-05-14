// ==========================================
// 1. SELEÇÃO DE ELEMENTOS E VARIÁVEIS GLOBAIS
// ==========================================
const codigoInput  = document.getElementById('codigoInput'), buscarBtn = document.getElementById('buscarBtn');
const resultadoDiv = document.getElementById('resultado'), btnNome = document.getElementById('btnNome'), btnCodigo = document.getElementById('btnCodigo');
const modal        = document.getElementById('modalLogin'), abrirModalBtn = document.getElementById('abrirModalBtn'), fecharModal = document.querySelector('.fechar-modal');
const tabLogin     = document.getElementById('tabLogin'), tabCadastro = document.getElementById('tabCadastro');
const formLogin    = document.getElementById('formLogin'), formCadastro = document.getElementById('formCadastro');

// ✅ onclick padrão definido IMEDIATAMENTE — antes de qualquer função async
abrirModalBtn.onclick = () => modal.style.display = 'flex';

const API = 'http://127.0.0.1:5000';
let usuarioAtual   = null;
let tipoBuscaAtual = 'nome';

const traduzirAlergeno = {
    "en:milk": "Leite / Lactose", "en:nuts": "Nozes / Castanhas", "en:soybeans": "Soja",
    "en:gluten": "Glúten", "en:peanuts": "Amendoim", "en:eggs": "Ovo", "en:fish": "Peixe",
    "en:sesame": "Gergelim", "en:sesame-seeds": "Gergelim", "en:crustaceans": "Crustáceos", "en:mustard": "Mostarda"
};

// ==========================================
// 2. MÁSCARA DE TELEFONE
// ==========================================
function inicializarMascaraTelefone() {
    const telInput = formCadastro.querySelector('input[type="tel"]');
    if (!telInput || telInput.dataset.mascaraAtiva) return;
    telInput.dataset.mascaraAtiva = 'true';

    telInput.addEventListener('keydown', (e) => {
        const teclasDeControle = ['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'];
        if (!teclasDeControle.includes(e.key) && !/^\d$/.test(e.key)) e.preventDefault();
    });

    telInput.addEventListener('input', () => {
        let v = telInput.value.replace(/\D/g, '').slice(0, 11);
        if (v.length > 6)      v = `(${v.slice(0,2)}) ${v.slice(2,7)}-${v.slice(7)}`;
        else if (v.length > 2) v = `(${v.slice(0,2)}) ${v.slice(2)}`;
        else if (v.length > 0) v = `(${v}`;
        telInput.value = v;
    });
}

// ==========================================
// 3. NAVEGAÇÃO E MODAL DE LOGIN
// ==========================================
const alternarBusca = (tipo, btnAtivo, btnInativo, placeholder) => {
    tipoBuscaAtual = tipo;
    btnAtivo.classList.add('ativo'); btnInativo.classList.remove('ativo');
    codigoInput.placeholder = placeholder; codigoInput.value = "";
};
btnNome.onclick   = () => alternarBusca('nome', btnNome, btnCodigo, "Ex: biscoito recheado");
btnCodigo.onclick = () => alternarBusca('codigo', btnCodigo, btnNome, "Ex: 7898024394181");

fecharModal.onclick = () => modal.style.display = 'none';
window.onclick = (e) => {
    if (e.target === modal) modal.style.display = 'none';
    if (e.target === document.getElementById('modalPerfil')) fecharModalPerfil();
};

const alternarAbas = (tabAtiva, tabInativa, formAtivo, formInativo) => {
    tabAtiva.classList.add('active'); tabInativa.classList.remove('active');
    formAtivo.classList.remove('hidden'); formInativo.classList.add('hidden');
};
tabLogin.onclick    = () => alternarAbas(tabLogin, tabCadastro, formLogin, formCadastro);
tabCadastro.onclick = () => {
    alternarAbas(tabCadastro, tabLogin, formCadastro, formLogin);
    inicializarMascaraTelefone();
};

// ==========================================
// 4. AUTENTICAÇÃO E SESSÃO
// ==========================================
function atualizarBotaoLogin() {
    if (usuarioAtual) {
        abrirModalBtn.textContent = `👤 ${usuarioAtual.nome.split(' ')[0]}`;
        abrirModalBtn.title       = "Clique para ver seu perfil";
        abrirModalBtn.onclick     = abrirModalPerfil;

        if (usuarioAtual.restricoes?.length > 0) {
            document.querySelectorAll('.grid-restricoes input[type="checkbox"]').forEach(cb => cb.checked = false);
            usuarioAtual.restricoes.forEach(r => {
                const cb = document.querySelector(`.grid-restricoes input[value="${r}"]`);
                if (cb) cb.checked = true;
            });
        }
    } else {
        abrirModalBtn.textContent = "👤 Entrar / Cadastrar";
        abrirModalBtn.title       = "";
        abrirModalBtn.onclick     = () => modal.style.display = 'flex';
    }
}

async function verificarSessao() {
    try {
        const res = await fetch(`${API}/api/perfil`, { credentials: 'include' });
        if (res.ok) { usuarioAtual = await res.json(); atualizarBotaoLogin(); }
    } catch (e) {}
}

async function fazerLogin(e) {
    e.preventDefault();
    const email   = formLogin.querySelector('input[type="email"]').value.trim();
    const senha   = formLogin.querySelector('input[type="password"]').value;
    const erroDiv = document.getElementById('erroLogin');
    erroDiv.textContent = '';

    try {
        const res   = await fetch(`${API}/api/login`, { method: 'POST', headers: {'Content-Type':'application/json'}, credentials: 'include', body: JSON.stringify({ email, senha }) });
        const dados = await res.json();
        if (!res.ok) return erroDiv.textContent = dados.erro || 'Erro ao fazer login.';
        usuarioAtual = dados.usuario;
        modal.style.display = 'none';
        formLogin.reset();
        atualizarBotaoLogin();
        mostrarNotificacao(`✅ Bem-vindo, ${usuarioAtual.nome.split(' ')[0]}!`);
    } catch (e) { erroDiv.textContent = 'Falha de comunicação com o servidor.'; }
}

async function fazerCadastro(e) {
    e.preventDefault();
    const inputs         = formCadastro.querySelectorAll('input');
    const nome           = inputs[0].value.trim();
    const email          = inputs[1].value.trim();
    const telefone       = inputs[2].value.trim();
    const senha          = inputs[3].value;
    const confirmarSenha = inputs[4].value;
    const erroDiv        = document.getElementById('erroCadastro');
    erroDiv.textContent  = '';

    if (senha !== confirmarSenha) return erroDiv.textContent = '⚠️ As senhas não coincidem.';
    if (senha.length < 8)        return erroDiv.textContent = '⚠️ A senha deve ter pelo menos 8 caracteres.';
    const telefoneLimpo = telefone.replace(/\D/g, '');
    if (telefoneLimpo.length < 10 || telefoneLimpo.length > 11) return erroDiv.textContent = '⚠️ Digite um telefone válido com DDD.';

    const restricoes = Array.from(document.querySelectorAll('#formCadastro input[type="checkbox"]:checked')).map(cb => cb.value);

    try {
        const res   = await fetch(`${API}/api/cadastro`, { method: 'POST', headers: {'Content-Type':'application/json'}, credentials: 'include', body: JSON.stringify({ nome, email, telefone, senha, confirmarSenha, restricoes }) });
        const dados = await res.json();
        if (!res.ok) return erroDiv.textContent = dados.erro || 'Erro ao criar conta.';
        usuarioAtual = dados.usuario;
        modal.style.display = 'none';
        formCadastro.reset();
        atualizarBotaoLogin();
        mostrarNotificacao(`✅ Conta criada! Bem-vindo, ${usuarioAtual.nome.split(' ')[0]}!`);
    } catch (e) { erroDiv.textContent = 'Falha de comunicação com o servidor.'; }
}

async function fazerLogout() {
    try { await fetch(`${API}/api/logout`, { method: 'POST', credentials: 'include' }); } catch (e) {}
    usuarioAtual = null;
    atualizarBotaoLogin();
    fecharModalPerfil();
    mostrarNotificacao('👋 Sessão encerrada.', 'info');
}

formLogin.addEventListener('submit', fazerLogin);
formCadastro.addEventListener('submit', fazerCadastro);

// ==========================================
// 5. MODAL DE PERFIL
// ==========================================
function abrirModalPerfil() {
    document.getElementById('modalPerfil').style.display = 'flex';
    mostrarAbaPerfil('dados');
    carregarDadosPerfil();
}

function fecharModalPerfil() {
    document.getElementById('modalPerfil').style.display = 'none';
}

function mostrarAbaPerfil(aba) {
    ['dados', 'registros'].forEach(a => {
        document.getElementById(`aba-${a}`).classList.toggle('hidden', a !== aba);
        const btn = document.getElementById(`tab-perfil-${a}`);
        btn.style.borderBottomColor = a === aba ? 'var(--verde-primario)' : 'transparent';
        btn.style.color             = a === aba ? 'var(--verde-primario)' : '#6b7280';
    });
    if (aba === 'registros') carregarHistorico();
}

function carregarDadosPerfil() {
    if (!usuarioAtual) return;
    document.getElementById('perfil-nome').value     = usuarioAtual.nome     || '';
    document.getElementById('perfil-email').value    = usuarioAtual.email    || '';
    document.getElementById('perfil-telefone').value = usuarioAtual.telefone || '';
    document.getElementById('perfil-msg-dados').textContent = '';
    document.getElementById('perfil-msg-senha').textContent = '';
}

async function salvarDadosPerfil() {
    const nome     = document.getElementById('perfil-nome').value.trim();
    const telefone = document.getElementById('perfil-telefone').value.trim();
    const msgDiv   = document.getElementById('perfil-msg-dados');
    msgDiv.style.color = '#ef4444';
    msgDiv.textContent = '';

    if (!nome) return msgDiv.textContent = '⚠️ O nome não pode estar vazio.';

    try {
        const res   = await fetch(`${API}/api/perfil/dados`, { method: 'PUT', headers: {'Content-Type':'application/json'}, credentials: 'include', body: JSON.stringify({ nome, telefone }) });
        const dados = await res.json();
        if (!res.ok) return msgDiv.textContent = dados.erro;
        usuarioAtual.nome     = nome;
        usuarioAtual.telefone = telefone;
        atualizarBotaoLogin();
        msgDiv.style.color = '#10b981';
        msgDiv.textContent = '✅ Dados atualizados com sucesso!';
    } catch (e) { msgDiv.textContent = 'Falha de comunicação.'; }
}

async function salvarNovaSenha() {
    const senhaAtual         = document.getElementById('perfil-senha-atual').value;
    const novaSenha          = document.getElementById('perfil-nova-senha').value;
    const confirmarNovaSenha = document.getElementById('perfil-confirmar-senha').value;
    const msgDiv             = document.getElementById('perfil-msg-senha');
    msgDiv.style.color       = '#ef4444';
    msgDiv.textContent       = '';

    if (novaSenha !== confirmarNovaSenha) return msgDiv.textContent = '⚠️ As senhas não coincidem.';
    if (novaSenha.length < 8)            return msgDiv.textContent = '⚠️ Mínimo de 8 caracteres.';

    try {
        const res   = await fetch(`${API}/api/perfil/senha`, { method: 'PUT', headers: {'Content-Type':'application/json'}, credentials: 'include', body: JSON.stringify({ senhaAtual, novaSenha, confirmarNovaSenha }) });
        const dados = await res.json();
        if (!res.ok) return msgDiv.textContent = dados.erro;
        document.getElementById('perfil-senha-atual').value     = '';
        document.getElementById('perfil-nova-senha').value      = '';
        document.getElementById('perfil-confirmar-senha').value = '';
        msgDiv.style.color = '#10b981';
        msgDiv.textContent = '✅ Senha alterada com sucesso!';
    } catch (e) { msgDiv.textContent = 'Falha de comunicação.'; }
}

// 🛡️ LGPD: Exclusão total de conta e dados
async function excluirConta() {
    const confirmacao = confirm("⚠️ ATENÇÃO: Tem certeza que deseja excluir sua conta permanentemente? Todo o seu histórico e dados serão apagados. Esta ação não pode ser desfeita.");
    if (!confirmacao) return;

    try {
        const res = await fetch(`${API}/api/perfil`, { 
            method: 'DELETE', 
            credentials: 'include' 
        });
        
        const dados = await res.json();

        if (!res.ok) {
            alert(dados.erro || "Erro ao excluir conta.");
            return;
        }

        usuarioAtual = null;
        atualizarBotaoLogin();
        fecharModalPerfil();
        document.getElementById('resultado').innerHTML = ''; 
        mostrarNotificacao('🗑️ Conta excluída com sucesso.', 'info');

    } catch (e) {
        alert('Falha de comunicação com o servidor.');
    }
}

// ==========================================
// 6. HISTÓRICO
// ==========================================
async function salvarNoHistorico(produto, seguro) {
    if (!usuarioAtual) return;
    try {
        await fetch(`${API}/api/historico`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({
                produto_nome:   produto.product_name  || 'Desconhecido',
                produto_imagem: produto.image_url     || '',
                alergenicos:    produto.allergens_tags || [],
                seguro:         seguro
            })
        });
    } catch (e) { console.error('Erro ao salvar histórico:', e); }
}

async function carregarHistorico() {
    const container = document.getElementById('lista-historico');
    container.innerHTML = '<p style="color:#888;font-size:13px;text-align:center;">Carregando...</p>';

    try {
        const res      = await fetch(`${API}/api/historico`, { credentials: 'include' });
        const registos = await res.json();

        if (!registos.length) {
            container.innerHTML = '<p style="color:#888;font-size:13px;text-align:center;">Nenhuma consulta ainda.</p>';
            return;
        }

        container.innerHTML = registos.map(r => {
            const icone  = r.seguro ? '🟢' : '🔴';
            const status = r.seguro ? 'Seguro' : 'Contém restrição';
            const data   = formatarData(r.consultado_em);
            return `
                <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(0,0,0,0.06);">
                    <div style="flex:1;min-width:0;">
                        <p style="margin:0;font-weight:600;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${r.produto_nome}</p>
                        <p style="margin:0;font-size:12px;color:#6b7280;">${icone} ${status} · ${data}</p>
                    </div>
                </div>`;
        }).join('');
    } catch (e) {
        container.innerHTML = '<p style="color:#ef4444;font-size:13px;">Erro ao carregar histórico.</p>';
    }
}

function formatarData(dataStr) {
    const data  = new Date(dataStr);
    const agora = new Date();
    const diff  = Math.floor((agora - data) / 1000);
    if (diff < 60)        return 'agora mesmo';
    if (diff < 3600)      return `há ${Math.floor(diff/60)} min`;
    if (diff < 86400)     return `há ${Math.floor(diff/3600)}h`;
    if (diff < 86400 * 2) return 'ontem';
    return data.toLocaleDateString('pt-BR');
}

// ==========================================
// 7. RENDERIZAÇÃO E BUSCA
// ==========================================
function renderizarProdutoNaTela(dados) {
    if (!dados.products || dados.products.length === 0) {
        return resultadoDiv.innerHTML = '<p style="color:#ef4444;text-align:center;font-weight:bold;">❌ Nenhum produto encontrado com este nome exato.</p>';
    }

    const produto      = dados.products[0];
    const nomeProduto  = produto.product_name || "Nome desconhecido";
    const ingredientes = produto.ingredients_text_pt || produto.ingredients_text || "Sem informações de ingredientes.";
    const alergenicos  = produto.allergens_tags || [];

    const alergenicosTraduzidos = alergenicos.map(tag => traduzirAlergeno[tag] || tag);
    const alergenicosTexto = alergenicosTraduzidos.length > 0 ? alergenicosTraduzidos.join(', ') : "Nenhuma tag registada.";

    const restricoesUsuario = usuarioAtual?.restricoes?.length > 0
        ? usuarioAtual.restricoes
        : Array.from(document.querySelectorAll('.grid-restricoes input[type="checkbox"]:checked')).map(cb => cb.value);

    let alerta = false, perigosEncontrados = [];
    restricoesUsuario.forEach(restricao => {
        if (alergenicos.includes(restricao)) {
            alerta = true;
            const labelEl = document.querySelector(`.grid-restricoes input[value="${restricao}"]`);
            if (labelEl) perigosEncontrados.push(labelEl.parentElement.textContent.trim());
        }
    });

    // Salva no histórico automaticamente se estiver logado
    salvarNoHistorico(produto, !alerta);

    const corBorda   = alerta ? "#ef4444" : "#10b981";
    const corFundo   = alerta ? "rgba(254,242,242,0.9)" : "rgba(236,253,245,0.9)";
    const icone      = alerta ? "⚠️" : "✅";
    const titulo     = alerta ? "ALERTA DE RESTRIÇÃO" : "PRODUTO SEGURO";
    const mensagem   = alerta
        ? `Contém ingredientes que precisa evitar: <strong>${perigosEncontrados.join(', ')}</strong>`
        : "Nenhuma das restrições marcadas foi encontrada neste produto.";
    const imagemHtml = produto.image_url
        ? `<img src="${produto.image_url}" alt="${nomeProduto}" style="width:90px;height:90px;object-fit:contain;border-radius:10px;float:right;margin-left:16px;">`
        : '';

    resultadoDiv.innerHTML = `
        <div style="border:2px solid ${corBorda};background-color:${corFundo};padding:20px;border-radius:20px;max-width:800px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,0.05);backdrop-filter:blur(10px);">
            <h3 style="color:${corBorda};margin:0 0 10px 0;display:flex;align-items:center;gap:8px;">${icone} ${titulo}</h3>
            <p style="margin-bottom:20px;font-size:14px;">${mensagem}</p>
            <hr style="border:none;border-top:1px solid rgba(0,0,0,0.1);margin-bottom:20px;">
            <div style="overflow:hidden;">
                ${imagemHtml}
                <h4 style="margin:0 0 12px 0;font-size:18px;">${nomeProduto}</h4>
                <div style="font-size:14px;color:var(--texto-escuro);">
                    <p style="margin-bottom:8px;"><strong>Alergénicos Mapeados:</strong> ${alergenicosTexto}</p>
                    <p style="margin:0;line-height:1.5;"><strong>Ingredientes:</strong> ${ingredientes}</p>
                </div>
            </div>
        </div>
        <div style="margin-top:15px;text-align:center;font-size:13px;font-weight:bold;text-shadow:1px 1px 2px rgba(255,255,255,0.8);color:${dados.origem==='local'?'#008f51':'#3b82f6'};">
            ${dados.origem === 'local' ? '⚡ Carregado do seu Banco Local (NutriCheck)' : '🌐 Transferido da Internet e guardado no Banco!'}
        </div>`;
}

async function buscarProduto() {
    const termoBusca = codigoInput.value.trim();
    if (!termoBusca) return resultadoDiv.innerHTML = '<p style="color:#ef4444;text-align:center;font-weight:bold;">Por favor, digite algo para pesquisar.</p>';
    resultadoDiv.innerHTML = '<p style="text-align:center;color:var(--texto-escuro);font-weight:500;">🔍 Pesquisando...</p>';

    try {
        const resposta = await fetch(`${API}/api/buscar?alimento=${encodeURIComponent(termoBusca)}&tipo=${tipoBuscaAtual}`, { credentials: 'include' });
        if (!resposta.ok) throw new Error();
        renderizarProdutoNaTela(await resposta.json());
    } catch (e) {
        resultadoDiv.innerHTML = '<p style="color:#ef4444;text-align:center;font-weight:bold;">❌ Falha de comunicação. Verifique se o servidor Python está a rodar.</p>';
    }
}

buscarBtn.addEventListener('click', buscarProduto);
codigoInput.addEventListener('keypress', e => { if (e.key === 'Enter') buscarProduto(); });

// ==========================================
// 8. NOTIFICAÇÃO FLUTUANTE (TOAST)
// ==========================================
function mostrarNotificacao(mensagem, tipo = 'sucesso') {
    const cores = { sucesso: '#10b981', erro: '#ef4444', info: '#3b82f6' };
    const toast = document.createElement('div');
    toast.textContent = mensagem;
    toast.style.cssText = `position:fixed;top:20px;right:20px;z-index:9999;background:${cores[tipo]};color:white;padding:14px 22px;border-radius:12px;font-size:14px;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,0.15);animation:fadeInOut 3s ease forwards;`;
    if (!document.getElementById('toastStyle')) {
        const style = document.createElement('style'); style.id = 'toastStyle';
        style.textContent = `@keyframes fadeInOut{0%{opacity:0;transform:translateY(-10px)}15%{opacity:1;transform:translateY(0)}80%{opacity:1}100%{opacity:0;transform:translateY(-10px)}}`;
        document.head.appendChild(style);
    }
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ==========================================
// INICIALIZAÇÃO
// ==========================================
verificarSessao();