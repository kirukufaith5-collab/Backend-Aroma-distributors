from flask import Blueprint ,request,jsonify
from app import db
from app.models import Batch
from app.schemas import batches_schema ,batch_schema

farmer_bp = Blueprint('farmer_bp', __name__)

# GET: Fetch batches for a specific farmer
@farmer_bp.route('/<int:farmer_id>/batches', methods=['GET'])
def get_farmer_batches(farmer_id):
    batches = Batch.query.filter_by(farmer_id=farmer_id).all()
    return jsonify(batches_schema.dump(batches)), 200

# POST: Log new harvest batch
# Farmer creates a new batch
@farmer_bp.route('/batches', methods=['POST'])
def create_batch():
    data = request.get_json()
    
    new_batch = Batch(
        farmer_id=data.get('farmer_id'),
        product_type=data.get('coffee_type'),
        quantity_kg=data.get('quantity_kg'),
        notes=data.get('notes', '')
    )
    
    db.session.add(new_batch)
    db.session.commit()
    
    return batch_schema.jsonify(new_batch), 201