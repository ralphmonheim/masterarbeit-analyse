"""Einfache Repository-Funktionen fuer die Kerntabellen."""

from __future__ import annotations

from typing import Any, Iterable

from sqlalchemy.orm import Session

from ..document_catalog import Document
from ..economic_analysis import EconomicScenario, EnergyPrice, GenericSystemCost, VariantCostResult
from ..material_catalog import Material, MaterialProperty
from ..option_catalog import OptionSet, OptionValue
from ..parameter_catalog import Parameter
from ..product_catalog import Product, ProductProperty
from ..source_catalog import Source
from ..system_catalog import DependencyRule, SystemTemplate, SystemTemplateValue
from ..variant_manager import Variant, VariantValue
from .models import (
    DbDependencyRule,
    DbDocument,
    DbEconomicScenario,
    DbEnergyPrice,
    DbGenericSystemCost,
    DbImportLog,
    DbMaterial,
    DbMaterialProperty,
    DbOptionSet,
    DbOptionValue,
    DbParameter,
    DbProduct,
    DbProductProperty,
    DbSource,
    DbSystemTemplate,
    DbSystemTemplateValue,
    DbVariant,
    DbVariantCostResult,
    DbVariantValue,
)

GeneratedVariant = tuple[Variant, list[VariantValue]]


def save_parameters(session: Session, parameters: Iterable[Parameter]) -> list[DbParameter]:
    """Speichert oder aktualisiert Parameter im aktuellen Session-Kontext."""
    rows = [
        DbParameter(
            parameter_key=parameter.parameter_key,
            display_name=parameter.display_name,
            category=parameter.category,
            parameter_class=parameter.parameter_class,
            option_set_key=parameter.option_set_key,
            unit=parameter.unit,
            is_variant_relevant=parameter.is_variant_relevant,
            is_naming_relevant=parameter.is_naming_relevant,
            is_export_relevant=parameter.is_export_relevant,
        )
        for parameter in parameters
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_option_sets(session: Session, option_sets: Iterable[OptionSet]) -> list[DbOptionSet]:
    """Speichert oder aktualisiert Optionsgruppen."""
    rows = [
        DbOptionSet(
            option_set_key=option_set.option_set_key,
            display_name=option_set.display_name,
            description=option_set.description,
        )
        for option_set in option_sets
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_option_values(session: Session, option_values: Iterable[OptionValue]) -> list[DbOptionValue]:
    """Speichert oder aktualisiert Optionswerte."""
    rows = [
        DbOptionValue(
            option_key=option_value.option_key,
            option_set_key=option_value.option_set_key,
            label=option_value.label,
            value=option_value.value,
            unit=option_value.unit,
            is_active=option_value.is_active,
        )
        for option_value in option_values
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_variants(session: Session, variants: Iterable[Variant]) -> list[DbVariant]:
    """Speichert oder aktualisiert Variantenstammdaten."""
    rows = [
        DbVariant(
            variant_key=variant.variant_key,
            variant_name=variant.variant_name,
            status=variant.status,
        )
        for variant in variants
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_variant_values(session: Session, variant_values: Iterable[VariantValue]) -> list[DbVariantValue]:
    """Speichert oder aktualisiert Variantenwerte."""
    rows = [
        DbVariantValue(
            variant_key=variant_value.variant_key,
            parameter_key=variant_value.parameter_key,
            option_key=variant_value.option_key,
            resolved_value=variant_value.resolved_value,
        )
        for variant_value in variant_values
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_generated_variants(
    session: Session,
    generated_variants: Iterable[GeneratedVariant],
) -> tuple[list[DbVariant], list[DbVariantValue]]:
    """Speichert Varianten und Variantenwerte aus der Generator-Struktur."""
    generated_variant_list = list(generated_variants)
    variant_rows = save_variants(session, [variant for variant, _values in generated_variant_list])
    value_rows = save_variant_values(
        session,
        [
            variant_value
            for _variant, variant_values in generated_variant_list
            for variant_value in variant_values
        ],
    )
    return variant_rows, value_rows


def save_system_templates(
    session: Session,
    system_templates: Iterable[SystemTemplate],
) -> list[DbSystemTemplate]:
    """Speichert oder aktualisiert Systemtemplates."""
    rows = [
        DbSystemTemplate(
            system_template_key=system_template.system_template_key,
            display_name=system_template.display_name,
            system_type=system_template.system_type,
            description=system_template.description,
            is_active=system_template.is_active,
        )
        for system_template in system_templates
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_system_template_values(
    session: Session,
    system_template_values: Iterable[SystemTemplateValue],
) -> list[DbSystemTemplateValue]:
    """Speichert oder aktualisiert Systemtemplate-Werte."""
    rows = [
        DbSystemTemplateValue(
            system_template_key=system_template_value.system_template_key,
            parameter_key=system_template_value.parameter_key,
            value=system_template_value.value,
            unit=system_template_value.unit,
            value_source=system_template_value.value_source,
        )
        for system_template_value in system_template_values
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_dependency_rules(
    session: Session,
    dependency_rules: Iterable[DependencyRule],
) -> list[DbDependencyRule]:
    """Speichert oder aktualisiert einfache Template-Abhaengigkeitsregeln."""
    rows = [
        DbDependencyRule(
            rule_key=dependency_rule.rule_key,
            system_template_key=dependency_rule.system_template_key,
            required_system_template_key=dependency_rule.required_system_template_key,
            description=dependency_rule.description,
            is_active=dependency_rule.is_active,
        )
        for dependency_rule in dependency_rules
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_generic_system_costs(
    session: Session,
    generic_system_costs: Iterable[GenericSystemCost],
) -> list[DbGenericSystemCost]:
    """Speichert oder aktualisiert generische Systemkosten."""
    rows = [
        DbGenericSystemCost(
            system_type=system_cost.system_type,
            display_name=system_cost.display_name,
            investment_cost_eur=system_cost.investment_cost_eur,
            maintenance_cost_eur_per_year=system_cost.maintenance_cost_eur_per_year,
            lifetime_years=system_cost.lifetime_years,
            is_example_value=system_cost.is_example_value,
        )
        for system_cost in generic_system_costs
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_energy_prices(
    session: Session,
    energy_prices: Iterable[EnergyPrice],
) -> list[DbEnergyPrice]:
    """Speichert oder aktualisiert generische Energiepreise."""
    rows = [
        DbEnergyPrice(
            energy_carrier=energy_price.energy_carrier,
            price_eur_per_kwh=energy_price.price_eur_per_kwh,
            is_example_value=energy_price.is_example_value,
        )
        for energy_price in energy_prices
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_economic_scenarios(
    session: Session,
    economic_scenarios: Iterable[EconomicScenario],
) -> list[DbEconomicScenario]:
    """Speichert oder aktualisiert einfache Wirtschaftlichkeitsszenarien."""
    rows = [
        DbEconomicScenario(
            scenario_key=scenario.scenario_key,
            display_name=scenario.display_name,
            observation_period_years=scenario.observation_period_years,
            heating_energy_carrier=scenario.heating_energy_carrier,
            cooling_energy_carrier=scenario.cooling_energy_carrier,
            default_heating_energy_kwh_per_year=scenario.default_heating_energy_kwh_per_year,
            default_cooling_energy_kwh_per_year=scenario.default_cooling_energy_kwh_per_year,
            is_example_value=scenario.is_example_value,
        )
        for scenario in economic_scenarios
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_variant_cost_results(
    session: Session,
    variant_cost_results: Iterable[VariantCostResult],
) -> list[DbVariantCostResult]:
    """Speichert oder aktualisiert generische Wirtschaftlichkeitsergebnisse."""
    rows = [
        DbVariantCostResult(
            variant_key=result.variant_key,
            scenario_key=result.scenario_key,
            variant_name=result.variant_name,
            selected_system_types=result.selected_system_types,
            investment_cost_eur=result.investment_cost_eur,
            maintenance_cost_eur_per_year=result.maintenance_cost_eur_per_year,
            maintenance_cost_total_eur=result.maintenance_cost_total_eur,
            energy_cost_eur_per_year=result.energy_cost_eur_per_year,
            energy_cost_total_eur=result.energy_cost_total_eur,
            replacement_cost_eur=result.replacement_cost_eur,
            total_cost_eur=result.total_cost_eur,
            observation_period_years=result.observation_period_years,
            heating_energy_kwh_per_year=result.heating_energy_kwh_per_year,
            cooling_energy_kwh_per_year=result.cooling_energy_kwh_per_year,
            uses_simulation_results=result.uses_simulation_results,
            uses_example_energy_values=result.uses_example_energy_values,
            assumption_notes=result.assumption_notes,
        )
        for result in variant_cost_results
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_sources(session: Session, sources: Iterable[Source]) -> list[DbSource]:
    """Speichert oder aktualisiert Quellen."""
    rows = [
        DbSource(
            source_key=source.source_key,
            source_type=source.source_type,
            title=source.title,
            url=source.url,
            citation=source.citation,
            accessed_at=source.accessed_at,
            data_quality=source.data_quality,
        )
        for source in sources
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_documents(session: Session, documents: Iterable[Document]) -> list[DbDocument]:
    """Speichert oder aktualisiert Dokumentreferenzen."""
    rows = [
        DbDocument(
            document_key=document.document_key,
            document_type=document.document_type,
            title=document.title,
            document_path=document.document_path,
            related_key=document.related_key,
            source=document.source,
            data_quality=document.data_quality,
        )
        for document in documents
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_products(session: Session, products: Iterable[Product]) -> list[DbProduct]:
    """Speichert oder aktualisiert Produkte."""
    rows = [
        DbProduct(
            product_key=product.product_key,
            product_type=product.product_type,
            manufacturer=product.manufacturer,
            product_name=product.product_name,
            nominal_power=product.nominal_power,
            price=product.price,
            currency=product.currency,
            gwp_value=product.gwp_value,
            gwp_unit=product.gwp_unit,
            product_url=product.product_url,
            document_path=product.document_path,
            source=product.source,
            data_quality=product.data_quality,
        )
        for product in products
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_product_properties(
    session: Session,
    product_properties: Iterable[ProductProperty],
) -> list[DbProductProperty]:
    """Speichert oder aktualisiert Produkteigenschaften."""
    rows = [
        DbProductProperty(
            product_key=product_property.product_key,
            property_key=product_property.property_key,
            value=product_property.value,
            unit=product_property.unit,
            source=product_property.source,
            data_quality=product_property.data_quality,
        )
        for product_property in product_properties
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_materials(session: Session, materials: Iterable[Material]) -> list[DbMaterial]:
    """Speichert oder aktualisiert Materialien."""
    rows = [
        DbMaterial(
            material_key=material.material_key,
            material_group=material.material_group,
            material_name=material.material_name,
            density=material.density,
            lambda_value=material.lambda_value,
            specific_heat_capacity=material.specific_heat_capacity,
            price=material.price,
            gwp_value=material.gwp_value,
            gwp_unit=material.gwp_unit,
            document_path=material.document_path,
            source=material.source,
            data_quality=material.data_quality,
        )
        for material in materials
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_material_properties(
    session: Session,
    material_properties: Iterable[MaterialProperty],
) -> list[DbMaterialProperty]:
    """Speichert oder aktualisiert Materialeigenschaften."""
    rows = [
        DbMaterialProperty(
            material_key=material_property.material_key,
            property_key=material_property.property_key,
            value=material_property.value,
            unit=material_property.unit,
            source=material_property.source,
            data_quality=material_property.data_quality,
        )
        for material_property in material_properties
    ]
    saved_rows = [session.merge(row) for row in rows]
    session.flush()
    return saved_rows


def save_import_log(
    session: Session,
    *,
    source_name: str,
    status: str,
    message: str = "",
    error_count: int = 0,
    details: dict[str, Any] | None = None,
) -> DbImportLog:
    """Speichert einen Import-Logeintrag."""
    row = DbImportLog(
        source_name=source_name,
        status=status,
        message=message,
        error_count=error_count,
        details=details,
    )
    session.add(row)
    session.flush()
    return row
