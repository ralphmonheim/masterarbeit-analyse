# Plan Status

Stand: 2026-06-08

Diese Datei ist die aktive Planungsuebersicht. Sie wird nach Modulen gefuehrt und nach jeder Planumsetzung aktualisiert. Vollstaendige alte Planstaende liegen unter `docs/project/plans/archived/`.

## Projektorganisation

### Abgeschlossen

- P003 Projektstruktur, Planungsbereich und Nutzerentscheidungen: modulare Dokumentationsstruktur, Planindex, Strukturreview, Cleanup-Plan, Implementierungshinweise und getrennter Bereich fuer Nutzerentscheidungen wurden vorbereitet. Betroffen: `docs/project/`, `docs/ma_analyse/`, `docs/ma_variants/`, `docs/ma_weather/`, `docs/common/`.
- `docs/project/plans/archived/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md` ist nach Umsetzung archiviert.
- `docs/project/plans/archived/PLAN_Projektplan_Version_1_0_0.md` ist ein abgelegter Plan und nicht mehr die aktive Steuerdatei.
- `data/test_output/` bleibt ein lokaler, semi-wichtiger Arbeits- und Smoke-Test-Ordner. Der Nutzer leert ihn regelmaessig manuell.
- `docs/examples/plot_templates/` bleibt die belastbare Referenzgalerie fuer aktuelle `ma_analyse`-Plot-Template-Beispiele.
- Der leere, nicht versionierte Ordner `scripts/` wurde entfernt.
- `docs/project/UPDATE_ROUTINES.md` dokumentiert die festen Codex-Routinen `update repo`, `direkt update repo` und `update planung`.
- Der alte leere Root-Dokumentenordner wurde entfernt; Produkt- und Materialdatenblaetter liegen aktiv unter `data/catalogs/documents/`.

### Offen

- P001 und P002 liegen mit vollstaendigen Planinhalten als Markdown-Dateien in `docs/project/plans/inbox/`.
- Neue externe Plaene nach manueller Ablage in `docs/project/plans/inbox/` pruefen und in `PLAN_INDEX.md` sowie in diese Statusdatei uebernehmen.
- Nach groesseren Aenderungen pruefen, ob alte Planstaende nach `docs/project/plans/archived/` ausgelagert werden sollen.

## Modul ma_analyse

### Abgeschlossen

- Plot-Template-Katalog aktualisiert: `heating-year` ist overlayfrei, `heating-overlay` fuehrt die festen Heating-Overlays separat.
- Cooling-Plot-Templates getrennt: `cooling-year`, `cooling-month`, `cooling-week` und `cooling-day` verwenden Rohwerte aus `zone_energy_q_cool`; `cooling-absolute-year`, `cooling-absolute-month`, `cooling-absolute-week` und `cooling-absolute-day` zeigen Betraege positiv nach oben.
- Plot-Template-Referenzgalerie unter `docs/examples/plot_templates/` wurde mit 33 aktuellen Beispielen neu erzeugt.
- GUI-Mousewheel-Handler faengt nicht aufloesbare Tkinter-Combobox-Popups robust ab und verhindert `KeyError: 'popdown'`.

### Teilweise umgesetzt

- Plot-Template-Katalog: Referenzbilder liegen unter `docs/examples/plot_templates/`; die Dokumentation liegt unter `docs/ma_analyse/plot_template_examples.md`.
- Heating-Jahresplot nutzt eine gemeinsame Layoutbasis. Absolute Cooling-Jahresplots koennen diese Layoutbasis ebenfalls nutzen; relative Cooling-Templates bleiben als eigene signierte Darstellung erhalten.
- Interne Lasten und Energiebilanz sind als Plot-Template-Experimente vorhanden.
- Harte Datenpfadmigration: `ma_analyse` nutzt `data/ma_analyse/input`, `data/ma_analyse/database` und `data/ma_analyse/output`; alte Root-Pfade wurden entfernt.

### Offen

- Overlay-Uebernahme in Hauptfunktionen klaeren. Betroffen: `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/gui/app.py`, `src/ma_analyse/app/cli.py`.
- Klaeren, ob der normale `cooling`-Befehl spaeter ebenfalls relative Rohwerte und absolute Betraege als eigene Modi erhalten soll.
- GUI in kleinere Komponenten fuer Layout, Dialoge, Auswahl und Laufsteuerung aufteilen. Betroffen: `src/ma_analyse/gui/app.py`.
- Heating und Cooling weiter in Datenladen, Runner und Plotmodule zerlegen. Betroffen: `src/ma_analyse/analysis/heating.py`, `src/ma_analyse/analysis/cooling.py`, `src/ma_analyse/analysis/energy/`.

### Unklar

- Welche Overlays sollen in Hauptfunktionen sichtbar werden: feste Standard-Overlays, freie Nutzer-Overlays oder nur CLI/Config?
- Soll die relative/absolute Cooling-Logik auch in den regulaeren `cooling`-Befehl und die GUI uebernommen werden?
- Soll aus den Internal-Loads-Templates ein eigener Befehl entstehen oder eine Integration in bestehende Auswertungen?
- Soll die Energiebilanz absolute Leistung `[W]` behalten oder spaeter auf `[W/m2]` umgerechnet werden?

## Modul ma_variants

### Abgeschlossen

- `ma_variants` ist als eigenes Paket unter `src/ma_variants/` vorhanden.
- Variantenbezogene Konfigurationen liegen unter `config/ma_variants/`.
- Variantenbezogene Import-, Export- und IDA-Uebergabeordner liegen unter `data/ma_variants/`.
- Produkt- und Materialdokumente liegen als eigener Katalogbereich unter `data/catalogs/documents/`.
- P001 Bestandspruefung: Import, Optionsimport, Variantenzahlung, Variantenerzeugung, Auswahl, Namensgebung und Export sind bereits als testbare Module vorhanden.
- P001 Variantenoberflaeche: `src/ma_variants/ui/app.py` bildet Parameter/Optionen, Variantenraum, Auswahl, Namensgebung, Export, Ergebnisse und Status getrennt ab.
- P001 UI-Services: `src/ma_variants/ui/services.py` kapselt manuelle Auswahl, reproduzierbare Zufallsauswahl, Filterauswahl und Namensgenerierung ausserhalb der Streamlit-Datei.

### Teilweise umgesetzt

- P001 Variantenmodul GUI und Logikpruefung: automatisierte Service-Tests sind umgesetzt; die manuelle Streamlit-Pruefung steht noch aus.

### Offen

- Streamlit-UI manuell mit `.\.venv\Scripts\python.exe -m streamlit run .\src\ma_variants\ui\app.py` pruefen.
- Nach erfolgreicher manueller UI-Pruefung P001 nach `docs/project/plans/archived/` verschieben und `PLAN_INDEX.md` aktualisieren.
- Falls weitere Modulordner unter `data/ma_variants/` gebraucht werden, zuerst im Planstatus dokumentieren.

## Modul ma_weather

### Entwurf

- P002 Wetterdatenanalyse TRY Modul Integration ist vorgesehen, aber noch nicht implementiert.
- `docs/project/plans/inbox/250603_Plan_Wetterdatenanalyse_TRY_Integration.md` liegt mit vollstaendigem Planinhalt vor und wird nach P001 geprueft.

### Offen

- Entscheiden, ob zuerst nur Dokumentation und Konfiguration oder direkt `src/ma_weather/` angelegt wird.
- Keine Wetterdaten-Fachlogik implementieren, bevor der Plan gelesen und freigegeben ist.

## Offene Nutzerentscheidungen

- Umgang mit alten lokalen Dateien in `data/test_output/`, falls sie vor dem Leeren noch dokumentiert werden sollen.
- Einordnung externer Chat- und Planexporte: Masterarbeit, Website oder anderes Projekt.
- Umgang mit echten Produkt- und Materialdatenblaettern im Git-Repo oder ausserhalb des Repos klaeren.

## Archiv

- `docs/project/plans/archived/2026-05-26.md`: alter Planstatus vor der modularen Struktur.
- `docs/project/plans/archived/250604_Plan_Projektstruktur_Review_Planungsbereich_Nutzerentscheidungen.md`: umgesetzter Strukturplan P003.
- `docs/project/plans/archived/PLAN_Projektplan_Version_1_0_0.md`: abgelegter Projektplan Version 1.0.0.
