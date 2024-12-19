from api.handlers.auth.userauth import home, signup, login, get_profile
from api.handlers.course.course import create_course, get_course
def register_routes(app):
    # Authentication
    app.add_url_rule('/', 'home', home, methods=['GET']) 
    app.add_url_rule('/signup', 'signup', signup, methods=['POST'])
    app.add_url_rule('/login', 'register', login, methods=['POST'])
    app.add_url_rule('/profile', 'profile', get_profile, methods=['GET'])
    
    # Course
    app.add_url_rule('/course', 'create_course', create_course, methods=['POST'])
    app.add_url_rule('/course', 'get_course', get_course, methods=['GET'])