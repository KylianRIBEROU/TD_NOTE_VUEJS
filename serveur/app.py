from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os.path
app = Flask(__name__)
CORS(app) # activation de CORS pour toutes les routes de notre application

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))
app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///" + mkpath("./quizz.db"))
db = SQLAlchemy(app)