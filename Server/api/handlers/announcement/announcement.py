from flask import jsonify, request, current_app
from api.handlers.utils.utils import token_required, role_instructor, upload_file_to_cloudinary
from extensions import course, current_user, profile, announcement, mongo_client
from bson import ObjectId

@token_required
@role_instructor
def create_announcement(course_id):
    session = mongo_client.start_session()
    try:
        with session.start_transaction():  
            data = request.form
            files = request.files.getlist('files')
            user_data = current_user.get()
            user = profile.find_one({'email': user_data['email']}, session=session)
            course_data = course.find_one({'_id': ObjectId(course_id), 'instructor_id': user['_id']}, session=session)
            if not course_data:
                return jsonify({'message': 'You are not authorized to create announcements for this course'}), 401
            if data:
                name = data.get('name')
                content = data.get('content')
                if not name or not content:
                    return jsonify({'message': 'Please provide all details'}), 400
                uploaded_files = []
                for file in files:
                    uploaded_link = upload_file_to_cloudinary(file)
                    if not uploaded_link:
                        session.abort_transaction()  
                        return jsonify({'message': 'Error uploading assignment file'}), 500
                    uploaded_files.append(uploaded_link)
                mongo_announcement = {
                    'name': name,
                    'content': content,
                    'files': uploaded_files,
                    'course_id': course_data['_id'],
                }
                saved_announcement = announcement.insert_one(mongo_announcement, session=session)
                course.update_one(
                    {'_id': course_data['_id']},
                    {'$addToSet': {'announcements': saved_announcement.inserted_id}},
                    session=session
                )
        return jsonify({'message': 'Announcement created successfully'}), 200
    except Exception as e:
        current_app.logger.error("Error during creating announcement: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    finally:
        session.end_session()  
        
@token_required
def get_announcement(course_id):
    try:
        user_data = current_user.get()
        user = profile.find_one({'email': user_data['email']})
        course_data = course.find_one({
            '$or': [
                {'instructor_id': user['_id']},
                {'enrolled_users': user['_id']}
            ],
            '_id': ObjectId(course_id)
        })
        if not course_data:
            return jsonify({'message': 'You are not authorized to view this course'}), 401
        announcements = announcement.find_one({'course_id': course_data['_id']}, {'_id': False, 'course_id': False})
        return jsonify({
            'announcements': list(announcements)
        }), 200
    except Exception as e:
        current_app.logger.error("Error during getting announcement: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500