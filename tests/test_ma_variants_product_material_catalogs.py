import csv

from ma_variants.document_catalog import import_documents
from ma_variants.material_catalog import import_materials
from ma_variants.product_catalog import import_products
from ma_variants.source_catalog import import_sources


def test_import_products_loads_example_catalog():
    result = import_products("config/ma_variants/products/example_products.yaml")

    assert result.errors == []
    assert [product.product_key for product in result.products] == [
        "example_heat_pump_01",
        "example_pv_module_01",
    ]
    assert result.products[0].nominal_power == 25
    assert result.products[0].document_path == "data/catalogs/documents/products/example_heat_pump_01_datasheet.pdf"
    assert [property_.property_key for property_ in result.product_properties] == ["scop", "module_area_m2"]


def test_import_products_reports_duplicates_and_invalid_values(tmp_path):
    config_path = tmp_path / "invalid_products.yaml"
    config_path.write_text(
        """
products:
  - product_key: product_a
    product_type: heating
    manufacturer: Beispiel
    product_name: Produkt A
    nominal_power: 10
    price: 1000
    currency: EUR
    gwp_value: 100
    gwp_unit: kgCO2e/unit
    product_url: https://example.invalid/product_a
    document_path: data/catalogs/documents/products/product_a.pdf
    source: source_a
    data_quality: example
  - product_key: product_a
    product_type: heating
    manufacturer: Beispiel
    product_name: Produkt A Kopie
    nominal_power: 10
    price: 1200
    currency: EUR
    gwp_value: 120
    gwp_unit: kgCO2e/unit
    product_url: https://example.invalid/product_a_copy
    document_path: data/catalogs/documents/products/product_a_copy.pdf
    source: source_a
    data_quality: example
  - product_key: product_b
    product_type: cooling
    manufacturer: Beispiel
    product_name: Produkt B
    nominal_power: 12
    price: -5
    currency: EUR
    gwp_value: 90
    gwp_unit: kgCO2e/unit
    product_url: https://example.invalid/product_b
    document_path: data/catalogs/documents/products/product_b.pdf
    source: source_a
    data_quality: example
""",
        encoding="utf-8",
    )

    result = import_products(config_path)

    assert any("Doppelter product_key 'product_a'" in error for error in result.errors)
    assert any("Product.price darf nicht negativ sein" in error for error in result.errors)


def test_import_materials_loads_example_catalog():
    result = import_materials("config/ma_variants/materials/example_materials.yaml")

    assert result.errors == []
    assert [material.material_key for material in result.materials] == [
        "example_insulation_01",
        "example_concrete_01",
    ]
    assert result.materials[0].lambda_value == 0.035
    assert result.materials[0].document_path == "data/catalogs/documents/materials/example_insulation_01_datasheet.pdf"
    assert [property_.property_key for property_ in result.material_properties] == [
        "fire_class",
        "compressive_strength_mpa",
    ]


def test_import_materials_supports_csv(tmp_path):
    csv_path = tmp_path / "materials.csv"
    fieldnames = [
        "material_key",
        "material_group",
        "material_name",
        "density",
        "lambda_value",
        "specific_heat_capacity",
        "price",
        "gwp_value",
        "gwp_unit",
        "document_path",
        "source",
        "data_quality",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "material_key": "csv_material_01",
                "material_group": "insulation",
                "material_name": "CSV Daemmung",
                "density": "40",
                "lambda_value": "0.04",
                "specific_heat_capacity": "900",
                "price": "20",
                "gwp_value": "1.5",
                "gwp_unit": "kgCO2e/kg",
                "document_path": "data/catalogs/documents/materials/csv_material_01.pdf",
                "source": "csv_source",
                "data_quality": "example",
            }
        )

    result = import_materials(csv_path)

    assert result.errors == []
    assert result.materials[0].material_key == "csv_material_01"
    assert result.materials[0].density == 40


def test_import_sources_and_documents_load_example_catalogs():
    source_result = import_sources("config/ma_variants/sources/example_sources.yaml")
    document_result = import_documents("config/ma_variants/documents/example_documents.yaml")

    assert source_result.errors == []
    assert document_result.errors == []
    assert [source.source_key for source in source_result.sources] == [
        "example_product_source",
        "example_material_source",
    ]
    assert document_result.documents[0].document_path.startswith("data/catalogs/documents/products/")
