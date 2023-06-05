import data.conexao as con
from datetime import datetime as dt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from model.agencia import Agencia
from model.banco import Banco
from model.cliente import Cliente
from model.conta import Conta
from model.transacao import Transacao
from view.telaGerente import Ui_MainWindow
from controller.agenciaControl import AgenciaControl
from controller.bancoControl import BancoControl
from controller.clienteControl import ClienteControl
from controller.contaControl import ContaControl
from controller.transacaoControl import TransacaoControl


class GUIGerente(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.numeroId = ''
        self.controleAgencia = AgenciaControl()
        self.controleBanco = BancoControl()
        self.controleCliente = ClienteControl()
        self.controleConta = ContaControl()
        self.controleTransacao = TransacaoControl()
        self.init_components()
        self.corSucesso = "background-color: rgb(209, 255, 209);"
        self.corErro = "background-color: rgb(250, 185, 185);"

    def init_components(self):
        self.label_logo.setPixmap(QPixmap('img\iefp-logo1.png'))
        self.pushButton_cliente.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_clientes))
        self.pushButton_conta.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_contas))
        self.pushButton_transacoes.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_transacoes))
        self.pushButton_salvarCliente.clicked.connect(self.salvarCliente)
        self.pushButton_limparCliente.clicked.connect(self.limparCliente)
        self.pushButton_editarCliente.clicked.connect(self.editarCliente)
        self.pushButton_consultarCliente.clicked.connect(self.consultarCliente)
        self.pushButton_excluirCliente.clicked.connect(self.excluirCliente)
        self.pushButton_atualizarCliente.clicked.connect(self.atualizarCliente)
        self.pushButton_voltarListaClientes.clicked.connect(
            self.voltarListaClientes)
        self.pushButton_salvarConta.clicked.connect(self.salvarConta)
        self.pushButton_limparConta.clicked.connect(self.limparConta)
        self.pushButton_editarConta.clicked.connect(self.editarConta)
        self.pushButton_consultarConta.clicked.connect(self.consultarConta)
        self.pushButton_excluirConta.clicked.connect(self.excluirConta)
        self.pushButton_atualizarConta.clicked.connect(self.atualizarConta)
        self.pushButton_voltarListaContas.clicked.connect(self.voltarListaContas)
        self.pushButton_listarTransacoes.clicked.connect(self.listarTransacoes)
        self.pushButton_excluirTransacao.clicked.connect(self.excluirTransacoes)
        self.frame_msgBar.hide()
        self.pushButton_fecharMsg.clicked.connect(
            lambda: self.frame_msgBar.hide())
        self.initBD()

    def initBD(self):
        agencias = con.selecionarDadosTabela('agencia')
        if agencias:
            for a in agencias:
                agencia = Agencia(a[1], a[2], a[3])
                self.controleAgencia.salvarAgencia(agencia)
        bancos = con.selecionarDadosTabela('banco')
        if bancos:
            for b in bancos:
                banco = Banco(b[1], b[2])
                self.controleBanco.salvarBanco(banco)
        clientes = con.selecionarDadosTabela('cliente')
        if clientes:
            for c in clientes:
                cliente = Cliente(c[1], c[2], c[3], c[4], c[5])
                self.controleCliente.salvarCliente(cliente)
        contas = con.selecionarDadosTabela('conta')
        if contas:
            for co in contas:
                conta = Conta(co[1], co[2], co[3], co[4],
                              co[5], co[6], co[7], co[8], co[9])
                self.controleConta.salvarConta(conta)
        transacoes = con.selecionarDadosTabela('transacao')
        if transacoes:
            for t in transacoes:
                transacao = Transacao(t[1], t[2], t[3], t[4])
                self.controleTransacao.salvarTransacao(transacao)
        lsAgencias = ['--- Selecione ---']
        for ag in self.controleAgencia.listaAgencias:
            lsAgencias.append(ag.morada)
        self.comboBox_agenciasConta.addItems(lsAgencias)
        lsBancos = ['--- Selecione ---']
        for bc in self.controleBanco.listaBancos:
            lsBancos.append(bc.nome)
        self.comboBox_bancosConta.addItems(lsBancos)
        tipos = ['--- Selecione ---']
        listaTiposConta = con.selecionarDadosTabela('tipoConta')
        for t in listaTiposConta:
            tipos.append(t[1])
        self.comboBox_tiposConta.addItems(tipos)
        self.listarClientes()
        self.listarContas()

    def listarClientes(self):
        contLinhas = 0
        self.tableWidget_clientes.clearContents()
        self.tableWidget_clientes.setRowCount(
            len(self.controleCliente.listaClientes))
        for cliente in self.controleCliente.listaClientes:
            self.tableWidget_clientes.setItem(
                contLinhas, 0, QTableWidgetItem(cliente.nome))
            self.tableWidget_clientes.setItem(
                contLinhas, 1, QTableWidgetItem(cliente.nif))
            self.tableWidget_clientes.setItem(
                contLinhas, 2, QTableWidgetItem(cliente.morada))
            self.tableWidget_clientes.setItem(
                contLinhas, 3, QTableWidgetItem(cliente.contato))
            self.tableWidget_clientes.setItem(
                contLinhas, 4, QTableWidgetItem(cliente.categoria))
            contLinhas += 1

    def salvarCliente(self):
        cliente = Cliente()
        cliente.nif = self.lineEdit_nifCliente.text()
        cliente.nome = self.lineEdit_nomeCliente.text()
        cliente.morada = self.lineEdit_moradaCliente.text()
        cliente.contato = self.lineEdit_contatoCliente.text()
        cliente.categoria = self.comboBox_categoriaCliente.currentText()
        if len(cliente.erroValidacao) != 0:
            self.label_msg.setText(cliente.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            if self.controleCliente.verificarCliente(cliente.nif):
                cliente.erroValidacao = f'Cliente {cliente.nif} já está cadastrado.'
            if len(cliente.erroValidacao) != 0:
                self.label_msg.setText(cliente.erroValidacao)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                campos = ['nif', 'nome', 'morada', 'contato', 'categoria']
                valores = [cliente.nif, cliente.nome,
                           cliente.morada, cliente.contato, cliente.categoria]
                con.inserirDadosTabela(
                    'cliente', campos, valores, 'nif', cliente.nif)
                msg = self.controleCliente.salvarCliente(cliente)
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                self.listarClientes()

    def limparCliente(self):
        self.lineEdit_nifCliente.clear()
        self.lineEdit_nomeCliente.clear()
        self.lineEdit_moradaCliente.clear()
        self.lineEdit_contatoCliente.clear()
        self.comboBox_categoriaCliente.setCurrentIndex(0)

    def consultarCliente(self):
        indice = self.tableWidget_clientes.currentRow()
        if indice != -1:
            clientes = con.selecionarCampoTabela('cliente', 'nif')
            nif = clientes[indice][0]
            self.numeroId = nif
            cliente = con.selecionarDadosTabela('cliente', 'nif', nif)
            self.label_consultarNifCliente.setText(cliente[0][1])
            self.label_consultarNomeCliente.setText(cliente[0][2])
            self.label_consultarMoradaCliente.setText(cliente[0][3])
            self.label_consultarContatoCliente.setText(cliente[0][4])
            self.label_consultarCategoriaCliente.setText(cliente[0][5])
            self.tabWidget_clientes.setCurrentIndex(2)
        else:
            self.label_msg.setText('Cliente não selecionado.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def voltarListaClientes(self):
        self.label_consultarNifCliente.clear()
        self.label_consultarNomeCliente.clear()
        self.label_consultarMoradaCliente.clear()
        self.label_consultarContatoCliente.clear()
        self.label_consultarCategoriaCliente.clear()
        self.numeroId = ''
        self.tabWidget_clientes.setCurrentIndex(1)

    def editarCliente(self):
        indice = self.tableWidget_clientes.currentRow()
        if indice != -1:
            clientes = con.selecionarCampoTabela('cliente', 'nif')
            nif = clientes[indice][0]
            self.numeroId = nif
            cliente = con.selecionarDadosTabela('cliente', 'nif', nif)
            self.label_editarNifCliente.setText(cliente[0][1])
            self.lineEdit_editarNomeCliente.setText(cliente[0][2])
            self.lineEdit_editarMoradaCliente.setText(cliente[0][3])
            self.lineEdit_editarContatoCliente.setText(cliente[0][4])
            self.tabWidget_clientes.setCurrentIndex(3)
        else:
            self.label_msg.setText('Cliente não selecionado.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def atualizarCliente(self):
        nif = self.numeroId
        if nif != None and len(nif) != 0:
            cliente = self.controleCliente.retornarCliente(nif)
            if cliente:
                cliente.nome = self.lineEdit_editarNomeCliente.text()
                cliente.morada = self.lineEdit_editarMoradaCliente.text()
                cliente.contato = self.lineEdit_editarContatoCliente.text()
                cliente.categoria = self.comboBox_editarCategoriaCliente.currentText()
                if len(cliente.erroValidacao) != 0:
                    self.label_msg.setText(cliente.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                    cliente.erroValidacao = ''
                else:
                    campos = ['nome', 'morada', 'contato', 'categoria']
                    valores = [cliente.nome, cliente.morada,
                               cliente.contato, cliente.categoria]
                    con.atualizarDadosTabela(
                        'cliente', 'nif', cliente.nif, campos, valores)
                    msg = 'Cliente atualizado com sucesso!'
                    self.label_msg.setText(msg)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.label_editarNifCliente.clear()
                    self.lineEdit_editarNomeCliente.clear()
                    self.lineEdit_editarMoradaCliente.clear()
                    self.lineEdit_editarContatoCliente.clear()
                    self.comboBox_editarCategoriaCliente.setCurrentIndex(0)
                    self.numeroId = ''
                    self.tabWidget_clientes.setCurrentIndex(1)
                    self.listarClientes()

    def excluirCliente(self):
        indice = self.tableWidget_clientes.currentRow()
        if indice != -1:
            clientes = con.selecionarCampoTabela('cliente', 'nif')
            nif = clientes[indice][0]
            contas = con.selecionarCampoTabela('conta', 'numero',  'nif', nif)
            if contas:
                self.label_msg.setText('Cliente possui conta(s) vinculada(s).')
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                con.excluirDadosTabela('cliente', 'nif', nif)
                msg = self.controleCliente.excluirCliente(indice)
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                self.listarClientes()
        else:
            msg = self.controleCliente.excluirCliente(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def listarContas(self):
        contLinhas = 0
        self.tableWidget_contas.clearContents()
        self.tableWidget_contas.setRowCount(
            len(self.controleConta.listaContas))
        for conta in self.controleConta.listaContas:
            self.tableWidget_contas.setItem(
                contLinhas, 0, QTableWidgetItem(conta.numero))
            self.tableWidget_contas.setItem(
                contLinhas, 1, QTableWidgetItem(conta.tipoConta))
            self.tableWidget_contas.setItem(
                contLinhas, 2, QTableWidgetItem(conta.nif))
            self.tableWidget_contas.setItem(
                contLinhas, 3, QTableWidgetItem(conta.codBanco))
            self.tableWidget_contas.setItem(
                contLinhas, 4, QTableWidgetItem(conta.numAgencia))
            self.tableWidget_contas.setItem(
                contLinhas, 5, QTableWidgetItem(conta.nib))
            self.tableWidget_contas.setItem(
                contLinhas, 6, QTableWidgetItem(conta.iban))
            self.tableWidget_contas.setItem(
                contLinhas, 7, QTableWidgetItem(f'{conta.saldo:10,.2f}'))
            self.tableWidget_contas.setItem(contLinhas, 8, QTableWidgetItem(
                conta.dataAbertura.strftime('%d/%m/%Y')))
            contLinhas += 1

    def salvarConta(self):
        conta = Conta()
        conta.nif = self.lineEdit_nifConta.text()
        conta.saldo = self.doubleSpinBox_saldoConta.value()
        conta.dataAbertura = dt.today()
        if len(conta.erroValidacao) != 0:
            self.label_msg.setText(conta.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            tipoConta = self.comboBox_tiposConta.currentText()
            nomeBanco = self.comboBox_bancosConta.currentText()
            moradaAgencia = self.comboBox_agenciasConta.currentText()
            if not self.controleCliente.verificarCliente(conta.nif):
                conta.erroValidacao = f'Cliente {conta.nif} não está cadastrado.'
            if len(tipoConta) == 0 or 'Selecione' in tipoConta:
                conta.erroValidacao = f'Selecione o Tipo de Conta.'
            if len(nomeBanco) == 0 or 'Selecione' in nomeBanco:
                conta.erroValidacao = f'Selecione o Banco.'
            if len(moradaAgencia) == 0 or 'Selecione' in moradaAgencia:
                conta.erroValidacao = f'Selecione a Agência.'
            if len(conta.erroValidacao) != 0:
                self.label_msg.setText(conta.erroValidacao)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                conta.tipoConta = tipoConta
                banco = con.selecionarCampoTabela(
                    'banco', 'codigo', 'nome', nomeBanco)
                conta.codBanco = banco[0][0]
                agencia = con.selecionarCampoTabela(
                    'agencia', 'numero', 'morada', moradaAgencia)
                conta.numAgencia = agencia[0][0]
                lista = self.controleConta.gerarContaNibIban(
                    conta.codBanco, conta.numAgencia)
                if lista:
                    conta.numero = lista[0]
                    conta.nib = lista[1]
                    conta.iban = lista[2]
                    self.label_numConta.setText(conta.numero)
                    self.label_nibConta.setText(conta.nib)
                    self.label_ibanConta.setText(conta.iban)
                    self.label_dataAberturaConta.setText(
                        conta.dataAbertura.strftime('%d/%m/%Y'))
                    if len(conta.erroValidacao) != 0:
                        self.label_msg.setText(conta.erroValidacao)
                        self.frame_msgBar.show()
                        self.label_msg.setStyleSheet(self.corErro)
                    else:
                        campos = ['numero', 'tipo', 'nif', 'cod_banco',
                                  'num_agencia', 'nib', 'iban', 'saldo', 'data_abertura']
                        valores = [conta.numero, conta.tipoConta, conta.nif, conta.codBanco,
                                   conta.numAgencia, conta.nib, conta.iban, conta.saldo,
                                   conta.dataAbertura]
                        con.inserirDadosTabela(
                            'conta', campos, valores, 'numero', conta.numero)
                        msg = self.controleConta.salvarConta(conta)
                        self.label_msg.setText(msg)
                        self.frame_msgBar.show()
                        self.label_msg.setStyleSheet(self.corSucesso)
                        self.listarContas()

    def limparConta(self):
        self.lineEdit_nifConta.clear()
        self.label_numConta.clear()
        self.label_nibConta.clear()
        self.label_ibanConta.clear()
        self.label_dataAberturaConta.clear()
        self.doubleSpinBox_saldoConta.clear()
        self.comboBox_agenciasConta.setCurrentIndex(0)
        self.comboBox_bancosConta.setCurrentIndex(0)
        self.comboBox_tiposConta.setCurrentIndex(0)

    def consultarConta(self):
        indice = self.tableWidget_contas.currentRow()
        if indice != -1:
            contas = con.selecionarCampoTabela('conta', 'numero')
            numero = contas[indice][0]
            self.numeroId = numero
            conta = con.selecionarDadosTabela('conta', 'numero', numero)
            self.label_consultarNumConta.setText(conta[0][1])
            self.label_consultarTipoConta.setText(conta[0][2])
            self.label_consultarNifConta.setText(conta[0][3])
            self.label_consultarBancoConta.setText(conta[0][4])
            self.label_consultarAgenciaConta.setText(conta[0][5])
            self.label_consultarNibConta.setText(conta[0][6])
            self.label_consultarIbanConta.setText(conta[0][7])
            self.label_consultarSaldoConta.setText(f'€{conta[0][8]:10,.2f}')
            self.label_consultarDataAberturaConta.setText(
                conta[0][9].strftime('%d/%m/%Y'))
            self.tabWidget_contas.setCurrentIndex(2)
        else:
            self.label_msg.setText('Conta não selecionada.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def voltarListaContas(self):
        self.label_consultarNumConta.clear()
        self.label_consultarTipoConta.clear()
        self.label_consultarNifConta.clear()
        self.label_consultarBancoConta.clear()
        self.label_consultarAgenciaConta.clear()
        self.label_consultarNibConta.clear()
        self.label_consultarIbanConta.clear()
        self.label_consultarSaldoConta.clear()
        self.label_consultarDataAberturaConta.clear()
        self.numeroId = ''
        self.tabWidget_contas.setCurrentIndex(1)

    def editarConta(self):
        indice = self.tableWidget_contas.currentRow()
        if indice != -1:
            contas = con.selecionarCampoTabela('conta', 'numero')
            numero = contas[indice][0]
            self.numeroId = numero
            conta = con.selecionarDadosTabela('conta', 'numero', numero)
            self.label_editarNumConta.setText(conta[0][1])
            self.label_editarTipoConta.setText(conta[0][2])
            self.label_editarNifConta.setText(conta[0][3])
            self.label_editarBancoConta.setText(conta[0][4])
            self.label_editarAgenciaConta.setText(conta[0][5])
            self.label_editarNibConta.setText(conta[0][6])
            self.label_editarIbanConta.setText(conta[0][7])
            self.doubleSpinBox_editarSaldoConta.setValue(conta[0][8])
            self.label_editarDataAberturaConta.setText(
                conta[0][9].strftime('%d/%m/%Y'))
            self.tabWidget_contas.setCurrentIndex(3)
        else:
            self.label_msg.setText('Conta não selecionada.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def atualizarConta(self):
        numero = self.numeroId
        if numero != None and len(numero) != 0:
            conta = self.controleConta.retornarConta(numero)
            if conta:
                conta.saldo = self.doubleSpinBox_editarSaldoConta.value()
                if len(conta.erroValidacao) != 0:
                    self.label_msg.setText(conta.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                    conta.erroValidacao = ''
                else:
                    campos = ['saldo']
                    valores = [conta.saldo]
                    con.atualizarDadosTabela(
                        'conta', 'numero', conta.numero, campos, valores)
                    msg = 'Conta atualizada com sucesso!'
                    self.label_msg.setText(msg)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.label_editarNumConta.clear()
                    self.label_editarTipoConta.clear()
                    self.label_editarNifConta.clear()
                    self.label_editarBancoConta.clear()
                    self.label_editarAgenciaConta.clear()
                    self.label_editarNibConta.clear()
                    self.label_editarIbanConta.clear()
                    self.doubleSpinBox_editarSaldoConta.clear()
                    self.label_editarDataAberturaConta.clear()
                    self.numeroId = ''
                    self.tabWidget_contas.setCurrentIndex(1)
                    self.listarContas()

    def excluirConta(self):
        indice = self.tableWidget_contas.currentRow()
        if indice != -1:
            contas = con.selecionarCampoTabela('conta', 'numero')
            numero = contas[indice][0]
            transacoes = con.selecionarDadosTabela('transacao', 'num_conta', numero)
            if transacoes:
                self.label_msg.setText('Conta possui transações vinculadas.')
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                con.excluirDadosTabela('conta', 'numero', numero)
                msg = self.controleConta.excluirConta(indice)
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                self.listarContas()

    def listarTransacoes(self):
        numConta = self.lineEdit_transacaoNumConta.text()
        self.numeroId = numConta
        if numConta != None and len(numConta) != 0:
            transacao = Transacao()
            transacao.numConta = numConta
            dataInicial = self.dateEdit_transacaoDataInicial.date()
            dataFinal = self.dateEdit_transacaoDataFinal.date()
            if len(transacao.erroValidacao) != 0:
                self.label_msg.setText(transacao.erroValidacao)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                if not self.controleConta.verificarConta(transacao.numConta):
                    transacao.erroValidacao = f'Conta {transacao.numConta} não existe.'
                    self.label_msg.setText(transacao.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                else:
                    contLinhas = 0
                    self.tableWidget_transacoes.clearContents()
                    self.tableWidget_transacoes.setRowCount(
                        len(self.controleTransacao.listaTransacoes))
                    for t in self.controleTransacao.listaTransacoes:
                        if t.numConta == transacao.numConta and (dataInicial <= t.data <= dataFinal):
                            self.tableWidget_transacoes.setItem(
                                contLinhas, 0, QTableWidgetItem(t.numConta))
                            self.tableWidget_transacoes.setItem(
                                contLinhas, 1, QTableWidgetItem(t.descricao))
                            self.tableWidget_transacoes.setItem(
                                contLinhas, 2, QTableWidgetItem(f'€{t.valor:10,.2f}'))
                            self.tableWidget_transacoes.setItem(contLinhas, 3, QTableWidgetItem(
                                t.data.strftime('%d/%m/%Y')))
                            contLinhas += 1
        else:
            contLinhas = 0
            self.tableWidget_transacoes.clearContents()
            self.tableWidget_transacoes.setRowCount(
                len(self.controleTransacao.listaTransacoes))
            for transacao in self.controleTransacao.listaTransacoes:
                self.tableWidget_transacoes.setItem(
                    contLinhas, 0, QTableWidgetItem(transacao.numConta))
                self.tableWidget_transacoes.setItem(
                    contLinhas, 1, QTableWidgetItem(transacao.descricao))
                self.tableWidget_transacoes.setItem(
                    contLinhas, 2, QTableWidgetItem(f'€{transacao.valor:10,.2f}'))
                self.tableWidget_transacoes.setItem(contLinhas, 3, QTableWidgetItem(
                    transacao.data.strftime('%d/%m/%Y')))
                contLinhas += 1
        self.tabWidget_transacoes.setCurrentIndex(1)

    def excluirTransacoes(self):
        numConta = self.numeroId
        transacoes = con.selecionarDadosTabela('transacao', 'num_conta', numConta)
        if not transacoes:
            self.label_msg.setText('Conta não possui transações vinculadas.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            con.excluirDadosTabela('transacao', 'num_conta', numConta)
            msg = self.controleTransacao.excluirTransacoes(numConta)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corSucesso)
        self.tableWidget_transacoes.clearContents()
        self.numeroId = ''
        self.tabWidget_transacoes.setCurrentIndex(0)
