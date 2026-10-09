from flask_restful import Resource,reqparse
from models.hotel import hotelModel

hoteis = [
    {"hotel_id": 'paraiso', "nome": 'Hotel Paraiso', "estrelas": 4.8, "diaria": 125.75, "cidade": 'Porto'},
    {"hotel_id": 'fukui', "nome": 'Fukui Paradise', "estrelas": 4.9, "diaria": 225.75, "cidade": 'Lisboa'},
    {"hotel_id": 'saint', "nome": 'Resort Saint', "estrelas": 4.3, "diaria": 165.75, "cidade": 'Coimbra'}
]

class Hoteis(Resource):
    def get(self):
        return {"hoteis": hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
    argumentos.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
    argumentos.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")

    def encontrar_hotel(self,hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
        return None #Cuidado com identação
    
    def get(self, hotel_id):
        hotel = self.encontrar_hotel(hotel_id)
        if hotel is not None:
                return hotel, 200
        return  { "mensagem": "Hotel não foi encontrado"}

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário

        hotel = self.encontrar_hotel(hotel_id)
        if hotel is not None:
            return { "mensagem": f"O hotel com id {hotel_id} já existe na lista"}

        novo_hotel = {"hotel_id": hotel_id, **dados}

        hoteis.append(novo_hotel)
        return novo_hotel,200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário

        #Se o hotel ID existe
        hotel = self.encontrar_hotel(hotel_id)
        if hotel is not None:
            hotel.update(dados)
            return hotel,200

        novo_hotel = {"hotel_id": hotel_id, **dados}

        #Se o hotel ID não existir        
        hoteis.append(novo_hotel)
        return novo_hotel,201

    def delete(self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return hoteis