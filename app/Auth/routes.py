from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models import Farmer, Admin

auth_bp = Blueprint('auth_bp', __name__)

# 1. POST: User Login (Returns JWT Token)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400

    # First search in Farmers table
    user = Farmer.query.filter_by(email=email).first()
    role = 'Farmer'
    user_id = user.farmer_id if user else None

    # If not a Farmer, search in Admins table
    if not user:
        user = Admin.query.filter_by(email=email).first()
        role = 'Admin'
        user_id = user.admin_id if user else None

    # Verify user exists and password matches
    if user and user.password_hash == password:
        # Stringify user_id to prevent JWT identity validation/decode errors (422)
        access_token = create_access_token(
            identity=str(user_id),
            additional_claims={'email': user.email, 'role': role}
        )
        
        return jsonify({
            'message': 'Login successful!',
            'token': access_token,
            'user': {
                'id': user_id,
                'name': user.name,
                'email': user.email,
                'role': role
            }
        }), 200

    return jsonify({'message': 'Invalid email or password!'}), 401