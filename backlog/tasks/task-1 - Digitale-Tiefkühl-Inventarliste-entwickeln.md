---
id: TASK-1
title: Digitale Tiefkühl-Inventarliste entwickeln
status: To Do
assignee: []
created_date: '2026-07-11 23:56'
updated_date: '2026-07-11 23:59'
labels:
  - umbrella
  - feature
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Ziel und Kontext

Eine lokal betreibbare, responsive Webanwendung entwickeln, die die Papierliste aus inventarliste.tex beziehungsweise inventarliste.pdf ersetzt. Der Bestand mehrerer Tiefkühltruhen soll am Desktop und besonders am Smartphone mit wenigen Interaktionen erfasst, durchsucht, geändert und archiviert werden können.

Der beigefügte Scan Scan 2026-07-12 00.40.34.pdf zeigt den konkreten Bedarf: Mengen werden häufig durchgestrichen und neu eingetragen; verwendet werden Stückzahlen, Gewichte, Packungsgrößen sowie Kombinationen mehrerer Packungen. Dieses reale Änderungsmuster ist bei Mengenmodell und Bedienung maßgeblich.

Dieser Umbrella Task beschreibt das vollständige Produktziel. Der ausführende AI-Agent muss vor der Implementierung eigenständig sinnvolle Subtasks im Backlog anlegen, Abhängigkeiten festlegen, sie umsetzen und verifizieren. Kleinere technische Entscheidungen darf er autonom treffen. Produktrelevante Entscheidungen sind früh als Backlog-Entscheidung oder ADR zu dokumentieren.

## Leitprinzipien

- Usability und geringe Klickzahl haben Vorrang vor visueller Raffinesse.
- Mobile Nutzung beim Einlagern, Entnehmen und Nachsehen ist ein primärer Anwendungsfall.
- Die Lösung bleibt klein, wartbar und lokal betreibbar.
- Pragmatismus hat Vorrang vor REST-Dogmatismus und unnötiger Abstraktion.
- Keine Erweiterung zu einem komplexen Warenwirtschaftssystem.

## Verbindliche Architektur

- Backend: Python mit Flask.
- Persistenz: SQLite; alle Anwendungstabellen verwenden den STRICT-Modus. Ein nachvollziehbarer Schema-Initialisierungs- und Upgrade-Mechanismus ist vorhanden.
- Python-Projekt: pyproject.toml, uv und projektlokale virtuelle Umgebung. Die README erklärt den Ablauf auch für Nutzer klassischer venv-Workflows.
- Qualität: Ruff für Linting und Black-artige Formatierung; reproduzierbare Prüfkommandos.
- Frontend: serverseitige Jinja-Templates plus möglichst wenig, modular aufgebautes Vanilla JavaScript. Kein großes SPA-Framework und zunächst kein HTMX.
- Frontend und Backend kommunizieren für dynamische Bestandsfunktionen über eine einfache, konsistente REST-artige JSON-API. Zweckmäßige Abweichungen sind erlaubt und zu dokumentieren.
- Die aktive Datenmenge ist klein; Suche und Filterung erfolgen clientseitig über den geladenen aktuellen Bestand.
- Frontend ist mobile-first, responsiv, Touch-freundlich, tastaturbedienbar und unterstützt Light- und Dark-Mode.
- Ein verfügbarer Browser MCP darf gemäß AGENTS.md während der Entwicklung für visuelle, responsive und interaktive Prüfungen verwendet werden.

## Truhen

- Das erste Release unterstützt mehrere benannte Tiefkühltruhen.
- Genau eine Truhe ist als klare Standardtruhe markiert. Die Anwendung öffnet beziehungsweise verwendet sie in schnellen Abläufen automatisch.
- Nutzer können die aktive Truhe mit wenigen Interaktionen wechseln.
- Truhen können mindestens angelegt, umbenannt und als Standard gesetzt werden.
- Das Verhalten beim Löschen einer Truhe mit Einträgen muss sicher sein. Empfohlen ist, das Löschen belegter Truhen zu verhindern oder nur eine explizite Archivierung anzubieten.
- Datenbankregeln verhindern, dass mehrere Standardtruhen existieren. Beim ersten Start wird entweder eine sinnvoll benannte Standardtruhe erzeugt oder die Ersteinrichtung fordert deren Namen an.

## Mengenmodell

Die Menge wird als Liste strukturierter Mengenbestandteile modelliert. So bleiben Null, Archivierung und Berechnungen eindeutig, während reale Kombinationen ohne Freitext-Tricks darstellbar sind.

Mindestens zwei Bestandteiltypen sind vorzusehen:

- Packungsbestand: nichtnegative Anzahl mal Packungsgröße und Einheit, zum Beispiel 1 × 1000 g oder 3 × 500 g;
- loser beziehungsweise angebrochener Bestand: nichtnegative Restmenge mit Einheit, zum Beispiel 800 g oder 2 Stück.

Ein Inventareintrag darf mehrere kompatible Bestandteile enthalten. Eine volle 1000-g-Brokkolitüte plus eine angebrochene Tüte mit 800 g wird als 1 × 1000 g + 800 g gespeichert und genau so verständlich angezeigt. Mengenbestandteile sind strukturiert, nicht bloß ein Anzeige-String. Ein optionaler kurzer Hinweis bleibt für nicht strukturierbare Besonderheiten verfügbar.

Bestandteile eines Eintrags müssen dieselbe physikalische Dimension verwenden; Gramm und Kilogramm dürfen normalisiert kombiniert werden, Gewicht und Stück jedoch nicht. Benötigt ein Produkt inkompatible Dimensionen, werden getrennte Inventareinträge verwendet. Mengen werden exakt gespeichert, etwa als skalierte Integer in kanonischen Basiseinheiten; binäre Gleitkommazahlen sind ausgeschlossen. In SQLite ist dafür vorzugsweise eine eigene STRICT-Kindertabelle für Mengenbestandteile zu verwenden.

Bei Teilentnahme aus einer vollen Packung muss die Anwendung den Bestand bequem umwandeln können: Aus 1 × 1000 g und einer Entnahme von 200 g entsteht 800 g loser Rest. Existiert zusätzlich bereits ein loser Rest, muss die UI eine verständliche, deterministische Darstellung erzeugen, ohne Daten zu verlieren. Die genaue Zusammenfassungsregel wird durch Tests mit den Beispielen aus dem Scan abgesichert.

Ein Eintrag wird atomar archiviert, sobald keine positive Menge mehr vorhanden ist, also alle Bestandteile null oder entfernt sind. Sobald bei einem archivierten Eintrag wieder mindestens ein positiver Bestandteil gespeichert wird, wird er automatisch reaktiviert.

Die Erfassung startet mit einem einfachen Mengenbestandteil. Weitere Bestandteile und Packungsgröße werden nur bei Bedarf über eine gut erreichbare Hinzufügen-Aktion eingeblendet. Zulässige Einheiten, Normalisierung und Dezimalregeln werden früh festgelegt und in Backend sowie UI identisch validiert.

## Inventareintrag

Mindestens folgende Felder:

- stabile ID;
- Referenz auf eine Truhe;
- Produkt oder Bezeichnung: Pflichtfeld, nach Trimmen nicht leer;
- strukturierte Menge gemäß Mengenmodell: Pflicht;
- Einfrierdatum: optionales Datum;
- Haltbar bis: optionales Datum;
- Archivierungszeitpunkt oder äquivalenter Archivstatus;
- Erstellungs- und Änderungszeitpunkt.

## Anmeldung und Änderungsprotokoll

- Die Anwendung besitzt einen einfachen Login mit Benutzername und Passwort.
- Benutzer werden ausschließlich aus einer festen, dokumentierten YAML-Konfigurationsdatei geladen; es gibt keine Benutzerverwaltung in der UI und keine Rollen oder Berechtigungsstufen. Jeder konfigurierte Benutzer darf alles sehen und ändern.
- Die YAML-Datei enthält mindestens eine Benutzerliste mit Benutzername und sicherem Passwort-Hash. Passwörter dürfen nicht im Klartext in das Repository gelangen. Eine versionierte Beispielkonfiguration ohne echte Secrets und eine ignorierte lokale Konfigurationsdatei sind vorzusehen; ein dokumentiertes Kommando erzeugt den Passwort-Hash.
- Nach erfolgreicher Anmeldung wird eine sichere serverseitig geschützte Session verwendet. Logout und verständliches Verhalten bei abgelaufener Session sind vorhanden.
- Zustandsändernde Browser-Anfragen sind gegen CSRF geschützt; Cookies besitzen für lokalen Betrieb sinnvolle Sicherheitsattribute.
- Eine append-only gedachte Audit-Log-Tabelle protokolliert mindestens Zeitpunkt, angemeldeten Benutzernamen, Aktion, betroffene Entität und ID sowie ausreichende Vorher- und Nachher-Daten zur Nachvollziehbarkeit.
- Mindestens Änderungen an Inventareinträgen, Archivierung, Reaktivierung sowie Änderungen an Truhen werden protokolliert.
- Das Audit-Log ist zunächst keine komplexe Benutzeroberfläche. Eine einfache, lesbare Änderungsverlauf-Ansicht ist jedoch bereitzustellen, damit die Anforderung wer wann was geändert hat praktisch nutzbar ist.
- Audit-Einträge werden bei derselben Datenbanktransaktion wie die fachliche Änderung geschrieben und sind über normale API-Operationen nicht veränderbar oder löschbar.

## Erforderliche Nutzerabläufe

- Einloggen und ausloggen.
- Standardtruhe direkt mit ihrem aktiven Bestand öffnen.
- Aktive Truhe schnell wechseln und klar erkennen.
- Truhen anlegen, umbenennen und Standardtruhe ändern.
- Neuen Eintrag mit Produkt und einfacher Menge schnell anlegen; Datums-, Packungsgrößen- und Hinweisfelder behindern den schnellen Ablauf nicht.
- Bestehenden Eintrag bearbeiten und Menge besonders schnell ändern.
- Menge auf null setzen und damit archivieren.
- Archivierten Eintrag durch Eingabe einer Menge größer null automatisch reaktivieren.
- Aktiven Bestand unmittelbar während der Eingabe nach Produkt und sinnvollerweise Mengentext durchsuchen; Truhenzuordnung bleibt eindeutig.
- Archivierte Einträge getrennt ansehen.
- Einfachen Änderungsverlauf einsehen.
- Klare Lade-, Leer-, Validierungs-, Authentifizierungs- und Fehlerzustände sehen.

## Konkrete schnelle Bedienabläufe

Die UI wird nicht nur nach vorhandenen Feldern, sondern anhand dieser Arbeitsabläufe entworfen und mit einem frühen mobilen Prototyp geprüft:

- Einlagern: Standardtruhe ist bereits gewählt; Produkt eingeben oder vorhandenes Produkt aus Vorschlägen wählen; einfache Menge direkt eintragen; bei Bedarf Packungsgröße oder weiteren Mengenbestandteil ergänzen; speichern; danach sofort wieder such- und eingabebereit sein.
- Schnelle Entnahme: Eintrag in Liste oder Suche antippen; kompakte mobile Aktionsfläche beziehungsweise Bottom Sheet öffnen; häufige Aktionen wie eine Packung entnehmen, Restmenge ändern und alles entnommen direkt anbieten; erst nach bestätigter Serverantwort den sichtbaren Bestand aktualisieren und Fehler ohne Eingabeverlust anzeigen.
- Teilentnahme: Eine Entnahme wie 200 g aus 1 × 1000 g muss mit wenigen Eingaben den Packungsbestand in 800 g Restbestand überführen.
- Gemischter Bestand: Bei 1 × 1000 g + 800 g muss eindeutig auswählbar oder durch eine dokumentierte Regel vorhersehbar sein, aus welchem Bestandteil entnommen wird. Keine überraschende automatische Verrechnung.
- Wiederkehrendes Produkt: Vorhandene Produktbezeichnung und übliche Einheit sollen vorgeschlagen werden, ohne veraltete Menge blind zu übernehmen.

Zielwerte für den Usability-Test, jeweils ab sichtbarer Bestandsansicht und ohne Login: Ein bekanntes Produkt mit einfacher Menge in höchstens vier zielgerichteten Interaktionen einlagern; eine ganze Packung in höchstens drei Interaktionen entnehmen; alles entnommen in höchstens drei Interaktionen auslösen. Texteingaben und notwendige Bestätigung bei destruktiven Aktionen werden dabei sinnvoll gezählt und dokumentiert. Diese Zielwerte dürfen nach einem begründeten Prototypentest angepasst werden, nicht stillschweigend.

Der Agent soll zuerst einen funktionalen mobilen Prototyp der Kernabläufe bauen, ihn per Browser MCP bei kleiner Viewportbreite mit den Scan-Beispielen prüfen und erkannte Reibung vor der visuellen Politur korrigieren.

## Theme und Bedienbarkeit

- Standardmäßig wird prefers-color-scheme des Systems respektiert.
- Ein kleiner, gut erreichbarer Umschalter erlaubt Light oder Dark manuell zu wählen und die Wahl lokal zu speichern.
- Der Umschalter darf keine primären Arbeitsabläufe verdecken und ist per Tastatur bedienbar sowie zugänglich beschriftet.
- Primäre Touch-Ziele sind ausreichend groß; sichtbare Labels, Fokuszustände und sinnvolle Fokusführung sind vorhanden.
- Die Gesamtseite benötigt bei üblichen Smartphone- und Desktop-Breiten kein horizontales Scrollen.

## API-Mindestumfang

Eine kleine dokumentierte JSON-API stellt mindestens bereit:

- Sessionstatus beziehungsweise die für das Frontend nötige Authentifizierungsintegration;
- Truhen auflisten, anlegen, umbenennen und Standard setzen;
- aktive Einträge einer Truhe auflisten;
- Eintrag anlegen, lesen und aktualisieren;
- archivierte Einträge auflisten;
- archivieren bei Menge null und automatisch reaktivieren bei Menge größer null;
- Audit-Verlauf lesend abrufen, mindestens für eine einfache Verlaufansicht.

HTTP-Statuscodes und JSON-Fehlerantworten sind konsistent und frontendtauglich. Alle Eingaben werden serverseitig validiert; Clientvalidierung ist zusätzlicher Komfort. API und UI verwenden dieselben fachlichen Regeln.

## Tests

- Pytest deckt Datenmodell, Authentifizierung, Session- und CSRF-Verhalten, API, Validierung, Audit-Transaktionen und SQLite-Persistenz ab.
- Das Vanilla JavaScript wird in kleine, möglichst pure Module getrennt, damit Such-, Mengenformatierungs-, State- und Theme-Logik automatisiert testbar sind.
- Für zentrale Browserabläufe sind automatisierte Frontend- beziehungsweise End-to-End-Tests vorzusehen. Bevorzugt wird eine schlanke, dokumentierte Lösung wie Playwright mit pytest, sofern Installationsaufwand und Zuverlässigkeit angemessen bleiben.
- Falls ein vollständiger Browser-Test in der Zielumgebung nach nachweislicher Prüfung unverhältnismäßig ist, sind mindestens pure JavaScript-Tests für Suche und Mengenformatierung plus dokumentierte Browser-MCP-Smoke-Tests Pflicht. Diese Abweichung ist zu begründen.
- Browser-MCP-Prüfungen ergänzen automatisierte Tests, ersetzen sie aber nicht ohne die genannte dokumentierte Ausnahme.

## Vorgeschlagener Subtask-Zuschnitt

Der Agent soll den Zuschnitt nach Repository-Inspektion festlegen, mindestens aber abdecken:

1. Produktannahmen, Mengenschema und Detailarchitektur festhalten.
2. Python-, uv-, Flask- und Ruff-Projektgrundlage samt Entwicklerkommandos schaffen.
3. STRICT-SQLite-Schema, Migrationen, Truhen, Inventar und Audit-Datenzugriff implementieren.
4. Konfigurationsbasierte Anmeldung, Sessions und CSRF-Schutz implementieren.
5. Fachlogik und JSON-API einschließlich Validierung, Archivierung und Reaktivierung implementieren.
6. Mobile-first Jinja- und Vanilla-JS-Oberfläche mit Suche, Mengenbedienung, Truhen, Archiv, Verlauf und Theme umsetzen.
7. Backend-, JavaScript- und Browser- beziehungsweise End-to-End-Tests ergänzen.
8. Dokumentation, frische Installation und abschließende Usability-Prüfung durchführen.

Subtasks sind klein genug für klare Verifikation, bilden aber nicht jede Datei einzeln ab.

## Akzeptanzkriterien

- Eine frische Arbeitskopie lässt sich ausschließlich anhand der README mit uv einrichten und lokal starten.
- Anwendungstabellen in SQLite sind tatsächlich STRICT; Schema-Upgrades benötigen keine undokumentierten manuellen Änderungen.
- Mehrere benannte Truhen werden unterstützt, genau eine davon ist Standard, und die Standardtruhe öffnet sich im normalen Einstieg automatisch.
- Der Wechsel der Truhe ist mobil mit wenigen Interaktionen möglich und die aktive Truhe jederzeit klar sichtbar.
- Produkt und Menge sind in UI und Backend Pflicht; leere oder ungültige Werte erzeugen verständliche Fehler ohne inkonsistente Daten.
- 3 × 500 g, 800 g Restmenge, 2 Stück sowie 1 × 1000 g + 800 g lassen sich strukturiert erfassen und verständlich anzeigen.
- Einfrierdatum, Haltbar-bis-Datum, Packungsgröße und Mengenhinweis können leer bleiben sowie später gesetzt, geändert oder entfernt werden.
- Menge null archiviert einen Eintrag atomar und entfernt ihn aus aktivem Bestand und aktiver Suche.
- Eine spätere Mengenänderung desselben archivierten Eintrags auf größer null reaktiviert ihn automatisch.
- Die Suche filtert den aktuellen aktiven Bestand ohne Seitenneuladen und Absende-Klick. Nach Anlegen, Ändern, Archivieren, Reaktivieren und Truhenwechsel verwendet sie aktuellen Client-State.
- Nur konfigurierte Benutzer können die Anwendung nutzen. Falsche Anmeldedaten werden ohne Informationsleck abgewiesen; Logout beendet die Session.
- Benutzer werden aus YAML geladen. Passwörter sind nicht im Repository im Klartext abgelegt und die README erklärt YAML-Konfiguration, lokale Dateiplatzierung und Hash-Erzeugung.
- Jede erfolgreiche fachliche Änderung erzeugt in derselben Transaktion einen Audit-Eintrag mit Benutzer, Zeitpunkt, Aktion und nachvollziehbarer Änderung. Fehlgeschlagene Transaktionen hinterlassen weder fachliche Teiländerungen noch irreführende Audit-Einträge.
- Nutzer können einen einfachen, chronologisch verständlichen Änderungsverlauf einsehen.
- API-Endpunkte liefern konsistente JSON-Antworten und getestete HTTP-Statuscodes; nicht authentifizierte und ungültige Requests sind abgedeckt.
- Standardmäßig folgt das Theme dem System. Der manuelle Umschalter funktioniert, ist zugänglich und merkt sich die Wahl.
- Oberfläche ist bei üblichen Smartphone- und Desktop-Breiten ohne horizontales Scrollen der Gesamtseite nutzbar; primäre Aktionen besitzen ausreichend große Touch-Ziele.
- Leere Listen, keine Suchtreffer, laufende Requests, abgelaufene Anmeldung und fehlgeschlagene Requests werden verständlich dargestellt.
- Kernabläufe sind per Tastatur bedienbar; Labels, Fokuszustände und Fokusführung sind erkennbar.
- Automatisierte Tests decken mindestens Mengenvarianten, Validierung, CRUD, optionale Felder, Truhenstandard, Login, CSRF, Audit, Archivierung und Reaktivierung ab.
- Suche und Mengenformatierung im Frontend sind automatisiert getestet; zentrale Browserabläufe sind automatisiert oder entsprechend der begründeten Ausnahme reproduzierbar geprüft.
- Ruff-Formatprüfung, Ruff-Linting und vollständige Testsuite laufen über dokumentierte Kommandos erfolgreich.

## Definition of Done und Stop-Bedingung

Der Umbrella Task ist abgeschlossen, sobald:

- alle erforderlichen Subtasks abgeschlossen und optionale Folgeideen ausdrücklich als nicht blockierend markiert sind;
- sämtliche Akzeptanzkriterien durch automatisierte Tests oder dokumentierte manuelle Prüfungen mit konkretem Ergebnis nachgewiesen sind;
- aus einer frischen Umgebung Installation, Konfiguration eines Testbenutzers, Datenbankinitialisierung, Start, Linting, Formatprüfung und Tests erfolgreich ausgeführt wurden;
- ein manueller Browser-Smoke-Test mindestens Login, Standardtruhe, Truhenwechsel, Eintrag mit 3 × 500 g, Eintrag mit 800 g, Suche, Mengenänderung, Archivierung bei null, Reaktivierung bei größer null, Audit-Anzeige, Logout sowie Light- und Dark-Darstellung bei mobiler und Desktop-Breite umfasst;
- die README Voraussetzungen, uv- und venv-Ablauf, Start, Benutzer- und Passwortkonfiguration, Datenbankpfad, Schema-Upgrade, Backup und Restore der SQLite-Datei, Tests und Ruff-Kommandos beschreibt;
- Architekturentscheidungen, Sicherheitsannahmen und bekannte Einschränkungen dokumentiert sind;
- keine kritischen oder hohen bekannten Defekte im beschriebenen Umfang offen sind;
- der Agent nach erfolgreicher Verifikation keine zusätzlichen Features oder Refactorings außerhalb dieses Scopes beginnt, sondern Verbesserungen separat dokumentiert und die Arbeit beendet.

## Nicht-Ziele des ersten Release

- Rollen, Berechtigungsabstufungen oder Benutzerverwaltung in der UI;
- Cloud-Hosting, Mehrgeräte-Konfliktauflösung, native App oder Offline-Synchronisation;
- Barcode-Scanner, Bilder, Benachrichtigungen oder automatische Haltbarkeitsberechnung;
- komplexe Kategorien, Einkaufslisten, Statistiken oder Warenwirtschaft;
- serverseitige Volltextsuche, Pagination oder Caching für große Datenmengen;
- visuelle Nachbildung der Papier-PDF.

## Festgelegte Reviewentscheidungen

- Mehrere Truhen mit genau einer klaren Standardtruhe.
- Strukturierte Mengenbestandteile für Packungsbestand, losen Rest und Kombinationen wie 1 × 1000 g + 800 g; optionales Freitext-Hinweisfeld.
- Automatische Reaktivierung archivierter Einträge bei neuer Menge größer null.
- System-Theme als Default plus kleiner persistenter Umschalter.
- Einfacher Login aus fester YAML-Konfigurationsdatei, keine Rollen, jeder Benutzer darf alles.
- Audit-Log für wer wann was geändert hat.
- Jinja plus Vanilla JavaScript.
- Angemessene automatisierte Frontendtests und erlaubte Browser-MCP-Unterstützung während der Entwicklung.
<!-- SECTION:DESCRIPTION:END -->
