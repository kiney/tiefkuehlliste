# Architektur und Produktentscheidungen

Die Anwendung ist ein einzelner Flask-Prozess mit serverseitigem Jinja-Einstieg, einer kleinen JSON-API und SQLite. Browser-State ist nur eine Darstellung des Servers; nach jeder bestätigten Änderung wird der betroffene Bestand neu geladen. Alle fachlichen Schreibvorgänge und ihr Audit-Eintrag laufen in derselben Transaktion.

## Mengen

Mengen bestehen aus geordneten Komponenten. `package` speichert eine ganzzahlige Anzahl und eine positive Packungsgröße, `loose` eine nichtnegative Restmenge. Gewicht wird als ganze Gramm, Stück als ganze Stück gespeichert; Eingaben in kg werden dezimal (maximal drei Nachkommastellen) exakt in Gramm umgerechnet. Gewicht und Stück dürfen in einem Eintrag nicht gemischt werden. Nullkomponenten werden beim Speichern entfernt; eine leere Komponentenliste archiviert den Eintrag, eine später positive Liste reaktiviert ihn.

Beispiele: `3 × 500 g`, `800 g`, `2 Stück` und `1 × 1000 g + 800 g` bleiben getrennt strukturiert und werden in dieser Reihenfolge angezeigt. Bei Entnahme wird eine Komponente ausdrücklich gewählt; die UI schlägt einen vorhandenen losen Rest vor einer vollen Packung vor. Eine ganze Packung reduziert deren Anzahl. Eine Teilentnahme aus einer Packung reduziert zunächst eine Packung und erzeugt den verbleibenden Inhalt als eigene lose Komponente. Vorhandene Reste werden nicht ungefragt zusammengefasst. Daher wird `1 × 1000 g + 800 g` bei Auswahl des 800-g-Rests und Entnahme von 200 g zu `1 × 1000 g + 600 g`. Bei `2 × 500 g + 250 g` führt zweimal 250 g entnehmen – zuerst aus dem vorgeschlagenen Rest, dann aus einer gewählten Packung – zu `1 × 500 g + 250 g`.

## Daten, API und Sicherheit

Migrationen sind nummerierte, idempotent registrierte SQL-Schritte. Alle fachlichen Tabellen sind `STRICT`. Ein partieller eindeutiger Index erlaubt höchstens eine Standardtruhe; Transaktionen sorgen beim Umschalten für genau eine. Beim ersten Start entsteht „Tiefkühltruhe“ als Standard.

Die API liegt unter `/api`, antwortet mit `{data: ...}` oder `{error: {code, message, fields?}}` und nutzt passende 2xx/4xx-Codes. Mutationen verlangen Anmeldung und einen CSRF-Header. Benutzer sowie Serveradresse und Port stammen aus der lokalen `config/config.yaml`; Passwörter werden ausschließlich als Werkzeug-Hashes gespeichert. CLI-Werte überschreiben Umgebungsvariablen und diese wiederum die YAML-Serverwerte. Flask signiert die Session; Cookies sind HttpOnly, SameSite=Lax und im dokumentierten HTTP-Lokalbetrieb nicht `Secure` (für HTTPS konfigurierbar). Es gibt keine Rollen. Audit-Daten sind nur lesbar und enthalten JSON-Snapshots vor/nach der Änderung.

Bekannte Grenzen des ersten Releases sind Einzelprozess-/lokaler Betrieb, keine Offline-Synchronisation und keine konfliktauflösende Mehrgerätebearbeitung. SQLite-Datei und Benutzerkonfiguration müssen vom Betreiber gesichert werden.

## Browser-Testentscheidung

Die Zielumgebung stellt keinen installierten Playwright-Testbrowser bereit; dessen zusätzlicher Download würde die kleine lokale Installation deutlich vergrößern. Deshalb nutzt das erste Release automatisierte Pytest-API-/Persistenztests und pure Node-Tests für Suche, Mengenformatierung und Theme sowie einen reproduzierbar protokollierten Chrome-DevTools-Smoke-Test. Das ist die in TASK-1 erlaubte Ausnahme; die Browserprüfung ergänzt die automatisierten fachlichen Tests, ersetzt sie nicht.
