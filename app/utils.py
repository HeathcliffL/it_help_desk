from functools import wraps

from flask import flash, redirect, session, url_for

from .models import User


VALID_CATEGORIES = {"Network", "Login Issue", "Software", "Hardware", "Other"}
VALID_PRIORITIES = {"Low", "Medium", "High"}
VALID_STATUSES = {"Open", "In Progress", "Resolved"}


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db_get_user(user_id)


def db_get_user(user_id: int):
    return User.query.filter_by(id=user_id).first()


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapped


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please log in first.", "warning")
                return redirect(url_for("auth.login"))
            if user.role != required_role:
                flash("You do not have permission to access that page.", "danger")
                return redirect(url_for("main.dashboard"))
            return view_func(*args, **kwargs)

        return wrapped

    return decorator
