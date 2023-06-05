class TransacaoControl:
    def __init__(self) -> None:
        self.listaTransacoes = []

    def salvarTransacao(self, transacao):
        self.listaTransacoes.append(transacao)
        return 'Transação salva com sucesso!'

    @property
    def listaTransacoes(self):
        return self.__listaTransacoes

    @listaTransacoes.setter
    def listaTransacoes(self, listaTransacoes):
        self.__listaTransacoes = []

    def verificarTransacao(self, numConta):
        valida = False
        for transacao in self.listaTransacoes:
            if numConta == transacao.numConta:
                valida = True
        return valida

    def salvarTransacao(self, transacao):
        self.listaTransacoes.append(transacao)
        return 'Transação salva com sucesso!'

    def excluirTransacao(self, indice):
        if indice != -1:
            del self.listaTransacoes[indice]
            return 'Transação removida com sucesso!'
        return 'Transação não selecionada.'

    def excluirTransacoes(self, numConta):
        count = 0
        for indice, transacao in enumerate(self.listaTransacoes):
            if transacao.numConta == numConta:
                del self.listaTransacoes[indice]
                count += 1
        if count == len(self.listaTransacoes):
            return 'Nenhum transação removida.'
        else:
            diferenca = len(self.listaTransacoes) - count
            return f'{diferenca} transações removidas com sucesso!'
