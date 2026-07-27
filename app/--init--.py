#This init.py file is used to intialize the Flask file and bind it to the database.
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import Config
from app.models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Blueprints will be registered here later!
    
    return app