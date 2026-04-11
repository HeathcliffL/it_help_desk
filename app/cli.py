import click
from werkzeug.security import generate_password_hash

from . import db
from .models import User


def register_commands(app):
    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()

        admin_email = "admin@campus.local"
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                username="admin",
                email=admin_email,
                password_hash=generate_password_hash("Admin123!"),
                role="admin",
            )
            db.session.add(admin)
            db.session.commit()
            click.echo("Database initialized and default admin created.")
        else:
            click.echo("Database initialized. Admin already exists.")
