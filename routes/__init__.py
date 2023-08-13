from .Login import login_bp
from .Reg import reg_bp
from .Index import index_bp
from .Query import query_bp
from .AddData import add_data_bp
from .AddUser import add_user_bp
from .Modify import modify_bp
from .Major import major_bp
from .Univ import univ_bp
from .AddTag import add_tag_bp
from .Score import score_bp
from .Help import help_bp
from .Excel import excel_bp
from .MyMajor import my_major_bp
from .AddMyMajor import add_my_major_bp


def init_app(app):
    app.register_blueprint(reg_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(modify_bp)
    app.register_blueprint(major_bp)
    app.register_blueprint(univ_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(help_bp)
    app.register_blueprint(excel_bp)
    app.register_blueprint(my_major_bp)
    app.register_blueprint(add_my_major_bp)
    app.register_blueprint(add_data_bp, url_prefix='/admin')
    app.register_blueprint(add_user_bp, url_prefix='/admin')
    app.register_blueprint(add_tag_bp, url_prefix='/admin')

    @app.after_request
    def _(response):
        if 'Cache-Control' not in response.headers:
            for tp in ["image", "font", "css", "javascript"]:
                if tp in response.headers["Content-Type"]:
                    response.headers['Cache-Control'] = "public, max-age=2592000"
                    break
            else:
                response.headers['Cache-Control'] = 'no-store'
        return response
        
    return app
