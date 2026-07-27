import os

class Config:
    # This creates a local database file named 'aroma-distributors.db' in my project folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///aroma_distributors.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this-later')