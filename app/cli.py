import click
from werkzeug.security import generate_password_hash

from . import db
from .models import Ticket, TicketComment, User


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

    @app.cli.command("seed-demo")
    def seed_demo_command():
        db.create_all()

        admin = User.query.filter_by(email="admin@campus.local").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@campus.local",
                password_hash=generate_password_hash("Admin123!"),
                role="admin",
            )
            db.session.add(admin)
            db.session.commit()

        alice = User.query.filter_by(email="alice@student.local").first()
        if not alice:
            alice = User(
                username="alice",
                email="alice@student.local",
                password_hash=generate_password_hash("Student123!"),
                role="user",
            )
            db.session.add(alice)
            db.session.commit()

        if Ticket.query.count() == 0:
            ticket1 = Ticket(
                title="Cannot connect to campus Wi-Fi",
                category="Network",
                priority="High",
                description="My laptop fails to authenticate on the campus wireless network in the library.",
                status="Open",
                user_id=alice.id,
            )
            ticket2 = Ticket(
                title="Software installation request",
                category="Software",
                priority="Medium",
                description="Please install Wireshark on the lab workstation assigned to me.",
                status="In Progress",
                user_id=alice.id,
            )
            db.session.add_all([ticket1, ticket2])
            db.session.commit()

            comment1 = TicketComment(
                ticket_id=ticket2.id,
                user_id=admin.id,
                content="Request received. The lab assistant will review this installation request.",
            )
            db.session.add(comment1)
            db.session.commit()

        click.echo("Demo users and demo tickets are ready.")
