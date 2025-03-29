from collections import defaultdict
from controllers.livros_controller import LivrosController
from controllers.usuarios_controller import UsuariosController
from controllers.emprestimos_controller import EmprestimosController

class EstatisticasController:
    def __init__(self):
        self.livros_ctrl = LivrosController()
        self.usuarios_ctrl = UsuariosController()
        self.emprestimos_ctrl = EmprestimosController()

    def livros_por_categoria(self):
        """Retorna um dicionário com a contagem de livros por categoria"""
        livros = self.livros_ctrl.listar_livros()
        categorias = defaultdict(int)
        
        for livro in livros:
            categoria = livro['Categoria']
            categorias[categoria] += 1
            
        return dict(sorted(categorias.items(), key=lambda item: item[1], reverse=True))

    def emprestimos_por_tipo_usuario(self):
        """Retorna um dicionário com a contagem de empréstimos por tipo de usuário"""
        usuarios = {u['ID']: u['Tipo'] for u in self.usuarios_ctrl.listar_usuarios()}
        emprestimos = self.emprestimos_ctrl.listar_emprestimos()
        
        tipos = defaultdict(int)
        
        for emp in emprestimos:
            tipo = usuarios.get(emp['UserID'], 'desconhecido')
            tipos[tipo] += 1
            
        return dict(sorted(tipos.items(), key=lambda item: item[1], reverse=True))

    def livros_mais_emprestados(self, limit=10):
        """Retorna uma lista ordenada dos livros mais emprestados"""
        livros = {l['ISBN']: {
            'titulo': l['Título'],
            'autor': l['Autor'],
            'categoria': l['Categoria']
        } for l in self.livros_ctrl.listar_livros()}
        
        emprestimos = self.emprestimos_ctrl.listar_emprestimos()
        
        contagem = defaultdict(int)
        for emp in emprestimos:
            contagem[emp['ISBN']] += 1
        
        # Ordena por quantidade de empréstimos (decrescente)
        livros_ordenados = sorted(
            contagem.items(),
            key=lambda item: item[1],
            reverse=True
        )[:limit]
        
        # Formata o resultado com informações completas
        resultado = []
        for isbn, qtd in livros_ordenados:
            livro_info = livros.get(isbn, {
                'titulo': 'Desconhecido',
                'autor': 'Desconhecido',
                'categoria': 'Desconhecido'
            })
            resultado.append({
                'titulo': livro_info['titulo'],
                'autor': livro_info['autor'],
                'categoria': livro_info['categoria'],
                'isbn': isbn,
                'emprestimos': qtd
            })
        
        return resultado

    def tempo_medio_emprestimo(self):
        """Calcula o tempo médio de empréstimo para livros já devolvidos"""
        emprestimos = self.emprestimos_ctrl.listar_emprestimos()
        tempos = []
        
        for emp in emprestimos:
            if emp['DataDevolucao']:
                try:
                    dt_emp = emp['DataEmprestimo']
                    dt_dev = emp['DataDevolucao']
                    
                    # Converter strings para datetime e calcular diferença
                    from datetime import datetime
                    dt_emp = datetime.strptime(dt_emp, "%Y-%m-%d %H:%M:%S")
                    dt_dev = datetime.strptime(dt_dev, "%Y-%m-%d %H:%M:%S")
                    delta = (dt_dev - dt_emp).days
                    tempos.append(delta)
                except:
                    continue
        
        if not tempos:
            return 0
            
        return sum(tempos) / len(tempos)

    def usuarios_mais_ativos(self, limit=5):
        """Retorna os usuários que mais fizeram empréstimos"""
        usuarios = {u['ID']: {
            'nome': u['Nome'],
            'tipo': u['Tipo']
        } for u in self.usuarios_ctrl.listar_usuarios()}
        
        emprestimos = self.emprestimos_ctrl.listar_emprestimos()
        
        contagem = defaultdict(int)
        for emp in emprestimos:
            contagem[emp['UserID']] += 1
        
        # Ordena por quantidade de empréstimos (decrescente)
        usuarios_ordenados = sorted(
            contagem.items(),
            key=lambda item: item[1],
            reverse=True
        )[:limit]
        
        # Formata o resultado com informações completas
        resultado = []
        for user_id, qtd in usuarios_ordenados:
            user_info = usuarios.get(user_id, {
                'nome': 'Desconhecido',
                'tipo': 'desconhecido'
            })
            resultado.append({
                'nome': user_info['nome'],
                'tipo': user_info['tipo'],
                'user_id': user_id,
                'emprestimos': qtd
            })
        
        return resultado