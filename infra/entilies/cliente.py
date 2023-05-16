from sqlalchemy import Integer, Column, String

from infra.configs.base import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, autoincrement=True, primary_key=True)
    cpf = Column(String(100), nullable=False)
    nome = Column(String(100), nullable=False)
    telefone_fixo = Column(String(100), nullable=True)
    telefone_celular = Column(String(100), nullable=False)
    sexo = Column(String(100), nullable=False)
    cep = Column(String(100), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(100), nullable=False)
    complemento = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)

    def __repr__(self):
        return f'id do cliente = {self.id}, nome do cliente = {self.nome}'

