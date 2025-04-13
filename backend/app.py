import os
from flask import Flask
from db import db


def create_app():
    app = Flask(__name__.split(".")[0])
    app.template_folder = "../frontend/"

    # Use an absolute path for the database file
    database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "database/history.db"))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
