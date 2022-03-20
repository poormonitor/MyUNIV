from .Login import login_bp
from .Index import index_bp
from .Query import query_bp
from .AddData import add_data_bp
from .AddUser import add_user_bp
from .Modify import modify_bp
from .Major import major_bp
from .Univ import univ_bp
from .AddTag import add_tag_bp
from .Score import score_bp


def init_app(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(modify_bp)
    app.register_blueprint(major_bp)
    app.register_blueprint(univ_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(add_data_bp, url_prefix='/admin')
    app.register_blueprint(add_user_bp, url_prefix='/admin')
    app.register_blueprint(add_tag_bp, url_prefix='/admin')
    return app
