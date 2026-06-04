"""create product material document source catalog tables

Revision ID: 20260603_0004
Revises: 20260603_0003
Create Date: 2026-06-03 17:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260603_0004"
down_revision = "20260603_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("source_key", sa.String(length=120), nullable=False),
        sa.Column("source_type", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("citation", sa.Text(), nullable=False),
        sa.Column("accessed_at", sa.String(length=64), nullable=False),
        sa.Column("data_quality", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("source_key"),
    )
    op.create_table(
        "documents",
        sa.Column("document_key", sa.String(length=120), nullable=False),
        sa.Column("document_type", sa.String(length=120), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("document_path", sa.Text(), nullable=False),
        sa.Column("related_key", sa.String(length=120), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("data_quality", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("document_key"),
    )
    op.create_index("ix_documents_related_key", "documents", ["related_key"])
    op.create_table(
        "products",
        sa.Column("product_key", sa.String(length=120), nullable=False),
        sa.Column("product_type", sa.String(length=120), nullable=False),
        sa.Column("manufacturer", sa.String(length=255), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=False),
        sa.Column("nominal_power", sa.Float(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(length=16), nullable=False),
        sa.Column("gwp_value", sa.Float(), nullable=False),
        sa.Column("gwp_unit", sa.String(length=64), nullable=False),
        sa.Column("product_url", sa.Text(), nullable=False),
        sa.Column("document_path", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("data_quality", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("product_key"),
    )
    op.create_index("ix_products_product_type", "products", ["product_type"])
    op.create_table(
        "materials",
        sa.Column("material_key", sa.String(length=120), nullable=False),
        sa.Column("material_group", sa.String(length=120), nullable=False),
        sa.Column("material_name", sa.String(length=255), nullable=False),
        sa.Column("density", sa.Float(), nullable=False),
        sa.Column("lambda_value", sa.Float(), nullable=False),
        sa.Column("specific_heat_capacity", sa.Float(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("gwp_value", sa.Float(), nullable=False),
        sa.Column("gwp_unit", sa.String(length=64), nullable=False),
        sa.Column("document_path", sa.Text(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("data_quality", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("material_key"),
    )
    op.create_index("ix_materials_material_group", "materials", ["material_group"])
    op.create_table(
        "product_properties",
        sa.Column("product_key", sa.String(length=120), nullable=False),
        sa.Column("property_key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("data_quality", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["product_key"], ["products.product_key"]),
        sa.PrimaryKeyConstraint("product_key", "property_key"),
    )
    op.create_table(
        "material_properties",
        sa.Column("material_key", sa.String(length=120), nullable=False),
        sa.Column("property_key", sa.String(length=120), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("unit", sa.String(length=64), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("data_quality", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["material_key"], ["materials.material_key"]),
        sa.PrimaryKeyConstraint("material_key", "property_key"),
    )


def downgrade() -> None:
    op.drop_table("material_properties")
    op.drop_table("product_properties")
    op.drop_index("ix_materials_material_group", table_name="materials")
    op.drop_table("materials")
    op.drop_index("ix_products_product_type", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_documents_related_key", table_name="documents")
    op.drop_table("documents")
    op.drop_table("sources")
