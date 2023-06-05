class ClienteControl:
    def __init__(self) -> None:
        self.listaClientes = []

    @property
    def listaClientes(self):
        return self.__listaClientes

    @listaClientes.setter
    def listaClientes(self, listaClientes):
        self.__listaClientes = []

    def verificarCliente(self, nif):
        valida = False
        for cliente in self.listaClientes:
            if nif == cliente.nif:
                valida = True
        return valida

    def retornarCliente(self, nif):
        for cliente in self.listaClientes:
            if nif == cliente.nif:
                return cliente
        return False

    def salvarCliente(self, cliente):
        self.listaClientes.append(cliente)
        return 'Cliente salvo com sucesso!'

    def atualizarCliente(self, nif, nome, morada, contato, categoria):
        for cliente in self.listaClientes:
            if cliente.nif == nif:
                cliente.nome = nome
                cliente.morada = morada
                cliente.contato = contato
                cliente.categoria = categoria
                return 'Cliente atualizado com sucesso!'
        return 'Cliente não selecionado'

    def excluirCliente(self, indice):
        if indice != -1:
            del self.listaClientes[indice]
            return 'Cliente removido com sucesso!'
        return 'Cliente não selecionado.'
