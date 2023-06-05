class Banco:
    def __init__(self, codigo=None, nome=None):
        self.codigo = codigo
        self.nome = nome
        self.erroValidacao = ''

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if codigo != None and len(codigo) != 0:
            if codigo.isnumeric() and int(codigo) > 0:
                self.__codigo = f'{codigo:0>4}'
            else:
                self.erroValidacao = f'Insira um código válido!'
        else:
            self.erroValidacao = f'O campo "Código" é obrigatório!'

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if nome != None and len(nome) != 0:
            self.__nome = nome
        else:
            self.erroValidacao = f'O campo "Nome" é obrigatório!'
