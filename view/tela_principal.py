import sys
import time

import requests
import json

from PySide6.QtWidgets import QLineEdit, QPushButton, QSizePolicy, QWidget, QApplication, \
    QMainWindow, QVBoxLayout, QComboBox, QLabel, QMessageBox, QAbstractItemView, QTableWidget, QTableWidgetItem
# from Pyside6.QWidgets import QMaindWindow, QVBoxLayout, QComboBox, QLabel

from infra.entilies import cliente
#from controller.cliente_dao import DataBase
from infra.entilies.cliente import Cliente
from infra.repository.cliente_repository import cliente_repository
from infra.configs.connection import DBConnectionHandler



class MainWindow(QMainWindow):

    def __init__(self):
        conn= cliente_repository()
        super().__init__()

        self.setMinimumSize(400, 300)

        self.setWindowTitle('Cadastro de Cliente')

        self.lbl_id= QLabel('id')
        self.txt_id= QLineEdit()
        self.txt_id.setReadOnly(True)
        self.lbl_cpf = QLabel('cpf')
        self.txt_cpf = QLineEdit()
        self.txt_cpf.setInputMask('000.000.000-00')
        self.lbl_nome = QLabel('nome')
        self.txt_nome = QLineEdit()
        self.lbl_telefone_fixo = QLabel('telefone fixo')
        self.txt_telefone_fixo = QLineEdit()
        self.txt_telefone_fixo.setInputMask('(00)0000-0000')
        self.lbl_telefone_celular = QLabel('telefone celular')
        self.txt_telefone_celular = QLineEdit()
        self.txt_telefone_celular.setInputMask('(00)00000-0000')
        self.lbl_sexo = QLabel('sexo')
        self.cb_sexo = QComboBox()
        self.cb_sexo.addItems(['Não informado', 'Masculino', 'Feminino'])
        self.lbl_cep = QLabel('cep')
        self.txt_cep = QLineEdit()
        self.txt_cep.setInputMask('00.000-000')
        self.lbl_logradouro = QLabel('logradouro')
        self.txt_logradouro = QLineEdit()
        self.lbl_numero = QLabel('numero')
        self.txt_numero = QLineEdit()
        self.lbl_complemento = QLabel('complemento')
        self.txt_complemento = QLineEdit()
        self.lbl_bairro = QLabel('bairro')
        self.txt_bairro = QLineEdit()
        self.lbl_municipio = QLabel('municipio')
        self.txt_municipio = QLineEdit()
        self.lbl_estado = QLabel('estado')
        self.txt_estado = QLineEdit()

        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Deletar')

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_cpf)
        layout.addWidget(self.txt_cpf)
        layout.addWidget(self.lbl_nome)
        layout.addWidget(self.txt_nome)
        layout.addWidget(self.lbl_telefone_fixo)
        layout.addWidget(self.txt_telefone_fixo)
        layout.addWidget(self.lbl_telefone_celular)
        layout.addWidget(self.txt_telefone_celular)
        layout.addWidget(self.lbl_sexo)
        layout.addWidget(self.cb_sexo)
        layout.addWidget(self.lbl_cep)
        layout.addWidget(self.txt_cep)
        layout.addWidget(self.lbl_logradouro)
        layout.addWidget(self.txt_logradouro)
        layout.addWidget(self.lbl_numero)
        layout.addWidget(self.txt_numero)
        layout.addWidget(self.lbl_complemento)
        layout.addWidget(self.txt_complemento)
        layout.addWidget(self.lbl_bairro)
        layout.addWidget(self.txt_bairro)
        layout.addWidget(self.lbl_municipio)
        layout.addWidget(self.txt_municipio)
        layout.addWidget(self.lbl_estado)
        layout.addWidget(self.txt_estado)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_remover)

        self.qtw_clientes = QTableWidget()
        self.qtw_clientes.setColumnCount(4)
        self.qtw_clientes.setHorizontalHeaderLabels(['ID','CPF', 'NOME', 'CEP'])

        self.qtw_clientes.setSelectionMode(QAbstractItemView.NoSelection)
        self.qtw_clientes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.qtw_clientes.cellDoubleClicked.connect(self.popular_campos)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)
        layout.addWidget(self.qtw_clientes)

        self.btn_remover.clicked.connect(self.deletar)
        self.btn_limpar.clicked.connect(self.limpar)
        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.txt_cep.editingFinished.connect(self.consulta_endereco)
        self.mostrarTudo()
        db=DBConnectionHandler()

    def mostrarTudo(self):
        conn = cliente_repository()
        self.qtw_clientes.setRowCount(0)
        dadinhos = conn.select_all()
        self.qtw_clientes.setRowCount(len(dadinhos))
        for linha, cliente in enumerate(dadinhos):
            obj = [cliente.id,cliente.cpf, cliente.nome, cliente.cep]
            for coluna, valor in enumerate(obj):
                item = QTableWidgetItem(str(valor))
                self.qtw_clientes.setItem(linha, coluna, item)


    def popular_campos(self, row, column):
        self.txt_id.setText(self.qtw_clientes.item(row, 0).text())
        self.txt_cpf.setText(self.qtw_clientes.item(row, 1).text())
        self.txt_nome.setText(self.qtw_clientes.item(row, 2).text())
        self.txt_cep.setText(self.qtw_clientes.item(row, 3).text())
        self.btn_salvar.setText("Atualizar")

    def deletar(self):
        conn = cliente_repository()
        try:
            conn.delete(int(self.txt_id.text()))
            self.mostrarTudo()
            self.limpar()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('ERROR')
            msg.setText('SELECIONE ALGO PARA REMOVER')
            msg.exec()


    def limpar(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)


    def salvar_cliente(self):
        conn = cliente_repository()

        if not self.campos_vazios():
            if self.btn_salvar.text() == "Salvar":
                retorno = conn.insert(self.txt_cpf.text(),self.txt_nome.text(),self.txt_telefone_fixo.text(),
                                      self.txt_telefone_celular.text(),self.cb_sexo.currentText(), self.txt_cep.text(),
                                      self.txt_logradouro.text(),self.txt_numero.text(),self.txt_complemento.text(),
                                      self.txt_bairro.text(),self.txt_municipio.text(),self.txt_estado.text())
                self.mostrarTudo()
                self.limpar()

                if retorno == None:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle('Cadastro Realizado')
                    msg.setText('Cadastro Realizado com Sucesso')
                    msg.exec()
                    self.limpar()
                    self.mostrarTudo()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle('Erro ao cadastrar')
                    msg.setText(f'Erro ao cadastrar o cliente, verifique seus dados')
                    msg.exec()
            elif self.btn_salvar.text() == 'Atualizar':
                retorno2 = conn.update(int(self.txt_id.text()),self.txt_cpf.text(),self.txt_nome.text(),self.txt_telefone_fixo.text(),
                                      self.txt_telefone_celular.text(),self.cb_sexo.currentText(), self.txt_cep.text(),
                                      self.txt_logradouro.text(),self.txt_numero.text(),self.txt_complemento.text(),
                                      self.txt_bairro.text(),self.txt_municipio.text(),self.txt_estado.text())
                if retorno2 != None:
                    print(retorno2)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle('update Realizado')
                    msg.setText('update Realizado com Sucesso')
                    msg.exec()
                    self.limpar()
                    self.mostrarTudo()
                    self.mostrarTudo()
                    self.limpar()
        else:
            print('deu ruim')

    def consulta_endereco(self):
        url = f'https://viacep.com.br/ws/{str(self.txt_cep.text()).replace(".", "").replace("-", "")}/json/'
        response = requests.get(url)
        endereco = json.loads(response.text)

        if response.status_code == 200 and 'erro' not in endereco:
            self.txt_logradouro.setText(endereco['logradouro'])
            self.txt_bairro.setText(endereco['bairro'])
            self.txt_municipio.setText(endereco['localidade'])
            self.txt_estado.setText(endereco['uf'])
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle('consultar cep')
            msg.setText('erro ao consultar cep, verifique seu dados')
            msg.exec()

    def campos_vazios(self):
        return self.txt_cpf.text() == '' \
            or self.txt_nome.text() == ''\
            or self.txt_telefone_fixo.text() == ''\
            or self.txt_telefone_celular.text() == ''\
            or self.cb_sexo.currentText() == ''\
            or self.txt_logradouro.text() == ''\
            or self.txt_numero.text() == ''\
            or self.txt_complemento.text() == ''\
            or self.txt_bairro.text() == ''\
            or self.txt_municipio.text() == ''\
            or self.txt_estado.text() == ''

