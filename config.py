import os

class Config:
    # Secret key for Flask session security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-flask-secret-key-12345')

    # Secret key used by Flask-JWT-Extended to sign tokens
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key-67890')

    # Production JWT secret key
    JWT_SECRET_KEY = 'aroma_distributors_super_secret_jwt_key_2026_production'

    # Database configuration set to dev.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')


    # Prevents unnecessary memory overhead from tracking modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False