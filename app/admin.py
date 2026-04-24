from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import Ticket
from .utils import VALID_STATUSES, current_user, role_required


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.app_context_processor
def inject_user():
    return {"current_user": current_user()}


@admin_bp.route("")
@role_required("admin")
def admin_panel():
    status_filter = request.args.get("status", "").strip()
    query = Ticket.query.order_by(Ticket.created_at.desc())
    if status_filter in VALID_STATUSES:
        query = query.filter_by(status=status_filter)
    tickets = query.all()
    return render_template(
        "admin_panel.html",
        tickets=tickets,
        statuses=sorted(VALID_STATUSES),
        selected_status=status_filter,
    )


@admin_bp.route("/tickets/<int:ticket_id>/status", methods=["POST"])
@role_required("admin")
def update_ticket_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get("status", "").strip()

    if new_status not in VALID_STATUSES:
        flash("Invalid status value.", "danger")
        return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))

    ticket.status = new_status
    db.session.commit()
    flash("Ticket status updated successfully.", "success")
    return redirect(url_for("main.ticket_detail", ticket_id=ticket.id))
