import json
import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from .auth import authenticate, ensure_csrf, login_required, validate_csrf
from .config import default_config_path, load_config
from .db import audit, close_db, get_db, init_db, now, transaction


def error(message, status=400, code="invalid_request", fields=None):
    body = {"code": code, "message": message}
    if fields:
        body["fields"] = fields
    return jsonify(error=body), status


def quantity_payload(parts):
    if not isinstance(parts, list):
        raise ValueError("Menge muss eine Liste sein.")
    result, dimension = [], None
    for part in parts:
        kind = part.get("kind")
        unit = part.get("unit")
        target_dimension = "weight" if unit in {"g", "kg"} else "count" if unit == "piece" else None
        if not target_dimension or kind not in {"package", "loose"}:
            raise ValueError("Mengenart oder Einheit ist ungültig.")
        if dimension and dimension != target_dimension:
            raise ValueError("Gewicht und Stück dürfen nicht gemischt werden.")
        dimension = target_dimension
        factor = 1000 if unit == "kg" else 1
        try:
            amount = float(part.get("amount", 0))
            scaled = round(amount * factor)
        except (TypeError, ValueError):
            raise ValueError("Menge muss eine Zahl sein.") from None
        if amount < 0 or abs(amount * factor - scaled) > 1e-9:
            raise ValueError("Menge ist negativ oder hat zu viele Nachkommastellen.")
        if scaled == 0:
            continue
        size = None
        if kind == "package":
            try:
                raw_size = float(part.get("package_size"))
                size = round(raw_size * factor)
            except (TypeError, ValueError):
                raise ValueError("Packungsgröße fehlt.") from None
            if scaled != int(scaled) or size <= 0 or abs(raw_size * factor - size) > 1e-9:
                raise ValueError("Packungsanzahl und -größe sind ungültig.")
        result.append({"kind": kind, "amount": int(scaled), "package_size": size})
    normalized = []
    package_positions = {}
    for part in result:
        if part["kind"] != "package":
            normalized.append(part)
            continue
        size = part["package_size"]
        if size in package_positions:
            normalized[package_positions[size]]["amount"] += part["amount"]
        else:
            package_positions[size] = len(normalized)
            normalized.append(part)
    return normalized, dimension or "weight"


def item_dict(db, item_id):
    row = db.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    if not row:
        return None
    data = dict(row)
    unit = "g" if data["dimension"] == "weight" else "piece"
    data["parts"] = [
        dict(p) | {"unit": unit}
        for p in db.execute(
            "SELECT kind,amount,package_size FROM quantity_parts WHERE item_id=? ORDER BY position",
            (item_id,),
        )
    ]
    return data


def validate_item(data):
    product = str(data.get("product", "")).strip()
    if not product:
        raise ValueError("Produkt ist erforderlich.")
    parts, dimension = quantity_payload(data.get("parts"))
    for field in ("frozen_on", "best_before"):
        value = data.get(field) or None
        if value:
            try:
                __import__("datetime").date.fromisoformat(value)
            except ValueError:
                raise ValueError(f"{field} ist kein gültiges Datum.") from None
    raw_note = data.get("note")
    return {
        "product": product,
        "parts": parts,
        "dimension": dimension,
        "frozen_on": data.get("frozen_on") or None,
        "best_before": data.get("best_before") or None,
        "note": (str(raw_note).strip() or None) if raw_note is not None else None,
    }


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    config_file = os.getenv("TIEFKUEHLLISTE_CONFIG", str(default_config_path()))
    if test_config and "CONFIG_FILE" in test_config:
        config_file = test_config["CONFIG_FILE"]
    file_config = load_config(config_file)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-me"),
        DATABASE=os.getenv("DATABASE", str(Path(app.instance_path) / "inventory.sqlite")),
        CONFIG_FILE=config_file,
        SERVER_HOST=file_config["server"]["host"],
        SERVER_PORT=file_config["server"]["port"],
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    @app.cli.command("init-db")
    def init_db_command():
        """Initialisiert oder aktualisiert das Datenbankschema."""
        init_db()
        print("Datenbank ist aktuell.")

    @app.get("/login")
    def login():
        return render_template("login.html", csrf_token=ensure_csrf())

    @app.post("/login")
    def login_post():
        csrf_error = validate_csrf()
        if csrf_error:
            return csrf_error
        if authenticate(request.form.get("username", ""), request.form.get("password", "")):
            session.clear()
            session["username"] = request.form["username"]
            ensure_csrf()
            return redirect(url_for("index"))
        return render_template(
            "login.html", csrf_token=ensure_csrf(), error="Benutzername oder Passwort ist falsch."
        ), 401

    @app.post("/logout")
    @login_required
    def logout():
        csrf_error = validate_csrf()
        if csrf_error:
            return csrf_error
        session.clear()
        return redirect(url_for("login"))

    @app.get("/")
    @login_required
    def index():
        return render_template("index.html", csrf_token=ensure_csrf(), username=session["username"])

    @app.before_request
    def api_csrf():
        if request.path.startswith("/api/"):
            return validate_csrf()

    @app.get("/api/session")
    def api_session():
        return jsonify(
            data={
                "authenticated": "username" in session,
                "username": session.get("username"),
                "csrf_token": ensure_csrf(),
            }
        )

    @app.get("/api/freezers")
    @login_required
    def freezers():
        return jsonify(
            data=[
                dict(r)
                for r in get_db().execute("SELECT * FROM freezers ORDER BY is_default DESC,name")
            ]
        )

    @app.post("/api/freezers")
    @login_required
    def create_freezer():
        name = str((request.get_json(silent=True) or {}).get("name", "")).strip()
        if not name:
            return error("Name ist erforderlich.")
        with transaction() as db:
            stamp = now()
            cur = db.execute(
                "INSERT INTO freezers(name,is_default,created_at,updated_at) VALUES(?,0,?,?)",
                (name, stamp, stamp),
            )
            after = dict(
                db.execute("SELECT * FROM freezers WHERE id=?", (cur.lastrowid,)).fetchone()
            )
            audit(db, session["username"], "create", "freezer", cur.lastrowid, after=after)
        return jsonify(data=after), 201

    @app.patch("/api/freezers/<int:freezer_id>")
    @login_required
    def update_freezer(freezer_id):
        data = request.get_json(silent=True) or {}
        with transaction() as db:
            old = db.execute("SELECT * FROM freezers WHERE id=?", (freezer_id,)).fetchone()
            if not old:
                return error("Truhe nicht gefunden.", 404, "not_found")
            before = dict(old)
            name = str(data.get("name", old["name"])).strip()
            if not name:
                return error("Name ist erforderlich.")
            if data.get("is_default"):
                db.execute("UPDATE freezers SET is_default=0 WHERE is_default=1")
            db.execute(
                "UPDATE freezers SET name=?,is_default=?,updated_at=? WHERE id=?",
                (name, 1 if data.get("is_default") else old["is_default"], now(), freezer_id),
            )
            after = dict(db.execute("SELECT * FROM freezers WHERE id=?", (freezer_id,)).fetchone())
            audit(db, session["username"], "update", "freezer", freezer_id, before, after)
        return jsonify(data=after)

    @app.get("/api/freezers/<int:freezer_id>/items")
    @login_required
    def items(freezer_id):
        archived = request.args.get("archived") == "1"
        rows = get_db().execute(
            "SELECT id FROM items WHERE freezer_id=? AND archived_at IS "
            + ("NOT NULL" if archived else "NULL")
            + " ORDER BY product COLLATE NOCASE",
            (freezer_id,),
        )
        return jsonify(data=[item_dict(get_db(), r["id"]) for r in rows])

    @app.post("/api/items")
    @login_required
    def create_item():
        data = request.get_json(silent=True) or {}
        try:
            clean = validate_item(data)
        except ValueError as exc:
            return error(str(exc))
        freezer_id = data.get("freezer_id")
        with transaction() as db:
            if not db.execute("SELECT 1 FROM freezers WHERE id=?", (freezer_id,)).fetchone():
                return error("Truhe nicht gefunden.", 404, "not_found")
            stamp = now()
            archived = None if clean["parts"] else stamp
            cur = db.execute(
                "INSERT INTO items(freezer_id,product,frozen_on,best_before,note,dimension,archived_at,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    freezer_id,
                    clean["product"],
                    clean["frozen_on"],
                    clean["best_before"],
                    clean["note"],
                    clean["dimension"],
                    archived,
                    stamp,
                    stamp,
                ),
            )
            for pos, p in enumerate(clean["parts"]):
                db.execute(
                    "INSERT INTO quantity_parts(item_id,position,kind,amount,package_size) VALUES(?,?,?,?,?)",
                    (cur.lastrowid, pos, p["kind"], p["amount"], p["package_size"]),
                )
            after = item_dict(db, cur.lastrowid)
            audit(db, session["username"], "create", "item", cur.lastrowid, after=after)
        return jsonify(data=after), 201

    @app.get("/api/items/<int:item_id>")
    @login_required
    def get_item(item_id):
        item = item_dict(get_db(), item_id)
        return jsonify(data=item) if item else error("Eintrag nicht gefunden.", 404, "not_found")

    @app.put("/api/items/<int:item_id>")
    @login_required
    def update_item(item_id):
        data = request.get_json(silent=True) or {}
        try:
            clean = validate_item(data)
        except ValueError as exc:
            return error(str(exc))
        with transaction() as db:
            before = item_dict(db, item_id)
            if not before:
                return error("Eintrag nicht gefunden.", 404, "not_found")
            archived = None if clean["parts"] else now()
            action = (
                "reactivate"
                if before["archived_at"] and not archived
                else "archive"
                if not before["archived_at"] and archived
                else "update"
            )
            db.execute(
                "UPDATE items SET product=?,frozen_on=?,best_before=?,note=?,dimension=?,archived_at=?,updated_at=? WHERE id=?",
                (
                    clean["product"],
                    clean["frozen_on"],
                    clean["best_before"],
                    clean["note"],
                    clean["dimension"],
                    archived,
                    now(),
                    item_id,
                ),
            )
            db.execute("DELETE FROM quantity_parts WHERE item_id=?", (item_id,))
            for pos, p in enumerate(clean["parts"]):
                db.execute(
                    "INSERT INTO quantity_parts(item_id,position,kind,amount,package_size) VALUES(?,?,?,?,?)",
                    (item_id, pos, p["kind"], p["amount"], p["package_size"]),
                )
            after = item_dict(db, item_id)
            audit(db, session["username"], action, "item", item_id, before, after)
        return jsonify(data=after)

    @app.post("/api/items/<int:item_id>/withdraw")
    @login_required
    def withdraw_item(item_id):
        data = request.get_json(silent=True) or {}
        try:
            index = int(data.get("part_index"))
            amount = int(data.get("amount"))
        except (TypeError, ValueError):
            return error("Bestandteil und Entnahmemenge sind erforderlich.")
        with transaction() as db:
            before = item_dict(db, item_id)
            if not before or before["archived_at"]:
                return error("Aktiver Eintrag nicht gefunden.", 404, "not_found")
            if index < 0 or index >= len(before["parts"]) or amount <= 0:
                return error("Entnahmemenge oder Bestandteil ist ungültig.")
            parts = [dict(part) for part in before["parts"]]
            selected = parts[index]
            if selected["kind"] == "loose":
                if amount > selected["amount"]:
                    return error("Entnahme ist größer als der gewählte Restbestand.")
                selected["amount"] -= amount
            else:
                size = selected["package_size"]
                if amount > size or selected["amount"] < 1:
                    return error("Aus einer Packung kann höchstens deren Größe entnommen werden.")
                selected["amount"] -= 1
                remainder = size - amount
                if remainder:
                    parts.append(
                        {
                            "kind": "loose",
                            "amount": remainder,
                            "package_size": None,
                            "unit": selected["unit"],
                        }
                    )
            parts = [part for part in parts if part["amount"] > 0]
            archived = None if parts else now()
            db.execute(
                "UPDATE items SET archived_at=?,updated_at=? WHERE id=?", (archived, now(), item_id)
            )
            db.execute("DELETE FROM quantity_parts WHERE item_id=?", (item_id,))
            for pos, part in enumerate(parts):
                db.execute(
                    "INSERT INTO quantity_parts(item_id,position,kind,amount,package_size) VALUES(?,?,?,?,?)",
                    (item_id, pos, part["kind"], part["amount"], part["package_size"]),
                )
            after = item_dict(db, item_id)
            audit(
                db,
                session["username"],
                "archive" if archived else "withdraw",
                "item",
                item_id,
                before,
                after,
            )
        return jsonify(data=after)

    @app.get("/api/audit")
    @login_required
    def audit_entries():
        entries = []
        for row in get_db().execute("SELECT * FROM audit_log ORDER BY id DESC"):
            entry = dict(row)
            for source, target in (("before_json", "before"), ("after_json", "after")):
                try:
                    entry[target] = json.loads(entry[source]) if entry[source] is not None else None
                except json.JSONDecodeError:
                    entry[target] = {"_unparseable_snapshot": entry[source]}
            entries.append(entry)
        return jsonify(data=entries)

    @app.errorhandler(sqlite3.IntegrityError)
    def integrity(_exc):
        return error("Die Änderung verletzt eine Datenregel.", 409, "conflict")

    return app
