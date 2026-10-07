from flask import Flask
from flask_restful import Resource,Api,reqparse

app = Flask(__name__)
api = Api(app)

hoteis = [
    {"hotel_id": 'paraiso', "nome": 'Hotel Paraiso', "estrelas": 4.8, "diaria": 125.75, "cidade": 'Porto'},
    {"hotel_id": 'fukui', "nome": 'Fukui Paradise', "estrelas": 4.9, "diaria": 225.75, "cidade": 'Lisboa'},
    {"hotel_id": 'saint', "nome": 'Resort Saint', "estrelas": 4.3, "diaria": 165.75, "cidade": 'Coimbra'}
]

class Hoteis(Resource):
    def get(self):
        return {"hoteis": hoteis}

class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
        return  { "mensagem": "Hotel não foi encontrado"}

    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
        argumentos.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
        argumentos.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
        argumentos.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")
        dados = argumentos.parse_args() #dados é um dicionário

        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return { "mensagem": f"O hotel com id {hotel_id} já existe na lista"}

        novo_hotel = {"hotel_id": hotel_id, **dados}

        hoteis.append(novo_hotel)
        return novo_hotel,200

    def put(self, hotel_id):
        argumentos1 = reqparse.RequestParser()
        argumentos1.add_argument("nome",type=str, required = True, help="O nome do hotel é obrigatório")
        argumentos1.add_argument("estrelas",type=float, required = True, help="As estrelas do hotel são obrigatório")
        argumentos1.add_argument("diaria",type=float, required = True, help="A diaria do hotel é obrigatória")
        argumentos1.add_argument("cidade",type=str, required = True, help="A cidade do hotel é obrigatório")
        dados1 = argumentos1.parse_args() #dados é um dicionário

        #Se o hotel ID existe
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                hotel.update(hotel)
                return hotel,200

        novo_hotel1 = {"hotel_id": hotel_id, **dados1}

        #Se o hotel ID não existir        
        hoteis.append(novo_hotel1)
        return novo_hotel1,201

    def delete(self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return hoteis

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)