---
id: TASK-1.5
title: Fachlogik und JSON-API implementieren
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:04'
updated_date: '2026-07-12 00:16'
labels: []
dependencies:
  - TASK-1.4
parent_task_id: TASK-1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Validierte REST-artige API für Truhen, Inventar, strukturierte Mengen, Archivierung, Reaktivierung und Audit-Verlauf umsetzen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Truhen- und Inventar-Endpunkte liefern konsistente JSON-Antworten
- [x] #2 Mengenvarianten und Dimensionsregeln werden serverseitig validiert
- [x] #3 Nullmenge archiviert und positive Menge reaktiviert atomar
- [x] #4 Teilentnahme und gemischter Bestand folgen dokumentierter Regel
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Validierung und Serializer implementieren.\n2. Truhen-, Inventar- und Audit-API bereitstellen.\n3. Archivierung, Reaktivierung und Entnahme testen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Pytest deckt CRUD, Mengen, Dimensionsfehler, atomare Fehler, Archivierung, Reaktivierung und Teilentnahme ab.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Konsistente JSON-API samt Fachvalidierung, Archiv/Reaktivierung und deterministischer Teilentnahme implementiert.
<!-- SECTION:FINAL_SUMMARY:END -->
