from flask import jsonify, request, current_app
from api.handlers.utils.utils import upload_file_to_cloudinary, token_required, role_student, role_instructor
from extensions import course, current_user, profile, assignment, submission, mongo_client
from bson import ObjectId
def create_submission(assignment_id):
    session = mongo_client.start_session()
    try:
        with session.start_transaction():
            user_data = current_user.get()
            user = profile.find_one({'email': user_data['email']}, session=session)
            assignment_id = ObjectId(assignment_id)
            course_data = course.find_one({
                '$and': [
                    {'assignments': assignment_id},
                    {'enrolled_users': user['_id']}
                ]
            })
            if not course_data:
                return jsonify({'message': 'You are not authorized to create submission for this assignment'}), 401
            files = request.files.getList('files')
            if not files:
                return jsonify({'message': 'Please provide submission files'}), 400
            uploaded_files = []
            for file in files:
                uploaded_link = upload_file_to_cloudinary(file)
                if not uploaded_link:
                    session.abort_transaction()
                    return jsonify({'message': 'Error uploading submission file'}), 500
                uploaded_files.append(uploaded_link)
            mongo_submission = {
                'files': uploaded_files,
                'assignment_id': assignment_id,
                'user_id': user['_id'],
                'graded': False
            }
            saved_submission = submission.insert_one(mongo_submission, session=session)
            assignment.update_one({'_id': assignment_id}, {'$addToSet': {'submissions': saved_submission.inserted_id}}, session=session)
            return jsonify({'message': 'Submission created successfully'}), 200
    except Exception as e:
        raise Exception(e)
    finally:
        session.end_session()

@token_required
@role_student
def delete_submission(submission_id):
    session = mongo_client.start_session()
    try:
        with session.start_transaction():
            user_data = current_user.get()
            user = profile.find_one({'email': user_data['email']}, session=session)
            submission_id = ObjectId(submission_id)
            submission_data = submission.find_one({'_id': submission_id, 'user_id': user['_id']}, session=session)
            if not submission_data:
                return jsonify({'message': 'You are not authorized to delete this submission'}), 401
            assignment_id = submission_data['assignment_id']
            assignment.update_one({'_id': assignment_id}, {'$pull': {'submissions': submission_id}}, session=session)
            submission.delete_one({'_id': submission_id}, session=session)
            return jsonify({'message': 'Submission deleted successfully'}), 200
    except Exception as e:
        current_app.logger.error("Error while deleting submission: %s", e)
        return jsonify({'message': 'Internal Server Error'}), 500
    finally:
        session.end_session()

@token_required
@role_instructor
def grade_submission(submission_id):
    session = mongo_client.start_session()
    try:
        with session.start_transaction():
            submission_id = ObjectId(submission_id)
            pipeline = [
                {
                    '$match': {'_id': submission_id}
                },
                {
                    '$lookup': {
                        'from': 'assignment',
                        'localField': 'assignment_id',
                        'foreignField': '_id',
                        'as': 'assignment'
                    }
                },
                {
                    '$unwind': {
                        'path': '$assignment',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                    '$lookup': {
                        'from': 'course',
                        'localField': 'assignment.course_id',
                        'foreignField': '_id',
                        'as': 'assignment.course'
                    }
                },
                {
                    '$unwind': {
                        'path': '$assignment.course',
                        'preserveNullAndEmptyArrays': True
                    }
                }
            ]
            submission_data = list(submission.aggregate(pipeline, session=session))[0]
            if not submission_data:
                return jsonify({'message': 'Submission not found'}), 404
            if submission_data['assignment']['course']['instructor_id'] != current_user.get()['email']:
                return jsonify({'message': 'You are not authorized to grade this submission'}), 401
            if submission_data['assignment']['graded'] == False:
                return jsonify({'message': 'Assignment is not graded'}), 400
            data = request.get_json()
            if data:
                grade = data['grade']
                if not grade:
                    return jsonify({'message': 'Please provide grade'}), 400
                if grade > submission_data['assignment']['full_marks']:
                    return jsonify({'message': 'Grade cannot be greater than full marks'}), 400
                submission.update_one({'_id': submission_id},{
                    '$set': {
                        'grade': grade,
                        'graded': True
                    }},
                    session=session
                )
                return jsonify({'message': 'Submission graded successfully'}), 200
            else:
                return jsonify({'message': 'Please provide grade'}), 400
    except Exception as e:
        current_app.logger.error("Error while grading submission: %s", e)
        return jsonify({'message': 'Internal Server Error'}),
    finally:
        session.end_session()