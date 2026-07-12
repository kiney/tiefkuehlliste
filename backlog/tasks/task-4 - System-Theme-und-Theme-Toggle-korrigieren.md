---
id: TASK-4
title: System-Theme und Theme-Toggle korrigieren
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:39'
updated_date: '2026-07-12 00:41'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die Oberfläche nutzt bei prefers-color-scheme: dark weiterhin helle eigene Farbvariablen. Der Toggle enthält zudem einen optisch unsichtbaren dritten System-Zustand. Systempräferenz soll beim ersten Besuch korrekt wirken und der manuelle Toggle direkt binär schalten.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Ohne gespeicherte Auswahl folgt die gesamte Oberfläche der OS-Präferenz light oder dark
- [x] #2 Ein Klick auf den Toggle ändert das sichtbare Theme bei jedem Klick
- [x] #3 Manuelle Auswahl light/dark bleibt lokal gespeichert
- [x] #4 Toggle-Beschriftung und Symbol nennen den nächsten beziehungsweise aktuellen Zustand verständlich
- [x] #5 Automatisierte Tests und Browserprüfung decken System-Dark und den Toggle ab
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. CSS-Variablen für System-Dark über prefers-color-scheme ergänzen.\n2. Theme-Modul von Drei-Zustands- auf effektiven binären Toggle umstellen.\n3. Zugängliche Beschriftung und Symbolzustand synchronisieren.\n4. Modul- und Browserprüfungen für System-Light/-Dark und manuelle Overrides durchführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
CSS setzt eigene Dark-Variablen nun für prefers-color-scheme. Unsichtbarer Drei-Zustands-Zyklus wurde durch binären Toggle des effektiven Themes ersetzt; neue Auswahl nutzt color-theme und migriert den alten Schlüssel weg. Browser: System-Dark #111713 ohne Attribut, Klick 1 Light #f4f7f2, Klick 2 Dark; System-Light ebenfalls verifiziert. Ruff, 12 Pytest- und Node-Tests grün.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Automatische OS-Theme-Erkennung und manuellen Toggle korrigiert. Der erste Start folgt Light/Dark des Systems, jeder Klick erzeugt eine sichtbare Änderung, manuelle Light-/Dark-Wahl bleibt gespeichert und der Button beschreibt Zustand und Ziel.
<!-- SECTION:FINAL_SUMMARY:END -->
