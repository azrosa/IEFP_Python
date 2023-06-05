class ContaControl:
    def __init__(self) -> None:
        self.listaContas = []

    @property
    def listaContas(self):
        return self.__listaContas

    @listaContas.setter
    def listaContas(self, listaContas):
        self.__listaContas = []

    def verificarConta(self, numero):
        valida = False
        for conta in self.listaContas:
            if numero == conta.numero:
                valida = True
        return valida

    def retornarConta(self, numero):
        for conta in self.listaContas:
            if conta.numero == numero:
                return conta
        return False

    # Função para gera número de conta válido, o NIB e o IBAN desta conta.
    def gerarContaNibIban(self, banco, agencia):
        for i in range(10**9, 10**10):
            if len(str(i)) == 10:
                conta = f'{i:0>11}'
                valNumber = int(banco + '00' + conta + str(2529) + '50')
                if  (valNumber % 97) == 1:
                    if not self.verificarConta(conta):
                        break
        nib = banco + agencia + '00' + conta
        iban = 'PT50' + nib
        return [conta, nib, iban]

    def salvarConta(self, conta):
        self.listaContas.append(conta)
        return 'Conta salva com sucesso!'

    def atualizarConta(self, numero, tipoConta, nif, codBanco, numAgencia, nib, iban, saldo, dataAbertura):
        for conta in self.listaContas:
            if conta.numero == numero:
                conta.tipoConta = tipoConta
                conta.nif = nif
                conta.codBanco = codBanco
                conta.numAgencia = numAgencia
                conta.nib = nib
                conta.iban = iban
                conta.saldo = saldo
                conta.dataAbertura = dataAbertura
                return 'Conta atualizada com sucesso!'
        return 'Conta não selecionada'

    def excluirConta(self, indice):
        if indice != -1:
            del self.listaContas[indice]
            return 'Conta removida com sucesso!'
        return 'Conta não selecionada.'