"""SQLAlchemy-Modelle fuer zentrale Variantenprojektdaten."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DbOptionSet(Base):
    """Tabelle `option_sets`."""

    __tablename__ = "option_sets"

    option_set_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    parameters: Mapped[list["DbParameter"]] = relationship(back_populates="option_set")
    option_values: Mapped[list["DbOptionValue"]] = relationship(back_populates="option_set")


class DbParameter(Base):
    """Tabelle `parameters`."""

    __tablename__ = "parameters"

    parameter_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    parameter_class: Mapped[str] = mapped_column(String(120), nullable=False)
    option_set_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("option_sets.option_set_key"),
        nullable=False,
        index=True,
    )
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    is_variant_relevant: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_naming_relevant: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_export_relevant: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    option_set: Mapped[DbOptionSet] = relationship(back_populates="parameters")
    variant_values: Mapped[list["DbVariantValue"]] = relationship(back_populates="parameter")


class DbOptionValue(Base):
    """Tabelle `option_values`."""

    __tablename__ = "option_values"

    option_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    option_set_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("option_sets.option_set_key"),
        nullable=False,
        index=True,
    )
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    option_set: Mapped[DbOptionSet] = relationship(back_populates="option_values")
    variant_values: Mapped[list["DbVariantValue"]] = relationship(back_populates="option_value")


class DbVariant(Base):
    """Tabelle `variants`."""

    __tablename__ = "variants"

    variant_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    variant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    values: Mapped[list["DbVariantValue"]] = relationship(back_populates="variant")


class DbVariantValue(Base):
    """Tabelle `variant_values`."""

    __tablename__ = "variant_values"

    variant_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("variants.variant_key"),
        primary_key=True,
    )
    parameter_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("parameters.parameter_key"),
        primary_key=True,
    )
    option_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("option_values.option_key"),
        nullable=False,
        index=True,
    )
    resolved_value: Mapped[Any] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    variant: Mapped[DbVariant] = relationship(back_populates="values")
    parameter: Mapped[DbParameter] = relationship(back_populates="variant_values")
    option_value: Mapped[DbOptionValue] = relationship(back_populates="variant_values")


class DbSystemTemplate(Base):
    """Tabelle `system_templates`."""

    __tablename__ = "system_templates"

    system_template_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    system_type: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    values: Mapped[list["DbSystemTemplateValue"]] = relationship(back_populates="system_template")


class DbSystemTemplateValue(Base):
    """Tabelle `system_template_values`."""

    __tablename__ = "system_template_values"

    system_template_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("system_templates.system_template_key"),
        primary_key=True,
    )
    parameter_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    value_source: Mapped[str] = mapped_column(String(64), nullable=False, default="template")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    system_template: Mapped[DbSystemTemplate] = relationship(back_populates="values")


class DbDependencyRule(Base):
    """Tabelle `dependency_rules`."""

    __tablename__ = "dependency_rules"

    rule_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    system_template_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("system_templates.system_template_key"),
        nullable=False,
        index=True,
    )
    required_system_template_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("system_templates.system_template_key"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbGenericSystemCost(Base):
    """Tabelle `generic_system_costs`."""

    __tablename__ = "generic_system_costs"

    system_type: Mapped[str] = mapped_column(String(120), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    investment_cost_eur: Mapped[float] = mapped_column(Float, nullable=False)
    maintenance_cost_eur_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    lifetime_years: Mapped[int] = mapped_column(Integer, nullable=False)
    is_example_value: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbEnergyPrice(Base):
    """Tabelle `energy_prices`."""

    __tablename__ = "energy_prices"

    energy_carrier: Mapped[str] = mapped_column(String(120), primary_key=True)
    price_eur_per_kwh: Mapped[float] = mapped_column(Float, nullable=False)
    is_example_value: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbEconomicScenario(Base):
    """Tabelle `economic_scenarios`."""

    __tablename__ = "economic_scenarios"

    scenario_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    observation_period_years: Mapped[int] = mapped_column(Integer, nullable=False)
    heating_energy_carrier: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("energy_prices.energy_carrier"),
        nullable=False,
    )
    cooling_energy_carrier: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("energy_prices.energy_carrier"),
        nullable=False,
    )
    default_heating_energy_kwh_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    default_cooling_energy_kwh_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    is_example_value: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbVariantCostResult(Base):
    """Tabelle `variant_cost_results`."""

    __tablename__ = "variant_cost_results"

    variant_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    scenario_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("economic_scenarios.scenario_key"),
        primary_key=True,
    )
    variant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    selected_system_types: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    investment_cost_eur: Mapped[float] = mapped_column(Float, nullable=False)
    maintenance_cost_eur_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    maintenance_cost_total_eur: Mapped[float] = mapped_column(Float, nullable=False)
    energy_cost_eur_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    energy_cost_total_eur: Mapped[float] = mapped_column(Float, nullable=False)
    replacement_cost_eur: Mapped[float] = mapped_column(Float, nullable=False)
    total_cost_eur: Mapped[float] = mapped_column(Float, nullable=False)
    observation_period_years: Mapped[int] = mapped_column(Integer, nullable=False)
    heating_energy_kwh_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    cooling_energy_kwh_per_year: Mapped[float] = mapped_column(Float, nullable=False)
    uses_simulation_results: Mapped[bool] = mapped_column(Boolean, nullable=False)
    uses_example_energy_values: Mapped[bool] = mapped_column(Boolean, nullable=False)
    assumption_notes: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbSource(Base):
    """Tabelle `sources`."""

    __tablename__ = "sources"

    source_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    source_type: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    citation: Mapped[str] = mapped_column(Text, nullable=False)
    accessed_at: Mapped[str] = mapped_column(String(64), nullable=False)
    data_quality: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbDocument(Base):
    """Tabelle `documents`."""

    __tablename__ = "documents"

    document_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    document_type: Mapped[str] = mapped_column(String(120), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    document_path: Mapped[str] = mapped_column(Text, nullable=False)
    related_key: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    data_quality: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )


class DbProduct(Base):
    """Tabelle `products`."""

    __tablename__ = "products"

    product_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    product_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    manufacturer: Mapped[str] = mapped_column(String(255), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    nominal_power: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(16), nullable=False)
    gwp_value: Mapped[float] = mapped_column(Float, nullable=False)
    gwp_unit: Mapped[str] = mapped_column(String(64), nullable=False)
    product_url: Mapped[str] = mapped_column(Text, nullable=False)
    document_path: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    data_quality: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    properties: Mapped[list["DbProductProperty"]] = relationship(back_populates="product")


class DbProductProperty(Base):
    """Tabelle `product_properties`."""

    __tablename__ = "product_properties"

    product_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("products.product_key"),
        primary_key=True,
    )
    property_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    data_quality: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    product: Mapped[DbProduct] = relationship(back_populates="properties")


class DbMaterial(Base):
    """Tabelle `materials`."""

    __tablename__ = "materials"

    material_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    material_group: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    material_name: Mapped[str] = mapped_column(String(255), nullable=False)
    density: Mapped[float] = mapped_column(Float, nullable=False)
    lambda_value: Mapped[float] = mapped_column(Float, nullable=False)
    specific_heat_capacity: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    gwp_value: Mapped[float] = mapped_column(Float, nullable=False)
    gwp_unit: Mapped[str] = mapped_column(String(64), nullable=False)
    document_path: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    data_quality: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    properties: Mapped[list["DbMaterialProperty"]] = relationship(back_populates="material")


class DbMaterialProperty(Base):
    """Tabelle `material_properties`."""

    __tablename__ = "material_properties"

    material_key: Mapped[str] = mapped_column(
        String(120),
        ForeignKey("materials.material_key"),
        primary_key=True,
    )
    property_key: Mapped[str] = mapped_column(String(120), primary_key=True)
    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    data_quality: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        server_default=func.now(),
        nullable=False,
    )

    material: Mapped[DbMaterial] = relationship(back_populates="properties")


class DbImportLog(Base):
    """Tabelle `import_logs`."""

    __tablename__ = "import_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    error_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        server_default=func.now(),
        nullable=False,
    )
