from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from app.utils import is_valid_email, check_unique_email, check_unique_username
from .models import User
import uuid
from flask_bcrypt import Bcrypt


api = Blueprint('api', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

@api.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    logged_user = get_jwt_identity()
    user = current_app.config['db'].collection('users').document(logged_user).get()
    if not user.exists:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@api.route('/register', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'Error': f'Invalid JSON data: {e}'}), 400

    required_fields = ['username', 'email', 'password_hash']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    if len(data['username']) < 4 or len(data['username']) > 20:
        return jsonify({'error': 'Username must be between 4 and 20 characters'}), 400

    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email address.'}), 400

    if not check_unique_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 409

    if not check_unique_username(data['username']):
        return jsonify({'error': 'Username already exists'}), 409

    pw_hash = bcrypt.generate_password_hash(data['password_hash']).decode('utf-8')
    new_user = User(
        id=str(uuid.uuid4()),
        username=data['username'],
        email=data['email'],
        password_hash=pw_hash
    )

    current_app.config['db'].collection('users').document(new_user.id).set(new_user.to_dict())
    return jsonify(new_user.to_dict()), 201

@api.route('/user', methods=['PUT'])
@jwt_required()
def update_user():
    logged_user = get_jwt_identity()
    user_doc = current_app.config['db'].collection('users').document(logged_user).get()
    if not user_doc.exists:
        return jsonify({'error': 'User not found'}), 404

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'Error': f'Invalid JSON data: {e}'}), 400

    if 'username' in data:
        if len(data['username']) < 4 or len(data['username']) > 20:
            return jsonify({'error': 'Username must be between 4 and 20 characters'}), 400
        if not check_unique_username(data['username']):
            return jsonify({'error': 'Username already exists'}), 409

    if 'email' in data:
        if not is_valid_email(data['email']):
            return jsonify({'error': 'Invalid email address.'}), 400
        if not check_unique_email(data['email']):
            return jsonify({'error': 'Email already exists'}), 409

    user = User.from_dict(user_doc.to_dict())
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    current_app.config['db'].collection('users').document(user.id).set(user.to_dict())
    return jsonify({'message': 'User updated'}), 200


@api.route('/user', methods=['DELETE'])
@jwt_required()
def delete_user():
    logged_user = get_jwt_identity()
    user = current_app.config['db'].collection('users').document(logged_user).get()
    if not user.exists:
        return jsonify({'error': 'User not found'}), 404

    current_app.config['db'].collection('users').document(logged_user).delete()
    return jsonify({'message': 'User deleted'}), 200

@api.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'Error': f'Invalid JSON data: {e}'}), 400

    required_fields = ['username', 'password_hash']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    user = current_app.config['db'].collection('users').where('username', '==', data['username']).get()
    if len(user) == 0:
        return jsonify({'error': 'User not found'}), 404

    user = user[0].to_dict()
    if not bcrypt.check_password_hash(user['password_hash'], data['password_hash']):
        return jsonify({'error': 'Invalid password'}), 401

    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token), 200
