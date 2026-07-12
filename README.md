# Tiefkühlliste

Eine kleine, lokal betriebene Flask-/SQLite-Anwendung für mehrere Tiefkühltruhen. Sie unterstützt strukturierte Packungs- und Restmengen, clientseitige Suche, Archiv, Änderungsverlauf und ein mobiles Light-/Dark-UI.

## Installation mit uv

Voraussetzungen: Python 3.11+, `uv`; für die JavaScript-Modultests Node 20+.

```sh
uv sync --extra dev
cp config/config.example.yaml config/config.yaml
uv run tiefkuehlliste-password 'ein-langes-passwort'
```

Den ausgegebenen Hash (nicht das Passwort) in `config/config.yaml` eintragen. Dort können außerdem Bind-Adresse und Port gesetzt werden:

```yaml
server:
  host: 127.0.0.1
  port: 5050
```

Danach einen zufälligen Sitzungsschlüssel setzen, Datenbank initialisieren und starten:

```sh
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
uv run flask --app tiefkuehlliste:create_app init-db
uv run tiefkuehlliste
```

Die URL folgt `server.host` und `server.port`. `tiefkuehlliste --port 8080` beziehungsweise `--host` überschreiben die YAML-Werte; `PORT` und `HOST` sind nachrangige Umgebungsvariablen. Mit `--config PFAD` oder `TIEFKUEHLLISTE_CONFIG` lässt sich eine andere Konfigurationsdatei wählen. Beim ersten Start wird `instance/inventory.sqlite` inklusive Standardtruhe angelegt. `DATABASE` setzt einen alternativen Datenbankpfad; für einen HTTPS-Reverse-Proxy aktiviert `COOKIE_SECURE=1` sichere Cookies.

Hinweis: Die Datenbank wird beim App-Start automatisch auf das aktuelle nummerierte Schema gebracht. Das zusätzliche `init-db`-Kommando ist idempotent und dient der expliziten Betriebsprüfung.

## Virtuelle Umgebung mit `uv venv`

```sh
uv venv
. .venv/bin/activate
uv pip install -e '.[dev]'
cp config/config.example.yaml config/config.yaml
tiefkuehlliste-password 'ein-langes-passwort'
tiefkuehlliste
```

Für einen direkten lokalen Test kann alternativ die mitgelieferte, von Git ignorierte
`config/config.yaml` verwendet werden. Sie nutzt Port `5050`; die Zugangsdaten stehen als Kommentar in der Datei.

## Prüfen

```sh
uv run ruff format --check .
uv run ruff check .
uv run pytest
npm test
```

## Backup und Restore

Während des Backups keine Änderungen ausführen. Ein konsistentes Online-Backup gelingt mit `sqlite3 instance/inventory.sqlite ".backup backup.sqlite"`; alternativ die Anwendung stoppen und die Datei kopieren. Zum Restore Anwendung stoppen, die defekte Datenbank sicher verwahren, die Backup-Datei an den in `DATABASE` konfigurierten Pfad kopieren und neu starten. `config/config.yaml` und `SECRET_KEY` separat sichern.

Details zu Mengen-, API- und Sicherheitsentscheidungen stehen in [docs/architecture.md](docs/architecture.md). Es gibt bewusst keine Rollen, Cloud-Synchronisation, Barcodes oder Warenwirtschaftsfunktionen.
Das konkrete mobile/desktop Prüfergebnis und die Interaktionszählung stehen in [docs/verification.md](docs/verification.md).
