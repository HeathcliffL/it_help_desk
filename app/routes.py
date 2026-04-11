from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import Ticket
from .utils import VALID_CATEGORIES, VALID_PRIORITIES, current_user, login_required


main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_user():
    return {"current_user": current_user()}


@main_bp.route("/")
def index():
    if current_user():
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    if user.role == "admin":
        return redirect(url_for("admin.admin_panel"))

    tickets = Ticket.query.filter_by(user_id=user.id).order_by(Ticket.created_at.desc()).all()
    return render_template("dashboard.html", tickets=tickets)


@main_bp.route("/tickets/new", methods=["GET", "POST"])
@login_required
def submit_ticket():
    if request.method == "POST":
        user = current_user()
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        priority = request.form.get("priority", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not category or not priority or not description:
            flash("All fields are required.", "danger")
        elif len(title) > 150:
            flash("Title must be 150 characters or fewer.", "danger")
        elif category not in VALID_CATEGORIES:
            flash("Invalid category.", "danger")
        elif priority not in VALID_PRIORITIES:
            flash("Invalid priority.", "danger")
        else:
            ticket = Ticket(
                title=title,
                category=category,
                priority=priority,
                description=description,
                user_id=user.id,
            )
            db.session.add(ticket)
            db.session.commit()
            flash("Ticket submitted successfully.", "success")
            return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))

    return render_template(
        "submit_ticket.html",
        categories=sorted(VALID_CATEGORIES),
        priorities=sorted(VALID_PRIORITIES),
    )


@main_bp.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    user = current_user()
    ticket = Ticket.query.get_or_404(ticket_id)

    if user.role != "admin" and ticket.user_id != user.id:
        flash("You are not allowed to view that ticket.", "danger")
        return redirect(url_for("main.dashboard"))

    return render_template("ticket_detail.html", ticket=ticket)
