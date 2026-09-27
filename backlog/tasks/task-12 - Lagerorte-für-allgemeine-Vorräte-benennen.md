---
id: TASK-12
title: Lagerorte für allgemeine Vorräte benennen
status: Done
assignee:
  - '@codex'
created_date: '2026-09-27 22:16'
updated_date: '2026-09-27 22:18'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die vorhandene Mehrlagerort-Funktion soll neben Tiefkühltruhen auch Vorratsschrank, Keller und ähnliche Orte verständlich darstellen. Sichtbare Begriffe und Datumshinweise werden allgemein formuliert; bestehende Daten und API bleiben kompatibel.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Oberfläche und Verlauf sprechen durchgängig von Lagerorten statt Truhen
- [x] #2 Einlagerungsdatum ist auch für ungekühlte Vorräte verständlich und vorhandene Werte bleiben erhalten
- [x] #3 Bestehende Lagerorte und API funktionieren ohne Datenmigration weiter; Dokumentation beschreibt die Nutzung für verschiedene Vorräte
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Sichtbare Begriffe in Oberfläche, Verlauf, CLI und API-Fehlern vereinheitlichen. 2. Einlagerungsdatum allgemein beschriften und bisheriges Datenfeld/API beibehalten. 3. README anpassen und bestehende Tests sowie gezielte Kompatibilitätsprüfung ausführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Sichtbare Texte und neuer Standardname sind lagerortneutral. Interne Tabelle, API-Routen, Audit-Entitäten und frozen_on-Feld bleiben für bestehende Daten kompatibel. Prüfung: 17 Pytest-Tests, JavaScript-Modultests, node --check und git diff --check erfolgreich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Vorratsliste verwendet Lagerort- und Einlagerungsbegriffe, startet neu mit Lagerort 1 und erhält bestehende Daten sowie API. README aktualisiert; Python- und JavaScript-Tests erfolgreich.
<!-- SECTION:FINAL_SUMMARY:END -->
