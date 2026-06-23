from pathlib import Path

import pytest

from ma_core import ConfigurationSource, load_configuration_file, save_yaml_configuration


def test_yaml_configuration_requires_new_name_on_collision(tmp_path):
    first = save_yaml_configuration(
        {"value": 1},
        target_dir=tmp_path,
        file_name="work.yaml",
    )

    assert first.created is True
    with pytest.raises(FileExistsError, match="anderen neuen Dateinamen"):
        save_yaml_configuration(
            {"value": 2},
            target_dir=tmp_path,
            file_name="work.yaml",
        )


def test_yaml_configuration_overwrites_only_confirmed_custom_source(tmp_path):
    target = tmp_path / "work.yaml"
    target.write_text("value: 1\n", encoding="utf-8")
    source = ConfigurationSource(path=target, is_template=False)

    with pytest.raises(PermissionError, match="bestaetigt"):
        save_yaml_configuration(
            {"value": 2},
            target_dir=tmp_path,
            file_name=target.name,
            source=source,
            overwrite_existing=True,
        )

    result = save_yaml_configuration(
        {"value": 2},
        target_dir=tmp_path,
        file_name=target.name,
        source=source,
        overwrite_existing=True,
        overwrite_confirmed=True,
    )

    assert result.overwritten is True
    assert load_configuration_file(target) == {"value": 2}


def test_yaml_configuration_never_overwrites_template(tmp_path):
    target = tmp_path / "example_template.yaml"
    target.write_text("value: 1\n", encoding="utf-8")

    with pytest.raises(PermissionError, match="Vorlagen"):
        save_yaml_configuration(
            {"value": 2},
            target_dir=tmp_path,
            file_name=target.name,
            source=ConfigurationSource(path=target, is_template=True),
            overwrite_existing=True,
            overwrite_confirmed=True,
        )


@pytest.mark.parametrize("file_name", ["../unsafe.yaml", "folder/unsafe.yaml", r"folder\unsafe.yaml"])
def test_yaml_configuration_rejects_paths(file_name, tmp_path):
    with pytest.raises(ValueError, match="Pfadangaben"):
        save_yaml_configuration(
            {"value": 1},
            target_dir=tmp_path,
            file_name=file_name,
        )


def test_yaml_configuration_adapter_rejects_json_target(tmp_path):
    with pytest.raises(ValueError, match="nur YAML"):
        save_yaml_configuration(
            {"value": 1},
            target_dir=tmp_path,
            file_name="work.json",
        )


def test_configuration_source_uses_path_objects():
    source = ConfigurationSource(path=Path("example.yaml"), is_template=True)

    assert source.path == Path("example.yaml")
