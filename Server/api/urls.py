from api.handlers.auth.auth import home, signup, login, get_profile
from api.handlers.course.course import create_course, get_course, get_course_course_by_id, enroll_course, unenroll_course, create_assignment
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
    app.add_url_rule('/course/create-assignment/<course_id>', 'create_assignment', create_assignment, methods=['POST'])