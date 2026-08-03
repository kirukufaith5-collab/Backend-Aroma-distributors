from flask import Blueprint, request, jsonify
from app import db
from app.models import ProductBatch, ClientOrder, Client, OrderedItem

admin_bp = Blueprint('admin', __name__)

# 1. GET: Fetch all batches
@admin_bp.route('/batches', methods=['GET'])
def get_all_batches():
    batches = ProductBatch.query.all()
    output = []
    for b in batches:
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

# 2. PUT/POST: Update batch status
@admin_bp.route('/batches/<int:batch_id>/status', methods=['PUT', 'POST'])
def update_batch_status(batch_id):
    batch = ProductBatch.query.get_or_404(batch_id)
    data = request.get_json() or {}
    batch.status = data.get('status', batch.status)
    db.session.commit()
    return jsonify({'message': f'Batch status updated to {batch.status}'}), 200

# 3. GET: Fetch all clients
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

# 4. GET: Fetch all orders (INITIALIZE output = [])
@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = ClientOrder.query.all()
    output = []  # Fixes NameError
    for o in orders:
        client_name = o.client.company_name if o.client else "Unknown Client"
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

# 5. POST: Create order (Supports text inputs with automatic record creation)
# app/Admin/routes.py

@admin_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    
    # Extract form values safely
    raw_client = data.get('client_id') or data.get('client_name') or data.get('client')
    raw_batch = data.get('batch_id') or data.get('product_type') or data.get('batch')
    
    try:
        allocated_weight = float(data.get('allocated_weight', 0))
    except (ValueError, TypeError):
        allocated_weight = 0.0

    # Validation: Ensure values exist
    if not raw_client or not raw_batch or allocated_weight <= 0:
        return jsonify({
            'message': 'Invalid input! Please provide client, batch, and a weight greater than 0.',
            'received': data
        }), 400

    try:
        # Resolve or Create Client
        if isinstance(raw_client, int) or str(raw_client).isdigit():
            client = Client.query.get(int(raw_client))
        else:
            client = Client.query.filter(Client.company_name.ilike(str(raw_client))).first()

        if not client:
            client = Client(company_name=str(raw_client))
            db.session.add(client)
            db.session.flush()

        # Resolve or Create ProductBatch
        if isinstance(raw_batch, int) or str(raw_batch).isdigit():
            batch = ProductBatch.query.get(int(raw_batch))
        else:
            batch = ProductBatch.query.filter(ProductBatch.product_type.ilike(str(raw_batch))).first()

        if not batch:
            batch = ProductBatch(
                farmer_id=1,  # Default fallback ID
                product_type=str(raw_batch),
                weight=allocated_weight,
                status='Approved'
            )
            db.session.add(batch)
            db.session.flush()

        # Create ClientOrder
        new_order = ClientOrder(
            client_id=client.client_id,
            created_by_admin_id=data.get('created_by_admin_id', 1),
            status='Pending'
        )
        db.session.add(new_order)
        db.session.flush()

        # Create OrderedItem Link
        new_item = OrderedItem(
            order_id=new_order.order_id,
            batch_id=batch.batch_id,
            allocated_weight=allocated_weight
        )
        db.session.add(new_item)
        
        db.session.commit()

        return jsonify({
            'message': 'Order created successfully!',
            'order_id': new_order.order_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Database insert error', 'error': str(e)}), 400