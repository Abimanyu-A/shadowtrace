from flask import Blueprint, request, render_template, redirect, url_for
from app.db import collection
from bson import ObjectId
import os

dashboard_bp = Blueprint("dashboard", __name__)

ADMIN_USER = os.environ.get("ADMIN_USERNAME")
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD")


def check_auth(username, password):
    return username == ADMIN_USER and password == ADMIN_PASS


@dashboard_bp.route("/dashboard/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if check_auth(username, password):
            # Store session in cookie
            resp = redirect(url_for("dashboard.dashboard_home"))
            resp.set_cookie("auth", "1")
            return resp
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


def is_authenticated():
    return request.cookies.get("auth") == "1"


@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard_home():
    if not is_authenticated():
        return redirect(url_for("dashboard.login"))

    ip_query = request.args.get("ip")
    fp_query = request.args.get("fingerprint")

    query = {}

    # Filter by IP
    if ip_query:
        query["ip"] = {"$regex": ip_query, "$options": "i"}

    # Filter by fingerprint
    if fp_query:
        query["fingerprint"] = {"$regex": fp_query, "$options": "i"}

    logs = []
    if collection is not None:
        raw_logs = list(collection.find(query).sort("_id", -1).limit(200))

        # Convert ObjectId → str for JSON serialization
        def make_jsonable(doc):
            new = {}
            for k, v in doc.items():
                if isinstance(v, ObjectId):
                    new[k] = str(v)
                else:
                    new[k] = v
            return new

        logs = [make_jsonable(doc) for doc in raw_logs]

    return render_template(
        "dashboard.html",
        logs=logs,
        ip_query=ip_query or "",
        fp_query=fp_query or ""
    )

