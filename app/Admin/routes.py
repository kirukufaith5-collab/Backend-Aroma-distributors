from flask import Blueprint, request, jsonify
from app import db
from app.models import Batch, Order
from app.schemas import batches_schema, orders_schema, order_schema

admin_bp = Blueprint('admin', __name__)

# GET: All batches for admin inspection
@admin_bp.route('/batches', methods=['GET'])
def get_all_batches():
    batches = Batch.query.all()
    return jsonify(batches_schema.dump(batches)), 200

# POST: Change batch status (Approve / Reject)
@admin_bp.route('/batches/<int:batch_id>/status', methods=['POST'])
def update_batch_status(batch_id):
    batch = Batch.query.get_or_404(batch_id)
    batch.status = request.json.get('status', batch.status)
    db.session.commit()
    return jsonify({"message": "Status updated successfully"}), 200

# GET: All client orders
@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders)), 200

# POST: Create client order
@admin_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        client_name=data['client_name'],
        product_type=data['product_type'],
        quantity=float(data['quantity']),
        unit_price=float(data['unit_price'])
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(order_schema.dump(new_order)), 201