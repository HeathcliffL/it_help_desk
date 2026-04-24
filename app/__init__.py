import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Default database: SQLite file in the project root (zero external deps).
    # To use Postgres instead, set DATABASE_URL, e.g.
    #   postgresql://user:pass@host:5432/campus_helpdesk
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_db_uri = "sqlite:///" + os.path.join(project_root, "helpdesk.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", default_db_uri)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from . import models  # noqa: F401
    from .routes import main_bp
    from .auth import auth_bp
    from .admin import admin_bp
    from .cli import register_commands

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    register_commands(app)

    return app
