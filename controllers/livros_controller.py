from models.livro import Livro
from utils.file_manager import FileManager

class LivrosController:
    def __init__(self):
        self.file_manager = FileManager('livros.csv', 
                                      ['Título', 'Autor', 'Ano', 'ISBN', 'Categoria'])

    def cadastrar_livro(self, livro_data):
        # Garante que as chaves estão no formato correto
        livro_data_formatada = {
            'Título': livro_data.get('Título', livro_data.get('Titulo', '')),
            'Autor': livro_data.get('Autor', ''),
            'Ano': livro_data.get('Ano', ''),
            'ISBN': livro_data.get('ISBN', ''),
            'Categoria': livro_data.get('Categoria', '')
        }
        livro = Livro(**livro_data_formatada)
        self.file_manager.add_data(livro.to_dict())
        return True

    def listar_livros(self):
        return self.file_manager.load_data()

    def buscar_livros(self, keyword):
        livros = self.listar_livros()
        return [livro for livro in livros if 
                keyword.lower() in ' '.join(str(v) for v in livro.values()).lower()]