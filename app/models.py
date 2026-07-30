from app import db
from datetime import datetime

# Farmers Model
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


# Admins Model
class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # Relationship (One Admin -> Many Client Orders created)
    orders = db.relationship('ClientOrder', backref='admin', lazy=True)

#Client model    
class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)         
    address = db.Column(db.String(200))       

    # Relationship (One Client -> Many Orders)
    orders = db.relationship('ClientOrder', backref='client', lazy=True)


#Product Batches Model
class ProductBatch(db.Model):
    __tablename__ = 'product_batches'

    batch_id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Available')

    # Relationships
    payouts = db.relationship('Payout', backref='batch', lazy=True)
    ordered_items = db.relationship('OrderedItem', backref='batch', lazy=True)