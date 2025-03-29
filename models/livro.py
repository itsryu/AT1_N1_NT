class Livro:
    def __init__(self, Título, Autor, Ano, ISBN, Categoria):
        self.Título = Título
        self.Autor = Autor
        self.Ano = Ano
        self.ISBN = ISBN
        self.Categoria = Categoria

    def to_dict(self):
        return {
            'Título': self.Título,
            'Autor': self.Autor,
            'Ano': self.Ano,
            'ISBN': self.ISBN,
            'Categoria': self.Categoria
        }