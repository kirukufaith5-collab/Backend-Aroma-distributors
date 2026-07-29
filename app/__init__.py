from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

#Initialize database and schema extensions
db =SQLAlchemy()
ma =Marshmallow()

def create_app():
    app =Flask(__name__)
    app.config.from_object(Config)

    #Bind extensions to app
    db.init_app(app)
    ma.init_app(app)

    #Register blueprints for routes
    from app.Admin.routes import admin_bp
    from app.Farmer.routes import farmer_bp
    from app.Auth.routes import auth_bp

    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(farmer_bp,url_prefix='/farmer')
    app.register_blueprint(auth_bp,url_prefix='/auth')

    #Create database tables
    with app.app_context():
     db.create_all()

     return app