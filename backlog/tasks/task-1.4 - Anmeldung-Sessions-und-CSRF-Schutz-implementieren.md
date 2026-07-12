---
id: TASK-1.4
title: 'Anmeldung, Sessions und CSRF-Schutz implementieren'
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:04'
updated_date: '2026-07-12 00:16'
labels: []
dependencies:
  - TASK-1.3
parent_task_id: TASK-1
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
YAML-basierte Benutzerkonfiguration, Passwortprüfung, geschützte Sessions, Logout und CSRF-Schutz implementieren.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Nur konfigurierte Benutzer können sich anmelden
- [x] #2 Passwort-Hashes werden sicher geprüft und Beispielkonfiguration enthält keine Secrets
- [x] #3 Session, Logout und CSRF-Verhalten sind getestet
- [x] #4 Cookie- und Fehlerverhalten sind für lokalen Betrieb dokumentiert
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. YAML-Benutzer laden.\n2. Login, Logout und Session implementieren.\n3. CSRF und Cookie-Defaults testen und dokumentieren.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Login, falsche Credentials, API-401, Logout und CSRF wurden automatisiert sowie Login/Logout im Browser geprüft.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
YAML-basierte Anmeldung mit sicheren Hashes, geschützter Session, CSRF und dokumentierten Cookie-Annahmen fertiggestellt.
<!-- SECTION:FINAL_SUMMARY:END -->
