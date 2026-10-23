from con_sql_alchemy import bd

class UserModel(bd.Model):
    __tablename__ = "utilizadores"
    user_id = bd.Column(bd.Integer, primary_key = True, autoincrement=True)
    username = bd.Column(bd.String(40))
    password = bd.Column(bd.String(40))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def json(self):
        return{
            "user_id": self.user_id,
            "username": self.username
        }

    @classmethod
    def find_user(cls,username):
        user = cls.query.filter_by(username = username).first() #Sem o first() devolve uma lista, com o first() devolve diretamente a instância do hotel
        #SELECT * FROM hoteis WHERE hotel_id = hotel_id LIMIT 1
        if user:
            return user
        return None

    def save_user(self):
        bd.session.add(self)
        bd.session.commit()

    def delete_user(self):
        bd.session.delete(self)
        bd.session.commit()