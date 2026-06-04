"""create system template tables

Revision ID: 20260603_0002
Revises: 20260603_0001
Create Date: 2026-06-03 13:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260603_0002"
down_revision = "20260603_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "system_templates",
        sa.Column("system_template_key", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("system_type", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("system_template_key"),
    )
    op.create_table(
        "dependency_rules",
        sa.Column("rule_key", sa.String(length=120), nullable=False),
        sa.Column("system_template_key", sa.String(length=120), nullable=False),
        sa.Column("required_system_template_key", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["required_system_template_key"], ["system_templates.system_template_key"]),
        sa.ForeignKeyConstraint(["system_template_key"], ["system_templates.system_template_key"]),
        sa.PrimaryKeyConstraint("rule_key"),
    )
    op.create_index(
        "ix_dependency_rules_required_system_template_key",
        "dependency_rules",
        ["required_system_template_key"],
    )
    op.create_index("ix_dependency_rules_system_template_key", "dependency_rules", ["system_template_key"])
    op.create_table(
        "system_template_values",
        sa.Column("system_template_key", sa.String(length=120), nullable=False),
        sa.Column("parameter_key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("value_source", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["system_template_key"], ["system_templates.system_template_key"]),
        sa.PrimaryKeyConstraint("system_template_key", "parameter_key"),
    )


def downgrade() -> None:
    op.drop_table("system_template_values")
    op.drop_index("ix_dependency_rules_system_template_key", table_name="dependency_rules")
    op.drop_index("ix_dependency_rules_required_system_template_key", table_name="dependency_rules")
    op.drop_table("dependency_rules")
    op.drop_table("system_templates")
