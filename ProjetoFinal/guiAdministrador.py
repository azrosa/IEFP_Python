import data.conexao as con
from datetime import datetime as dt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from model.agencia import Agencia
from model.banco import Banco
from model.utilizador import Utilizador
from view.telaAdministrador import Ui_MainWindow
from controller.agenciaControl import AgenciaControl
from controller.bancoControl import BancoControl
from controller.userControl import UserControl


class GUIAdministrador(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.numeroId = ''
        self.controleAgencia = AgenciaControl()
        self.controleBanco = BancoControl()
        self.controleUser = UserControl()
        self.init_components()
        self.corSucesso = "background-color: rgb(209, 255, 209);"
        self.corErro = "background-color: rgb(250, 185, 185);"

    def init_components(self):
        self.label_logo.setPixmap(QPixmap('img\iefp-logo1.png'))
        self.pushButton_utilizador.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_utilizadores))
        self.pushButton_banco.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_bancos))
        self.pushButton_agencia.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_agencias))
        self.pushButton_salvarUtilizador.clicked.connect(self.salvarUtilizador)
        self.pushButton_limparUtilizador.clicked.connect(self.limparUtilizador)
        self.pushButton_editarUtilizador.clicked.connect(self.editarUtilizador)
        self.pushButton_consultarUtilizador.clicked.connect(
            self.consultarUtilizador)
        self.pushButton_excluirUtilizador.clicked.connect(
            self.excluirUtilizador)
        self.pushButton_atualizarUtilizador.clicked.connect(
            self.atualizarUtilizador)
        self.pushButton_voltarListaUtilizadores.clicked.connect(
            self.voltarListaUtilizadores)
        self.pushButton_salvarBanco.clicked.connect(self.salvarBanco)
        self.pushButton_limparBanco.clicked.connect(self.limparBanco)
        self.pushButton_editarBanco.clicked.connect(self.editarBanco)
        self.pushButton_consultarBanco.clicked.connect(self.consultarBanco)
        self.pushButton_excluirBanco.clicked.connect(self.excluirBanco)
        self.pushButton_atualizarBanco.clicked.connect(self.atualizarBanco)
        self.pushButton_voltarListaBancos.clicked.connect(
            self.voltarListaBancos)
        self.pushButton_salvarAgencia.clicked.connect(self.salvarAgencia)
        self.pushButton_limparAgencia.clicked.connect(self.limparAgencia)
        self.pushButton_editarAgencia.clicked.connect(self.editarAgencia)
        self.pushButton_consultarAgencia.clicked.connect(self.consultarAgencia)
        self.pushButton_excluirAgencia.clicked.connect(self.excluirAgencia)
        self.pushButton_atualizarAgencia.clicked.connect(self.atualizarAgencia)
        self.pushButton_voltarListaAgencias.clicked.connect(
            self.voltarListaAgencias)
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
        utilizadores = con.selecionarDadosTabela('utilizador')
        if utilizadores:
            for u in utilizadores:
                utilizador = Utilizador(u[1], u[2], u[3])
                self.controleUser.salvarUtilizador(utilizador)
        lsBancos = ['--- Selecione ---']
        for bc in self.controleBanco.listaBancos:
            lsBancos.append(bc.nome)
        self.comboBox_bancosAgencia.addItems(lsBancos)
        self.listarAgencias()
        self.listarBancos()
        self.listarUtilizadores()

    def listarUtilizadores(self):
        contLinhas = 0
        self.tableWidget_utilizadores.clearContents()
        self.tableWidget_utilizadores.setRowCount(
            len(self.controleUser.listaUtilizadores))
        for utilizador in self.controleUser.listaUtilizadores:
            self.tableWidget_utilizadores.setItem(
                contLinhas, 0, QTableWidgetItem(utilizador.nome))
            self.tableWidget_utilizadores.setItem(
                contLinhas, 1, QTableWidgetItem(utilizador.senha))
            self.tableWidget_utilizadores.setItem(
                contLinhas, 2, QTableWidgetItem(utilizador.cargo))
            contLinhas += 1

    def salvarUtilizador(self):
        utilizador = Utilizador()
        utilizador.nome = self.lineEdit_nomeUtilizador.text()
        utilizador.senha = self.lineEdit_senhaUtilizador.text()
        utilizador.cargo = self.comboBox_cargoUtilizador.currentText()
        if len(utilizador.cargo) == 0 or 'Selecione' in utilizador.cargo:
            utilizador.erroValidacao = f'Selecione o cargo.'
        if len(utilizador.erroValidacao) != 0:
            self.label_msg.setText(utilizador.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            if self.controleUser.verificarUtilizador(utilizador.nome):
                utilizador.erroValidacao = f'Utilizador {utilizador.nome} já está cadastrado.'
            if len(utilizador.erroValidacao) != 0:
                self.label_msg.setText(utilizador.erroValidacao)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                campos = ['nome', 'senha', 'cargo']
                valores = [utilizador.nome, utilizador.senha, utilizador.cargo]
                con.inserirDadosTabela(
                    'utilizador', campos, valores, 'nome', utilizador.nome)
                msg = self.controleUser.salvarUtilizador(utilizador)
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                self.listarUtilizadores()

    def limparUtilizador(self):
        self.lineEdit_nomeUtilizador.clear()
        self.lineEdit_senhaUtilizador.clear()
        self.comboBox_cargoUtilizador.setCurrentIndex(0)

    def consultarUtilizador(self):
        indice = self.tableWidget_utilizadores.currentRow()
        if indice != -1:
            utilizadores = con.selecionarCampoTabela('utilizador', 'nome')
            nome = utilizadores[indice][0]
            self.numeroId = nome
            utilizador = con.selecionarDadosTabela('utilizador', 'nome', nome)
            self.label_consultarNomeUtilizador.setText(utilizador[0][1])
            self.label_consultarSenhaUtilizador.setText(utilizador[0][2])
            self.label_consultarCargoUtilizador.setText(utilizador[0][3])
            self.tabWidget_utilizadores.setCurrentIndex(2)
        else:
            self.label_msg.setText('Utilizador não selecionado.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def voltarListaUtilizadores(self):
        self.label_consultarNomeUtilizador.clear()
        self.label_consultarSenhaUtilizador.clear()
        self.label_consultarCargoUtilizador.clear()
        self.numeroId = ''
        self.tabWidget_utilizadores.setCurrentIndex(1)

    def editarUtilizador(self):
        indice = self.tableWidget_utilizadores.currentRow()
        if indice != -1:
            utilizadores = con.selecionarCampoTabela('utilizador', 'nome')
            nome = utilizadores[indice][0]
            self.numeroId = nome
            utilizador = con.selecionarDadosTabela('utilizador', 'nome', nome)
            self.label_editarNomeUtilizador.setText(utilizador[0][1])
            self.tabWidget_utilizadores.setCurrentIndex(3)
        else:
            self.label_msg.setText('Utilizador não selecionado.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def atualizarUtilizador(self):
        nome = self.numeroId
        if nome != None and len(nome) != 0:
            utilizador = self.controleUser.retornarUtilizador(nome)
            if utilizador:
                utilizador.nome = self.label_editarNomeUtilizador.text()
                utilizador.senha = self.lineEdit_editarSenhaUtilizador.text()
                utilizador.cargo = self.comboBox_editarCargoUtilizador.currentText()
                if len(utilizador.erroValidacao) != 0:
                    self.label_msg.setText(utilizador.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                    utilizador.erroValidacao = ''
                else:
                    campos = ['nome', 'senha', 'cargo']
                    valores = [utilizador.nome,
                               utilizador.senha, utilizador.cargo]
                    con.atualizarDadosTabela(
                        'utilizador', 'nome', utilizador.nome, campos, valores)
                    msg = 'Utilizador atualizado com sucesso!'
                    self.label_msg.setText(msg)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.label_editarNomeUtilizador.clear()
                    self.lineEdit_editarSenhaUtilizador.clear()
                    self.comboBox_editarCargoUtilizador.setCurrentIndex(0)
                    self.numeroId = ''
                    self.tabWidget_utilizadores.setCurrentIndex(1)
                    self.listarUtilizadores()

    def excluirUtilizador(self):
        global numeroId
        indice = self.tableWidget_utilizadores.currentRow()
        if indice != -1:
            utilizadores = con.selecionarCampoTabela('utilizador', 'nome')
            nome = utilizadores[indice][0]
            utilizador = con.selecionarDadosTabela('utilizador', 'nome', nome)
            con.excluirDadosTabela('utilizador', 'nome', nome)
            msg = self.controleUser.excluirUtilizador(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corSucesso)
            self.listarUtilizadores()
        else:
            msg = self.controleUser.excluirUtilizador(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def listarBancos(self):
        contLinhas = 0
        self.tableWidget_bancos.clearContents()
        self.tableWidget_bancos.setRowCount(
            len(self.controleBanco.listaBancos))
        for banco in self.controleBanco.listaBancos:
            self.tableWidget_bancos.setItem(
                contLinhas, 0, QTableWidgetItem(banco.codigo))
            self.tableWidget_bancos.setItem(
                contLinhas, 1, QTableWidgetItem(banco.nome))
            contLinhas += 1

    def salvarBanco(self):
        banco = Banco()
        banco.codigo = self.lineEdit_codBanco.text()
        banco.nome = self.lineEdit_nomeBanco.text()
        if len(banco.erroValidacao) != 0:
            self.label_msg.setText(banco.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            if self.controleBanco.verificarBanco(banco.codigo):
                banco.erroValidacao = f'Banco {banco.codigo} já está cadastrado.'
                self.label_msg.setText(banco.erroValidacao)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                campos = ['codigo', 'nome']
                valores = [banco.codigo, banco.nome]
                con.inserirDadosTabela(
                    'banco', campos, valores, 'codigo', banco.codigo)
                msg = self.controleBanco.salvarBanco(banco)
                self.label_msg.setText(msg)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corSucesso)
                lsBancos = ['--- Selecione ---']
                for bc in self.controleBanco.listaBancos:
                    lsBancos.append(bc.nome)
                self.comboBox_bancosAgencia.addItems(lsBancos)
                self.listarBancos()

    def limparBanco(self):
        self.lineEdit_codBanco.clear()
        self.lineEdit_nomeBanco.clear()

    def consultarBanco(self):
        indice = self.tableWidget_bancos.currentRow()
        if indice != -1:
            bancos = con.selecionarCampoTabela('banco', 'codigo')
            codigo = bancos[indice][0]
            self.numeroId = codigo
            banco = con.selecionarDadosTabela('banco', 'codigo', codigo)
            self.label_consultarCodBanco.setText(banco[0][1])
            self.label_consultarNomeBanco.setText(banco[0][2])
            self.tabWidget_bancos.setCurrentIndex(2)
        else:
            self.label_msg.setText('Banco não selecionado.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def voltarListaBancos(self):
        self.label_consultarCodBanco.clear()
        self.label_consultarNomeBanco.clear()
        self.numeroId = ''
        self.tabWidget_bancos.setCurrentIndex(1)

    def editarBanco(self):
        indice = self.tableWidget_bancos.currentRow()
        if indice != -1:
            bancos = con.selecionarCampoTabela('banco', 'codigo')
            codigo = bancos[indice][0]
            self.numeroId = codigo
            banco = con.selecionarDadosTabela('banco', 'codigo', codigo)
            self.label_editarCodBanco.setText(banco[0][1])
            self.lineEdit_editarNomeBanco.setText(banco[0][2])
            self.tabWidget_bancos.setCurrentIndex(3)
        else:
            self.label_msg.setText('Banco não selecionado.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def atualizarBanco(self):
        codigo = self.numeroId
        if codigo != None and len(codigo) != 0:
            banco = self.controleBanco.retornarBanco(codigo)
            if banco:
                banco.nome = self.lineEdit_editarNomeBanco.text()
                if len(banco.erroValidacao) != 0:
                    self.label_msg.setText(banco.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                    banco.erroValidacao = ''
                else:
                    campos = ['nome']
                    valores = [banco.nome]
                    con.atualizarDadosTabela(
                        'banco', 'codigo', banco.codigo, campos, valores)
                    msg = 'Banco atualizado com sucesso!'
                    self.label_msg.setText(msg)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.label_editarCodBanco.clear()
                    self.lineEdit_editarNomeBanco.clear()
                    self.numeroId = ''
                    self.tabWidget_bancos.setCurrentIndex(1)
                    self.listarBancos()

    def excluirBanco(self):
        global numeroId
        indice = self.tableWidget_bancos.currentRow()
        if indice != -1:
            bancos = con.selecionarCampoTabela('banco', 'codigo')
            codigo = bancos[indice][0]
            banco = con.selecionarDadosTabela('banco', 'codigo', codigo)
            con.excluirDadosTabela('banco', 'codigo', codigo)
            msg = self.controleBanco.excluirBanco(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corSucesso)
            lsBancos = ['--- Selecione ---']
            for bc in self.controleBanco.listaBancos:
                lsBancos.append(bc.nome)
            self.comboBox_bancosAgencia.addItems(lsBancos)
            self.listarBancos()
        else:
            msg = self.controleBanco.excluirBanco(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def listarAgencias(self):
        contLinhas = 0
        self.tableWidget_agencias.clearContents()
        self.tableWidget_agencias.setRowCount(
            len(self.controleAgencia.listaAgencias))
        for agencia in self.controleAgencia.listaAgencias:
            self.tableWidget_agencias.setItem(
                contLinhas, 0, QTableWidgetItem(agencia.numero))
            self.tableWidget_agencias.setItem(
                contLinhas, 1, QTableWidgetItem(agencia.codBanco))
            self.tableWidget_agencias.setItem(
                contLinhas, 2, QTableWidgetItem(agencia.morada))
            contLinhas += 1

    def salvarAgencia(self):
        agencia = Agencia()
        agencia.numero = self.lineEdit_numAgencia.text()
        agencia.morada = self.lineEdit_moradaAgencia.text()
        if len(agencia.erroValidacao) != 0:
            self.label_msg.setText(agencia.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            if self.controleAgencia.verificarAgencia(agencia.numero):
                agencia.erroValidacao = f'Agencia {agencia.numero} já está cadastrada.'
            nomeBanco = self.comboBox_bancosAgencia.currentText()
            if len(nomeBanco) == 0 or 'Selecione' in nomeBanco:
                agencia.erroValidacao = f'Selecione o Banco.'
            if len(agencia.erroValidacao) != 0:
                self.label_msg.setText(agencia.erroValidacao)
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
            else:
                banco = con.selecionarCampoTabela(
                    'banco', 'codigo', 'nome', nomeBanco)
                agencia.codBanco = banco[0][0]
                if len(agencia.erroValidacao) != 0:
                    self.label_msg.setText(agencia.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                else:
                    campos = ['numero', 'cod_banco', 'morada']
                    valores = [agencia.numero,
                               agencia.codBanco, agencia.morada]
                    con.inserirDadosTabela(
                        'agencia', campos, valores, 'numero', agencia.numero)
                    msg = self.controleAgencia.salvarAgencia(agencia)
                    self.label_msg.setText(msg)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.listarAgencias()

    def limparAgencia(self):
        self.lineEdit_numeroAgencia.clear()
        self.lineEdit_moradaAgencia.clear()
        self.comboBox_bancosAgencia.setCurrentIndex(0)

    def consultarAgencia(self):
        indice = self.tableWidget_agencias.currentRow()
        if indice != -1:
            agencias = con.selecionarCampoTabela('agencia', 'numero')
            numero = agencias[indice][0]
            self.numeroId = numero
            agencia = con.selecionarDadosTabela('agencia', 'numero', numero)
            self.label_consultarNumAgencia.setText(agencia[0][1])
            self.label_consultarBancoAgencia.setText(agencia[0][2])
            self.label_consultarMoradaAgencia.setText(agencia[0][3])
            self.tabWidget_agencias.setCurrentIndex(2)
        else:
            self.label_msg.setText('Agencia não selecionada.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def voltarListaAgencias(self):
        self.label_consultarNumAgencia.clear()
        self.label_consultarBancoAgencia.clear()
        self.label_consultarMoradaAgencia.clear()
        self.numeroId = ''
        self.tabWidget_agencias.setCurrentIndex(1)

    def editarAgencia(self):
        indice = self.tableWidget_agencias.currentRow()
        if indice != -1:
            agencias = con.selecionarCampoTabela('agencia', 'numero')
            numero = agencias[indice][0]
            self.numeroId = numero
            agencia = con.selecionarDadosTabela('agencia', 'numero', numero)
            self.label_editarNumAgencia.setText(agencia[0][1])
            self.label_editarBancoAgencia.setText(agencia[0][2])
            self.lineEdit_editarMoradaAgencia.setText(agencia[0][3])
            self.tabWidget_agencias.setCurrentIndex(3)
        else:
            self.label_msg.setText('Agencia não selecionada.')
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)

    def atualizarAgencia(self):
        numero = self.numeroId
        if numero != None and len(numero) != 0:
            agencia = self.controleAgencia.retornarAgencia(numero)
            if agencia:
                agencia.numero = self.label_editarNumAgencia.text()
                agencia.codBanco = self.label_editarBancoAgencia.text()
                agencia.morada = self.lineEdit_editarMoradaAgencia.text()
                if len(agencia.erroValidacao) != 0:
                    self.label_msg.setText(agencia.erroValidacao)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corErro)
                    agencia.erroValidacao = ''
                else:
                    campos = ['numero', 'cod_banco', 'morada']
                    valores = [agencia.numero,
                               agencia.codBanco, agencia.morada]
                    con.atualizarDadosTabela(
                        'agencia', 'numero', agencia.numero, campos, valores)
                    msg = 'Agencia atualizada com sucesso!'
                    self.label_msg.setText(msg)
                    self.frame_msgBar.show()
                    self.label_msg.setStyleSheet(self.corSucesso)
                    self.label_editarNumAgencia.clear()
                    self.label_editarBancoAgencia.clear()
                    self.lineEdit_editarMoradaAgencia.clear()
                    self.numeroId = ''
                    self.tabWidget_agencias.setCurrentIndex(1)
                    self.listarAgencias()

    def excluirAgencia(self):
        global numeroId
        indice = self.tableWidget_agencias.currentRow()
        if indice != -1:
            agencias = con.selecionarCampoTabela('agencia', 'numero')
            numero = agencias[indice][0]
            agencia = con.selecionarDadosTabela('agencia', 'numero', numero)
            con.excluirDadosTabela('agencia', 'numero', numero)
            msg = self.controleAgencia.excluirAgencia(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corSucesso)
            self.listarAgencias()
        else:
            msg = self.controleAgencia.excluirAgencia(indice)
            self.label_msg.setText(msg)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
