from functools import wraps
from flask import request, jsonify, current_app
from extensions import jwt_manager, current_user
import cloudinary.uploader

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'})
        try:
            token = token.split(' ')[1]
            decoded_token = jwt_manager.decode_token(token)
            current_user.set(decoded_token)
        except Exception as e:
            current_app.logger.error("Error decoding token: %s", e)
            return jsonify({'message': 'Provide a valid token'}), 401
        return f(*args, **kwargs)
    return decorated

def role_instructor(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_data = current_user.get()
        role = user_data['role']
        if role != 'INSTRUCTOR':
            return jsonify({'message': 'User must be an instructor'}), 401
        return f(*args, **kwargs)
    return decorated

def role_student(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_data = current_user.get()
        role = user_data['role']
        if role != 'STUDENT':
            return jsonify({'message': 'User must be a student'}), 401
        return f(*args, **kwargs)
    return decorated

def upload_image_to_cloudinary(file):
    try:
        upload_data = cloudinary.uploader.upload(file, folder="Classroom/assignment-files")
        return upload_data['secure_url']
    except Exception as e:
        current_app.logger.error("Error uploading assignment file: %s", e)
        return None
    
            
            
