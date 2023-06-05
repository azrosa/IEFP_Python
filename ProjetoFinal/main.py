import sys
from PyQt6.QtWidgets import QApplication
from guiLogin import GUILogin
from guiAdministrador import GUIAdministrador
from guiGerente import GUIGerente
from guiEscriturario import GUIEscriturario


def main():
    qt = QApplication(sys.argv)
    gui = GUILogin()
    gui.show()
    qt.exec()
    novaGui = gui.entrarLogin()
    if novaGui:
        gui = novaGui
        gui.show()
        qt.exec()
    gui.close()


if __name__ == '__main__':
    main()
