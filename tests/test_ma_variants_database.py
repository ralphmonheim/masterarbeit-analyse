from dataclasses import replace

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from ma_variants.database import (
    Base,
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
    build_database_url_from_env,
    load_database_settings,
    save_dependency_rules,
    save_documents,
    save_economic_scenarios,
    save_energy_prices,
    save_generated_variants,
    save_generic_system_costs,
    save_import_log,
    save_material_properties,
    save_materials,
    save_option_sets,
    save_option_values,
    save_parameters,
    save_product_properties,
    save_products,
    save_sources,
    save_system_template_values,
    save_system_templates,
    save_variant_cost_results,
)
from ma_variants.document_catalog import import_documents
from ma_variants.economic_analysis import calculate_variant_costs, import_economic_assumptions
from ma_variants.importing.catalog import import_catalog
from ma_variants.material_catalog import import_materials
from ma_variants.product_catalog import import_products
from ma_variants.source_catalog import import_sources
from ma_variants.system_catalog import import_system_catalog
from ma_variants.variant_manager import generate_variants


def _session_factory():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


def _load_example_catalog(tmp_path):
    return import_catalog(
        "config/ma_variants/parameters/example_parameters.yaml",
        "config/ma_variants/options/example_options.yaml",
        report_path=tmp_path / "import_report.json",
    )


def test_database_url_uses_explicit_environment_url():
    url = "postgresql+psycopg://user:secret@localhost:5432/ma_variants"

    settings = load_database_settings({"MA_VARIANTS_DATABASE_URL": url, "MA_VARIANTS_DB_ECHO": "true"})

    assert settings.url == url
    assert settings.echo is True


def test_database_url_is_built_from_environment_parts():
    url = build_database_url_from_env(
        {
            "MA_VARIANTS_DB_DIALECT": "postgresql+psycopg",
            "MA_VARIANTS_DB_HOST": "db.local",
            "MA_VARIANTS_DB_PORT": "5544",
            "MA_VARIANTS_DB_NAME": "ma variants",
            "MA_VARIANTS_DB_USER": "project user",
            "MA_VARIANTS_DB_PASSWORD": "secret pass",
        }
    )

    assert url == "postgresql+psycopg://project%20user:secret%20pass@db.local:5544/ma%20variants"


def test_repository_saves_catalog_variants_and_import_log(tmp_path):
    catalog = _load_example_catalog(tmp_path)
    system_catalog = import_system_catalog("config/ma_variants/systems/example_system_templates.yaml")
    economic_assumptions, economic_errors = import_economic_assumptions(
        "config/ma_variants/economic/example_economic_assumptions.yaml"
    )
    assert economic_errors == []
    generated_variants = generate_variants(catalog.parameters, catalog.option_values)[:2]
    variant_cost_result = calculate_variant_costs(
        variant=generated_variants[0][0],
        assumptions=economic_assumptions,
        selected_system_types=["heating", "cooling"],
    )
    Session = _session_factory()

    with Session.begin() as session:
        save_option_sets(session, catalog.option_sets)
        save_parameters(session, catalog.parameters)
        save_option_values(session, catalog.option_values)
        save_system_templates(session, system_catalog.system_templates)
        save_system_template_values(session, system_catalog.system_template_values)
        save_dependency_rules(session, system_catalog.dependency_rules)
        save_generic_system_costs(session, economic_assumptions.generic_system_costs)
        save_energy_prices(session, economic_assumptions.energy_prices)
        save_economic_scenarios(session, economic_assumptions.economic_scenarios)
        variant_rows, variant_value_rows = save_generated_variants(session, generated_variants)
        variant_cost_rows = save_variant_cost_results(session, [variant_cost_result])
        import_log = save_import_log(
            session,
            source_name="example_parameters.yaml",
            status="success",
            message="example import",
            error_count=0,
            details={"parameters": len(catalog.parameters)},
        )

        assert len(variant_rows) == 2
        assert len(variant_value_rows) == 6
        assert len(variant_cost_rows) == 1
        assert import_log.id == 1

    with Session() as session:
        assert session.scalar(select(func.count()).select_from(DbOptionSet)) == 3
        assert session.scalar(select(func.count()).select_from(DbParameter)) == 3
        assert session.scalar(select(func.count()).select_from(DbOptionValue)) == 6
        assert session.scalar(select(func.count()).select_from(DbSystemTemplate)) == 4
        assert session.scalar(select(func.count()).select_from(DbSystemTemplateValue)) == 13
        assert session.scalar(select(func.count()).select_from(DbDependencyRule)) == 1
        assert session.scalar(select(func.count()).select_from(DbGenericSystemCost)) == 4
        assert session.scalar(select(func.count()).select_from(DbEnergyPrice)) == 2
        assert session.scalar(select(func.count()).select_from(DbEconomicScenario)) == 1
        assert session.scalar(select(func.count()).select_from(DbVariant)) == 2
        assert session.scalar(select(func.count()).select_from(DbVariantValue)) == 6
        assert session.scalar(select(func.count()).select_from(DbVariantCostResult)) == 1
        assert session.scalar(select(func.count()).select_from(DbImportLog)) == 1

        option_value = session.get(DbOptionValue, "heating_capacity_100")
        assert option_value is not None
        assert option_value.value == 100

        variant_value = session.get(DbVariantValue, ("variant_0001", "heating_capacity_factor"))
        assert variant_value is not None
        assert variant_value.option_key == "heating_capacity_100"

        system_template_value = session.get(DbSystemTemplateValue, ("PV_01", "pv_peak_power_kwp"))
        assert system_template_value is not None
        assert system_template_value.value == 14.4

        variant_cost_result_row = session.get(DbVariantCostResult, ("variant_0001", "example_20y"))
        assert variant_cost_result_row is not None
        assert variant_cost_result_row.selected_system_types == ["heating", "cooling"]


def test_repository_updates_existing_parameter_without_deleting_related_data(tmp_path):
    catalog = _load_example_catalog(tmp_path)
    Session = _session_factory()

    with Session.begin() as session:
        save_option_sets(session, catalog.option_sets)
        save_parameters(session, catalog.parameters)
        updated_parameter = replace(catalog.parameters[0], display_name="Heizleistung angepasst")
        save_parameters(session, [updated_parameter])

    with Session() as session:
        assert session.scalar(select(func.count()).select_from(DbParameter)) == 3
        stored_parameter = session.get(DbParameter, "heating_capacity_factor")
        assert stored_parameter is not None
        assert stored_parameter.display_name == "Heizleistung angepasst"


def test_repository_saves_product_material_document_and_source_catalogs():
    product_catalog = import_products("config/ma_variants/products/example_products.yaml")
    material_catalog = import_materials("config/ma_variants/materials/example_materials.yaml")
    document_catalog = import_documents("config/ma_variants/documents/example_documents.yaml")
    source_catalog = import_sources("config/ma_variants/sources/example_sources.yaml")
    assert product_catalog.errors == []
    assert material_catalog.errors == []
    assert document_catalog.errors == []
    assert source_catalog.errors == []
    Session = _session_factory()

    with Session.begin() as session:
        save_sources(session, source_catalog.sources)
        save_documents(session, document_catalog.documents)
        save_products(session, product_catalog.products)
        save_product_properties(session, product_catalog.product_properties)
        save_materials(session, material_catalog.materials)
        save_material_properties(session, material_catalog.material_properties)

    with Session() as session:
        assert session.scalar(select(func.count()).select_from(DbSource)) == 2
        assert session.scalar(select(func.count()).select_from(DbDocument)) == 2
        assert session.scalar(select(func.count()).select_from(DbProduct)) == 2
        assert session.scalar(select(func.count()).select_from(DbProductProperty)) == 2
        assert session.scalar(select(func.count()).select_from(DbMaterial)) == 2
        assert session.scalar(select(func.count()).select_from(DbMaterialProperty)) == 2

        product = session.get(DbProduct, "example_heat_pump_01")
        assert product is not None
        assert product.document_path == "data/catalogs/documents/products/example_heat_pump_01_datasheet.pdf"

        material_property = session.get(DbMaterialProperty, ("example_concrete_01", "compressive_strength_mpa"))
        assert material_property is not None
        assert material_property.value == 30
