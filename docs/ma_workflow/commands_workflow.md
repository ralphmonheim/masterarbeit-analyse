# Befehle ma_workflow

`ma_workflow` hat aktuell keine eigene Kommandozeile.

Das Modul wird von `ma_ui` und spaeteren Services importiert. Es enthaelt
Workflow-Kataloge und Adapterfunktionen, aber keine direkte Bedienoberflaeche.

## Sammelbefehle

Keine. `ma_workflow` wird aktuell nicht direkt gestartet.

## Einzelbefehle

### Pruefung

```powershell
.\.venv\Scripts\python.exe -m pytest tests -k "ma_workflow or ma_ui_shell"
```

## Referenz und Hinweise

Aktuelle pruefbare Bausteine:

- Workflow-Katalog
- zentrale Modulumsetzungsstaende fuer Streamlit
- Dashboard-Aktionen
- Pre-Process- und Post-Process-Listen
- Feedback-Zielmodule
- Analyse-Adapter zu `ma_analyse.services`
