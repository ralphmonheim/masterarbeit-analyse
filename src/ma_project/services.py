"""Laden, Validieren und Speichern der Projekt-Demokonfiguration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ma_core import (
    ConfigurationSaveResult,
    ConfigurationSource,
    list_configuration_files,
    load_configuration_file,
    save_yaml_configuration,
)

from .models import SimulationProgramProfile, VariantNamingPart, VariantNamingProfile

DEFAULT_SIMULATION_PROGRAM_CONFIG = Path(
    "config/ma_project/simulation_programs/example_simulation_programs.yaml"
)
DEFAULT_NAMING_CONFIG = Path("config/ma_variants/naming/example_naming_rules.yaml")
LOCAL_SIMULATION_PROGRAM_DIR = Path("data/ma_project/config/simulation_programs")
LOCAL_NAMING_DIR = Path("data/ma_project/config/naming")


def template_source(path: str | Path) -> ConfigurationSource:
    """Kennzeichnet eine versionierte Ausgangsdatei als geschuetzte Vorlage."""
    return ConfigurationSource(path=Path(path), is_template=True)


def custom_source(path: str | Path) -> ConfigurationSource:
    """Kennzeichnet eine lokale Arbeitsdatei als eigene Konfiguration."""
    return ConfigurationSource(path=Path(path), is_template=False)


def load_simulation_program_profiles(
    config_path: str | Path = DEFAULT_SIMULATION_PROGRAM_CONFIG,
    *,
    is_template: bool = True,
) -> tuple[list[SimulationProgramProfile], str, ConfigurationSource]:
    """Laedt Programmliste und aktives Programm."""
    path = Path(config_path)
    data = load_configuration_file(path)
    raw_programs = data.get("simulation_programs")
    if not isinstance(raw_programs, list) or not raw_programs:
        raise ValueError("simulation_programs muss eine nicht leere Liste sein.")

    programs = [
        SimulationProgramProfile(
            program_key=str(raw_program.get("program_key", "")),
            display_name=str(raw_program.get("display_name", "")),
            version=str(raw_program.get("version", "")),
            note=str(raw_program.get("note", "")),
        )
        for raw_program in raw_programs
        if isinstance(raw_program, dict)
    ]
    if len(programs) != len(raw_programs):
        raise ValueError("Jeder Eintrag in simulation_programs muss ein Objekt sein.")

    program_keys = [program.program_key for program in programs]
    if len(program_keys) != len(set(program_keys)):
        raise ValueError("Programmschluessel muessen eindeutig sein.")

    active_program_key = str(data.get("active_program_key", ""))
    if active_program_key not in set(program_keys):
        raise ValueError("active_program_key muss auf ein vorhandenes Simulationsprogramm verweisen.")
    return programs, active_program_key, ConfigurationSource(path=path, is_template=is_template)


def simulation_program_payload(
    programs: list[SimulationProgramProfile],
    active_program_key: str,
) -> dict[str, Any]:
    """Erzeugt die formatneutrale Nutzlast einer Programmliste."""
    program_keys = [program.program_key for program in programs]
    if not programs:
        raise ValueError("Mindestens ein Simulationsprogramm ist erforderlich.")
    if len(program_keys) != len(set(program_keys)):
        raise ValueError("Programmschluessel muessen eindeutig sein.")
    if active_program_key not in set(program_keys):
        raise ValueError("Das aktive Simulationsprogramm ist nicht in der Programmliste enthalten.")
    return {
        "active_program_key": active_program_key,
        "simulation_programs": [
            {
                "program_key": program.program_key,
                "display_name": program.display_name,
                "version": program.version,
                "note": program.note,
            }
            for program in programs
        ],
    }


def load_variant_naming_profile(
    config_path: str | Path = DEFAULT_NAMING_CONFIG,
    *,
    is_template: bool = True,
) -> tuple[VariantNamingProfile, ConfigurationSource]:
    """Laedt ein neutrales Benennungsprofil aus YAML oder JSON."""
    path = Path(config_path)
    data = load_configuration_file(path)
    raw_naming = data.get("naming")
    if not isinstance(raw_naming, dict):
        raise ValueError("Konfiguration muss ein Objekt 'naming' enthalten.")
    raw_parts = raw_naming.get("parts")
    if not isinstance(raw_parts, list):
        raise ValueError("naming.parts muss eine Liste sein.")

    parts: list[VariantNamingPart] = []
    for raw_part in raw_parts:
        if not isinstance(raw_part, dict):
            raise ValueError("Jeder Eintrag in naming.parts muss ein Objekt sein.")
        raw_tokens = raw_part.get("option_tokens")
        if not isinstance(raw_tokens, dict):
            raise ValueError("option_tokens muss ein Objekt sein.")
        parts.append(
            VariantNamingPart(
                parameter_key=str(raw_part.get("parameter_key", "")),
                option_tokens={str(key): str(value) for key, value in raw_tokens.items()},
            )
        )

    raw_include_index = raw_naming.get("include_index", True)
    if not isinstance(raw_include_index, bool):
        raise ValueError("naming.include_index muss true oder false sein.")
    raw_index_width = raw_naming.get("index_width", 3)
    if isinstance(raw_index_width, bool) or not isinstance(raw_index_width, int):
        raise ValueError("naming.index_width muss eine ganze Zahl sein.")

    profile = VariantNamingProfile(
        prefix=str(raw_naming.get("prefix", "V")),
        index_width=raw_index_width,
        separator=str(raw_naming.get("separator", "_")),
        include_index=raw_include_index,
        parts=tuple(parts),
    )
    return profile, ConfigurationSource(path=path, is_template=is_template)


def variant_naming_payload(profile: VariantNamingProfile) -> dict[str, Any]:
    """Erzeugt die formatneutrale Nutzlast eines Benennungsprofils."""
    return {
        "naming": {
            "prefix": profile.prefix,
            "index_width": profile.index_width,
            "separator": profile.separator,
            "include_index": profile.include_index,
            "parts": [
                {
                    "parameter_key": part.parameter_key,
                    "option_tokens": dict(part.option_tokens),
                }
                for part in profile.parts
            ],
        }
    }


def save_simulation_program_profiles(
    programs: list[SimulationProgramProfile],
    active_program_key: str,
    *,
    file_name: str,
    source: ConfigurationSource | None = None,
    overwrite_existing: bool = False,
    overwrite_confirmed: bool = False,
    target_dir: str | Path = LOCAL_SIMULATION_PROGRAM_DIR,
) -> ConfigurationSaveResult:
    """Speichert eine eigene Programmliste unter den verbindlichen Schutzregeln."""
    return save_yaml_configuration(
        simulation_program_payload(programs, active_program_key),
        target_dir=target_dir,
        file_name=file_name,
        source=source,
        overwrite_existing=overwrite_existing,
        overwrite_confirmed=overwrite_confirmed,
    )


def save_variant_naming_profile(
    profile: VariantNamingProfile,
    *,
    file_name: str,
    source: ConfigurationSource | None = None,
    overwrite_existing: bool = False,
    overwrite_confirmed: bool = False,
    target_dir: str | Path = LOCAL_NAMING_DIR,
) -> ConfigurationSaveResult:
    """Speichert ein eigenes Benennungsprofil unter den Schutzregeln."""
    return save_yaml_configuration(
        variant_naming_payload(profile),
        target_dir=target_dir,
        file_name=file_name,
        source=source,
        overwrite_existing=overwrite_existing,
        overwrite_confirmed=overwrite_confirmed,
    )


def list_local_simulation_program_files(
    target_dir: str | Path = LOCAL_SIMULATION_PROGRAM_DIR,
) -> tuple[Path, ...]:
    return list_configuration_files(target_dir)


def list_local_naming_files(target_dir: str | Path = LOCAL_NAMING_DIR) -> tuple[Path, ...]:
    return list_configuration_files(target_dir)
