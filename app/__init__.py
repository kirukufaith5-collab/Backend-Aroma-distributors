from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import Config

# Initialize database and schema extensions
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    # Load settings from config.py
    app.config.from_object(Config)
    
    # Fallback SQLite URI if not set in Config
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    # Bind extensions to app
    db.init_app(app)
    ma.init_app(app)
    CORS(app)

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