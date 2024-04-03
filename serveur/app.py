from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

import os.path
app = Flask(__name__)
cors = CORS(app, resources={r"/flaskapi/v1.0/*" : {"origins": "*"}})  # Permet à toutes les routes d'accepter les requêtes CORS
swagger = Swagger(app, template_file="../OpenAPI_doc_serveurREST.yaml")

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))
app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///" + mkpath("./quizz.db"))
db = SQLAlchemy(app)