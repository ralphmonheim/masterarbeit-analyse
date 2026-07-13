# Warn- und Stopplogik

Die gemeinsamen Vorlagen unter `../shared/warning_templates.md` sind
verbindlich. Die folgenden Texte konkretisieren sie fuer IDA ICE.

## Gelb

> WARNUNG - PRUEFUNG ERFORDERLICH
> Der angeforderte Vorgang betrifft eine vollstaendige oder gemischte
> IDA-ICE-Datei, mitgelieferte EQUA-Inhalte, moegliche Drittinhalte oder
> vertrauliche Projektdaten.
> Betroffene Grenze: [Grenze]
> Hauptrisiko: [Lizenz / Urheberrecht / Geschaeftsgeheimnis / Datenschutz / Vertraulichkeit]
> Vorgesehener Zweck: [Zweck]
> Sichere Alternative: [lokale Verarbeitung / bereinigter Export / begrenzte
> Parameterliste / manuelle Uebertragung / schriftliche Freigabe]
> Nur der eindeutig zulaessige Teil des Vorgangs wird fortgesetzt.

## Rot

> STOPP - FESTGELEGTE COMPLIANCE-GRENZE UEBERSCHRITTEN
> Der angeforderte Vorgang betrifft eine nach der aktuellen Pruefung nicht
> erlaubte oder nicht ausreichend freigegebene Verarbeitung.
> Betroffene Grenze: [Grenze]
> Relevante EULA-Regel: [Abschnitt]
> Risiko: [Reverse Engineering / Bibliotheksreproduktion / automatisierter
> Simulationsstart / Weitergabe / Schutzmassnahmen / konkurrierende Funktion]
> Der Vorgang wird nicht durchgefuehrt.
> Voraussetzung fuer eine Neubewertung: ausdrueckliche schriftliche Freigabe
> von EQUA oder dokumentierte anderweitige Rechtsgrundlage.
