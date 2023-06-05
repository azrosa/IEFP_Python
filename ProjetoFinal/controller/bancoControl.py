class BancoControl:
    def __init__(self) -> None:
        self.listaBancos = []

    @property
    def listaBancos(self):
        return self.__listaBancos

    @listaBancos.setter
    def listaBancos(self, listaBancos):
        self.__listaBancos = []

    def verificarBanco(self, codigo):
        valida = False
        for banco in self.listaBancos:
            if codigo == banco.codigo:
                valida = True
        return valida

    def retornarBanco(self, codigo):
        for banco in self.listaBancos:
            if banco.codigo == codigo:
                return banco
        return False

    def salvarBanco(self, banco):
        self.listaBancos.append(banco)
        return 'Banco salvo com sucesso!'

    def excluirBanco(self, indice):
        if indice != -1:
            del self.listaBancos[indice]
            return 'Banco removido com sucesso!'
        return 'Banco não selecionado.'
