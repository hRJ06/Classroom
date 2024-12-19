from flask import jsonify, request, current_app
from extensions import profile, student, instructor, bcrypt, jwt_manager, current_user
from api.handlers.utils.auth_utils import token_required

def home():
    return jsonify({'message': 'Welcome to Google ClassRoom'})

def signup():
    try:
        data = request.get_json()
        if data:
            name = data['name']
            email = data['email']
            password = data['password']
            role = data['role']
            if not name or not email or not password or not role:
                return jsonify({'message': 'Please provide all details'}), 400
            existing_user = profile.find_one({'email': email})
            if existing_user:
                return jsonify({'message': 'User already exist'}), 500
            hashed_password = bcrypt.generate_password_hash(password)
            user_profile = {
                'name': name,
                'email': email,
                'password': hashed_password,
                'role': role,
            }
            saved_user_profile = profile.insert_one(user_profile)
            if data['role'] != 'STUDENT':
                instructor.insert_one({'profile_id': saved_user_profile.inserted_id})
            else:
                student.insert_one({'profile_id': saved_user_profile.inserted_id})
            return jsonify({'message': 'User signup was successful'}), 200
        else:
            return jsonify({'message': 'Please provide all details'}), 400
    except Exception as e:
        current_app.logger.error('Error during signup: %s', e)
        return jsonify({'message': 'Internal Server Error'}), 400
    
def login():
    try:
        data = request.get_json()
        if data:
            email = data['email']
            password = data['password']
            if not email or not password:
                return jsonify({'message': 'Please provide all details'}), 400
        else:
            return jsonify({'message': 'Please provide all details'}), 400
        existing_user = profile.find_one({'email': data['email']})
        if not existing_user:
            return jsonify({'message': 'User not registered'}), 404
        if not bcrypt.check_password_hash(existing_user['password'], data['password']):
            return jsonify({'message': 'Please provide correct password'}), 401
        payload = {
            'email': existing_user['email'],
            'role': existing_user['role']
        }
        token = jwt_manager.create_token(payload)
        return jsonify({'token': token}), 200
        
    except Exception as e:
        current_app.logger.error('Error during login: %s', e)
        return jsonify({'message': 'Internal Server Error'}), 500


@token_required
def get_profile():
    try:
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        if user:
            user.pop('_id', None)
            user.pop('password', None)
            return jsonify({'user': user}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        current_app.logger.error('Error fetching profile: %s', e)
        return jsonify({'message': 'Internal Server Error'}), 500