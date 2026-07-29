from app import db
from datetime import datetime

#User model (For farmer and Admins)

class User(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable =False, unique =True)
    password=db.Column(db.String(128),nullable=False)
    role =db.Column(db.String(20),nullable =False)#Admin or Farmer

    #Batch model (Farmer Deliveries)
class Batch(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    created_at = db.Column(db.String(20), default=datetime.utcnow().strftime('%Y-%m-%d'))
    farmer_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable =False)
    weight = db.Column(db.Float,nullable=True)
    notes = db.Column(db.String(100),default='-')
    status =db.Column(db.String(20),default ='PENDING')

#Order model (Client B2B sales)
class Order(db.Model):
    id =db.Column(db.Integer ,primary_key =True)
    date = db.Column(db.String(20), default=datetime.utcnow().strftime('%Y-%m-%d'))
    client_name =db.Column(db.String(100),nullable=False)
    product_type =db.Column(db.String(50),nullable=False)
    quantity =db.Column(db.Float,nullable=False)
    unit_price =db.Column(db.Float,nullable=False)
    status=db.Column(db.String(20),default='ACTIVE')