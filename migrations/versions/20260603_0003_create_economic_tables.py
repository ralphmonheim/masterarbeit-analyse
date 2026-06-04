"""create economic analysis tables

Revision ID: 20260603_0003
Revises: 20260603_0002
Create Date: 2026-06-03 16:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260603_0003"
down_revision = "20260603_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "generic_system_costs",
        sa.Column("system_type", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("investment_cost_eur", sa.Float(), nullable=False),
        sa.Column("maintenance_cost_eur_per_year", sa.Float(), nullable=False),
        sa.Column("lifetime_years", sa.Integer(), nullable=False),
        sa.Column("is_example_value", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("system_type"),
    )
    op.create_table(
        "energy_prices",
        sa.Column("energy_carrier", sa.String(length=120), nullable=False),
        sa.Column("price_eur_per_kwh", sa.Float(), nullable=False),
        sa.Column("is_example_value", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("energy_carrier"),
    )
    op.create_table(
        "economic_scenarios",
        sa.Column("scenario_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("observation_period_years", sa.Integer(), nullable=False),
        sa.Column("heating_energy_carrier", sa.String(length=120), nullable=False),
        sa.Column("cooling_energy_carrier", sa.String(length=120), nullable=False),
        sa.Column("default_heating_energy_kwh_per_year", sa.Float(), nullable=False),
        sa.Column("default_cooling_energy_kwh_per_year", sa.Float(), nullable=False),
        sa.Column("is_example_value", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["cooling_energy_carrier"], ["energy_prices.energy_carrier"]),
        sa.ForeignKeyConstraint(["heating_energy_carrier"], ["energy_prices.energy_carrier"]),
        sa.PrimaryKeyConstraint("scenario_key"),
    )
    op.create_table(
        "variant_cost_results",
        sa.Column("variant_key", sa.String(length=120), nullable=False),
        sa.Column("scenario_key", sa.String(length=120), nullable=False),
        sa.Column("variant_name", sa.String(length=255), nullable=False),
        sa.Column("selected_system_types", sa.JSON(), nullable=False),
        sa.Column("investment_cost_eur", sa.Float(), nullable=False),
        sa.Column("maintenance_cost_eur_per_year", sa.Float(), nullable=False),
        sa.Column("maintenance_cost_total_eur", sa.Float(), nullable=False),
        sa.Column("energy_cost_eur_per_year", sa.Float(), nullable=False),
        sa.Column("energy_cost_total_eur", sa.Float(), nullable=False),
        sa.Column("replacement_cost_eur", sa.Float(), nullable=False),
        sa.Column("total_cost_eur", sa.Float(), nullable=False),
        sa.Column("observation_period_years", sa.Integer(), nullable=False),
        sa.Column("heating_energy_kwh_per_year", sa.Float(), nullable=False),
        sa.Column("cooling_energy_kwh_per_year", sa.Float(), nullable=False),
        sa.Column("uses_simulation_results", sa.Boolean(), nullable=False),
        sa.Column("uses_example_energy_values", sa.Boolean(), nullable=False),
        sa.Column("assumption_notes", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["scenario_key"], ["economic_scenarios.scenario_key"]),
        sa.PrimaryKeyConstraint("variant_key", "scenario_key"),
    )


def downgrade() -> None:
    op.drop_table("variant_cost_results")
    op.drop_table("economic_scenarios")
    op.drop_table("energy_prices")
    op.drop_table("generic_system_costs")
