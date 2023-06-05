class Transacao:
    def __init__(self, numConta=None, descricao=None, valor=None, data=None):
        self.numConta = numConta
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.erroValidacao = ''

    @property
    def numConta(self):
        return self.__numConta

    @numConta.setter
    def numConta(self, numConta):
        if numConta != None and len(numConta) != 0:
            if numConta.isnumeric() and (10**9 < int(numConta) < 10**11):
                self.__numConta = f'{numConta:0>11}'
            else:
                self.erroValidacao = f'Insira um número válido!'
        else:
            self.erroValidacao = f'O campo "Número da Conta" é obrigatório!'

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if descricao != None and len(descricao) > 3:
            self.__descricao = descricao
        else:
            self.erroValidacao = f'O campo "Descrição" é obrigatório!'

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if valor != 0:
            self.__valor = valor
        else:
            self.erroValidacao = f'O campo "Valor" é obrigatório!'

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if data != None:
            self.__data = data
        else:
            self.erroValidacao = f'O campo "Data" é obrigatório!'
