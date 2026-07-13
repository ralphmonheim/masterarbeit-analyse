"""Zeitplanreferenzen fuer ma_technical v2."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TechnicalSchedule:
    """Zeitplan im ma_technical-Register."""

    schedule_id: str
    name: str
    schedule_type: str
    values_reference: str = ""
    notes: str = ""


@dataclass(frozen=True, slots=True)
class TechnicalScheduleRegistry:
    """Sammlung technischer Zeitplaene einer Modellrevision."""

    schedules: tuple[TechnicalSchedule, ...] = ()
    registry_revision: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "schedules", tuple(self.schedules))
