import sys
from PySide6.QtWidgets import QApplication

#from controller.cliente_dao import DataBase
from view.tela_principal import MainWindow
from infra.entilies.cliente import Cliente



args = sys.argv

app = QApplication(sys.argv)
principal = MainWindow()
principal.show()
app.exec()
