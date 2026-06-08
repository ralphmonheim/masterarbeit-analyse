# ma_variants Befehle

Das Variantenmodul wird aktuell vor allem ueber Python-Tests und die lokale Streamlit-Oberflaeche bedient.

## Lokale Variantenoberflaeche

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\src\ma_variants\ui\app.py
```

Standardpfade:

- Parameter: `config/ma_variants/parameters/example_parameters.yaml`
- Optionen: `config/ma_variants/options/example_options.yaml`
- Namensregeln: `config/ma_variants/naming/example_naming_rules.yaml`
- Exporte: `data/ma_variants/exports/`

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_ma_variants_ui.py
.\.venv\Scripts\python.exe -m pytest tests\test_ma_variants_variant_manager.py
.\.venv\Scripts\python.exe -m pytest tests\test_ma_variants_importers.py
```

Komplette Varianten-Tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -k ma_variants
```

## Hinweise

- Es gibt noch keinen eigenen CLI-Einstieg `python -m ma_variants`.
- Fachlogik liegt in `src/ma_variants/`; die UI ruft nur bestehende Services auf.
- Ausgaben und lokale Arbeitsdaten fuer Varianten liegen unter `data/ma_variants/`.
