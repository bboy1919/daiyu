from flask import Flask
from .views.account import ac
from .views.index import ind


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object('settings.Config')

    flask_app.register_blueprint(ac)
    flask_app.register_blueprint(ind)

    return flask_app