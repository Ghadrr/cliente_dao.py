
from infra.configs.connection import DBConnectionHandler
from infra.entilies.cliente import Cliente

class cliente_repository:

    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Cliente).all()
            print(data)
            return data

    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Cliente).filter(Cliente.id == id).first()
            return data

    def insert(self, cpf, nome, telefone_fixo, telefone_celular,sexo,cep,logradouro,numero,complemento,bairro,
               municipio,estado):
        with DBConnectionHandler() as db:
            data_insert = Cliente(cpf=cpf,nome=nome,telefone_fixo=telefone_fixo,telefone_celular=telefone_celular,
                                  sexo=sexo,cep=cep,logradouro=logradouro,numero=numero,complemento=complemento,
                                  bairro=bairro,municipio=municipio,estado=estado)
            db.session.add(data_insert)
            db.session.commit()

    def delete(self, id):
        with DBConnectionHandler() as db:
            db.session.query(Cliente).filter(Cliente.id == id).delete()
            db.session.commit()


    def update(self, id, cpf, nome, telefone_fixo, telefone_celular,sexo,cep,logradouro,numero,complemento,bairro,
               municipio,estado):
        with DBConnectionHandler() as db:
            db.session.query(Cliente).filter(Cliente.id==id)\
                .update({'cpf':cpf, 'nome':nome,'telefone_fixo':telefone_fixo,'telefone_celular':telefone_celular,
                         'sexo':sexo,'cep':cep,'logradouro':logradouro,'numero':numero,'complemento':complemento,
                         'bairro':bairro,'municipio':municipio,'estado':estado})
        db.session.commit()

