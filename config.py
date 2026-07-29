import os

# Base directory of the backend folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    #SEcret key for sessions/auth
    SECRET_KEY='my-secret-key-123'

    #Sqlite database file path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHMEY_TRACK_MODIFICATIONS =False