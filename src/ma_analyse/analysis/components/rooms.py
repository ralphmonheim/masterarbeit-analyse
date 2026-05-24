"""Helfer fuer Raumdateien in aufbereiteten Variantenordnern."""

from __future__ import annotations

import os
from pathlib import Path

from ...core.config import ROOM_FILE_EXTENSION


def get_room_data_file(variant_dir: str | Path, room_name: str, extension: str = ROOM_FILE_EXTENSION) -> str:
    """Liefert den erwarteten Dateipfad fuer eine aufbereitete Raumdatei."""
    return os.path.join(str(variant_dir), f"{room_name.replace(' ', '_')}{extension}")
