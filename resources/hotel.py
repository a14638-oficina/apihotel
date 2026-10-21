from flask_restful import Resource,reqparse
from models.hotel import hotelModel

hoteis = [
    {"hotel_id": 'paraiso', "nome": 'Hotel Paraiso', "estrelas": 4.8, "diaria": 125.75, "cidade": 'Porto'},
    {"hotel_id": 'fukui', "nome": 'Fukui Paradise', "estrelas": 4.9, "diaria": 225.75, "cidade": 'Lisboa'},
    {"hotel_id": 'saint', "nome": 'Resort Saint', "estrelas": 4.3, "diaria": 165.75, "cidade": 'Coimbra'}
]

class Hoteis(Resource):
    def get(self):
        return {"hoteis": [hotel.json() for hotel in hotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
    argumentos.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
    argumentos.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")
    
    def get(self, hotel_id):
        hotel = hotelModel.find_hotel(hotel_id) #Devolve o hotel ou devolve None
        if hotel is not None:
                return hotel.json(), 200
        return  { "mensagem": "Hotel não foi encontrado"}

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        hotel = hotelModel.find_hotel(hotel_id)

        novo_hotel = hotelModel(hotel_id, **dados)

        try:
            novo_hotel.save_hotel()
            return hotel.json(),200
        except:
            return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500
        

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        
        #Se o hotel ID existe
        hotel = hotelModel.find_hotel(hotel_id)
        if hotel is not None:
            hotel.update_hotel(dados)
            return hotel.json(),200

        novo_hotel = hotelModel(hotel_id, **dados)

        #Se o hotel ID não existir
        try:
            hotel.update_hotel(*dados)
            hotel.save_hotel()
            return hotel.json(),200
        except:
            return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500

    def delete(self,hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        novo_hotel = hotelModel(hotel_id, **dados)

        hotel = hotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                novo_hotel.delete_hotel()
                return hotel.json(),200
            except:
                return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500
        return {"Mensagem": "Hotel não encontrado"},404