# ma_core

- **Zweck:** Gemeinsame Pfad-, Konfigurations-, Logging-, ID- und Vorlagenregeln.
- **Eingaben:** technische Projektkonfiguration und wiederverwendbare Konventionen.
- **Ausgaben:** stabile Grundlagen fuer alle Fachmodule, einschliesslich
  Vorlagenschutz, formatneutraler Konfigurations-I/O, `InputSource`,
  `InputChange`, eindeutiger IDs, append-only Sitzungslogs und einer zentralen
  technischen Compliance-Grenze.
- **Abgrenzung:** keine Fachberechnungen und keine fachlichen Datenmodelle.
- **Abhaengigkeiten:** keine; Phase 0.
- **Status:** teilweise umgesetzt; P010 und P028 liefern getestete technische
  Grundlagen. `ma_core.compliance` stellt Metadaten-Preflight,
  Gruen-Gelb-Rot-/Unknown-Entscheidung, sichere Operationswrapper,
  Datenbereinigung und datensparsames JSONL-Audit bereit.
- **Naechster Schritt:** Die P010- und Compliance-Vertraege kontrolliert an
  weiteren Datei- und Systemgrenzen wiederverwenden.

## Compliance-Grenze

Vor geschuetzten Dateioperationen wird eine `OperationRequest` erzeugt und
mit `ComplianceService.evaluate()` geprueft. Gelbe Entscheidungen duerfen nur
ueber `approve_yellow()` und mit allen geforderten Referenzen freigegeben
werden. Rote und unbekannte Entscheidungen sind nicht uebersteuerbar.

Der DWD-TRY-2011-Konverter ist der erste produktive Adapter: Er liest `.idm`
und `.PRN` erst nach dokumentierter Nutzerbestaetigung und Referenz auf die
produktspezifischen Bezugsrechte. Die allgemeine Komponente veraendert keine
bestehenden Fachmodelle oder `ma_validation`-Freigaben.
