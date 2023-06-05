class Cliente:
    def __init__(self, nif=None, nome=None, morada=None, contato=None, categoria=None):
        self.nif = nif
        self.nome = nome
        self.morada = morada
        self.contato = contato
        self.categoria = categoria
        self.erroValidacao = ''

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
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if nome != None and len(nome) != 0:
            self.__nome = nome
        else:
            self.erroValidacao = f'O campo "Nome" é obrigatório!'

    @property
    def morada(self):
        return self.__morada

    @morada.setter
    def morada(self, morada):
        if morada != None and len(morada) != 0:
            self.__morada = morada
        else:
            self.erroValidacao = f'O campo "Morada" é obrigatório!'

    @property
    def contato(self):
        return self.__contato

    @contato.setter
    def contato(self, contato):
        if contato != None and len(contato) != 0:
            if contato.isnumeric() and (10**8 < int(contato) < 10**9):
                self.__contato = f'{contato:09s}'
            else:
                self.erroValidacao = f'Insira um contato válido!'
        else:
            self.erroValidacao = f'O campo "Contato" é obrigatório!'

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        if categoria != None and 'Selecione' not in categoria:
            self.__categoria = categoria
        else:
            self.erroValidacao = f'O campo "Categoria" é obrigatório!'
