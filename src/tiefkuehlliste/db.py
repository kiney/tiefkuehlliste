import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL) STRICT;
CREATE TABLE IF NOT EXISTS freezers(
 id INTEGER PRIMARY KEY, name TEXT NOT NULL CHECK(length(trim(name)) > 0),
 is_default INTEGER NOT NULL DEFAULT 0 CHECK(is_default IN (0,1)),
 created_at TEXT NOT NULL, updated_at TEXT NOT NULL
) STRICT;
CREATE UNIQUE INDEX IF NOT EXISTS one_default_freezer ON freezers(is_default) WHERE is_default=1;
CREATE TABLE IF NOT EXISTS items(
 id INTEGER PRIMARY KEY, freezer_id INTEGER NOT NULL REFERENCES freezers(id),
 product TEXT NOT NULL CHECK(length(trim(product)) > 0), frozen_on TEXT, best_before TEXT,
 note TEXT, dimension TEXT NOT NULL CHECK(dimension IN ('weight','count')),
 archived_at TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
) STRICT;
CREATE TABLE IF NOT EXISTS quantity_parts(
 id INTEGER PRIMARY KEY, item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
 position INTEGER NOT NULL, kind TEXT NOT NULL CHECK(kind IN ('package','loose')),
 amount INTEGER NOT NULL CHECK(amount >= 0), package_size INTEGER,
 CHECK((kind='package' AND package_size IS NOT NULL AND package_size > 0) OR
       (kind='loose' AND package_size IS NULL)), UNIQUE(item_id, position)
) STRICT;
CREATE TABLE IF NOT EXISTS audit_log(
 id INTEGER PRIMARY KEY, occurred_at TEXT NOT NULL, username TEXT NOT NULL,
 action TEXT NOT NULL, entity TEXT NOT NULL, entity_id INTEGER NOT NULL,
 before_json TEXT, after_json TEXT
) STRICT;
"""


def now():
    return datetime.now(UTC).isoformat(timespec="seconds")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    if not db.execute("SELECT 1 FROM schema_migrations WHERE version=1").fetchone():
        db.execute("INSERT INTO schema_migrations VALUES(1,?)", (now(),))
    if not db.execute("SELECT 1 FROM freezers").fetchone():
        stamp = now()
        db.execute(
            "INSERT INTO freezers(name,is_default,created_at,updated_at) VALUES(?,1,?,?)",
            ("Tiefkühltruhe", stamp, stamp),
        )
    db.commit()


@contextmanager
def transaction():
    db = get_db()
    try:
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise


def audit(db, username, action, entity, entity_id, before=None, after=None):
    db.execute(
        "INSERT INTO audit_log(occurred_at,username,action,entity,entity_id,before_json,after_json) VALUES(?,?,?,?,?,?,?)",
        (
            now(),
            username,
            action,
            entity,
            entity_id,
            json.dumps(before, ensure_ascii=False) if before is not None else None,
            json.dumps(after, ensure_ascii=False) if after is not None else None,
        ),
    )
