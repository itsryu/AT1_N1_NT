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
  <li><strong>Estrutura:</strong> Padrão MVC (Model-View-Controller)</li>
  <li><strong>Controle de Versão:</strong> Git</li>
  <li><strong>IDE:</strong> Visual Studio Code</li>
</ul>

<h2>📂 Organização do Projeto</h2>
<pre>
AT1_N1_NT/
├── controllers/          # Lógica de controle e intermedia a comunicação entre models e views
├── models/               # Estruturas de dados
├── views/                # Interfaces gráficas (páginas)
│   ├── livros_view.py
│   ├── usuarios_view.py
│   ├── emprestimos_view.py
│   └── estatisticas_view.py
├── main.py               # Ponto de entrada
└── README.md             # Documentação
</pre>

<h2>🚀 Instalação e Execução</h2>

<h3>1. Clone o repositório:</h3>
<pre><code>git clone https://github.com/itsryu/AT1_N1_NT.git
cd AT1_N1_NT</code></pre>

<h3>2. Execute a aplicação:</h3>
<pre><code>python main.py</code></pre>

<h2>👥 Integrantes do Grupo</h2>
<div align="center">
    <table>
        <tr>
            <th>Nome Completo</th>
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
    </table>
</div>

</details>

<h2>📜 Licença</h2>
<p>Este projeto está licenciado sob a <a href="LICENSE">MIT License</a>.</p>

<blockquote>
<p><strong>⚠️ Aviso:</strong> Ao utilizar ou modificar este projeto, mantenha os créditos dos integrantes e respeite a licença de uso.</p>
</blockquote>