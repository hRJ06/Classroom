from flask import jsonify, request, current_app
from api.handlers.utils.auth_utils import token_required, role_instructor
from extensions import course, current_user, profile, instructor

@token_required
@role_instructor
def create_course():
    try:
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        data = request.get_json() 
        if data:
            name = data['name']
            code = data['code']
            if not name or not code:
                return jsonify({'message': 'Please provide all details'}), 400
            mongo_course = {
                'name': name,
                'instructor_id': user['_id'],
                'code': code,
            }
            saved_course = course.insert_one(mongo_course)
            profile.update_one(
                {'_id': user['_id']},
                {'$addToSet': {'courses': saved_course.inserted_id}}
            )
            return jsonify({'message': 'Course created successfully'}), 200
        else:
            return jsonify({'message': 'Please provide all details'}), 400
    except Exception as e:
        current_app.logger.error("Error during creating course: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 400
    

@token_required
def get_course():
    try:
        user_data = current_user.get()
        user = profile.aggregate([
            {'$match': {'email': user_data['email']}},
            {'$lookup': {
                'from': 'course',  
                'localField': 'courses',  
                'foreignField': '_id',  
                'as': 'courses'  
            }},
            {'$project': {
                'courses': {'$map': {
                    'input': '$courses',
                    'as': 'course',
                    'in': {'name': '$$course.name', 'code': '$$course.code'}
                }}
            }}
        ]).next()  
        courses = user.get('courses', [])
        return jsonify({'courses': courses})
    except Exception as e:  
        current_app.logger.error("Error during getting courses: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 400