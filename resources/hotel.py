from flask_restful import Resource,reqparse
from models.hotel import hotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    parametros = reqparse.RequestParser() # Seleciona todos os dados passados na url
    parametros.add_argument("cidade", type=str, default="", location="args")
    parametros.add_argument("estrelas_min", type=float, default=0, location="args")
    parametros.add_argument("estrelas_max", type=float, default=0, location="args")
    parametros.add_argument("diaria_min", type=float, default=0, location="args")
    parametros.add_argument("diaria_max", type=float, default=0, location="args")
    parametros.add_argument("itens", type=int, default=5, location="args")
    parametros.add_argument("pagina", type=int, default=1, location="args")
    # Buscar
    def get(self):
        meus_filtros = Hoteis.parametros.parse_args()
        query = hotelModel.query # Pesquisar por ... na tabela que hotelModel representa

        if meus_filtros["cidade"]:
            query = query.filter(hotelModel.cidade == meus_filtros["cidade"])
        if meus_filtros["estrelas_min"]:
            query = query.filter(hotelModel.estrelas >= meus_filtros["estrelas_min"])
        if meus_filtros["estrelas_max"]:
            query = query.filter(hotelModel.estrelas <= meus_filtros["estrelas_max"])
        if meus_filtros["diaria_min"]:
            query = query.filter(hotelModel.diaria >= meus_filtros["diaria.min"])
        if meus_filtros["diaria_max"]:
            query = query.filter(hotelModel.diaria <= meus_filtros["diaria_max"])

        page = meus_filtros["pagina"]
        num_hoteis_por_pag = meus_filtros["itens"]
        pagination = query.paginate(page=page, per_page=num_hoteis_por_pag,error_out=False)

        resultado_hotel = [hotel.json() for hotel in pagination.items]

        return {
            "hoteis" : resultado_hotel, 
            "qtde_itens": pagination.total, "qtde_paginas" : pagination.page, "pagina_atual" : page
            }

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

    @jwt_required()
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        hotel = hotelModel.find_hotel(hotel_id)

        if hotel:
            return { "mensagem": "Já existe um hotel com este id."}

        try:
            novo_hotel = hotelModel(hotel_id, **dados)
            novo_hotel.save_hotel()
            return novo_hotel.json(),200
        except:
            return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500
        

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args() #dados é um dicionário
        
        #Se o hotel ID existe
        hotel = hotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                lista = [dado for dado in dados.values()]
                hotel.update_hotel(*lista)
                hotel.save_hotel()
                return hotel.json(),200
            except:
                return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500

    @jwt_required()
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