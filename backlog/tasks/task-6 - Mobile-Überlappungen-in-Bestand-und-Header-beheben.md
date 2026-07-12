---
id: TASK-6
title: Mobile Überlappungen in Bestand und Header beheben
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 23:11'
updated_date: '2026-07-12 23:14'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Auf schmalen Android-Viewports überlagern lange Mengen den Produktnamen. Der hohe sticky Header verdeckt beim Scrollen Überschriften und Formularbereiche. Die mobile Kartenstruktur und Headerposition werden robust für etwa 320 bis 430 CSS-Pixel gemacht.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Produktname und lange kombinierte Menge stehen mobil in getrennten Zeilen ohne Überlagerung
- [x] #2 Mobile Mengen dürfen sinnvoll umbrechen und bleiben vollständig lesbar
- [x] #3 Der Header verdeckt beim Scrollen keine Inhalte
- [x] #4 Aktionsknöpfe bleiben bei drei Aktionen lesbar und mindestens 44 px hoch
- [x] #5 Bei 320, 360, 390 und 430 px entsteht kein horizontaler Überlauf
- [x] #6 Desktop-Tabellenansicht bleibt unverändert nutzbar
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Mobile Bestandszeile auf vertikale Produkt-, Mengen- und Hinweisbereiche umstellen.\n2. Sticky Header mobil deaktivieren und Aktionsraster für sehr schmale Viewports stabilisieren.\n3. Mehrere mobile Breiten sowie Scrollzustand im Browser prüfen.\n4. Automatisierte Suite ausführen und Regressionen ausschließen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Mobile Bestandszeile nutzt jetzt eine Spalte: Produkt, umbrechende Menge mit Label, Hinweis, Aktionen. Header ist unter 650 px nicht sticky. Aktionsraster passt sich mit 1-3 Spalten an. Browsermessungen bei 320/360/390/430 px: jeweils 0 px Seitenüberlauf, keine geometrische Überlagerung, Mindesthöhe der Buttons 44 px; Desktop 1440 px blieb table-row/sticky ohne Überlauf. Ruff, 14 Pytest- und Node-Tests grün.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Mobile Textüberlagerungen beseitigt: lange Mengen stehen unter dem Produkt, Aktionen brechen kontrolliert um und der Header scrollt mobil aus dem Weg. Schmale Android- sowie Desktopbreiten wurden verifiziert.
<!-- SECTION:FINAL_SUMMARY:END -->
