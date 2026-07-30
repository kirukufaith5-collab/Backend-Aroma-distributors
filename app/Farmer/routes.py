from flask import Blueprint, request, jsonify
from app import db
from app.models import ProductBatch

farmer_bp = Blueprint('farmer_bp', __name__)


# 1. GET: Fetch all batches for a specific farmer

@farmer_bp.route('/<int:farmer_id>/batches', methods=['GET'])
def get_farmer_batches(farmer_id):
    # Search the database for all batches matching this farmer_id
    batches = ProductBatch.query.filter_by(farmer_id=farmer_id).all()
    
    # Format the database results into a list of Python dictionaries
    output = []
    for b in batches:
        output.append({
            'batch_id': b.batch_id,
            'farmer_id': b.farmer_id,
            'product_type': b.product_type,
            'weight': b.weight,
            'status': b.status
        })
    
    return jsonify(output), 200