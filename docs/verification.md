# Abnahmeprotokoll

[Deutsche Fassung](#deutsch) · [Englische Fassung](#english)

## Deutsch

Abnahme am 12. Juli 2026 gegen die lokale Flask-Anwendung.

### Automatisiert

- `uv sync --extra dev`: frische projektlokale Umgebung erfolgreich aufgelöst und installiert.
- `ruff format --check .` und `ruff check .`: erfolgreich.
- `pytest`: 5 Tests erfolgreich; STRICT-Schema, Standardtruhe, Auth/CSRF, CRUD, optionale Felder, Mengenvarianten, Dimensionsvalidierung, Audit-Atomarität, Archiv/Reaktivierung und Teilentnahme abgedeckt.
- `npm test`: Suche, Mengenformatierung und Theme-Zustandsfolge erfolgreich.
- Neue Datenbank unter `/tmp/tiefkuehlliste-fresh.sqlite` per dokumentiertem `flask ... init-db` erfolgreich initialisiert.

### Browser-Smoke-Test

Chrome DevTools, mobil 390 × 844 mit Touch und Desktop 1440 × 900:

- Login mit konfiguriertem Benutzer und Logout erfolgreich.
- Standardtruhe öffnete automatisch; zweite Truhe „Kellertruhe“ angelegt und Wechsel zeigte deren leeren Bestand.
- `3 × 500 g` und `800 g` angelegt und verständlich dargestellt.
- Suche nach `800` filterte sofort auf genau einen Eintrag.
- Menge von `800 g` auf `600 g` geändert.
- „Alles entnommen“ archivierte den Eintrag; Eingabe von `500 g` reaktivierte ihn.
- Verlauf zeigte Benutzer, Aktion, Entität, ID und Zeitpunkt chronologisch.
- System-Dark-Mode erkannt; manueller Dark-Zustand in `localStorage` und DOM persistent gesetzt; Light-Zustand ebenfalls durchschaltbar.
- Mobil und Desktop betrug die Differenz aus Dokument- und Viewportbreite 0 px; sichtbare Labels und zugängliche Namen waren im Accessibility-Tree vorhanden.

Einlagern benötigt Produkttext, Mengentext und Speichern (3 zielgerichtete Interaktionen, innerhalb des Ziels 4). Eine ganze Packung wird über „Aus Packung“, vorbelegten Packungswert und Bestätigung in höchstens 3 Interaktionen entnommen. „Alles entnommen“ benötigt Aktion und Sicherheitsbestätigung (2, innerhalb des Ziels 3). Die Teilentnahme benennt die gewählte Packung ausdrücklich und bewahrt die Eingabe bei Serverfehlern im Formular.

Bei der Prüfung gefundener horizontaler Mobil-Überlauf und eine `null`-Hinweisdarstellung wurden behoben und anschließend erneut geprüft. Keine kritischen oder hohen bekannten Defekte verblieben.


## English

Verified against the local Flask application on July 12, 2026.

### Automated checks

- `uv sync --extra dev`: fresh project-local environment resolved and installed successfully.
- `ruff format --check .` and `ruff check .`: successful.
- `pytest`: 5 tests passed; covering the STRICT schema, default freezer, authentication/CSRF, CRUD, optional fields, quantity variants, dimension validation, audit atomicity, archiving/reactivation, and partial withdrawals.
- `npm test`: search, quantity formatting, and theme state transitions passed.
- A new database at `/tmp/tiefkuehlliste-fresh.sqlite` was initialized successfully using the documented `flask ... init-db` command.

### Browser smoke test

Chrome DevTools, mobile at 390 × 844 with touch and desktop at 1440 × 900:

- Login with the configured user and logout succeeded.
- The default freezer opened automatically; a second freezer named “Kellertruhe” was created, and switching to it showed its empty inventory.
- `3 × 500 g` and `800 g` were added and displayed clearly.
- Searching for `800` immediately filtered the list to exactly one entry.
- The quantity was changed from `800 g` to `600 g`.
- “Alles entnommen” archived the entry; entering `500 g` reactivated it.
- The history showed user, action, entity, ID, and timestamp in chronological order.
- System dark mode was detected; the manual dark setting persisted in `localStorage` and the DOM, and the light setting could also be selected.
- On mobile and desktop, the difference between document width and viewport width was 0 px; visible labels and accessible names were present in the accessibility tree.

Storing an item requires the product text, quantity text, and Save action (3 targeted interactions, within the goal of 4). Taking a whole package requires at most 3 interactions: “Aus Packung”, the prefilled package value, and confirmation. “Alles entnommen” requires the action and a safety confirmation (2 interactions, within the goal of 3). Partial withdrawal explicitly identifies the selected package and preserves the input in the form if the server returns an error.

Horizontal mobile overflow and a `null` note display found during verification were fixed and retested. No known critical or high-severity defects remained.
