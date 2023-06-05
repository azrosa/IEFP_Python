from hashlib import sha256


class Utilizador:
    def __init__(self, nome=None, senha=None, cargo=None):
        self.nome = nome
        self.senha = senha
        self.cargo = cargo
        self.erroValidacao = ''

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if nome != None and len(nome) != 0:
            self.__nome = nome
        else:
            self.erroValidacao = f'O campo "Nome" é obrigatório!'

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha):
        if senha != None and len(senha) != 0:
            self.__senha = sha256(senha.encode()).hexdigest()
        else:
            self.erroValidacao = f'O campo "Senha" é obrigatório!'

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo):
        if cargo != None and len(cargo) != 0:
            self.__cargo = cargo
        else:
            self.erroValidacao = f'O campo "Cargo" é obrigatório!'
