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

# 3. GET: Fetch all client orders

@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = ClientOrder.query.all()
    output = []
    for o in orders:
        output.append({
            'order_id': o.order_id,
            'client_id': o.client_id,
            'created_by_admin_id': o.created_by_admin_id,
            'status': o.status,
            'closed_at': o.closed_at
        })
    return jsonify(output), 200

# 4. POST: Create a new client order

@admin_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    # Check for required fields based on the database schema
    if not data or 'client_id' not in data or 'created_by_admin_id' not in data:
        return jsonify({'message': 'client_id and created_by_admin_id are required!'}), 400

    new_order = ClientOrder(
        client_id=data.get('client_id'),
        created_by_admin_id=data.get('created_by_admin_id'),
        status=data.get('status', 'Pending')
    )
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully!',
        'order_id': new_order.order_id
    }), 201


# 5. DELETE: Cancel or delete an order
@admin_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = ClientOrder.query.get_or_404(order_id)
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': f'Order {order_id} deleted successfully!'}), 200