from blueprints.user.user import bp_user

def init_app(app):
    app.register_blueprint(bp_user)