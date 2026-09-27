---
id: TASK-11
title: Kurze Bestätigung nach Bestandsänderungen anzeigen
status: Done
assignee:
  - '@codex'
created_date: '2026-09-27 21:58'
updated_date: '2026-09-27 22:01'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Nach dem Eintragen oder Entnehmen eines Produkts zeigt die Oberfläche kurz an, welches Produkt und welche Menge geändert wurde.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Neue Einträge und Zusammenführungen zeigen Produkt und hinzugefügte Menge an.
- [x] #2 Teil- und Komplettentnahmen zeigen Produkt und entnommene Menge beziehungsweise vollständige Entnahme an.
- [x] #3 Die Meldung erscheint nur nach erfolgreicher Speicherung, verschwindet automatisch und ist für Screenreader zugänglich.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Eine kurze zugängliche Meldung in der Bestandsansicht ergänzen. 2. Nach erfolgreichen Einträgen, Zusammenführungen und Entnahmen passende Produkt- und Mengenangaben anzeigen. 3. Relevante Tests und Prüfungen ausführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Meldung wird nach erfolgreichen API-Buchungen angezeigt, enthält Produkt und normalisierte Menge, verschwindet nach 3,5 Sekunden und nutzt eine dauerhafte Live-Region. Verifiziert: npm test, .venv/bin/python -m pytest -q (16 Tests), node --check und git diff --check. Browser-Smoke-Test durch Sandbox-Socket-Sperre nicht möglich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Kurze Bestandsmeldungen für neue und zusammengeführte Einträge, Bearbeitungen sowie Teil- und Komplettentnahmen ergänzt. JavaScript- und Backend-Tests erfolgreich.
<!-- SECTION:FINAL_SUMMARY:END -->
