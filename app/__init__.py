from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    from .controllers import (auth_controller, task_controller)

    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(task_controller.bp)

    return app
