from flask import jsonify, request, current_app
from api.handlers.utils.utils import token_required, role_instructor, role_student, upload_image_to_cloudinary
from extensions import course, current_user, profile, assignment
from bson import ObjectId

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
        return jsonify({'message': 'Internal Server Error'}), 500
    
@token_required
def get_course_course_by_id(course_id):
    try:
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        course_data = course.find_one({
            '$and': [
                {
                    '$or': [
                        {'instructor_id': user['_id']},
                        {'enrolled_users': user['_id']}
                    ]
                },
                {'_id': ObjectId(course_id)}
            ]
        }, {'_id': 0, 'instructor_id': 0}) 
        if not course_data:
            return jsonify({'message': 'You are not authorized to view this course'}), 401
        return jsonify({'course': course_data}), 200
    except Exception as e:
        current_app.logger.error("Error during getting course: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    
    
@token_required
@role_student
def enroll_course(course_id):
    try:
        data = request.get_json()
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        if data:
            code = data['code']
            if not code:
                return jsonify({'message': 'Please provide enrollment code'}), 400
            course_data = course.find_one({'_id': ObjectId(course_id)})
            if not course_data:
                return jsonify({'message': 'Course not found'}), 404
            if course_data['code'] != code:
                return jsonify({'message': 'Invalid enrollment code'}), 400
            if user['_id'] in course_data.get('enrolled_users', []):
                return jsonify({'message': 'You are already enrolled in this course'}), 400
            course.update_one(
                {'_id': ObjectId(course_id)},
                {'$addToSet': {'enrolled_users': user['_id']}}
            )
            profile.update_one(
                {'_id': user['_id']},
                {'$addToSet': {'courses': course_data['_id']}}
            )
            return jsonify({'message': 'Course enrolled successfully'}), 200
        else:
            return jsonify({'message': 'Please provide all details'}), 400
    except Exception as e:
        current_app.logger.error("Error during enrolling course: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500

@token_required
@role_student
def unenroll_course(course_id):
    try:
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        course_data = course.find_one({'_id': ObjectId(course_id)})
        if not course_data:
            return jsonify({'message': 'Course not found'}), 404
        if user['_id'] not in course_data.get('enrolled_users', []):
            return jsonify({'message': 'You are not enrolled in this course'}), 400
        course.update_one(
            {'_id': ObjectId(course_id)},
            {'$pull': {'enrolled_users': user['_id']}}
        )
        profile.update_one(
            {'_id': user['_id']},
            {'$pull': {'courses': course_data['_id']}}
        )
        return jsonify({'message': 'Course unenrolled successfully'}), 200
    except Exception as e:
        current_app.logger.error("Error during unenrolling course: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500

@token_required
@role_instructor
def create_assignment(course_id):
    try:
        data = request.form
        files = request.files.getlist('files')
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        course_data = course.find_one({'_id': ObjectId(course_id), 'instructor_id': user['_id']})
        if not course_data:
            return jsonify({'message': 'You are not authorized to create assignment for this course'}), 401
        uploaded_files = []
        for file in files:
            uploaded_link = upload_image_to_cloudinary(file)
            if not uploaded_link:
                return jsonify({'message': 'Error uploading assignment file'}), 500
            uploaded_files.append(uploaded_link)
        if data:
            name = data['name']
            description = data['description']
            deadline = data['deadline']
            if not name or not description or not deadline:
                return jsonify({'message': 'Please provide all details'}), 400
            mongo_assignment = {
                'name': name,
                'description': description,
                'due_date': deadline,
                'files': uploaded_files,
                'course_id': course_data['_id'],
            }
            assignment.insert_one(mongo_assignment)
            course.update_one({'_id': course_data['_id']}, {'$addToSet': {'assignments': mongo_assignment['_id']}})
            return jsonify({'message': 'Assignment created successfully'}), 200
        
    except Exception as e:
        current_app.logger.error("Error during creating assignment: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    