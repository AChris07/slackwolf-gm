from flask import Flask

from slackwolf.routes import commands


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_object('config')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    app.register_blueprint(commands.bp)

    return app
