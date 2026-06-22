import importlib
from pathlib import Path

from ma_workflow import list_module_definitions


def _module_documentation_path(module_key: str) -> Path:
    if module_key == "project_documentation":
        return Path("docs/project/README.md")
    return Path("docs").joinpath(*module_key.split("."), "README.md")


def test_all_target_python_packages_are_importable_without_side_effects():
    package_names = [
        module.python_package
        for module in list_module_definitions()
        if module.python_package is not None
    ]

    imported = [importlib.import_module(package_name) for package_name in package_names]

    assert len(imported) == len(package_names)
    assert all(module.__name__ == package_name for module, package_name in zip(imported, package_names, strict=True))


def test_every_module_has_complete_module_documentation():
    required_sections = (
        "Zweck",
        "Eingaben",
        "Ausgaben",
        "Abgrenzung",
        "Abhaengigkeiten",
        "Status",
        "Naechster Schritt",
    )
    missing_docs = [
        module.module_key
        for module in list_module_definitions()
        if not _module_documentation_path(module.module_key).is_file()
    ]
    incomplete_docs = [
        module.module_key
        for module in list_module_definitions()
        if _module_documentation_path(module.module_key).is_file()
        and any(
            section not in _module_documentation_path(module.module_key).read_text(encoding="utf-8")
            for section in required_sections
        )
    ]

    assert missing_docs == []
    assert incomplete_docs == []


def test_ida_ice_adapters_are_explicit_and_importable():
    export_adapter = importlib.import_module("ma_export_simulation.adapters.ida_ice")
    import_adapter = importlib.import_module("ma_import_simulation.adapters.ida_ice")

    assert export_adapter.ADAPTER_KEY == "ida_ice"
    assert import_adapter.ADAPTER_KEY == "ida_ice"
