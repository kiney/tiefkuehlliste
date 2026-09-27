---
id: TASK-14
title: Gunicorn-Control-Socket im Container deaktivieren
status: Done
assignee:
  - '@codex'
created_date: '2026-09-27 23:05'
updated_date: '2026-09-27 23:06'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Gunicorn 26 versucht den standardmäßigen Control-Socket unter /home/tiefkuehlliste anzulegen. Dieser Pfad ist für den nicht privilegierten Container-Benutzer nicht beschreibbar und erzeugt beim Start Permission denied. Die App benötigt den Control-Socket nicht.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Gunicorn versucht beim Container-Start keinen Control-Socket unter /home/tiefkuehlliste anzulegen
- [x] #2 App-Start über Gunicorn, HOST/PORT und Zugriffslogs bleiben erhalten
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Dokumentierten Gunicorn-Schalter --no-control-socket im Container-CMD ergänzen. 2. CMD-Argumente und bestehende Tests prüfen. 3. Ursache und erneuten Image-Build dokumentieren.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Gunicorn 26 legt den Control-Socket standardmäßig unter HOME/.gunicorn an. Der Container-Benutzer hat kein beschreibbares Home; --no-control-socket deaktiviert die ungenutzte Funktion. CMD-Argumente inklusive HOST/PORT geprüft, 17 Pytest-Tests und git diff --check erfolgreich. Echter Image-Start in Sandbox nicht möglich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Gunicorn-Control-Socket im Container deaktiviert, damit der Start keine Permission-denied-Meldung für /home/tiefkuehlliste mehr auslöst. App-Factory, HOST/PORT und Zugriffslogs bleiben erhalten; Tests erfolgreich.
<!-- SECTION:FINAL_SUMMARY:END -->
