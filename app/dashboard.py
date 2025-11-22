from flask import Blueprint, request, render_template, redirect, url_for
from app.db import collection
import os

dashboard_bp = Blueprint("dashboard", __name__)

ADMIN_USER = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "admin123")


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

    logs = list(collection.find().sort("_id", -1).limit(100)) if collection is not None else []

    return render_template("dashboard.html", logs=logs)
