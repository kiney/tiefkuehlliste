import sqlite3


def test_auth_csrf_and_logout(client):
    assert client.get("/").status_code == 302
    assert client.get("/api/freezers").status_code == 401
    client.get("/login")
    with client.session_transaction() as s:
        token = s["csrf_token"]
    assert (
        client.post(
            "/login", data={"username": "anna", "password": "wrong", "csrf_token": token}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/login", data={"username": "anna", "password": "secret", "csrf_token": "bad"}
        ).status_code
        == 403
    )


def test_inventory_and_archive_use_semantic_tables(client, auth):
    page = client.get("/", headers=auth)
    assert page.status_code == 200
    assert page.text.count('<table class="inventory-table">') == 2
    assert '<tbody id="items"></tbody>' in page.text
    assert '<tbody id="archived"></tbody>' in page.text


def test_strict_schema_and_single_default(app):
    db = sqlite3.connect(app.config["DATABASE"])
    tables = {
        r[0]: r[1]
        for r in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table'")
        if not r[0].startswith("sqlite_")
    }
    assert all("STRICT" in sql for sql in tables.values())
    assert db.execute("SELECT count(*) FROM freezers WHERE is_default=1").fetchone()[0] == 1


def test_freezers_items_quantities_archive_audit(client, auth):
    freezers = client.get("/api/freezers", headers=auth).json["data"]
    default = freezers[0]
    second = client.post("/api/freezers", headers=auth, json={"name": "Keller"})
    assert second.status_code == 201
    changed = client.patch(
        f"/api/freezers/{second.json['data']['id']}", headers=auth, json={"is_default": True}
    )
    assert changed.json["data"]["is_default"] == 1
    payload = {
        "freezer_id": default["id"],
        "product": "Brokkoli",
        "parts": [
            {"kind": "package", "amount": 3, "package_size": 500, "unit": "g"},
            {"kind": "loose", "amount": 0.8, "unit": "kg"},
        ],
        "frozen_on": "2026-01-02",
        "best_before": "2026-10-01",
        "note": "Scan-Beispiel",
    }
    made = client.post("/api/items", headers=auth, json=payload)
    assert made.status_code == 201
    item = made.json["data"]
    assert item["parts"] == [
        {"kind": "package", "amount": 3, "package_size": 500, "unit": "g"},
        {"kind": "loose", "amount": 800, "package_size": None, "unit": "g"},
    ]
    payload.update(product="Brokkoli offen", parts=[], note="")
    archived = client.put(f"/api/items/{item['id']}", headers=auth, json=payload).json["data"]
    assert archived["archived_at"]
    assert client.get(f"/api/freezers/{default['id']}/items", headers=auth).json["data"] == []
    payload["parts"] = [{"kind": "loose", "amount": 2, "unit": "piece"}]
    active = client.put(f"/api/items/{item['id']}", headers=auth, json=payload).json["data"]
    assert active["archived_at"] is None and active["note"] is None
    actions = [r["action"] for r in client.get("/api/audit", headers=auth).json["data"]]
    assert {"create", "archive", "reactivate", "update"} <= set(actions)


def test_validation_is_atomic(client, auth):
    freezer = client.get("/api/freezers", headers=auth).json["data"][0]
    bad = client.post(
        "/api/items", headers=auth, json={"freezer_id": freezer["id"], "product": " ", "parts": []}
    )
    assert bad.status_code == 400
    mixed = client.post(
        "/api/items",
        headers=auth,
        json={
            "freezer_id": freezer["id"],
            "product": "Mix",
            "parts": [
                {"kind": "loose", "amount": 1, "unit": "g"},
                {"kind": "loose", "amount": 1, "unit": "piece"},
            ],
        },
    )
    assert mixed.status_code == 400
    assert client.get("/api/audit", headers=auth).json["data"] == []


def test_partial_withdrawal_converts_package_and_merges_loose(client, auth):
    freezer = client.get("/api/freezers", headers=auth).json["data"][0]
    made = client.post(
        "/api/items",
        headers=auth,
        json={
            "freezer_id": freezer["id"],
            "product": "Gemüse",
            "parts": [
                {"kind": "package", "amount": 1, "package_size": 1000, "unit": "g"},
                {"kind": "loose", "amount": 800, "unit": "g"},
            ],
        },
    ).json["data"]
    result = client.post(
        f"/api/items/{made['id']}/withdraw",
        headers=auth,
        json={"part_index": 0, "amount": 200},
    )
    assert result.status_code == 200
    assert result.json["data"]["parts"] == [
        {"kind": "loose", "amount": 1600, "package_size": None, "unit": "g"}
    ]
