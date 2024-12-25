from flask import jsonify, request, current_app
from api.handlers.utils.utils import token_required, role_instructor, role_student, upload_file_to_cloudinary
from api.handlers.submission.submission import create_submission
from extensions import course, current_user, profile, assignment, mongo_client
from bson import ObjectId

@token_required
@role_instructor
def create_assignment(course_id):
    session = mongo_client.start_session()
    try:
        with session.start_transaction():
            data = request.form
            files = request.files.getlist('files')
            user_data = current_user.get()
            user = profile.find_one({'email': user_data['email']}, session=session)
            course_data = course.find_one({'_id': ObjectId(course_id), 'instructor_id': user['_id']}, session=session)
            if not course_data:
                return jsonify({'message': 'You are not authorized to create assignment for this course'}), 401
            uploaded_files = []
            for file in files:
                uploaded_link = upload_file_to_cloudinary(file)
                if not uploaded_link:
                    session.abort_transaction()
                    return jsonify({'message': 'Error uploading assignment file'}), 500
                uploaded_files.append(uploaded_link)
            if data:
                name = data['name']
                description = data['description']
                graded = data['graded']
                marks = data['marks']
                deadline = data['deadline']
                if not name or not description or not deadline:
                    return jsonify({'message': 'Please provide all details'}), 400
                mongo_assignment = {
                    'name': name,
                    'description': description,
                    'due_date': deadline,
                    'files': uploaded_files,
                    'course_id': course_data['_id'],
                    'graded' : True if graded == 'true' else False,
                    'full_marks': marks,
                }
                saved_assignment = assignment.insert_one(mongo_assignment, session=session)
                course.update_one({'_id': course_data['_id']}, {'$addToSet': {'assignments': saved_assignment.inserted_id}}, session=session)
            return jsonify({'message': 'Assignment created successfully'}), 200
    except Exception as e:
        current_app.logger.error("Error during creating assignment: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    finally:
        session.end_session()

    
@token_required
def get_assignment(course_id):
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
        assignments = assignment.find({'course_id': course_data['_id']}, {'_id': 0, 'course_id': 0})
        return jsonify({'assignments': list(assignments)}), 200
    except Exception as e:
        current_app.logger.error("Error during getting assignment: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    
@token_required
@role_student
def add_submission(assignment_id):
    try:
        create_submission()
        return jsonify({'message': 'Submission successfully added'}), 200
    except Exception as e:
        current_app.logger.error("Error during adding submission: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500