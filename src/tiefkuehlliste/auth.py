import argparse
import secrets
from functools import wraps
from pathlib import Path

import yaml
from flask import current_app, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


def load_users(path):
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        return {}
    return {u["username"]: u["password_hash"] for u in data.get("users", [])}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "username" not in session:
            if request.path.startswith("/api/"):
                return jsonify(
                    error={"code": "authentication_required", "message": "Anmeldung erforderlich."}
                ), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def ensure_csrf():
    token = session.setdefault("csrf_token", secrets.token_urlsafe(32))
    return token


def validate_csrf():
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        sent = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
        if not sent or not secrets.compare_digest(sent, session.get("csrf_token", "")):
            return jsonify(
                error={"code": "csrf_failed", "message": "Sicherheits-Token ungültig."}
            ), 403
    return None


def authenticate(username, password):
    stored = load_users(current_app.config["USERS_FILE"]).get(username)
    return bool(stored and check_password_hash(stored, password))


def password_main():
    parser = argparse.ArgumentParser(description="Erzeugt einen sicheren Passwort-Hash.")
    parser.add_argument("password")
    args = parser.parse_args()
    print(generate_password_hash(args.password))
