<h1 align="center">Sistema de Gestão de Biblioteca Digital</h1>

<p>Este projeto foi desenvolvido em grupo para a disciplina de <strong>Novas Tecnologias</strong> da Universidade Católica de Brasília. Nosso objetivo foi criar um sistema em Python que permita o gerenciamento de uma biblioteca digital de forma simples e eficaz, utilizando boas práticas de programação, estruturas de dados e conceitos fundamentais abordados durante as aulas.</p>

<h2>📌 IMPORTANTE</h2>
<p>Todo o trabalho foi realizado em grupo, onde cada integrante contribuiu para o design, a implementação e a validação do sistema. Os principais conceitos utilizados incluem:</p>
<ul>
  <li>Atribuição, variáveis e tipos numéricos</li>
  <li>Manipulação de strings, listas, dicionários, tuplas e conjuntos</li>
  <li>Operadores lógicos e booleanos</li>
  <li>Tratamento de arquivos para persistência dos dados</li>
  <li>Estruturação do código seguindo o padrão MVC</li>
  <li>Duas interfaces: GUI (gráfica) e CLI (linha de comando)</li>
</ul>

<h2>📚 Funcionalidades do Sistema</h2>

<h3>1. Cadastro de Livros</h3>
<ul>
  <li>Registra livros com título, autor, ano de publicação, ISBN e categoria</li>
  <li>Armazena os livros utilizando dicionários e listas</li>
  <li>Permite a listagem e busca por título, autor ou categoria</li>
</ul>

<h3>2. Cadastro de Usuários</h3>
<ul>
  <li>Registra usuários com nome, e-mail, ID único e tipo (aluno, professor, visitante)</li>
  <li>Utiliza dicionários, listas e conjuntos para garantir a integridade dos dados</li>
</ul>

<h3>3. Sistema de Empréstimos</h3>
<ul>
  <li>Associa um livro a um usuário com data de empréstimo</li>
  <li>Permite registro de devoluções e listagem de empréstimos ativos</li>
</ul>

<h3>4. Estatísticas e Relatórios</h3>
<ul>
  <li>Gera relatórios sobre livros por categoria</li>
  <li>Informa quantidade de empréstimos por tipo de usuário</li>
  <li>Lista os livros mais emprestados</li>
</ul>

<h3>5. Persistência de Dados</h3>
<ul>
  <li>Salva dados em arquivos CSV</li>
  <li>Carrega dados automaticamente ao iniciar o sistema</li>
</ul>

<h2>🛠️ Tecnologias & Ferramentas</h2>
<ul>
  <li><strong>Linguagem:</strong> Python</li>
  <li><strong>Interface Gráfica:</strong> Tkinter</li>
  <li><strong>Interface CLI:</strong> Rich</li>
  <li><strong>Estrutura:</strong> Padrão MVC (Model-View-Controller)</li>
  <li><strong>Controle de Versão:</strong> Git</li>
  <li><strong>IDE:</strong> Visual Studio Code</li>
</ul>

<h2>📂 Organização do Projeto</h2>
<pre>
AT1_N1_NT/
├── src/
│   ├── core/               # Lógica principal compartilhada
│   │   ├── controllers/    # Regras de negócio
│   │   └── models/         # Modelos de dados
│   ├── gui/                # Interface gráfica
│   │   ├── views/          # Telas da aplicação
│   │   └── app.py          # Ponto de entrada GUI
│   ├── cli/                # Interface de linha de comando
│   │   ├── commands/       # Implementação dos comandos
|   |   ├── views/          # Telas do console
│   │   └── app.py          # Ponto de entrada CLI
│   └── shared/             # Utilitários compartilhados
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação
└── CHANGELOG.md            # Histórico de mudanças
</pre>

<h2>🚀 Instalação e Execução</h2>

<h3>1. Clone o repositório:</h3>
<pre><code>1. git clone https://github.com/itsryu/AT1_N1_NT.git<br>
2. cd AT1_N1_NT</code></pre>

<h3>2. Instale as dependências:</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>3. Execução da Interface Gráfica (GUI):</h3>
<pre><code>python src/gui/app.py</code></pre>

<h3>4. Execução da Interface de Linha de Comando (CLI):</h3>
<pre><code>python src/cli/app.py</code></pre>

<h2>👥 Integrantes do Grupo</h2>
<div align="center">
    <table>
        <tr>
            <th>Nome</th>
            <th>Matrícula</th>
            <th>GitHub</th>
        </tr>
        <tr>
            <td>João Victor</td>
            <td>UC23103118</td>
            <td><a href="https://github.com/itsryu">itsryu</a></td>
        </tr>
        <tr>
            <td>Aline Oliveira</td>
            <td>UC23101158</td>
            <td><a href="https://github.com/alineop120">alineop120</a></td>
        </tr>
        <tr>
            <td>Cariny Saldanha</td>
            <td>UC23101592</td>
            <td><a href="https://github.com/carinysaldanha">carinysaldanha</a></td>
        </tr>
        <tr>
            <td>João Carlos Lima</td>
            <td>UC23200044</td>
            <td><a href="https://github.com/jaolimadev">jaolimadev</a></td>
        </tr>
    </table>
</div>

<h2>📜 Licença</h2>
<p>Este projeto está licenciado sob a <a href="LICENSE">MIT License</a>.</p>

<blockquote>
<p><strong>⚠️ Aviso:</strong> Ao utilizar ou modificar este projeto, mantenha os créditos dos integrantes e respeite a licença de uso.</p>
</blockquote>