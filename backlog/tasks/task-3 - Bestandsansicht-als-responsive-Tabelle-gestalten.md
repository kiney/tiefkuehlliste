---
id: TASK-3
title: Bestandsansicht als responsive Tabelle gestalten
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:32'
updated_date: '2026-07-12 00:35'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die Kartenansicht zerquetscht Produkt, Menge und Aktionen bei schmalen Breiten. Aktiver Bestand und Archiv werden als ruhige, kompakte Tabellen-/Listenansicht mit stabilen Informationsspalten und responsiven Aktionszeilen dargestellt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Desktop zeigt Produkt, Menge, Hinweis und Aktionen in klar getrennten Tabellenspalten
- [x] #2 Mobil bleiben Produkt und Menge lesbar; Aktionen umbrechen als eigene Zeile statt Wörter zu zerlegen
- [x] #3 Bestand und Archiv verwenden dieselbe Darstellung
- [x] #4 Gesamtseite hat bei 390 px und Desktopbreite keinen horizontalen Überlauf
- [x] #5 Bestehende Bearbeitungs-, Entnahme-, Archiv- und Reaktivierungsaktionen bleiben funktionsfähig
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Semantische Tabellenstruktur für Bestand und Archiv einführen.\n2. Rendering auf Tabellenzeilen und stabile Aktionsgruppen umstellen.\n3. Responsive CSS für Desktopspalten und mobile Zeilen ergänzen.\n4. Automatisierte Checks und Browserprüfung bei Mobil-/Desktopbreite durchführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Bestand und Archiv verwenden semantische Tabellen. Desktop: vier stabile Spalten; mobil: Produkt/Menge im Kopf, Hinweis und Aktionszeile darunter. Browserprüfung bei 390x844 und 1440x900 ergab 0 px horizontalen Überlauf, 44 px Aktionsziele und funktionierende Bearbeitung. Ruff, 12 Pytest- und Node-Tests erfolgreich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Zerquetschte Karten durch eine responsive Tabellen-/Listenansicht ersetzt. Produkt, Menge, Hinweis und Aktionen bleiben auf Desktop und Smartphone klar lesbar; alle bestehenden Aktionen bleiben erhalten.
<!-- SECTION:FINAL_SUMMARY:END -->
