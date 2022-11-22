from flask import Flask

from flask_app.website.views import views


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello'
    app.register_blueprint(views, url_prefix='/')
    return app
