# Projektstruktur Review, Planungsbereich und Nutzerentscheidungen

## Ziel

Vorhandene Projektstruktur pruefen, modulare Planungs- und Dokumentationsstruktur anlegen und Nutzerentscheidungen getrennt dokumentieren.

## Status

Abgeschlossen als Strukturumsetzung am 2026-06-04.

## Kurzbeschreibung

Das Projekt wurde in der Dokumentation nach Projektorganisation und Modulen gegliedert. `PLAN_STATUS.md` ist nun die aktive modulare Steuerdatei. Nutzerentscheidungen und technische Entscheidungen werden getrennt gefuehrt.

## Abhaengigkeiten

Keine.

## Umgesetzte Schritte

- Planungsbereich unter `docs/project/plans/` angelegt.
- Entscheidungsbereich unter `docs/project/decisions/` angelegt.
- Modulbereiche fuer `docs/ma_analyse/`, `docs/ma_variants/` und `docs/ma_weather/` angelegt.
- `config/ma_variants/`, `data/ma_variants/` und `data/catalogs/` strukturiert.
- `data/test_output/` und `docs/examples/plot_templates/` fachlich eingeordnet.

## Offene Punkte

- Externe Plaene P001 und P002 manuell einfuegen.
- Spaetere `ma_analyse`-Datenpfadmigration separat planen.

## Naechster Schritt

P001 oder P002 erst nach vollstaendiger Planablage und Pruefung umsetzen.
