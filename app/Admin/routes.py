from flask import Blueprint, request, jsonify
from app import db
from app.models import ProductBatch, ClientOrder, Client, OrderedItem

admin_bp = Blueprint('admin', __name__)


# -------------------------------------------------------------
# 1. GET: Fetch all batches for admin inspection
# -------------------------------------------------------------
@admin_bp.route('/batches', methods=['GET'])
def get_all_batches():
    batches = ProductBatch.query.all()
    output = []
    for b in batches:
        # Include farmer name via relationship if available
        farmer_name = b.farmer.name if hasattr(b, 'farmer') and b.farmer else f"Farmer #{b.farmer_id}"
        
        output.append({
            'batch_id': b.batch_id,
            'farmer_id': b.farmer_id,
            'farmer_name': farmer_name,
            'product_type': b.product_type,
            'weight': b.weight,
            'status': b.status
        })
    return jsonify(output), 200


# -------------------------------------------------------------
# 2. PUT: Change batch status (Approve / Reject)
# -------------------------------------------------------------
@admin_bp.route('/batches/<int:batch_id>/status', methods=['PUT', 'POST'])
def update_batch_status(batch_id):
    batch = ProductBatch.query.get_or_404(batch_id)
    data = request.get_json() or {}
    
    batch.status = data.get('status', batch.status)
    db.session.commit()
    
    return jsonify({'message': f'Batch status updated to {batch.status}'}), 200


# -------------------------------------------------------------
# 3. GET: Fetch all clients (For dropdown in React Create Order form)
# -------------------------------------------------------------
@admin_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    output = []
    for c in clients:
        output.append({
            'client_id': c.client_id,
            'company_name': c.company_name
        })
    return jsonify(output), 200


# -------------------------------------------------------------
# 4. GET: Fetch all client orders with Client & Batch details
# -------------------------------------------------------------
@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = ClientOrder.query.all()
    output = []
    for o in orders:
        # Get client company name from Client relationship
        client_name = o.client.company_name if o.client else "Unknown Client"
        
        # Get allocated weight and product type from ordered_items relationship
        first_item = o.ordered_items[0] if o.ordered_items else None
        product_type = first_item.batch.product_type if (first_item and first_item.batch) else "Produce"
        allocated_weight = first_item.allocated_weight if first_item else 0.0

        output.append({
            'order_id': o.order_id,
            'client_id': o.client_id,
            'client_name': client_name,
            'product_type': product_type,
            'allocated_weight': allocated_weight,
            'created_by_admin_id': o.created_by_admin_id,
            'status': o.status,
            'closed_at': o.closed_at
        })
    return jsonify(output), 200


# -------------------------------------------------------------
# 5. POST: Create a new client order (Creates ClientOrder + OrderedItem)
# -------------------------------------------------------------
@admin_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    if not data or 'client_id' not in data:
        return jsonify({'message': 'client_id is required!'}), 400

    try:
        # Step A: Insert into client_orders table
        new_order = ClientOrder(
            client_id=data.get('client_id'),
            created_by_admin_id=data.get('created_by_admin_id', 1), # Defaults to Admin 1
            status=data.get('status', 'Pending')
        )
        db.session.add(new_order)
        db.session.commit()  # Commits to generate new_order.order_id

        # Step B: If batch_id and allocated_weight are provided, link them in ordered_items
        if 'batch_id' in data and 'allocated_weight' in data:
            new_item = OrderedItem(
                order_id=new_order.order_id,
                batch_id=data.get('batch_id'),
                allocated_weight=float(data.get('allocated_weight'))
            )
            db.session.add(new_item)
            db.session.commit()

        return jsonify({
            'message': 'Order created successfully!',
            'order_id': new_order.order_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create order', 'error': str(e)}), 400


# -------------------------------------------------------------
# 6. POST: Close an existing order
# -------------------------------------------------------------
@admin_bp.route('/orders/<int:order_id>/close', methods=['POST', 'PUT'])
def close_order(order_id):
    order = ClientOrder.query.get_or_404(order_id)
    order.status = 'Closed'
    db.session.commit()
    return jsonify({'message': f'Order #{order_id} marked as closed.'}), 200


# -------------------------------------------------------------
# 7. DELETE: Cancel or delete an order
# -------------------------------------------------------------
@admin_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = ClientOrder.query.get_or_404(order_id)
    
    # Delete associated ordered items first to maintain referential integrity
    OrderedItem.query.filter_by(order_id=order_id).delete()
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': f'Order {order_id} deleted successfully!'}), 200