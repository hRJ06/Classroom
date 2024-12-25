from api.handlers.auth.auth import home, signup, login, get_profile
from api.handlers.course.course import create_course, get_course, get_course_course_by_id, enroll_course, unenroll_course, archive_course, unarchive_course
from api.handlers.assignment.assignment import create_assignment, get_assignment, add_submission
from api.handlers.submission.submission import delete_submission, grade_submission
from api.handlers.announcement.announcement import create_announcement, get_announcement
def register_routes(app):
    # Authentication
    app.add_url_rule('/', 'home', home, methods=['GET']) 
    app.add_url_rule('/signup', 'signup', signup, methods=['POST'])
    app.add_url_rule('/login', 'register', login, methods=['POST'])
    app.add_url_rule('/profile', 'profile', get_profile, methods=['GET'])
    # Course
    app.add_url_rule('/course', 'create_course', create_course, methods=['POST'])
    app.add_url_rule('/course', 'get_course', get_course, methods=['GET'])
    app.add_url_rule('/course/<course_id>', 'get_course_by_id', get_course_course_by_id, methods=['GET'])
    app.add_url_rule('/course/enroll/<course_id>', 'enroll_course', enroll_course, methods=['PUT'])
    app.add_url_rule('/course/unenroll/<course_id>', 'unenroll_course', unenroll_course, methods=['PUT'])
    app.add_url_rule('/course/archive/<course_id>', 'archive_course', archive_course, methods=['PUT'])
    app.add_url_rule('/course/unarchive/<course_id>', 'unarchive_course', unarchive_course, methods=['PUT'])
    # Assignment
    app.add_url_rule('/assignment/create-assignment/<course_id>', 'create_assignment', create_assignment, methods=['POST'])
    app.add_url_rule('/assignment/get-assignment/<course_id>', 'get_assignment', get_assignment, methods=['GET'])
    app.add_url_rule('assignment/add-submission/<assignment_id>', 'add_submission', add_submission, methods=['POST'])
    # Announcement
    app.add_url_rule('/announcement/create-announcement/<course_id>', 'create_announcement', create_announcement, methods=['POST'])
    app.add_url_rule('/announcement/get-announcement/<course_id>', 'get_announcement', get_announcement, methods=['GET'])
    # Submission
    app.add_url_rule('/submission/delete-submission/<submission_id>', 'delete_submission', delete_submission, methods=['DELETE'])
    app.add_url_rule('/submission/grade-submission/<submission_id>', 'grade_submission', grade_submission, methods=['PUT'])