---
id: TASK-1.8
title: 'Dokumentation, Frischinstallation und Usability-Abnahme'
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:04'
updated_date: '2026-07-12 00:16'
labels: []
dependencies:
  - TASK-1.7
parent_task_id: TASK-1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
README, Betriebsdokumentation, frische Installation und vollständige mobile/desktop Browser-Abnahme durchführen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 README dokumentiert uv, venv, Start, Benutzer, Datenbank, Migration, Backup, Restore und Prüfkommandos
- [x] #2 Frische Installation und vollständige Prüfsuite sind erfolgreich nachgewiesen
- [x] #3 Browser-Smoke-Test deckt alle in TASK-1 geforderten Abläufe mobil und desktop ab
- [x] #4 Keine kritischen oder hohen bekannten Defekte bleiben offen
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. README für Installation und Betrieb schreiben.\n2. uv, Datenbankinitialisierung und Prüfsuite ausführen.\n3. Mobile/Desktop-Abnahme dokumentieren und Defekte beseitigen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
README deckt uv/venv, Konfiguration, Migration, Start, Backup/Restore und Checks ab. uv sync, frische /tmp-Datenbank, Ruff, Pytest und npm test erfolgreich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Betriebsdokumentation, Frischinitialisierung und vollständige Usability-Abnahme abgeschlossen; keine kritischen/hohen Defekte bekannt.
<!-- SECTION:FINAL_SUMMARY:END -->
