# P021 Analyse Stufe 4 Sensitivitaet

Stand: 2026-07-28
Status: Geplant
Prioritaet: Mittel
Abhaengigkeiten: P008, P013, P015, P019

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

## Offene Umnutzungs-Sensitivitaet 2026-07-28

Als spaetere Sensitivitaetsrichtung bleibt eine Umnutzung des SmallOffice
offen. Der erste Untersuchungsansatz soll ein alternatives Nutzungs- und
Belegungsprofil auf dem bestehenden thermischen Modell verwenden. Damit kann
zunaechst getrennt untersucht werden, wie sich eine andere Nutzung bei
unveraenderter Geometrie und Zonierung auf Randbedingungen und Ergebnisse
auswirkt.

Ein neuer Zonenzuschnitt ist nicht Teil von V1 und waere eine eigene,
spaeter zu entscheidende strukturelle Sensitivitaet. Nutzungsart,
Profilquelle, betroffene Raeume oder Zonen, Vergleichsmetriken und
Akzeptanzkriterien sind vor einer Umsetzung fachlich festzulegen.

## Eingangsauswertung 2026-08-14: Sensitivitaetsquellen

Das aufgenommene Literaturpaket ordnet Sensitivitaetsmethodik Stage 4 zu und
liefert insbesondere Metadaten fuer Tian (2013), Sanchez et al. (2012) und
CIBSE TM54. Es begruendet noch keine konkrete Ereignisdefinition,
Robustheitsmetrik oder Akzeptanzschwelle; diese bleiben fachlich offen und
werden erst nach manueller Quellpruefung weiter geplant.
