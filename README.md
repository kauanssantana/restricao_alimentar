# 🍏🔍 NutriCheck

> O seu assistente inteligente e seguro para verificar restrições alimentares e ingredientes em tempo real!

![Capa do Projeto](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Open Food Facts](https://img.shields.io/badge/Open_Food_Facts-34495E?style=for-the-badge)

---

## 📖 Sobre o Projeto

O **NutriCheck** é uma aplicação web Full-Stack desenvolvida para ajudar pessoas com restrições alimentares (como alergias e intolerâncias) ou foco fitness a identificar rapidamente se um produto é seguro para o consumo. 

O sistema integra-se à API global do [Open Food Facts](https://br.openfoodfacts.org/) para buscar dados de milhares de produtos. Além disso, a aplicação possui um back-end robusto focado em **Segurança da Informação e Governança de TI (Adequação LGPD)**, garantindo a proteção e o direito de exclusão dos dados dos usuários. Tudo envelopado numa interface moderna com *Glassmorphism* e 100% responsiva (Mobile-First).

<img width="1600" height="787" alt="img" src="https://github.com/user-attachments/assets/db19e86d-c573-4280-bd28-2aba9add0196" />

---

## ✨ Principais Funcionalidades

* 🔍 **Busca Inteligente:** Pesquise produtos pelo Nome ou pelo Código de Barras de forma instantânea.
* ⚠️ **Alertas Personalizados:** Cadastre suas restrições (Lactose, Glúten, Soja, Amendoim, etc.) e o sistema destacará automaticamente em verde (Seguro) ou vermelho (Perigo) se o produto contém o que você precisa evitar.
* 💾 **Caching Local:** Produtos pesquisados são salvos no banco de dados SQLite local, tornando as buscas futuras extremamente rápidas e economizando requisições à API externa.
* 🕘 **Histórico de Usuário:** Uma área de perfil dedicada que salva automaticamente as últimas 10 consultas do usuário para fácil acesso no supermercado.
* 🛡️ **Segurança e Privacidade (LGPD):** * Sistema de autenticação com senhas criptografadas (Hash).
  * Defesa ativa contra ataques de Força Bruta (*Rate Limiting* bloqueia IPs após múltiplas tentativas falhas).
  * Exclusão permanente de conta: O usuário pode deletar seu perfil e todo o seu histórico com um clique (Efeito Cascata no banco de dados).

---

## 💻 Tecnologias Utilizadas

O projeto foi dividido em duas camadas, utilizando as melhores práticas de desenvolvimento sem depender de frameworks pesados no Front-end:

**Front-end:**
* **HTML5 & CSS3:** Design moderno (Glassmorphism), Flexbox, CSS Grid e responsividade total.
* **JavaScript (ES6+):** Consumo de APIs (Fetch), manipulação do DOM e gestão de estado local.

**Back-end & Banco de Dados:**
* **Python 3 & Flask:** Criação de rotas RESTful API e gestão de sessões.
* **Werkzeug:** Criptografia e segurança de senhas.
* **SQLite3:** Banco de dados relacional (Tabelas de Usuários, Alimentos, Histórico e Logs de Auditoria).

---

## 🚀 Como Executar o Projeto

1. Faça o clone deste repositório:
   ```bash
   git clone [https://github.com/kauanssantana/nutricheck.git](https://github.com/kauanssantana/nutricheck.git)

2. Acesse a pasta do projeto:
      ```bash
      cd nutricheck

3. Instale as dependências do Python:
      ```bash
      pip install Flask flask-cors requests werkzeug

4. Inicie o servidor Back-end (ele criará o banco de dados nutricheck.db automaticamente com o catálogo inicial):
      ```bash
      python app.py

5. Abra o arquivo index.html no seu navegador web preferido e comece a usar!


---

## 🛡️ Licença & Copyright
Copyright (c) 2026 Kauan Santana Almeida. Todos os direitos reservados.

A cópia, distribuição, modificação ou uso comercial deste código, seja parcial ou integral, é estritamente proibida sem a autorização prévia e expressa do autor. O uso não autorizado deste software está sujeito às penalidades previstas na lei de direitos autorais.
