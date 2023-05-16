from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.configs.base import Base
from infra.entilies.cliente import Cliente
import pymysql


class DBConnectionHandler:
    def __init__(self):

        self.__connection_string = 'mysql+pymysql://root:Senac2021@localhost:3306/clientes'
        # Instância do engine(genrenciador do banco)
        self.__engine = self.__create_engine()
        # Sessão nula para que possa ser alocada uma nova ao ser instanciado um obj
        self.session = None
        # Validação de criação de banco de dados
        self.__create_database()

    def __create_database(self):
        engine = create_engine(self.__connection_string, echo=True)
        try:
            engine.connect()
            print('ja tem')
        except Exception as e:
            if '1049' in str(e):
                engine = create_engine(self.__connection_string.rsplit('/', 1)[0], echo=True)
                conn = engine.connect()
                conn.execute(f'CREATE DATABASE IF NOT EXISTS {self.__connection_string.rsplit("/", 1)[1]}')
                conn.close()
                print("Banco criado!!!!!")
                self.__create_table()
            else:
                raise e

    def __create_table(self):

        Base.metadata.create_all(bind=self.__engine)
        print('tabela(s) criada(s)')

    def __create_engine(self):
        engine = create_engine(self.__connection_string, echo=True)
        return engine

    def get_engine(self):
        return self.__engine

        # Funções mágicas que definem qualquer comportamento do serem gerdos instânciados

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        print('Gerando conexão')
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Fechando conexão')
        self.session.close()
