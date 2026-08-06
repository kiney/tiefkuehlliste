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

## Container mit Podman

Das Image lauscht standardmäßig auf `0.0.0.0:2480` und läuft als nicht
privilegierter Benutzer. Im Container werden diese Pfade verwendet:

- `/config/config.yaml`: YAML-Konfiguration, nur lesend einbinden
- `/data/inventory.sqlite`: SQLite-Datenbank; das gesamte Verzeichnis `/data`
  beschreibbar und persistent einbinden

Für eine direkt auf dem Host sichtbare Datenbank das lokale, von Git ignorierte
Verzeichnis `instance/` verwenden:

```sh
podman build -t tiefkuehlliste .
mkdir -p instance
podman run --rm -p 2480:2480 \
  -v ./instance:/data:Z,U \
  -v ./config/config.yaml:/config/config.yaml:ro,Z \
  -e SECRET_KEY='einen-langen-zufaelligen-wert-eintragen' \
  tiefkuehlliste
```

Damit liegt die Datenbank dauerhaft unter `./instance/inventory.sqlite`. Die
Podman-Option `U` passt den Eigentümer des Host-Verzeichnisses an den
Container-Benutzer an und kann dessen Eigentümer auf dem Host verändern. `Z`
setzt bei aktiviertem SELinux das passende private Label. Das gesamte Verzeichnis
wird eingebunden, damit SQLite auch Journaldateien daneben anlegen kann.

Alternativ hält ein benanntes Podman-Volume die Daten außerhalb des
Projektverzeichnisses:

```sh
podman volume create tiefkuehlliste-data
podman run --rm -p 2480:2480 \
  -v tiefkuehlliste-data:/data:U \
  -v ./config/config.yaml:/config/config.yaml:ro,Z \
  -e SECRET_KEY='einen-langen-zufaelligen-wert-eintragen' \
  tiefkuehlliste
```

Vor dem Start `config/config.yaml` wie oben beschrieben anlegen und einen echten
Passwort-Hash eintragen. Die Konfiguration bleibt durch `ro` schreibgeschützt;
`SECRET_KEY` wird separat als Umgebungsvariable übergeben. Ohne expliziten
`/data`-Mount erzeugt Podman wegen der `VOLUME`-Anweisung ein anonymes Volume,
das sich für gezielte Backups und Restores schlechter zuordnen lässt.

Ein anderer Host-Port kann links in der Portzuordnung gewählt werden,
beispielsweise `-p 8080:2480`. Um auch den Port im Container zu ändern,
zusätzlich `-e PORT=8080` und `-p 8080:8080` setzen.

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
