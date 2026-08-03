from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import ProductBatch

farmer_bp = Blueprint('farmer_bp', __name__)


# 1. GET: Fetch batches for a farmer (URL param OR Token-based)
@farmer_bp.route('/batches', methods=['GET'])
@farmer_bp.route('/<int:farmer_id>/batches', methods=['GET'])
def get_farmer_batches(farmer_id=None):
    # If farmer_id is not passed in URL, attempt to read from query params
    if not farmer_id:
        farmer_id = request.args.get('farmer_id')

    if farmer_id:
        batches = ProductBatch.query.filter_by(farmer_id=farmer_id).all()
    else:
        # Fallback to returning all batches if no specific farmer is specified
        batches = ProductBatch.query.all()
    
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


# 2. POST: Create a new harvest batch
@farmer_bp.route('/batches', methods=['POST'])
@jwt_required()
def create_batch():
    data = request.get_json()
    
    if not data or 'product_type' not in data or 'weight' not in data:
        return jsonify({'message': 'Missing required fields: product_type, weight'}), 400

    # Extract farmer_id from JWT identity if not explicitly sent in body
    current_user_id = get_jwt_identity()
    farmer_id = data.get('farmer_id', current_user_id)

    new_batch = ProductBatch(
        farmer_id=farmer_id,
        product_type=data.get('product_type'),
        weight=data.get('weight'),
        status=data.get('status', 'Available')
    )
    
    db.session.add(new_batch)
    db.session.commit()
    
    return jsonify({
        'message': 'Batch created successfully!',
        'batch': {
            'batch_id': new_batch.batch_id,
            'farmer_id': new_batch.farmer_id,
            'product_type': new_batch.product_type,
            'weight': new_batch.weight,
            'status': new_batch.status
        }
    }), 201


# 3. PUT: Update a batch
@farmer_bp.route('/batches/<int:batch_id>', methods=['PUT'])
def update_batch(batch_id):
    batch = ProductBatch.query.get_or_404(batch_id)
    data = request.get_json()

    batch.product_type = data.get('product_type', batch.product_type)
    batch.weight = data.get('weight', batch.weight)
    
    db.session.commit()
    return jsonify({'message': 'Batch updated successfully!'}), 200


# 4. DELETE: Remove a harvest batch
@farmer_bp.route('/batches/<int:batch_id>', methods=['DELETE'])
def delete_batch(batch_id):
    batch = ProductBatch.query.get_or_404(batch_id)
    
    db.session.delete(batch)
    db.session.commit()

    return jsonify({'message': f'Batch {batch_id} deleted successfully!'}), 200