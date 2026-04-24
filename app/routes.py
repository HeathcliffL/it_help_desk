from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import Ticket, TicketComment
from .utils import (
    VALID_CATEGORIES,
    VALID_PRIORITIES,
    current_user,
    login_required,
)


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
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        priority = request.form.get("priority", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not category or not priority or not description:
            flash("All fields are required.", "danger")
        elif len(title) > 150:
            flash("Title must be 150 characters or fewer.", "danger")
        elif len(description) < 10:
            flash("Description must be at least 10 characters long.", "danger")
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
                user_id=current_user().id,
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


@main_bp.route("/tickets/<int:ticket_id>/comments", methods=["POST"])
@login_required
def add_comment(ticket_id):
    user = current_user()
    ticket = Ticket.query.get_or_404(ticket_id)

    if user.role != "admin" and ticket.user_id != user.id:
        flash("You are not allowed to comment on that ticket.", "danger")
        return redirect(url_for("main.dashboard"))

    content = request.form.get("content", "").strip()
    if not content:
        flash("Comment content is required.", "danger")
    elif len(content) < 3:
        flash("Comment must be at least 3 characters long.", "danger")
    else:
        comment = TicketComment(ticket_id=ticket.id, user_id=user.id, content=content)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added successfully.", "success")

    return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))


@main_bp.route("/tickets/<int:ticket_id>/reopen", methods=["POST"])
@login_required
def reopen_ticket(ticket_id):
    """Reopen a resolved ticket.

    Intentional Phase 0 analysis surface: the reopen reason uses only minimal
    validation. It checks that a reason exists, but it does not enforce length,
    rate limits, or duplicate reopen protection. This keeps the feature simple
    while giving the peer security team a realistic weak area to analyze.
    """
    user = current_user()
    ticket = Ticket.query.get_or_404(ticket_id)

    if user.role != "admin" and ticket.user_id != user.id:
        flash("You are not allowed to reopen that ticket.", "danger")
        return redirect(url_for("main.dashboard"))

    if ticket.status != "Resolved":
        flash("Only resolved tickets can be reopened.", "warning")
        return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))

    reason = request.form.get("reason", "").strip()
    if not reason:
        flash("A reopen reason is required.", "danger")
        return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))

    ticket.status = "Open"
    db.session.add(
        TicketComment(
            ticket_id=ticket.id,
            user_id=user.id,
            content=f"Ticket reopened. Reason: {reason}",
        )
    )
    db.session.commit()
    flash("Ticket reopened and moved back to Open.", "success")
    return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))
