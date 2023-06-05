class Agencia:
    def __init__(self, numero=None, codBanco=None, morada=None):
        self.numero = numero
        self.codBanco = codBanco
        self.morada = morada
        self.erroValidacao = ''

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero):
        if numero != None and len(numero) != 0:
            if numero.isnumeric() and int(numero) > 0:
                self.__numero = f'{numero:0>4}'
            else:
                self.erroValidacao = f'Insira um número válido!'
        else:
            self.erroValidacao = f'O campo "Número da Agência" é obrigatório!'

    @property
    def codBanco(self):
        return self.__codBanco

    @codBanco.setter
    def codBanco(self, codBanco):
        if codBanco != None and len(codBanco) != 0:
            if codBanco.isnumeric() and int(codBanco) > 0:
                self.__codBanco = f'{codBanco:0>4}'
            else:
                self.erroValidacao = f'Insira um código válido!'
        else:
            self.erroValidacao = f'O campo "Código do Banco" é obrigatório!'

    @property
    def morada(self):
        return self.__morada

    @morada.setter
    def morada(self, morada):
        if morada != None and len(morada) != 0:
            self.__morada = morada
        else:
            self.erroValidacao = f'O campo "Morada" é obrigatório!'
