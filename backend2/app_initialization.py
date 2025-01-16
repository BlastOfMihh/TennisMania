from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_socketio import SocketIO
from db import db
import os


app = Flask(__name__)

pathOfCurrentDirectory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(pathOfCurrentDirectory, 'the_database.db') # this configures the database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}},
     support_credentials=True,
     headers=['Content-Type', 'Authorization'])

api = Api(app)

db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")


