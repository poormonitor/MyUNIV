from .Login import login_bp
from .Index import index_bp
from .Query import query_bp
from .AddData import add_data_bp


def init_app(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(add_data_bp, url_prefix='/admin')
    return app
