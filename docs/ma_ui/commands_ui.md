# Befehle ma_ui

## Zentrale Streamlit-Oberflaeche starten

Empfohlen ist der Modulaufruf ueber die Projekt-venv:

```powershell
.\.venv\Scripts\python.exe -m streamlit run src\ma_ui\app.py
```

Alternative:

```powershell
.\.venv\Scripts\streamlit.exe run src\ma_ui\app.py
```

## Hinweise

- `ma_ui` ist aktuell eine minimale Shell mit Zielstruktur fuer
  `module_views/` und `shared/`.
- Fachlogik wird nicht in der UI berechnet.
- Analyseaufrufe laufen ueber `ma_workflow` und die Service-Fassade von
  `ma_analyse`.
- Die bestehende Tkinter-GUI von `ma_analyse` bleibt separat bestehen.
- Wenn Streamlit nach Codeaenderungen alte Importfehler zeigt, den laufenden
  Streamlit-Prozess stoppen und mit dem empfohlenen venv-Befehl neu starten.
