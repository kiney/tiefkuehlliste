---
id: TASK-7
title: 'Packungsauswahl, Produktzusammenführung und eigene Bestätigungsdialoge'
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 23:22'
updated_date: '2026-07-12 23:28'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Mehrere Packungsgrößen benötigen bei der Schnellaktion eine Quellenauswahl. Beim Anlegen eines gleichnamigen Produkts soll Zusammenführen angeboten werden, ohne getrennte Chargen zu verhindern. Native Browserdialoge werden durch konsistente App-Dialoge ersetzt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 1 Packung öffnet bei mehreren Packungskomponenten eine eindeutige Auswahl und entnimmt die gewählte Größe
- [x] #2 Bei genau einer Packungskomponente bleibt die Schnellaktion direkt
- [x] #3 Gleichnamige aktive Produkte werden vor dem Neuanlegen als Zusammenführungsziele angeboten
- [x] #4 Zusammenführen addiert strukturierte Mengen zum gewählten Eintrag und behält dessen Metadaten
- [x] #5 Separat anlegen bleibt ausdrücklich möglich, insbesondere für abweichende Haltbarkeit
- [x] #6 Alles entnehmen verwendet einen gestylten App-Dialog ohne native confirm-Ausgabe
- [x] #7 Aktionsbezeichnungen sind sprachlich konsistent
- [x] #8 Automatisierte Tests und Browserprüfungen decken alle drei Abläufe mobil und am Desktop ab
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Packungs-Schnellaktion um Auswahlmodus für mehrere Größen erweitern.\n2. Gleichnamige Produkte erkennen und Zusammenführungsdialog mit Zielwahl bauen.\n3. Eigenen Bestätigungsdialog für Alles entnehmen einführen und Texte vereinheitlichen.\n4. Pure JS-Logik, API-Verhalten und Browserabläufe testen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
1-Packung-Aktion öffnet bei mehreren Packungskomponenten den bestehenden App-Entnahmedialog im Ganzpackungsmodus; 1000-g/500-g-Auswahl im Browser geprüft, gewählte 500-g-Komponente sank korrekt. Gleichnamige Produkte werden trim-/case-insensitiv und dimensionskompatibel erkannt; Browserprüfung bot Erbsen-Ziel mit Haltbarkeit an, Zusammenführung behielt 2027-01-01, separat anlegen ergab zweiten Eintrag. Gleiche Packungsgrößen werden serverseitig addiert. Alles entnehmen nutzt eigenen Dialog; kein confirm()/prompt() verbleibt. Mobil 360 px ohne Überlauf. Ruff, 15 Pytest- und Node-Tests grün.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Packungsquellenauswahl, optionales Zusammenführen gleichnamiger Produkte und konsistente App-Dialoge umgesetzt. Getrennte Chargen bleiben möglich, bestehende Metadaten werden beim Merge bewahrt und identische Packungsgrößen verständlich summiert.
<!-- SECTION:FINAL_SUMMARY:END -->
