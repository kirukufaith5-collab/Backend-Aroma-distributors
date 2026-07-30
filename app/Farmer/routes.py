from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
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


# 2. POST: Create a new harvest batch

@farmer_bp.route('/batches', methods=['POST'])
@jwt_required()
def create_batch():

    data = request.get_json()
    
    # Simple check to make sure required information is present
    if not data or 'farmer_id' not in data or 'product_type' not in data or 'weight' not in data:
        return jsonify({'message': 'Missing required fields: farmer_id, product_type, weight'}), 400

    # Create a new instance of the ProductBatch model
    new_batch = ProductBatch(
        farmer_id=data.get('farmer_id'),
        product_type=data.get('product_type'),
        weight=data.get('weight'),
        status=data.get('status', 'Available') # Default status to 'Available'
    )
    
    # Save the new batch to SQLite
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


# 3. PUT: Update a batch (e.g., change weight or type)
@farmer_bp.route('/batches/<int:batch_id>', methods=['PUT'])
def update_batch(batch_id):
    # Find the batch by ID or return a 404 error if it doesn't exist
    batch = ProductBatch.query.get_or_404(batch_id)
    data = request.get_json()

    # Update fields if new data was provided, otherwise keep existing values
    batch.product_type = data.get('product_type', batch.product_type)
    batch.weight = data.get('weight', batch.weight)
    
    # Save updates to database
    db.session.commit()

    return jsonify({'message': 'Batch updated successfully!'}), 200


# 4. DELETE: Remove a harvest batch
@farmer_bp.route('/batches/<int:batch_id>', methods=['DELETE'])
def delete_batch(batch_id):
    # Find the batch to delete
    batch = ProductBatch.query.get_or_404(batch_id)
    
    # Remove from database and save changes
    db.session.delete(batch)
    db.session.commit()

    return jsonify({'message': f'Batch {batch_id} deleted successfully!'}), 200