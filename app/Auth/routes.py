from flask import Blueprint, request, jsonify
from app import db
from app.models import User

# Define the blueprint
auth_bp = Blueprint('auth_bp', __name__)

# Route for registering a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    # 1. Grab JSON data sent from Postman or React
    data = request.get_json()
    
    # 2. Extract values from the JSON
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'Farmer') # Default to Farmer if not provided

    # 3. Simple check to make sure fields aren't missing
    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    # 4. Check if the user already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists!'}), 400

    # 5. Create a new User instance and save to database
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201


# Route for logging in
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find the user by username
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password matches
    if user and user.password == password:
        return jsonify({
            'message': 'Login successful!',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }), 200

    return jsonify({'message': 'Invalid username or password!'}), 401