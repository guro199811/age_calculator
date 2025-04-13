from flask import Blueprint, render_template, request

from db import db
from models.history import History


blp = Blueprint("base", __name__)


@blp.route("/", methods=["GET"])
def base_route():
    """
    Base route for the API.
    :return: Rendered template with limited history records
    """
    limit = request.args.get("limit", default=10, type=int)
    history = db.session.execute(
        db.select(History).order_by(History.id.desc()).limit(limit)
    ).scalars()
    return render_template("base.html", context=history if history else None)
