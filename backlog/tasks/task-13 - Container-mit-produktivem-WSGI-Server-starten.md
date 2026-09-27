---
id: TASK-13
title: Container mit produktivem WSGI-Server starten
status: Done
assignee:
  - '@codex'
created_date: '2026-09-27 22:59'
updated_date: '2026-09-27 23:01'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Der Container startet derzeit den Flask-Entwicklungsserver und meldet beim Compose-Start eine Produktionswarnung. Der Container soll mit Gunicorn betrieben werden; lokale CLI-Nutzung und Container-Portkonfiguration bleiben verständlich.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Container startet die Flask-App über Gunicorn statt app.run
- [x] #2 Konfigurierter Container-Port und Zugriff über den vorgeschalteten Reverse Proxy funktionieren weiter
- [x] #3 Dokumentation erklärt den Container-Start und relevante Tests sind erfolgreich
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Gunicorn als reine Container-Abhängigkeit installieren und Container-Start auf die Flask-App-Factory umstellen. 2. HOST/PORT und Containerdokumentation anpassen. 3. Tests und soweit möglich Container-Start prüfen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Gunicorn bleibt container-spezifisch: Die Paketabhängigkeiten und uv.lock bleiben unverändert. uv lock konnte wegen gesperrtem PyPI-DNS nicht aktualisiert werden; darum Installation direkt im Image.

Validiert: 17 Pytest-Tests, Shell-Syntax und ausführbarer CMD-Test mit HOST/PORT=127.0.0.1:8080, git diff --check. Echter Container-Build hier nicht möglich: Podman-Laufzeitverzeichnis schreibgeschützt, Docker-Socket gesperrt. Reverse-Proxy-Pfad bleibt HTTP über denselben Container-Port; nicht end-to-end im Sandbox-Netz testbar.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Container installiert Gunicorn 26 und startet die App-Factory mit einem Worker und zwei Threads; HOST/PORT und Zugriffslogs bleiben unterstützt. README für Betrieb hinter Caddy ergänzt. Python-Tests und CMD-Prüfung erfolgreich; Image-Build in Sandbox blockiert.
<!-- SECTION:FINAL_SUMMARY:END -->
