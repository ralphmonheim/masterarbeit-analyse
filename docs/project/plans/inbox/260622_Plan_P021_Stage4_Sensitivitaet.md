# P021 Analyse Stufe 4 Sensitivitaet

Stand: 2026-06-22
Status: Geplant
Prioritaet: Mittel
Abhaengigkeiten: P008, P019

## Ziel

Kritische Wetter- und Betriebsfaelle erkennen und vorhandene Tages-,
Wochen- und Variantenanalysen fuer Robustheits- und Sensitivitaetsfragen
verwenden.

## Arbeitspakete

- Ereignisdefinitionen fuer Hitze, Kaelte, Strahlung und Beleuchtung planen.
- Niederschlag nur bei belastbarer Datenspalte beruecksichtigen.
- Wetterereignisse als Zeitfenster an bestehende Analysebefehle uebergeben.
- Sollwerte, Profile, interne Lasten, technische Leistungen, Bauteile und
  Fenster als spaetere Sensitivitaetsparameter strukturieren.
- Ergebnisdarstellung fuer Parametereinfluss und Robustheit planen.
- Wetterdatensaetze nach ihrer Rolle unterscheiden: reale Wetterjahre duerfen
  Messdatenvergleiche und Ereignisanalysen unterstuetzen, ersetzen aber nicht
  stillschweigend TRY-, Designwetter- oder normative Nachweisdatensaetze.

## Akzeptanzkriterien

- Ereignisauswahl ist aus Wetterdaten reproduzierbar.
- Jahresdaten werden nicht als einziges Analysezeitfenster vorausgesetzt.
- Vorhandene Zeitfensterfunktionen werden wiederverwendet.

## Handover-Ergaenzung 2026-07-21

Die Kapazitaets- und Robustheitsbewertung bewertet unter den untersuchten
Klima- und Betriebsrandbedingungen unter anderem Ueber- und
Untertemperaturstunden, operative Temperaturen, nicht gedeckte Leistung,
Systemauslastung, Komfortverletzungen und die Abweichung zum Referenzklima.
Sie veraendert weder technische Kapazitaeten noch Varianten automatisch.
Ein daraus abgeleiteter `StudyDirectionProposal` bleibt bis zur
Nutzerfreigabe ein nicht-ausfuehrbarer Vorschlag fuer `ma_parameters`.
