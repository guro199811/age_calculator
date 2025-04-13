from flask import Flask

from db import db
from routes.calculate_age_route import blp as calculate_age_route
from routes.base_route import blp as base_route
from utils import absolute_path


def create_app():
    """
    Creates flask app, configures it and initializes the database
    :return: Flask app
    """
    app = Flask(__name__)

    # Configure template and static folders with absolute paths
    frontend_path = absolute_path(__file__, "../frontend")
    static_path = absolute_path(__file__, "../frontend/static")
    app.template_folder = frontend_path
    app.static_folder = static_path
    app.static_url_path = ""

    database_path = absolute_path(__file__, "database/history.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
    # Adjusting Cors to accept all origins
    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["CORS_ORIGINS"] = "*"
    app.config["CORS_METHODS"] = "GET, POST, OPTIONS"
    app.config["CORS_ALLOW_CREDENTIALS"] = True
    app.config["DEBUG"] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register the blueprints
    app.register_blueprint(base_route)
    app.register_blueprint(calculate_age_route)

    return app
