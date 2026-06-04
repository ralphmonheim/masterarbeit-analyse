"""Gemeinsame SQLAlchemy-Basis fuer `ma_variants`."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative Base fuer alle Varianten-Tabellen."""
