# Architektur und Produktentscheidungen

[Deutsche Fassung](#deutsch) · [Englische Fassung](#english)

## Deutsch

Die Anwendung ist ein einzelner Flask-Prozess mit serverseitigem Jinja-Einstieg, einer kleinen JSON-API und SQLite. Browser-State ist nur eine Darstellung des Servers; nach jeder bestätigten Änderung wird der betroffene Bestand neu geladen. Alle fachlichen Schreibvorgänge und ihr Audit-Eintrag laufen in derselben Transaktion.

### Mengen

Mengen bestehen aus geordneten Komponenten. `package` speichert eine ganzzahlige Anzahl und eine positive Packungsgröße, `loose` eine nichtnegative Restmenge. Gewicht wird als ganze Gramm, Stück als ganze Stück gespeichert; Eingaben in kg werden dezimal (maximal drei Nachkommastellen) exakt in Gramm umgerechnet. Gewicht und Stück dürfen in einem Eintrag nicht gemischt werden. Nullkomponenten werden beim Speichern entfernt; eine leere Komponentenliste archiviert den Eintrag, eine später positive Liste reaktiviert ihn.

Beispiele: `3 × 500 g`, `800 g`, `2 Stück` und `1 × 1000 g + 800 g` bleiben getrennt strukturiert und werden in dieser Reihenfolge angezeigt. Bei Entnahme wird eine Komponente ausdrücklich gewählt; die UI schlägt einen vorhandenen losen Rest vor einer vollen Packung vor. Eine ganze Packung reduziert deren Anzahl. Eine Teilentnahme aus einer Packung reduziert zunächst eine Packung und erzeugt den verbleibenden Inhalt als eigene lose Komponente. Vorhandene Reste werden nicht ungefragt zusammengefasst. Daher wird `1 × 1000 g + 800 g` bei Auswahl des 800-g-Rests und Entnahme von 200 g zu `1 × 1000 g + 600 g`. Bei `2 × 500 g + 250 g` führt zweimal 250 g entnehmen – zuerst aus dem vorgeschlagenen Rest, dann aus einer gewählten Packung – zu `1 × 500 g + 250 g`.

Beim Neuanlegen eines gleichnamigen Produkts bietet die UI vorhandene, dimensionskompatible Einträge als Zusammenführungsziel an. Gleiche Packungsgrößen werden dabei zu einer Packungskomponente addiert; lose Reste bleiben getrennt. Der Zieleintrag behält Einfrierdatum, Haltbarkeit und Hinweis. Für unterschiedliche Chargen oder Haltbarkeiten kann der Nutzer ausdrücklich separat anlegen.

### Daten, API und Sicherheit

Migrationen sind nummerierte, idempotent registrierte SQL-Schritte. Alle fachlichen Tabellen sind `STRICT`. Ein partieller eindeutiger Index erlaubt höchstens eine Standardtruhe; Transaktionen sorgen beim Umschalten für genau eine. Beim ersten Start entsteht „Tiefkühltruhe“ als Standard.

Die API liegt unter `/api`, antwortet mit `{data: ...}` oder `{error: {code, message, fields?}}` und nutzt passende 2xx/4xx-Codes. Mutationen verlangen Anmeldung und einen CSRF-Header. Benutzer sowie Serveradresse und Port stammen aus der lokalen `config/config.yaml`; Passwörter werden ausschließlich als Werkzeug-Hashes gespeichert. CLI-Werte überschreiben Umgebungsvariablen und diese wiederum die YAML-Serverwerte. Flask signiert die Session; Cookies sind HttpOnly, SameSite=Lax und im dokumentierten HTTP-Lokalbetrieb nicht `Secure` (für HTTPS konfigurierbar). Es gibt keine Rollen. Audit-Daten sind nur lesbar und enthalten JSON-Snapshots vor/nach der Änderung.

Bekannte Grenzen des ersten Releases sind Einzelprozess-/lokaler Betrieb, keine Offline-Synchronisation und keine konfliktauflösende Mehrgerätebearbeitung. SQLite-Datei und Benutzerkonfiguration müssen vom Betreiber gesichert werden.

### Browser-Testentscheidung

Die Zielumgebung stellt keinen installierten Playwright-Testbrowser bereit; dessen zusätzlicher Download würde die kleine lokale Installation deutlich vergrößern. Deshalb nutzt das erste Release automatisierte Pytest-API-/Persistenztests und pure Node-Tests für Suche, Mengenformatierung und Theme sowie einen reproduzierbar protokollierten Chrome-DevTools-Smoke-Test. Das ist die in TASK-1 erlaubte Ausnahme; die Browserprüfung ergänzt die automatisierten fachlichen Tests, ersetzt sie nicht.


## English

The application runs as a single Flask process with a server-rendered Jinja entry point, a small JSON API, and SQLite. Browser state is only a representation of server state; after every confirmed change, the affected inventory is reloaded. Every domain write and its audit entry run in the same transaction.

### Quantities

Quantities consist of ordered components. A `package` stores an integer count and a positive package size, while a `loose` component stores a non-negative remainder. Weight is stored as whole grams and item counts as whole units; kilogram input is converted exactly to grams using decimals with no more than three decimal places. Weight and item counts cannot be mixed in a single entry. Zero-valued components are removed when saved; an empty component list archives the entry, and a later positive list reactivates it.

Examples such as `3 × 500 g`, `800 g`, `2 items`, and `1 × 1000 g + 800 g` remain separately structured and are displayed in that order. A component must be selected explicitly when taking something out; the UI suggests an existing loose remainder before a full package. Taking a whole package reduces its count. Taking part of a package first reduces the package count by one and creates the remaining contents as a separate loose component. Existing remainders are not combined without asking. Therefore, selecting the 800 g remainder in `1 × 1000 g + 800 g` and taking 200 g results in `1 × 1000 g + 600 g`. With `2 × 500 g + 250 g`, taking 250 g twice—first from the suggested remainder and then from a selected package—results in `1 × 500 g + 250 g`.

When a product with the same name is added, the UI offers existing entries with a compatible dimension as merge targets. Packages of the same size are added to a package component, while loose remainders stay separate. The target entry keeps its freezing date, best-before date, and note. Users can explicitly create a separate entry for different batches or shelf lives.

### Data, API, and security

Migrations are numbered, idempotently registered SQL steps. All domain tables are `STRICT`. A partial unique index permits at most one default freezer; transactions ensure that switching the default results in exactly one. On first launch, “Tiefkühltruhe” is created as the default.

The API is available under `/api`, responds with `{data: ...}` or `{error: {code, message, fields?}}`, and uses appropriate 2xx/4xx status codes. Mutations require authentication and a CSRF header. Users, server address, and port come from the local `config/config.yaml`; passwords are stored exclusively as password-tool hashes. CLI values override environment variables, which in turn override the YAML server values. Flask signs the session; cookies are HttpOnly and SameSite=Lax, and are not `Secure` in the documented local HTTP setup (configurable for HTTPS). There are no roles. Audit data is read-only and contains JSON snapshots from before and after each change.

Known limitations of the first release are single-process/local operation, no offline synchronization, and no conflict-resolving multi-device editing. Operators must back up the SQLite file and user configuration.

### Browser testing decision

The target environment does not provide an installed Playwright test browser, and downloading one would significantly increase the size of this small local installation. The first release therefore uses automated Pytest API/persistence tests, pure Node tests for search, quantity formatting, and themes, plus a reproducibly documented Chrome DevTools smoke test. This is the exception permitted by TASK-1; browser testing supplements the automated domain tests rather than replacing them.
