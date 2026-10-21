from con_sql_alchemy import bd

class hotelModel(bd.Model):
    __tablename__ = "hoteis"
    hotel_id = bd.Column(bd.String, primary_key = True)
    nome = bd.Column(bd.String(80))
    estrelas = bd.Column(bd.Float(precision=1))
    diaria = bd.Column(bd.Float(precision=2))
    cidade = bd.Column(bd.String(80))

    def __init__(self,hotel_id,nome,estrelas,diaria,cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return{
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria, 
            "cidade": self.cidade
        }

    @classmethod
    def find_hotel(cls,hotel_id):
        hotel = cls.query.filter.by(hotel_id = hotel_id).first() #Sem o first() devolve uma lista, com o first() devolve diretamente a instância do hotel
        #SELECT * FROM hoteis WHERE hotel_id = hotel_id LIMIT 1
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        bd.session.add(self)
        bd.session.commit()

    def update_hotel(self,nome_atualizado, estrelas_atualizadas, diaria_atualizada, cidade_atualizada):
        self.nome = nome_atualizado
        self.estrelas = estrelas_atualizadas
        self.diaria = diaria_atualizada
        self.cidade = cidade_atualizada

    def delete_hotel(self):
        bd.session.delete(self)
        bd.session.commit()