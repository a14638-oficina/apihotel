from flask_restful import Resource,reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token

class user(Resource):  
    def get(self, username):
        user = UserModel.find_user(username) #Devolve o Utilizador ou devolve None
        if user is not None:
                return user.json(), 200
        return  { "mensagem": "Utilizador não foi encontrado"}

    def delete(self,username):
        user = UserModel.find_user(username) #Devolve o Utilizador ou devolve None
        if user is not None:
            try:
                user.delete_user()
                return {"mensagem": "Utilizador encontrado"},200
            except:
                return {"Mensagem": "Um erro interno do servidor aconteceu ..."},500
        return {"Mensagem": "Hotel não encontrado"},404

class userRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username",type=str, required = True, help="O username é obrigatório")
    argumentos.add_argument("password",type=str, required = True, help="A password é obrigatório")

    def post(self):
        dados = userRegister.argumentos.parse_args()
        if UserModel.find_user(dados["username"]):
            return{"mensagem": "Utilizador com este username já existente"},400
        newUser = UserModel(**dados)
        try:
            newUser.save_user()
            return {"mensagem": "Utilizador criado com sucesso"},200
        except:
            return {"mensagem": "Ocorreu um erro interno"},500

class userLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username",type=str, required = True, help="O username é obrigatório")
    argumentos.add_argument("password",type=str, required = True, help="A password é obrigatório")

    def post(self):
        dados = userLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["username"])

        if user and compare_digest(user.password, dados["password"]):
            token = create_access_token(identity=user.username)
            return {"access token": token}, 200
        return {"mensagem": "O utilizador ou password está incorreto"}, 401