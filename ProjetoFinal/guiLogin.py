import data.conexao as con
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from model.utilizador import Utilizador
from view.telaLogin import Ui_MainWindow
from controller.userControl import UserControl
from guiAdministrador import GUIAdministrador
from guiGerente import GUIGerente
from guiEscriturario import GUIEscriturario


class GUILogin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        super().setupUi(self)
        self.numeroId = ''
        self.controleUser = UserControl()
        self.init_components()
        self.corSucesso = "background-color: rgb(209, 255, 209);"
        self.corErro = "background-color: rgb(250, 185, 185);"

    def init_components(self):
        self.label_logo.setPixmap(QPixmap('img\iefp-logo.png'))
        self.pushButton_entrarLogin.clicked.connect(self.entrarLogin)
        self.frame_msgBar.hide()
        self.pushButton_fecharMsg.clicked.connect(
            lambda: self.frame_msgBar.hide())
        self.initBD()

    def initBD(self):
        utilizadores = con.selecionarDadosTabela('utilizador')
        if utilizadores:
            for u in utilizadores:
                utilizador = Utilizador(u[1], u[2], u[3])
                self.controleUser.salvarUtilizador(utilizador)

    def entrarLogin(self):
        user = Utilizador()
        user.nome = self.lineEdit_nomeLogin.text()
        user.senha = self.lineEdit_senhaLogin.text()
        if len(user.erroValidacao) != 0:
            self.label_msg.setText(user.erroValidacao)
            self.frame_msgBar.show()
            self.label_msg.setStyleSheet(self.corErro)
        else:
            utilizador = self.controleUser.retornarUtilizador(user.nome)
            if utilizador:
                if utilizador.cargo == 'administrador':
                    gui = GUIAdministrador()
                elif utilizador.cargo == 'gerente':
                    gui = GUIGerente()
                elif utilizador.cargo == 'escriturario':
                    gui = GUIEscriturario()
                self.close()
                return gui
            else:
                self.label_msg.setText('Utilizador/senha inválido.')
                self.frame_msgBar.show()
                self.label_msg.setStyleSheet(self.corErro)
                return False
