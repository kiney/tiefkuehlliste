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


def test_withdrawal_prefers_explicit_loose_source(client, auth):
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
        json={"part_index": 1, "amount": 200},
    )
    assert result.status_code == 200
    assert result.json["data"]["parts"] == [
        {"kind": "package", "amount": 1, "package_size": 1000, "unit": "g"},
        {"kind": "loose", "amount": 600, "package_size": None, "unit": "g"},
    ]


def test_repeated_withdrawal_uses_selected_component_without_merging(client, auth):
    freezer = client.get("/api/freezers", headers=auth).json["data"][0]
    made = client.post(
        "/api/items",
        headers=auth,
        json={
            "freezer_id": freezer["id"],
            "product": "Brokkoli",
            "parts": [
                {"kind": "package", "amount": 2, "package_size": 500, "unit": "g"},
                {"kind": "loose", "amount": 250, "unit": "g"},
            ],
        },
    ).json["data"]
    first = client.post(
        f"/api/items/{made['id']}/withdraw",
        headers=auth,
        json={"part_index": 1, "amount": 250},
    ).json["data"]
    assert first["parts"] == [{"kind": "package", "amount": 2, "package_size": 500, "unit": "g"}]
    second = client.post(
        f"/api/items/{made['id']}/withdraw",
        headers=auth,
        json={"part_index": 0, "amount": 250},
    ).json["data"]
    assert second["parts"] == [
        {"kind": "package", "amount": 1, "package_size": 500, "unit": "g"},
        {"kind": "loose", "amount": 250, "package_size": None, "unit": "g"},
    ]


def test_withdrawal_from_loose_only_and_whole_package(client, auth):
    freezer = client.get("/api/freezers", headers=auth).json["data"][0]
    loose = client.post(
        "/api/items",
        headers=auth,
        json={
            "freezer_id": freezer["id"],
            "product": "Steak",
            "parts": [{"kind": "loose", "amount": 500, "unit": "g"}],
        },
    ).json["data"]
    reduced = client.post(
        f"/api/items/{loose['id']}/withdraw",
        headers=auth,
        json={"part_index": 0, "amount": 200},
    ).json["data"]
    assert reduced["parts"][0]["amount"] == 300

    package = client.post(
        "/api/items",
        headers=auth,
        json={
            "freezer_id": freezer["id"],
            "product": "Pizza",
            "parts": [{"kind": "package", "amount": 2, "package_size": 1, "unit": "piece"}],
        },
    ).json["data"]
    reduced = client.post(
        f"/api/items/{package['id']}/withdraw",
        headers=auth,
        json={"part_index": 0, "amount": 1},
    ).json["data"]
    assert reduced["parts"][0]["amount"] == 1


def test_equal_package_sizes_are_combined(client, auth):
    freezer = client.get("/api/freezers", headers=auth).json["data"][0]
    made = client.post(
        "/api/items",
        headers=auth,
        json={
            "freezer_id": freezer["id"],
            "product": "Erbsen",
            "parts": [
                {"kind": "package", "amount": 1, "package_size": 500, "unit": "g"},
                {"kind": "package", "amount": 2, "package_size": 500, "unit": "g"},
            ],
        },
    ).json["data"]
    assert made["parts"] == [{"kind": "package", "amount": 3, "package_size": 500, "unit": "g"}]


def test_audit_api_returns_all_entries_with_parsed_snapshots(client, auth):
    db = sqlite3.connect(client.application.config["DATABASE"])
    rows = [
        (
            f"2026-01-01T00:00:{index % 60:02d}+00:00",
            "anna",
            "update",
            "item",
            index,
            '{"amount": 1}',
            '{"amount": 2, "parts": [{"kind": "loose", "amount": 2}]}',
        )
        for index in range(205)
    ]
    db.executemany(
        "INSERT INTO audit_log(occurred_at,username,action,entity,entity_id,before_json,after_json) VALUES(?,?,?,?,?,?,?)",
        rows,
    )
    db.commit()
    response = client.get("/api/audit", headers=auth)
    assert response.status_code == 200
    assert len(response.json["data"]) == 205
    assert response.json["data"][0]["before"] == {"amount": 1}
    assert response.json["data"][0]["after"]["parts"][0]["kind"] == "loose"
