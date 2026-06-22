"""Kompatibilitaetszugriff auf den zentralen Workflow-Katalog."""

from __future__ import annotations

from .catalog import get_workflow_step, list_workflow_steps, steps_by_phase

__all__ = ["get_workflow_step", "list_workflow_steps", "steps_by_phase"]
