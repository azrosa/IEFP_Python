class Conta:
    def __init__(self, numero=None, tipoConta=None, nif=None, codBanco=None, numAgencia=None, nib=None, iban=None, saldo=None, dataAbertura=None):
        self.numero = numero
        self.tipoConta = tipoConta
        self.nif = nif
        self.codBanco = codBanco
        self.numAgencia = numAgencia
        self.nib = nib
        self.iban = iban
        self.saldo = saldo
        self.dataAbertura = dataAbertura
        self.erroValidacao = ''

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero):
        if numero != None and len(numero) != 0:
            if numero.isnumeric() and (10**9 < int(numero) < 10**11):
                self.__numero = f'{numero:0>11}'
            else:
                self.erroValidacao = f'Insira um Número de conta válido!'
        else:
            self.erroValidacao = f'O campo "Número da Conta" é obrigatório!'

    @property
    def nif(self):
        return self.__nif

    @nif.setter
    def nif(self, nif):
        if nif != None and len(nif) != 0:
            if nif.isnumeric() and (10**7 < int(nif) < 10**9):
                self.__nif = f'{nif:0>9}'
            else:
                self.erroValidacao = f'Insira um NIF válido!'
        else:
            self.erroValidacao = f'O campo "NIF" é obrigatório!'

    @property
    def codBanco(self):
        return self.__codBanco

    @codBanco.setter
    def codBanco(self, codBanco):
        if codBanco != None and len(codBanco) != 0:
            if codBanco.isnumeric() and (0 < int(codBanco) < 10**4):
                self.__codBanco = codBanco
            else:
                self.erroValidacao = f'Selecione um banco!'
        else:
            self.erroValidacao = f'O campo "Banco" é obrigatório!'

    @property
    def numAgencia(self):
        return self.__numAgencia

    @numAgencia.setter
    def numAgencia(self, numAgencia):
        if numAgencia != None and len(numAgencia) != 0:
            if numAgencia.isnumeric() and (0 < int(numAgencia) < 10**4):
                self.__numAgencia = numAgencia
            else:
                self.erroValidacao = f'Selecione uma agência!'
        else:
            self.erroValidacao = f'O campo "Agência" é obrigatório!'

    @property
    def nib(self):
        return self.__nib

    @nib.setter
    def nib(self, nib):
        if nib != None and len(nib) != 0:
            self.__nib = nib
        else:
            self.erroValidacao = f'O campo "NIB" é obrigatório!'

    @property
    def iban(self):
        return self.__iban

    @iban.setter
    def iban(self, iban):
        if iban != None and len(iban) != 0:
            self.__iban = iban
        else:
            self.erroValidacao = f'O campo "IBAN" é obrigatório!'

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo):
        if saldo != 0:
            self.__saldo = saldo
        else:
            self.erroValidacao = f'O campo "Saldo" é obrigatório!'

    @property
    def dataAbertura(self):
        return self.__dataAbertura

    @dataAbertura.setter
    def dataAbertura(self, dataAbertura):
        if dataAbertura != None:
            self.__dataAbertura = dataAbertura
        else:
            self.erroValidacao = f'O campo "Data de Abertura" é obrigatório!'

    def depositar(self, valor):
        self.saldo += valor
        return f"Depósito de €{valor:,.2f} realizado com sucesso."

    def levantar(self, valor):
        if self.saldo < valor:
            return False
        else:
            self.saldo -= valor
            return f"Levantamento de €{valor:,.2f} realizado com sucesso."
