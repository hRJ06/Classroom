from flask import jsonify
def home():
    return jsonify({'message': 'Welcome to Google ClassRoom'});