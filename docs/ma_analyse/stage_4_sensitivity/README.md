# ma_analyse.stage_4_sensitivity

## Zweck

Robustheit und Parametereinfluss anhand kritischer Wetter-, Betriebs- und
Variantenfaelle untersuchen.

## Eingaben

- kritische Wetterereignisse
- Varianten, Parameterstudien und Analysezeitfenster

## Ausgaben

- Sensitivitaetsvergleiche, kritische Zeitraeume und Robustheitshinweise

## Abgrenzung

- keine vollstaendige probabilistische Risikoanalyse
- keine ausschliessliche Beschraenkung auf Jahreskennwerte

## Abhaengigkeiten

- `ma_weather`
- `ma_analyse.stage_2_optimization`

## Status

Geplant. Tages-/Wochenanalysen und Wetterkennwerte sind als Vorarbeiten
vorhanden; die fachliche ereignisbasierte Verknuepfung fehlt.

## Naechster Schritt

P021 umsetzen und Wetterereignisse mit den vorhandenen Zeitfensteranalysen
verbinden.
