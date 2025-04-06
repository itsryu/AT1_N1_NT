# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2025-04-03

### Adicionado
- Nova interface de linha de comando (CLI) completa
  - Comandos para todas as operações do sistema
  - Modo interativo e execução direta de comandos
  - Sistema de ajuda integrado
- Estrutura do projeto reorganizada:
  - `src/cli/` para a interface de linha de comando
  - `src/gui/` para a interface gráfica
  - `src/core/` contendo a lógica central compartilhada
  - `src/shared/` com utilitários comuns a ambas interfaces
- Novos módulos no core:
  - `controllers/` para regras de negócio
  - `models/` para entidades do sistema
- Documentação ampliada incluindo guia de uso da CLI

### Alterado
- Refatoração completa da arquitetura para suportar múltiplas interfaces
- Melhoria no sistema de logging compartilhado
- Atualização das dependências no `requirements.txt`

### Removido
- Código duplicado entre interfaces
- Implementações obsoletas na pasta `data/`

### Correções
- Problemas de importação entre módulos
- Otimização no carregamento de recursos

## [1.0.1] - 2025-04-01

### Adicionado
- Arquivo `CHANGELOG.md` para documentação de mudanças

### Removido
- Pasta `data/` obsoleta

## [1.0.0] - 2025-03-25

### Adicionado
- Primeira versão estável do sistema
- Funcionalidades básicas de gerenciamento:
  - Cadastro de livros
  - Registro de usuários
  - Controle de empréstimos
- Interface gráfica com Tkinter

---

### Notas sobre a versão 2.0.0:
Esta versão representa uma grande evolução na arquitetura do sistema, permitindo agora:
- Uso tanto via interface gráfica quanto linha de comando
- Melhor organização do código fonte
- Maior facilidade de manutenção
- Preparação para futuras expansões

As mudanças na estrutura de pastas refletem as boas práticas de organização de projetos Python modernos, separando claramente:
- A lógica de negócio (`core`)
- As interfaces com o usuário (`gui` e `cli`)
- Os recursos compartilhados (`shared`)