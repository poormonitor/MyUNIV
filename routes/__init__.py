from .Login import login_bp
from .Index import index_bp


def init_app(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(index_bp)
    return app
