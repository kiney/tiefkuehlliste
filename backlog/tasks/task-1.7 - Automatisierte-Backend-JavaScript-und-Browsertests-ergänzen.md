---
id: TASK-1.7
title: 'Automatisierte Backend-, JavaScript- und Browsertests ergänzen'
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:04'
updated_date: '2026-07-12 00:16'
labels: []
dependencies:
  - TASK-1.6
parent_task_id: TASK-1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Pytest-, JavaScript- und Browser-/E2E-Tests für die vollständigen Produktanforderungen aufbauen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Backendtests decken Auth, CSRF, CRUD, Mengen, Audit und Persistenz ab
- [x] #2 JavaScript-Tests decken Suche, Mengenformatierung, State und Theme ab
- [x] #3 Zentrale Browserabläufe sind automatisiert oder die dokumentierte Ausnahme ist reproduzierbar belegt
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Backendtests für Fachlichkeit und Sicherheit ergänzen.\n2. Pure JavaScript-Module testen.\n3. Echte Browser-Smoke-Tests durchführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
5 Pytest-Fälle und Node-Modultest laufen grün; reale Chrome-Prüfung deckte Login, Mengen, Suche, Änderung, Archiv/Reaktivierung, Audit, Theme, Truhenwechsel und Logout ab.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Automatisierte Backend- und JS-Tests plus reproduzierbare Browser-MCP-Abnahme abgeschlossen.
<!-- SECTION:FINAL_SUMMARY:END -->
