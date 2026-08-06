---
id: TASK-10
title: Container-Mounts und privaten Registry-Workflow dokumentieren
status: Done
assignee:
  - '@codex'
created_date: '2026-08-06 19:38'
updated_date: '2026-08-06 19:42'
labels: []
dependencies: []
modified_files:
  - README.md
  - .gitignore
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die Podman-Dokumentation soll eindeutig erklären, wie Konfiguration und SQLite-Daten auf den Host beziehungsweise in ein Volume gemappt werden. Zusätzlich soll ein nur lokal verwendetes, ignoriertes Makefile Builds und Pushes zu einer privaten Registry vereinfachen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Die Dokumentation beschreibt Host-Pfade, Container-Pfade, Schreibrechte und Persistenz für Config und SQLite-Datenbank
- [x] #2 Das lokale Makefile wird von Git ignoriert
- [x] #3 Build-Ziel und Push-Befehlsfolge werden ohne Registry-Push geprüft
- [x] #4 Ein lokales Makefile baut das Image mit einem fest hinterlegten privaten Registry-Namen und bietet ein Push-Ziel
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Podman-Mount-Beispiele für Bind-Mount und benanntes Volume präzisieren.
2. Lokales Makefile mit Build- und Push-Ziel erstellen und ignorieren.
3. Build tatsächlich, Push nur als Dry-Run prüfen.
4. Dokumentations- und Projektprüfungen abschließen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Podman-Dokumentation um Config-Bind-Mount, SQLite-Verzeichnis-Mount, SELinux-Label, UID-Anpassung und benanntes Volume ergänzt.
Lokales Makefile erstellt; git check-ignore bestätigt die Ignore-Regel. make build erzeugte das privat getaggte Image erfolgreich. make -n push bestätigte Build- und Push-Befehle, ohne Netzwerk-Push. Ein temporärer Bind-Mount-Test bestätigte /data-Eigentümer und die angelegte inventory.sqlite; Testartefakte wurden entfernt.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Persistenz- und Config-Mounts sind vollständig dokumentiert. Ein von Git ignoriertes lokales Makefile bietet Build und Push für die private Registry; Build und Mount wurden real, Push ausschließlich per Dry-Run geprüft.
<!-- SECTION:FINAL_SUMMARY:END -->
