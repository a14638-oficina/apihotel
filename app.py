from flask import Flask
from flask_restful import Resource,Api

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

    def delete(self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return hoteis

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)