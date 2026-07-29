import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Fix Render's URI format for SQLAlchemy 1.4+
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
if db_uri and db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key')

db = SQLAlchemy(app)