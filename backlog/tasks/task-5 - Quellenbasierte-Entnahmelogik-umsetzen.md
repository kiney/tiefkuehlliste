---
id: TASK-5
title: Quellenbasierte Entnahmelogik umsetzen
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:47'
updated_date: '2026-07-12 00:52'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Teilentnahmen müssen bei losen Mengen und Packungen möglich sein. Vorhandene Restmengen werden standardmäßig zuerst gewählt; die Quelle bleibt sichtbar auswählbar. Das Öffnen einer Packung erzeugt einen separaten Rest statt vorhandene Reste überraschend zusammenzufassen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Jeder aktive Eintrag bietet eine Teilentnahme unabhängig vom Mengenbestandteiltyp
- [x] #2 Bei vorhandenen Restmengen ist ein Rest die vorausgewählte Entnahmequelle
- [x] #3 1 × 1000 g + 800 g wird bei 200 g Entnahme aus dem Rest zu 1 × 1000 g + 600 g
- [x] #4 2 × 500 g + 250 g wird bei zwei Entnahmen zu je 250 g deterministisch zu 1 × 500 g + 250 g
- [x] #5 Nutzer können bei mehreren Komponenten die Quelle ausdrücklich auswählen
- [x] #6 Eine ganze Packung bleibt als schneller Ablauf entnehmbar
- [x] #7 Automatisierte Tests und Browserprüfung decken Rest-, Packungs- und Mischbestand ab
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Entnahmeregel fachlich auf explizite Komponentenquelle und getrennte Reste umstellen.\n2. Eigenen zugänglichen Entnahmedialog statt Browser-Prompt implementieren.\n3. Teilentnahme für alle Einträge und separate Schnellaktion für ganze Packungen anbieten.\n4. Datenbereinigung für historische None-Hinweise ergänzen.\n5. API-, Sequenz- und Browserfälle mit den Nutzerbeispielen prüfen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
API reduziert exakt die gewählte Komponente und hält beim Öffnen einer Packung neue Reste separat. Eigener Dialog sortiert vorhandene Reste vor Packungen und zeigt alle Quellen. Reine Mengen erhalten ebenfalls Entnehmen; 1 Packung bleibt Schnellaktion. Migration 2 bereinigt historische note='None'. Tests: 14 Pytest und Node grün. Isolierter Browserfall: 1×1000 g + 800 g, Rest vorausgewählt, 200 g Entnahme ergab 1×1000 g + 600 g; mobil 0 px Überlauf.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Entnahme auf explizite, rest-first Quellenwahl umgestellt. Teilentnahme funktioniert für lose Mengen und Packungen, öffnet Packungen nachvollziehbar in separate Reste und vermeidet überraschende Summen. Browser-Prompt wurde durch einen zugänglichen Dialog ersetzt.
<!-- SECTION:FINAL_SUMMARY:END -->
