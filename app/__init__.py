from flask import Flask
from .config import Config
from .mysql_connector import init_mysql_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_mysql_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app