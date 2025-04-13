from flask import Flask

from db import db
from routes.calculate_age_route import blp as calculate_age_route
from routes.base_route import blp as base_route
from utils import get_resource_path, check_database_path


def create_app(db_url=None) -> Flask:
    """
    Creates flask app, configures it and initializes the database
    :return: Flask app
    """
    app = Flask(__name__)

    # Configure template and static folders with correct paths
    frontend_path = get_resource_path("frontend")
    static_path = get_resource_path("frontend/static")
    app.template_folder = frontend_path
    app.static_folder = static_path
    app.static_url_path = ""

    # Setup database path
    database_path = db_url if db_url is not None else check_database_path()

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
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
