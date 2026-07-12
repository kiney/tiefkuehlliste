---
id: DRAFT-1
title: Digitale Tiefkühl-Inventarliste entwickeln
status: Draft
assignee: []
created_date: '2026-07-11 23:40'
labels:
  - umbrella
  - feature
  - draft
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Ziel und Kontext

Eine lokal betreibbare, responsive Webanwendung entwickeln, die die bisherige Papierliste aus inventarliste.tex beziehungsweise inventarliste.pdf ersetzt. Nutzer sollen den Inhalt einer oder mehrerer Tiefkühltruhen am Desktop und besonders am Smartphone mit möglichst wenigen Interaktionen erfassen, durchsuchen, aktualisieren und archivieren können.

Dieser Umbrella Task beschreibt das vollständige Produktziel. Der ausführende AI-Agent soll vor der Implementierung eigenständig sinnvolle, überschaubare Subtasks im Backlog anlegen, Abhängigkeiten festlegen, sie nacheinander umsetzen und verifizieren. Er darf kleinere technische Entscheidungen autonom treffen. Offene, produktrelevante Entscheidungen sind früh sichtbar zu dokumentieren.

## Leitprinzipien

- Usability und geringe Klickzahl haben Vorrang vor visueller Raffinesse.
- Mobile Nutzung beim Einlagern, Entnehmen und Nachsehen ist ein primärer Anwendungsfall; Desktop muss ebenfalls gut funktionieren.
- Die Lösung bleibt bewusst klein, wartbar und lokal betreibbar.
- Pragmatismus hat Vorrang vor REST-Dogmatismus und unnötiger Abstraktion.
- Keine stillschweigende Erweiterung zu einem komplexen Warenwirtschaftssystem.

## Verbindlicher technischer Rahmen

- Backend: Python mit Flask.
- Persistenz: SQLite im STRICT-Modus; Migrationen oder ein nachvollziehbarer Schema-Initialisierungs- und Upgrade-Mechanismus müssen vorhanden sein.
- Python-Projekt: pyproject.toml, uv und projektlokale virtuelle Umgebung. Dokumentation soll auch für Nutzer verständlich sein, die klassische venv-Abläufe gewohnt sind.
- Qualität: Ruff für Linting und Black-artige Formatierung; reproduzierbare Prüfkommandos.
- Frontend: responsive, schlicht, barrierearm, Touch-freundlich sowie Light- und Dark-Mode. Systempräferenz soll mindestens unterstützt werden.
- Frontend und Backend kommunizieren über eine einfache, konsistente REST-artige JSON-API. Zweckmäßige Abweichungen sind erlaubt, müssen aber nachvollziehbar sein.
- Die Datenmenge ist klein. Eine clientseitige Suche über den geladenen aktiven Bestand ist ausdrücklich zulässig, sofern Aktualität, Fehlerfälle und Bedienbarkeit sauber gelöst sind.

## Früh zu treffende Frontend-Entscheidung

Als erster Architektur-Subtask sind mindestens diese Varianten kurz zu bewerten und eine davon begründet festzulegen:

1. Server-renderte Jinja-Templates plus wenig Vanilla JavaScript: kleinster Abhängigkeitsumfang, clientseitige Suche und interaktive Formulare gezielt in JavaScript.
2. Jinja plus HTMX plus wenig Vanilla JavaScript: gute progressive Interaktion, allerdings ist bei einer primär JSON-basierten API zu klären, ob HTMX echten Nutzen bringt oder parallele HTML- und JSON-Pfade erzeugt.
3. Kleines clientseitiges Frontend ohne großes Framework, zum Beispiel ES-Module oder eine sehr kleine reaktive Bibliothek: klare Nutzung der JSON-API, aber mehr eigener Client-State und Build- beziehungsweise Dependency-Entscheidungen.

Bewertungskriterien: minimale Bedienwege, Komplexität, Wartbarkeit durch einen Backend-Entwickler, progressive Verbesserung, API-Konsistenz, Testbarkeit, benötigte Toolchain und langfristige Abhängigkeiten. Kein großes SPA-Framework ohne nachweisbaren Mehrwert. Die Entscheidung ist als ADR oder Backlog-Entscheidung festzuhalten, bevor größere UI-Arbeit beginnt.

## Fachliches Datenmodell

Mindestens eine Entität für einen Inventareintrag mit:

- stabiler ID;
- Produkt oder Bezeichnung: Pflichtfeld, nach Trimmen nicht leer;
- Menge: Pflichtfeld. Das konkrete Format ist im Architektur-Subtask festzulegen. Es muss alltagstaugliche Angaben wie Stückzahlen und Einheiten ermöglichen und zugleich eine eindeutige Entscheidung erlauben, ob die Menge null ist;
- Einfrierdatum: optionales Datum;
- Haltbar bis: optionales Datum;
- Archivstatus beziehungsweise Archivierungszeitpunkt;
- Erstellungs- und Änderungszeitpunkt.

Falls mehrere Truhen bereits im ersten Release unterstützt werden, ist dies minimal zu modellieren. Andernfalls soll die Architektur eine spätere Ergänzung nicht unnötig erschweren, ohne vorsorglich unnötige Tabellen und UI zu bauen.

Wichtige Regel: Wird die Menge eines aktiven Eintrags auf null gesetzt, wandert der Eintrag automatisch in den Archivbereich und erscheint nicht mehr im aktiven Bestand. Der Agent muss festlegen und testen, ob archivierte Einträge wiederhergestellt werden können; empfohlen ist eine einfache Wiederherstellung, sofern sie ohne nennenswerte Zusatzkomplexität möglich ist.

## Erforderliche Nutzerabläufe

- Aktiven Bestand ohne Umwege sehen; wichtige Informationen sind auf kleinen Bildschirmen schnell erfassbar.
- Neuen Eintrag mit Produkt und Menge schnell anlegen; optionale Datumsfelder dürfen den schnellen Ablauf nicht behindern.
- Bestehenden Eintrag bearbeiten.
- Menge besonders schnell ändern beziehungsweise auf null setzen.
- Aktive Einträge unmittelbar nach Produkt und sinnvollerweise auch nach Mengenangabe durchsuchen oder filtern; die Suche reagiert ohne zusätzlichen Absende-Klick.
- Archivierte Einträge getrennt vom aktiven Bestand ansehen.
- Klare Lade-, Leer-, Validierungs- und Fehlerzustände sehen.
- Bedienung per Touch und Tastatur; Formulare besitzen sichtbare Labels und sinnvolle Fokusführung.
- Light- und Dark-Mode ohne unleserliche Kontraste verwenden.

## API-Mindestumfang

Eine kleine, dokumentierte API bereitstellen für:

- aktive Einträge auflisten;
- Eintrag anlegen;
- Eintrag lesen oder die für die Bearbeitung nötigen Daten beziehen;
- Eintrag aktualisieren, einschließlich Mengenänderung und automatischer Archivierung bei null;
- archivierte Einträge auflisten;
- optional Wiederherstellung, falls im Architekturentscheid aufgenommen.

HTTP-Statuscodes und JSON-Fehlerantworten müssen konsistent und für das Frontend verwertbar sein. Eingaben werden serverseitig validiert; Clientvalidierung ist nur eine zusätzliche Komfortfunktion. API und UI dürfen keine unterschiedlichen fachlichen Regeln implementieren.

## Vorgeschlagener Subtask-Zuschnitt

Der ausführende Agent soll den genauen Zuschnitt nach Repository-Inspektion festlegen, mindestens aber diese Arbeitsbereiche abdecken:

1. Bestand, Produktannahmen und Frontend-Architektur analysieren und Entscheidung dokumentieren.
2. Python-, uv-, Flask- und Ruff-Projektgrundlage samt Entwicklerkommandos schaffen.
3. STRICT-SQLite-Schema, Initialisierung oder Migration und Datenzugriff implementieren.
4. Fachlogik und REST-artige API einschließlich Validierung und Archivierung implementieren.
5. Mobile-first Oberfläche, Suche, Formulare, Archiv und Theme umsetzen.
6. Automatisierte Backend-, API- und relevante Frontend- beziehungsweise End-to-End-Tests ergänzen.
7. Dokumentation, frische Installation und abschließende manuelle Usability-Prüfung durchführen.

Subtasks sollen klein genug für klare Verifikation sein, aber nicht jede einzelne Datei als eigenen Task abbilden.

## Akzeptanzkriterien

- Eine frische Arbeitskopie lässt sich ausschließlich anhand der README mit uv einrichten und lokal starten.
- Die Anwendung persistiert Daten in einer SQLite-Datenbank, deren Anwendungstabellen tatsächlich STRICT sind.
- Produkt und Menge werden in UI und Backend als Pflichtfelder behandelt; leere oder ungültige Werte erzeugen verständliche Fehler und keine inkonsistenten Datensätze.
- Einfrierdatum und Haltbar-bis-Datum können leer bleiben und später gesetzt, geändert oder entfernt werden.
- Ein gültiger Eintrag kann über die mobile Oberfläche mit einem kurzen, nachvollziehbaren Ablauf angelegt werden.
- Aktive Einträge lassen sich anzeigen und bearbeiten; eine Mengenänderung auf null archiviert atomar und entfernt den Eintrag aus der aktiven Ansicht.
- Archivierte Einträge erscheinen in einem getrennten Archivbereich und nicht in normalen Suchergebnissen des aktiven Bestands.
- Die Suche filtert den überschaubaren aktiven Bestand ohne Seitenneuladen und reagiert während der Eingabe. Nach Anlegen, Ändern und Archivieren verwendet sie den aktuellen Client-Datenbestand.
- API-Endpunkte liefern konsistente JSON-Antworten, passende HTTP-Statuscodes und getestete Fehlerfälle.
- Serverseitige Validierung verhindert insbesondere leere Pflichtfelder, nicht interpretierbare Mengen und ungültige Datumswerte.
- Die Oberfläche ist bei üblichen Smartphone- und Desktop-Breiten ohne horizontales Scrollen der Gesamtseite nutzbar; primäre Aktionen haben ausreichend große Touch-Ziele.
- Light- und Dark-Mode sind nutzbar; mindestens prefers-color-scheme wird respektiert. Falls ein manueller Umschalter implementiert wird, bleibt die Wahl erhalten.
- Leere Listen, keine Suchtreffer, laufende Requests und fehlgeschlagene Requests werden verständlich dargestellt.
- Der Kernablauf ist per Tastatur bedienbar, Eingabefelder haben Labels und Fokuszustände sind erkennbar.
- Automatisierte Tests decken mindestens Datenvalidierung, CRUD der API, optionale Datumsfelder, SQLite-Persistenz und den Übergang aktiv zu archiviert bei Menge null ab.
- Ruff-Formatprüfung, Ruff-Linting und die vollständige Testsuite laufen erfolgreich über dokumentierte Kommandos.
- Es sind keine nicht dokumentierten manuellen Datenbankänderungen nötig.

## Definition of Done und Stop-Bedingung

Der Umbrella Task ist abgeschlossen, sobald alle folgenden Punkte erfüllt sind:

- Alle für diesen Umbrella Task angelegten, erforderlichen Subtasks sind abgeschlossen; optionale Folgeideen sind ausdrücklich als nicht blockierende spätere Tasks markiert.
- Sämtliche Akzeptanzkriterien sind entweder durch automatisierte Tests oder durch eine dokumentierte manuelle Prüfung mit konkretem Ergebnis nachgewiesen.
- Aus einer frischen Umgebung wurden Installation, Datenbankinitialisierung, Start, Linting, Formatprüfung und Tests erfolgreich ausgeführt.
- Ein manueller Smoke-Test umfasst: ersten Eintrag anlegen, optionales Datum leer lassen, suchen, Menge bearbeiten, auf null setzen, im Archiv wiederfinden sowie Light- und Dark-Darstellung bei mobiler und Desktop-Breite prüfen.
- README beschreibt Voraussetzungen, uv-Setup mit virtueller Umgebung, Start, Konfiguration, Datenbankpfad, Tests, Ruff-Kommandos und gegebenenfalls Backup oder Wiederherstellung der SQLite-Datei.
- Relevante Architekturentscheidungen und bekannte Einschränkungen sind dokumentiert.
- Keine kritischen oder hohen bekannten Defekte im beschriebenen Umfang sind offen.
- Der Agent führt nach erfolgreicher Verifikation keine zusätzlichen Features, Refactorings oder Designpolitur außerhalb dieses Scopes mehr aus, sondern dokumentiert mögliche Verbesserungen separat und beendet die Arbeit.

## Nicht-Ziele des ersten Release

Sofern nicht durch einen späteren Review ergänzt:

- Benutzerkonten, Rollen und Mehrbenutzer-Synchronisation;
- Cloud-Hosting, native Mobile-App oder Offline-Synchronisation;
- Barcode-Scanner, Bilder, Benachrichtigungen oder automatische Haltbarkeitslogik;
- komplexe Kategorien, Einkaufslisten, Statistiken oder Warenwirtschaft;
- serverseitige Volltextsuche, Pagination oder Caching für große Datenmengen;
- visuelle Nachbildung der Papier-PDF.

## Offene Reviewpunkte vor Promotion zum Task

- Soll Release 1 genau eine Tiefkühltruhe verwalten oder mehrere benannte Truhen?
- Wie soll Menge modelliert und eingegeben werden: strukturierter Zahlenwert plus Einheit, oder alltagstauglicher Text mit separater numerischer Restmenge?
- Soll das Archiv eine Wiederherstellen-Funktion erhalten?
- Soll es zusätzlich zur Systempräferenz einen manuellen Theme-Umschalter geben?
- Ist lokaler Einzelbenutzerbetrieb ohne Authentifizierung die verbindliche Zielumgebung?
<!-- SECTION:DESCRIPTION:END -->
