from app import create_app
from flaskwebgui import FlaskUI


if __name__ == "__main__":
    app = create_app()
    FlaskUI(app=app, width=600, height=800, server="flask").run()
