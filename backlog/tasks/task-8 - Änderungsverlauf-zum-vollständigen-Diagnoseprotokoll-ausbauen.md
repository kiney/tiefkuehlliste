---
id: TASK-8
title: Änderungsverlauf zum vollständigen Diagnoseprotokoll ausbauen
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 23:34'
updated_date: '2026-07-12 23:40'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Der Änderungsverlauf dient primär der Fehleranalyse. Ereignisse sollen vollständig abrufbar sein und neben einer übersichtlichen Zusammenfassung alle Vorher-/Nachher-Daten sowie feldweise Änderungen zeigen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Audit-API liefert alle Einträge ohne stilles 200-Einträge-Limit
- [x] #2 API stellt Vorher- und Nachher-Snapshots als strukturierte JSON-Werte bereit
- [x] #3 Jedes Ereignis zeigt Zeitpunkt, Benutzer, Aktion, Entität und ID
- [x] #4 Geänderte Felder werden mit lesbarem Vorher-/Nachher-Vergleich dargestellt
- [x] #5 Vollständige Snapshots inklusive Mengenbestandteilen bleiben als formatierte Rohdaten einsehbar
- [x] #6 Erstellung, Änderung, Entnahme, Archivierung, Reaktivierung und Truhenänderung sind verständlich benannt
- [x] #7 Darstellung bleibt mobil ohne horizontalen Seitenüberlauf nutzbar
- [x] #8 Automatisierte Tests und Browserprüfung decken API, Differenzlogik und Darstellung ab
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Audit-API ohne Begrenzung und mit geparsten Snapshots ausgeben.\n2. Pure JS-Differenz- und Formatierungslogik ergänzen.\n3. Verlauf als aufklappbare Diagnoseereignisse mit Feldvergleich und vollständigen Snapshots darstellen.\n4. API-, Modul-, Mobile- und Desktopprüfungen durchführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Audit-API liefert alle Ereignisse ohne Limit und ergänzt before/after als geparste Objekte, während Roh-JSON erhalten bleibt. UI nutzt aufklappbare Ereignisse mit deutsch benannter Aktion/Entität, Zeit, Benutzer, ID, feldweiser Differenz und vollständigen Vorher-/Nachher-Snapshots; Alle öffnen/schließen vorhanden. Test mit 205 Datensätzen beweist fehlende Begrenzung. Browser-Entnahme zeigte parts-Diff 150 g→100 g und vollständige Snapshots. Bei 320 px werden Feld/Vorher/Nachher vertikal dargestellt, 0 px Seitenüberlauf. Ruff, 16 Pytest- und Node-Tests grün.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Änderungsverlauf zu einem vollständigen Diagnoseprotokoll ausgebaut: unbegrenzte Ereignisliste, strukturierte Feld-Diffs, vollständige Roh-Snapshots und responsive aufklappbare Darstellung mit verständlichen deutschen Bezeichnungen.
<!-- SECTION:FINAL_SUMMARY:END -->
