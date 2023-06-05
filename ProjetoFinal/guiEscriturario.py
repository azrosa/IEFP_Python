import data.conexao as con
from datetime import datetime as dt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from model.agencia import Agencia
from model.banco import Banco
from model.cliente import Cliente
from model.conta import Conta
from model.transacao import Transacao
from view.telaEscriturario import Ui_MainWindow
from controller.agenciaControl import AgenciaControl
from controller.bancoControl import BancoControl
from controller.clienteControl import ClienteControl
from controller.contaControl import ContaControl
from controller.transacaoControl import TransacaoControl


class GUIEscriturario(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.numeroId = ''
        self.controleCliente = ClienteControl()
        self.controleConta = ContaControl()
        self.controleTransacao = TransacaoControl()
        self.corSucesso = "background-color: rgb(209, 255, 209);"
        self.corErro = "background-color: rgb(250, 185, 185);"
        self.init_components()

    def init_components(self):
        self.label_logo.setPixmap(QPixmap('img\iefp-logo1.png'))
        self.pushButton_cliente.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_cliente))
        self.pushButton_conta.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_conta))
        self.pushButton_deposito.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_deposito))
        self.pushButton_levantamento.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_levantamento))
        self.pushButton_transacoes.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_transacoes))
        self.pushButton_consultarCliente.clicked.connect(self.consultarCliente)
        self.pushButton_voltarConsultaCliente.clicked.connect(self.voltarConsultaCliente)
        self.pushButton_consultarConta.clicked.connect(self.consultarConta)
        self.pushButton_voltarConsultaConta.clicked.connect(self.voltarConsultaConta)
        self.pushButton_salvarDeposito.clicked.connect(self.salvarDeposito)
        self.pushButton_voltarDepositar.clicked.connect(self.voltarDepositar)
        self.pushButton_salvarLevantamento.clicked.connect(self.salvarLevantamento)
        self.pushButton_voltarLevantar.clicked.connect(self.voltarLevantar)
        self.pushButton_listarTransacoes.clicked.connect(self.listarTransacoesConta)
        self.frame_msgBar.hide()
        self.pushButton_fecharMsg.clicked.connect(
            lambda: self.frame_msgBar.hide())
        self.initBD()

    def initBD(self):
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

    def consultarCliente(self):
        validarCliente = Cliente()
        validarCliente.nif = self.lineEdit_consultaNifCliente.text()
        if len(validarCliente.erroValidacao) != 0:
            self.label_msg.setText(validarCliente.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            validar = self.controleCliente.verificarCliente(validarCliente.nif)
            if not validar:
                self.label_msg.setText('Cliente não existe.')
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                cliente = con.selecionarDadosTabela(
                    'cliente', 'nif', validarCliente.nif)
                self.label_consultarNifCliente.setText(cliente[0][1])
                self.label_consultarNomeCliente.setText(cliente[0][2])
                self.label_consultarMoradaCliente.setText(cliente[0][3])
                self.label_consultarContatoCliente.setText(cliente[0][4])
                self.label_consultarCategoriaCliente.setText(cliente[0][5])
                msg = 'Cliente verificado com sucesso!'
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                self.lineEdit_consultaNifCliente.clear()
                self.tabWidget_cliente.setCurrentIndex(1)

    def voltarConsultaCliente(self):
        self.label_consultarNifCliente.clear()
        self.label_consultarNomeCliente.clear()
        self.label_consultarMoradaCliente.clear()
        self.label_consultarContatoCliente.clear()
        self.label_consultarCategoriaCliente.clear()
        self.tabWidget_cliente.setCurrentIndex(0)

    def consultarConta(self):
        validarConta = Conta()
        validarConta.numero = self.lineEdit_consultaNumConta.text()
        if len(validarConta.erroValidacao) != 0:
            self.label_msg.setText(validarConta.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            validar = self.controleConta.verificarConta(validarConta.numero)
            if not validar:
                self.label_msg.setText('Conta não existe.')
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                conta = con.selecionarDadosTabela(
                    'conta', 'numero', validarConta.numero)
                self.label_consultarNumConta.setText(conta[0][1])
                self.label_consultarTipoConta.setText(conta[0][2])
                self.label_consultarNifConta.setText(conta[0][3])
                self.label_consultarBancoConta.setText(conta[0][4])
                self.label_consultarAgenciaConta.setText(conta[0][5])
                self.label_consultarNibConta.setText(conta[0][6])
                self.label_consultarIbanConta.setText(conta[0][7])
                self.label_consultarSaldoConta.setText(
                    f'€{conta[0][8]:10,.2f}')
                self.label_consultarDataAberturaConta.setText(
                    conta[0][9].strftime('%d/%m/%Y'))
                msg = 'Conta verificada com sucesso!'
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                self.lineEdit_consultaNumConta.clear()
                self.tabWidget_conta.setCurrentIndex(1)

    def voltarConsultaConta(self):
        self.label_consultarNumConta.clear()
        self.label_consultarTipoConta.clear()
        self.label_consultarNifConta.clear()
        self.label_consultarBancoConta.clear()
        self.label_consultarAgenciaConta.clear()
        self.label_consultarNibConta.clear()
        self.label_consultarIbanConta.clear()
        self.label_consultarSaldoConta.clear()
        self.label_consultarDataAberturaConta.clear()
        self.tabWidget_conta.setCurrentIndex(0)

    def salvarDeposito(self):
        transacao = Transacao()
        transacao.numConta = self.lineEdit_depositoNumConta.text()
        transacao.descricao = ' + '+ self.lineEdit_depositoDescricao.text()
        transacao.valor = self.doubleSpinBox_depositoValor.value()
        transacao.data = dt.today()
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
                conta = self.controleConta.retornarConta(transacao.numConta)
                if conta:
                    depositou = conta.depositar(transacao.valor)
                    con.atualizarCampoTabela(
                        'conta', 'saldo', conta.saldo, 'numero', conta.numero)
                    campos = ['num_conta', 'descricao', 'valor', 'data']
                    valores = [transacao.numConta, transacao.descricao,
                               transacao.valor, transacao.data]
                    con.adicionarDadosTabela(
                        'transacao', campos, valores, 'num_conta', transacao.numConta)
                    self.controleTransacao.salvarTransacao(transacao)
                    self.label_msg.setText(depositou)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.lineEdit_depositoNumConta.clear()
                    self.lineEdit_depositoDescricao.clear()
                    self.doubleSpinBox_depositoValor.clear()
                    self.label_visualizarDepositoNumConta.setText(
                        transacao.numConta)
                    self.label_visualizarDepositoDescricao.setText(
                        transacao.descricao)
                    self.label_visualizarDepositoValor.setText(
                        f'€{transacao.valor:10,.2f}')
                    self.label_visualizarDepositoData.setText(
                        transacao.data.strftime('%d/%m/%Y'))
                    self.tabWidget_deposito.setCurrentIndex(1)

    def voltarDepositar(self):
        self.label_visualizarDepositoNumConta.clear()
        self.label_visualizarDepositoDescricao.clear()
        self.label_visualizarDepositoValor.clear()
        self.label_visualizarDepositoData.clear()
        self.tabWidget_deposito.setCurrentIndex(0)

    def salvarLevantamento(self):
        transacao = Transacao()
        transacao.numConta = self.lineEdit_levantamentoNumConta.text()
        transacao.descricao = ' - '+ self.lineEdit_levantamentoDescricao.text()
        transacao.valor = self.doubleSpinBox_levantamentoValor.value()
        transacao.data = dt.today()
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
                conta = self.controleConta.retornarConta(transacao.numConta)
                if conta:
                    levantou = conta.levantar(transacao.valor)
                    if not levantou:
                        msg = f"Não existe saldo suficiente na conta {conta.numero}"
                        self.label_msg.setText(msg)
                        self.frame_msgBar.show()
                        self.label_msg.setStyleSheet(self.corErro)
                    else:
                        con.atualizarCampoTabela(
                            'conta', 'saldo', conta.saldo, 'numero', conta.numero)
                        campos = ['num_conta', 'descricao', 'valor', 'data']
                        valores = [transacao.numConta, transacao.descricao,
                                   transacao.valor, transacao.data]
                        con.adicionarDadosTabela(
                            'transacao', campos, valores, 'num_conta', transacao.numConta)
                        self.controleTransacao.salvarTransacao(transacao)
                        self.label_msg.setText(levantou)
                        self.frame_msgBar.show()
                        self.label_msg.setStyleSheet(self.corSucesso)
                        self.lineEdit_levantamentoNumConta.clear()
                        self.lineEdit_levantamentoDescricao.clear()
                        self.doubleSpinBox_levantamentoValor.clear()
                        self.label_visualizarLevantamentoNumConta.setText(
                            transacao.numConta)
                        self.label_visualizarLevantamentoDescricao.setText(
                            transacao.descricao)
                        self.label_visualizarLevantamentoValor.setText(
                            f'€{transacao.valor:10,.2f}')
                        self.label_visualizarLevantamentoData.setText(
                            transacao.data.strftime('%d/%m/%Y'))
                        self.tabWidget_levantamento.setCurrentIndex(1)

    def voltarLevantar(self):
        self.label_visualizarLevantamentoNumConta.clear()
        self.label_visualizarLevantamentoDescricao.clear()
        self.label_visualizarLevantamentoValor.clear()
        self.label_visualizarLevantamentoData.clear()
        self.tabWidget_levantamento.setCurrentIndex(0)

    def listarTransacoesConta(self):
        transacao = Transacao()
        transacao.numConta = self.lineEdit_transacaoNumConta.text()
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
                self.tabWidget_transacoes.setCurrentIndex(1)
