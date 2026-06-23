"""Fachmodelle fuer die Auswahl aktiver Parameteroptionen."""

from __future__ import annotations

from dataclasses import dataclass

from ma_core import ConfigurationSource


@dataclass(frozen=True, slots=True)
class ParameterOptionSelection:
    """Speichert die aktiven Optionswerte je Optionsgruppe."""

    active_option_keys_by_set: dict[str, tuple[str, ...]]
    source: ConfigurationSource
