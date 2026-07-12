# Abnahmeprotokoll

Abnahme am 12. Juli 2026 gegen die lokale Flask-Anwendung.

## Automatisiert

- `uv sync --extra dev`: frische projektlokale Umgebung erfolgreich aufgelöst und installiert.
- `ruff format --check .` und `ruff check .`: erfolgreich.
- `pytest`: 5 Tests erfolgreich; STRICT-Schema, Standardtruhe, Auth/CSRF, CRUD, optionale Felder, Mengenvarianten, Dimensionsvalidierung, Audit-Atomarität, Archiv/Reaktivierung und Teilentnahme abgedeckt.
- `npm test`: Suche, Mengenformatierung und Theme-Zustandsfolge erfolgreich.
- Neue Datenbank unter `/tmp/tiefkuehlliste-fresh.sqlite` per dokumentiertem `flask ... init-db` erfolgreich initialisiert.

## Browser-Smoke-Test

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
