---
id: TASK-9
title: Container-Image für Tiefkühlliste
status: Done
assignee:
  - '@codex'
created_date: '2026-08-06 19:28'
updated_date: '2026-08-06 19:34'
labels: []
dependencies: []
modified_files:
  - Dockerfile
  - .dockerignore
  - README.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die Flask-Anwendung soll als OCI-/Docker-Image gebaut und mit Podman betrieben werden können. Der Container stellt die Anwendung standardmäßig auf Port 2480 bereit.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Ein Dockerfile baut die Anwendung reproduzierbar als Container-Image
- [x] #2 Die Anwendung lauscht im Container standardmäßig auf 0.0.0.0:2480 und das Image dokumentiert Port 2480
- [x] #3 Persistente SQLite-Daten können außerhalb der flüchtigen Container-Schicht abgelegt werden
- [x] #4 Build und HTTP-Erreichbarkeit werden mit Podman erfolgreich geprüft
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Container-Laufzeitverhalten und Persistenzpfade festlegen.
2. Dockerfile und notwendige Build-Kontextregeln erstellen.
3. Image mit Podman bauen und HTTP-Start auf Port 2480 testen.
4. Nutzung knapp dokumentieren und Projektprüfungen ausführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Mehrstufiges Python-Image mit nicht privilegiertem Benutzer (UID 10001), EXPOSE 2480 und /data-Volume umgesetzt. Der im Wheel-Installationslayout benötigte Flask-Instance-Pfad wird vorab mit passenden Rechten angelegt.
Validierung: podman build erfolgreich; Container lauschte auf 0.0.0.0:2480; GET /login ergab HTTP 200; Inspect bestätigte Benutzer tiefkuehlliste, 2480/tcp und /data-Volume. uv run ruff format --check ., uv run ruff check ., uv run pytest (16 bestanden) und npm test erfolgreich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Dockerfile, Build-Kontextregeln und Podman-Dokumentation ergänzt. Das getestete Image läuft ohne Root-Rechte, veröffentlicht standardmäßig Port 2480 und persistiert SQLite unter /data; Build, HTTP-Smoke-Test und sämtliche Projektprüfungen waren erfolgreich.
<!-- SECTION:FINAL_SUMMARY:END -->
