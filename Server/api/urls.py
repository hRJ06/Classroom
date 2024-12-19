from api.handlers.auth.userauth import home, signup, login
def register_routes(app):
    app.add_url_rule('/', 'home', home, methods=['GET']) 
    app.add_url_rule('/signup', 'signup', signup, methods=['POST'])
    app.add_url_rule('/login', 'register', login, methods=['POST'])