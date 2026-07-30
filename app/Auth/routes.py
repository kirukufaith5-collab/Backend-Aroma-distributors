from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models import Farmer, Admin

auth_bp = Blueprint('auth_bp', __name__)

# 1. POST: Register a new Farmer or Admin
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Extract common fields
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role', 'Farmer')  # 'Farmer' or 'Admin'

    # 1. Validate required fields
    if not email or not password or not name:
        return jsonify({'message': 'Email, password, and name are required!'}), 400

    # 2. Check if user exists in either table
    existing_farmer = Farmer.query.filter_by(email=email).first()
    existing_admin = Admin.query.filter_by(email=email).first()
    
    if existing_farmer or existing_admin:
        return jsonify({'message': 'Email is already registered!'}), 400

    # 3. Create the user based on specified role
    if role.lower() == 'admin':
        new_user = Admin(
            email=email,
            password_hash=password,  # Storing password
            name=name
        )
    else:
        new_user = Farmer(
            email=email,
            password_hash=password,
            name=name,
            farm_name=data.get('farm_name', ''),
            farm_location=data.get('farm_location', '')
        )

    # 4. Save new user to SQLite
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'{role} registered successfully!'}), 201



# 2. POST: User Login (Returns JWT Token)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400

    # 1. First search in Farmers table
    user = Farmer.query.filter_by(email=email).first()
    role = 'Farmer'
    user_id = user.farmer_id if user else None

    # 2. If not a Farmer, search in Admins table
    if not user:
        user = Admin.query.filter_by(email=email).first()
        role = 'Admin'
        user_id = user.admin_id if user else None

    # 3. Verify user exists and password matches
    if user and user.password_hash == password:
        # Generate a JWT access token containing identity and role info
        access_token = create_access_token(identity={'id': user_id, 'email': user.email, 'role': role})
        
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