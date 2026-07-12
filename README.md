# Tiefkühlliste

Eine kleine, lokal betriebene Flask-/SQLite-Anwendung für mehrere Tiefkühltruhen. Sie unterstützt strukturierte Packungs- und Restmengen, clientseitige Suche, Archiv, Änderungsverlauf und ein mobiles Light-/Dark-UI.

## Installation mit uv

Voraussetzungen: Python 3.11+, `uv`; für die JavaScript-Modultests Node 20+.

```sh
uv sync --extra dev
cp config/users.example.yaml config/users.yaml
uv run tiefkuehlliste-password 'ein-langes-passwort'
```

Den ausgegebenen Hash (nicht das Passwort) in `config/users.yaml` eintragen. Danach einen zufälligen Sitzungsschlüssel setzen, Datenbank initialisieren und starten:

```sh
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
uv run flask --app tiefkuehlliste:create_app init-db
uv run tiefkuehlliste
```

Die Anwendung ist unter `http://127.0.0.1:5000` erreichbar. Beim ersten Start wird `instance/inventory.sqlite` inklusive Standardtruhe angelegt. `DATABASE` und `USERS_FILE` können alternative Pfade setzen; `HOST`, `PORT` und für einen HTTPS-Reverse-Proxy `COOKIE_SECURE=1` ändern den Betrieb.

Hinweis: Die Datenbank wird beim App-Start automatisch auf das aktuelle nummerierte Schema gebracht. Das zusätzliche `init-db`-Kommando ist idempotent und dient der expliziten Betriebsprüfung.

## Klassisches venv

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
cp config/users.example.yaml config/users.yaml
tiefkuehlliste-password 'ein-langes-passwort'
tiefkuehlliste
```

## Prüfen

```sh
uv run ruff format --check .
uv run ruff check .
uv run pytest
npm test
```

## Backup und Restore

Während des Backups keine Änderungen ausführen. Ein konsistentes Online-Backup gelingt mit `sqlite3 instance/inventory.sqlite ".backup backup.sqlite"`; alternativ die Anwendung stoppen und die Datei kopieren. Zum Restore Anwendung stoppen, die defekte Datenbank sicher verwahren, die Backup-Datei an den in `DATABASE` konfigurierten Pfad kopieren und neu starten. `config/users.yaml` und `SECRET_KEY` separat sichern.

Details zu Mengen-, API- und Sicherheitsentscheidungen stehen in [docs/architecture.md](docs/architecture.md). Es gibt bewusst keine Rollen, Cloud-Synchronisation, Barcodes oder Warenwirtschaftsfunktionen.
Das konkrete mobile/desktop Prüfergebnis und die Interaktionszählung stehen in [docs/verification.md](docs/verification.md).
