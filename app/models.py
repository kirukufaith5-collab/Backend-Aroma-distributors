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

# Client Orders Model
class ClientOrder(db.Model):
    __tablename__ = 'client_orders'

    order_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    closed_at = db.Column(db.DateTime, nullable=True)

    # Relationship
    ordered_items = db.relationship('OrderedItem', backref='order', lazy=True)

 #  Ordered Items (Join Table for Many-to-Many between Orders and Batches)
class OrderedItem(db.Model):
    __tablename__ = 'ordered_items'

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('client_orders.order_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('product_batches.batch_id'), nullable=False)
    allocated_weight = db.Column(db.Float, nullable=False)
# Payouts Model
class Payout(db.Model):
    __tablename__ = 'payouts'

    payout_id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.farmer_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('product_batches.batch_id'), nullable=False)
    amount_owed = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Unpaid')
    paid_at = db.Column(db.DateTime, nullable=True)