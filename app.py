#venv é .venv/bin/activate | é um ambiente de trabalho virtual/maquina virtual
from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from con_sql_alchemy import bd

app = Flask(__name__)
api = Api(app)

#Configurações
#SQLITE não se utiliza em base de dados
#Foi utilizada agora por ser apenas um teste
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hoteis.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    bd.init_app(app)
    with app.app_context():
        bd.create_all() #Cria todas as tabelas definidas no modelo do SQLAlchemy
    app.run(debug=True)