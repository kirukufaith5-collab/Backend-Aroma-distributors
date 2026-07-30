from flask import Blueprint, request, jsonify
from app import db
from app.models import ProductBatch, ClientOrder

admin_bp = Blueprint('admin', __name__)


# 1. GET: Fetch all batches for admin inspection

@admin_bp.route('/batches', methods=['GET'])
def get_all_batches():
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


# 2. PUT: Change batch status (Approve / Reject)

@admin_bp.route('/batches/<int:batch_id>/status', methods=['PUT'])
def update_batch_status(batch_id):
    # Find batch by ID
    batch = ProductBatch.query.get_or_404(batch_id)
    data = request.get_json()
    
    # Update status value
    batch.status = data.get('status', batch.status)
    db.session.commit()
    
    return jsonify({'message': f'Batch status updated to {batch.status}'}), 200