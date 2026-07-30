from app import db
from datetime import datetime

# 1. Farmers Model
class Farmer(db.Model):
    __tablename__ = 'farmers'

    farmer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    farm_name = db.Column(db.String(100))
    farm_location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (One Farmer -> Many Batches / Payouts)
    batches = db.relationship('ProductBatch', backref='farmer', lazy=True)
    payouts = db.relationship('Payout', backref='farmer', lazy=True)


    # 2. Admins Model
class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Relationship (One Admin -> Many Client Orders created)
    orders = db.relationship('ClientOrder', backref='admin', lazy=True)