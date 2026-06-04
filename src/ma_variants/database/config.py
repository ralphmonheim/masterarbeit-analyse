"""Datenbankkonfiguration aus Umgebungsvariablen."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import quote


class DatabaseConfigurationError(RuntimeError):
    """Wird ausgeloest, wenn keine vollstaendige DB-Konfiguration vorhanden ist."""


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    """Konfiguration fuer SQLAlchemy Engine und Session."""

    url: str
    echo: bool = False
    pool_pre_ping: bool = True


def _env_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _required_env(env: Mapping[str, str], key: str) -> str:
    value = env.get(key)
    if value:
        return value
    raise DatabaseConfigurationError(
        "Datenbankkonfiguration unvollstaendig. "
        "Setze MA_VARIANTS_DATABASE_URL oder mindestens "
        "MA_VARIANTS_DB_NAME und MA_VARIANTS_DB_USER."
    )


def build_database_url_from_env(env: Mapping[str, str] | None = None) -> str:
    """Erzeugt eine PostgreSQL-URL aus Umgebungsvariablen."""
    env_values = os.environ if env is None else env
    explicit_url = env_values.get("MA_VARIANTS_DATABASE_URL")
    if explicit_url:
        return explicit_url

    dialect = env_values.get("MA_VARIANTS_DB_DIALECT", "postgresql+psycopg")
    host = env_values.get("MA_VARIANTS_DB_HOST", "localhost")
    port = env_values.get("MA_VARIANTS_DB_PORT", "5432")
    database_name = _required_env(env_values, "MA_VARIANTS_DB_NAME")
    user = _required_env(env_values, "MA_VARIANTS_DB_USER")
    password = env_values.get("MA_VARIANTS_DB_PASSWORD")

    quoted_user = quote(user, safe="")
    auth = quoted_user
    if password:
        auth = f"{quoted_user}:{quote(password, safe='')}"

    return f"{dialect}://{auth}@{host}:{port}/{quote(database_name, safe='')}"


def load_database_settings(env: Mapping[str, str] | None = None) -> DatabaseSettings:
    """Laedt DB-Settings ohne Zugangsdaten im Code zu hinterlegen."""
    env_values = os.environ if env is None else env
    return DatabaseSettings(
        url=build_database_url_from_env(env_values),
        echo=_env_bool(env_values.get("MA_VARIANTS_DB_ECHO"), default=False),
        pool_pre_ping=_env_bool(env_values.get("MA_VARIANTS_DB_POOL_PRE_PING"), default=True),
    )
