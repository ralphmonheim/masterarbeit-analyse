"""create ma_variants core tables

Revision ID: 20260603_0001
Revises:
Create Date: 2026-06-03 12:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260603_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "option_sets",
        sa.Column("option_set_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("option_set_key"),
    )
    op.create_table(
        "variants",
        sa.Column("variant_key", sa.String(length=120), nullable=False),
        sa.Column("variant_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("variant_key"),
    )
    op.create_table(
        "import_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "option_values",
        sa.Column("option_key", sa.String(length=120), nullable=False),
        sa.Column("option_set_key", sa.String(length=120), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["option_set_key"], ["option_sets.option_set_key"]),
        sa.PrimaryKeyConstraint("option_key"),
    )
    op.create_index("ix_option_values_option_set_key", "option_values", ["option_set_key"])
    op.create_table(
        "parameters",
        sa.Column("parameter_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("parameter_class", sa.String(length=120), nullable=False),
        sa.Column("option_set_key", sa.String(length=120), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("is_variant_relevant", sa.Boolean(), nullable=False),
        sa.Column("is_naming_relevant", sa.Boolean(), nullable=False),
        sa.Column("is_export_relevant", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["option_set_key"], ["option_sets.option_set_key"]),
        sa.PrimaryKeyConstraint("parameter_key"),
    )
    op.create_index("ix_parameters_option_set_key", "parameters", ["option_set_key"])
    op.create_table(
        "variant_values",
        sa.Column("variant_key", sa.String(length=120), nullable=False),
        sa.Column("parameter_key", sa.String(length=120), nullable=False),
        sa.Column("option_key", sa.String(length=120), nullable=False),
        sa.Column("resolved_value", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["option_key"], ["option_values.option_key"]),
        sa.ForeignKeyConstraint(["parameter_key"], ["parameters.parameter_key"]),
        sa.ForeignKeyConstraint(["variant_key"], ["variants.variant_key"]),
        sa.PrimaryKeyConstraint("variant_key", "parameter_key"),
    )
    op.create_index("ix_variant_values_option_key", "variant_values", ["option_key"])


def downgrade() -> None:
    op.drop_index("ix_variant_values_option_key", table_name="variant_values")
    op.drop_table("variant_values")
    op.drop_index("ix_parameters_option_set_key", table_name="parameters")
    op.drop_table("parameters")
    op.drop_index("ix_option_values_option_set_key", table_name="option_values")
    op.drop_table("option_values")
    op.drop_table("import_logs")
    op.drop_table("variants")
    op.drop_table("option_sets")
