from api.handlers.auth.userauth import home
def register_routes(app):
    app.add_url_rule('/', 'home', home, methods=['GET']) 