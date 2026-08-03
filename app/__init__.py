from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

# Initialize database and schema extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load settings from config.py
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = 'aroma_distributors_super_secret_key_2026_production'
     # Ensure this is set for JWT

    # Fallback SQLite URI if not set in Config
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'

    # Bind extensions to app
    db.init_app(app)
    ma.init_app(app)
    CORS(app)
    jwt.init_app(app)

    # Register blueprints for routes
    from app.Admin.routes import admin_bp
    from app.Farmer.routes import farmer_bp
    from app.Auth.routes import auth_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Create database tables on startup
    with app.app_context():
        from app import models
        db.create_all()

    return app  # Returns the app instance after setup is complete