#venv é .venv/bin/activate | é um ambiente de trabalho virtual/maquina virtual
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from con_sql_alchemy import bd
from resources.user import user,userRegister,userLogin
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app) #Inicializa o JWT para tratar da autenticação das páginas

#Configurações
#SQLITE não se utiliza em base de dados
#Foi utilizada agora por ser apenas um teste
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "my_secret_long_key_very_secret"

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")
api.add_resource(user, "/users/<string:username>")
api.add_resource(userRegister,"/registar")
api.add_resource(userLogin,"/login")

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all() #Cria todas as tabelas definidas no modelo do SQLAlchemy
    app.run(debug=True)