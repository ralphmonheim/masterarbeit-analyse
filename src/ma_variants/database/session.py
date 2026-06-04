"""Engine- und Session-Helfer fuer SQLAlchemy."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import DatabaseSettings, load_database_settings


def create_db_engine(settings: DatabaseSettings | None = None, **engine_kwargs: object) -> Engine:
    """Erstellt eine SQLAlchemy Engine aus env-basierten Settings."""
    resolved_settings = settings or load_database_settings()
    return create_engine(
        resolved_settings.url,
        echo=resolved_settings.echo,
        pool_pre_ping=resolved_settings.pool_pre_ping,
        future=True,
        **engine_kwargs,
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Erstellt eine Session-Factory fuer Repository-Funktionen."""
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)
