---
id: TASK-2
title: Allgemeine App-Konfiguration und Server-CLI ergänzen
status: Done
assignee:
  - '@codex'
created_date: '2026-07-12 00:27'
updated_date: '2026-07-12 00:29'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Die bisher reine users.yaml wird zu einer allgemeinen Anwendungskonfiguration mit Server-Port und Benutzerliste. Das tiefkuehlliste-Kommando erhält eine echte CLI-Hilfe und --port überschreibt den konfigurierten Port.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Port ist in der allgemeinen YAML-Konfiguration einstellbar
- [x] #2 tiefkuehlliste --help zeigt Hilfe und startet keinen Server
- [x] #3 tiefkuehlliste --port PORT überschreibt den YAML-Port
- [x] #4 Beispielkonfiguration und README dokumentieren Dateinamen, Priorität und Nutzung
- [x] #5 Automatisierte Tests decken Konfiguration und CLI-Priorität ab
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Konfigurationsformat und Ladefunktion auf allgemeine config.yaml umstellen.\n2. argparse-CLI mit --host, --port und korrektem --help implementieren.\n3. Beispiel-/Lokalkonfiguration und README migrieren.\n4. Konfigurations- und CLI-Tests ergänzen und alle Checks ausführen.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Konfiguration auf config/config.yaml mit server.host, server.port und users migriert. Priorität: CLI > HOST/PORT > YAML. Lokale ignorierte Konfiguration nutzt Port 5050. Verifikation: 11 Pytest-Tests, Node-Modultest, Ruff Format/Lint und echte --help-Ausgabe erfolgreich.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Allgemeine YAML-App-Konfiguration und argparse-Server-CLI umgesetzt. --help startet keinen Dienst; --port überschreibt Umgebungs- und YAML-Werte. README, Beispiel- und lokale Testkonfiguration wurden aktualisiert.
<!-- SECTION:FINAL_SUMMARY:END -->
