class Usuario:
    TIPOS_PERMITIDOS = ('aluno', 'professor', 'visitante')
    
    def __init__(self, nome, email, id_usuario, tipo):
        if tipo not in self.TIPOS_PERMITIDOS:
            raise ValueError(f"Tipo de usuário inválido. Deve ser um dos: {self.TIPOS_PERMITIDOS}")
        
        self.nome = nome
        self.email = email
        self.id_usuario = id_usuario
        self.tipo = tipo

    def to_dict(self):
        return {
            'Nome': self.nome,
            'Email': self.email,
            'ID': self.id_usuario,
            'Tipo': self.tipo
        }