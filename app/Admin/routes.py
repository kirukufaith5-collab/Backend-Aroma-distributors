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