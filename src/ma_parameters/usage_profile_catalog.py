"""Vom Nutzer bereitgestellte Metadaten der 43 Nutzungsprofilgruppen.

Die Datei enthaelt bewusst nur Profilnummern und Bezeichnungen. Geschuetzte
Tabellenwerte werden hier weder extrahiert noch vervielfaeltigt.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UsageProfileMetadata:
    profile_id: str
    table_reference: str
    name: str
    standard_name: str = "DIN/TS 18599-10"
    edition: str = "2025-10"
    source_status: str = "user_supplied_metadata_only"
    review_status: str = "profile_values_not_released"
    metadata_revision: str = "1.0"


_PROFILE_NAMES = (
    "Einzelbüro",
    "Gruppenbüro (zwei bis sechs Arbeitsplätze)",
    "Großraumbüro (ab sieben Arbeitsplätzen)",
    "Besprechung/Sitzungszimmer/Seminar",
    "Schalterhalle",
    "Einzelhandel/Kaufhaus",
    "Einzelhandel/Kaufhaus (Lebensmittelabteilung mit Kühlprodukten)",
    "Klassenzimmer (Schule), Gruppenraum (Kindergarten)",
    "Hörsaal, Auditorium",
    "Bettenzimmer",
    "Hotelzimmer",
    "Kantine",
    "Restaurant",
    "Küche in Nichtwohngebäuden",
    "Küche – Vorbereitung, Lager",
    "WC und Sanitärräume in Nichtwohngebäuden",
    "sonstige Aufenthaltsräume",
    "Nebenflächen ohne Aufenthaltsräume",
    "Verkehrsfläche",
    "Lager",
    "Rechenzentrum",
    "gewerbliche und industrielle Hallen – schwere Arbeit",
    "gewerbliche und industrielle Hallen – mittelschwere Arbeit",
    "gewerbliche und industrielle Hallen – leichte Arbeit",
    "Zuschauerbereich",
    "Theater – Foyer",
    "Bühne",
    "Messe/Kongress",
    "Ausstellungsräume und Museum",
    "Bibliothek – Lesesaal",
    "Bibliothek – Freihandbereich",
    "Bibliothek – Magazin und Depot",
    "Turnhalle",
    "Parkhaus (Büro- und Privatnutzung)",
    "Parkhaus (öffentliche Nutzung)",
    "Saunabereich",
    "Fitnessraum",
    "Labor",
    "Untersuchungs- und Behandlungsräume",
    "Spezialpflegebereiche",
    "Flure des allgemeinen Pflegebereichs",
    "Arztpraxen und Therapeutische Praxen",
    "Lagerhallen, Logistikhallen",
)

DIN_USAGE_PROFILE_METADATA = tuple(
    UsageProfileMetadata(
        profile_id=f"DIN18599-A{number:02d}",
        table_reference=f"A.{number}",
        name=name,
    )
    for number, name in enumerate(_PROFILE_NAMES, start=1)
)

_IFC_NAME_RULES = (
    (("toilet", "wc", "sanit"), "DIN18599-A16"),
    (("meeting", "conference", "besprech"), "DIN18599-A04"),
    (("corridor", "flur"), "DIN18599-A19"),
    (("lobby", "entrance", "reception", "empfang"), "DIN18599-A05"),
    (("break", "aufenthalt"), "DIN18599-A17"),
    (("copy", "kopier", "technik", "neben"), "DIN18599-A18"),
    (("office", "büro", "buero"), "DIN18599-A01"),
    (("storage", "lager"), "DIN18599-A20"),
)


def suggest_usage_profile_id(ifc_room_name: str) -> str | None:
    """Liefert nur bei einem eindeutigen einfachen Namenstreffer einen Vorschlag."""
    normalized_name = ifc_room_name.casefold()
    matches = {
        profile_id
        for keywords, profile_id in _IFC_NAME_RULES
        if any(keyword in normalized_name for keyword in keywords)
    }
    return next(iter(matches)) if len(matches) == 1 else None
