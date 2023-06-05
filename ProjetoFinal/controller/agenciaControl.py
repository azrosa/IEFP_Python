class AgenciaControl:
    def __init__(self) -> None:
        self.listaAgencias = []

    @property
    def listaAgencias(self):
        return self.__listaAgencias

    @listaAgencias.setter
    def listaAgencias(self, listaAgencias):
        self.__listaAgencias = []

    def verificarAgencia(self, numero):
        valida = False
        for agencia in self.listaAgencias:
            if numero == agencia.numero:
                valida = True
        return valida

    def retornarAgencia(self, numero):
        for agencia in self.listaAgencias:
            if agencia.numero == numero:
                return agencia
        return False

    def salvarAgencia(self, agencia):
        self.listaAgencias.append(agencia)
        return 'Agência salva com sucesso!'

    def excluirAgencia(self, indice):
        if indice != -1:
            del self.listaAgencias[indice]
            return 'Agência removida com sucesso!'
        return 'Agência não selecionada.'
