from flask import jsonify, request, current_app
from extensions import profile, student, instructor, bcrypt, jwt_manager
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
        else:
            return jsonify({'message': 'Please provide all details'}), 400
        existing_user = profile.find_one({'email': data['email']})
        if existing_user:
            return jsonify({'message': 'User already exist'}), 500
        hashed_password = bcrypt.generate_password_hash(data['password'])
        user_profile = {
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password,
            'role': data['role'],
        }
        saved_user_profile = profile.insert_one(user_profile)
        if data['role'] != 'STUDENT':
            instructor.insert_one({'profile_id': saved_user_profile.inserted_id})
        else:
            student.insert_one({'profile_id': saved_user_profile.inserted_id})
        return jsonify({'message': 'User signup was successful'}), 200
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
            return jsonify({'message': 'User not registered'}), 400
        if not bcrypt.check_password_hash(existing_user['password'], data['password']):
            return jsonify({'message': 'Please provide wrong password'}), 401
        payload = {
            'email': existing_user['email'],
            'role': existing_user['role']
        }
        token = jwt_manager.create_token(payload)
        return jsonify({'token': token}), 200
        
    except Exception as e:
        current_app.logger.error('Error during login: %s', e)
        return jsonify({'message': 'Internal Server Error'}), 400