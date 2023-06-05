class UserControl:
    def __init__(self) -> None:
        self.listaUtilizadores = []

    @property
    def listaUtilizadores(self):
        return self.__listaUtilizadores

    @listaUtilizadores.setter
    def listaUtilizadores(self, listaUtilizadores):
        self.__listaUtilizadores = []

    def verificarUtilizador(self, nome):
        valida = False
        for user in self.listaUtilizadores:
            if user.nome == nome:
                valida = True
        return valida

    def retornarUtilizador(self, nome):
        for user in self.listaUtilizadores:
            if user.nome == nome:
                return user
        return False

    def salvarUtilizador(self, utilizador):
        self.listaUtilizadores.append(utilizador)
        return 'Utilizador salvo com sucesso!'

    def excluirUtilizador(self, indice):
        if indice != -1:
            del self.listaUtilizadores[indice]
            return 'Utilizador removido com sucesso!'
        return 'Utilizador não selecionado.'
