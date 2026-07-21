"""Tests fuer die lokale, bewusst schmale IFC-Lite-Ableitung."""

from __future__ import annotations

import json

import pytest
import yaml

from ma_building.ifc_lite_import import (
    authorize_user_owned_ifc_lite_derivation,
    derive_ifc_lite_building_candidate,
)


def test_derives_storey_and_space_quantities_into_local_candidate(tmp_path) -> None:
    source = tmp_path / "small.ifc"
    source.write_text(
        """ISO-10303-21;
HEADER;
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPROJECT('project',#2,'Projekt',$,$,$,$,$,$);
#3=IFCBUILDING('building',#2,'Gebaeude',$,$,$,$,$,.ELEMENT.,$,$,$);
#4=IFCBUILDINGSTOREY('storey',#2,'EG',$,$,$,$,$,.ELEMENT.,0.);
#5=IFCSPACE('space',#2,'Buero',$,$,$,$,$,.ELEMENT.,.INTERNAL.,$);
#6=IFCELEMENTQUANTITY('quantities',#2,'BaseQuantities',$,$,(#7,#8));
#7=IFCQUANTITYAREA('NetFloorArea',$,$,20.0,$);
#8=IFCQUANTITYVOLUME('NetVolume',$,$,60.0,$);
#9=IFCRELAGGREGATES('building_storey',#2,$,$,#3,(#4));
#10=IFCRELAGGREGATES('storey_space',#2,$,$,#4,(#5));
#11=IFCRELDEFINESBYPROPERTIES('space_quantities',#2,$,$,(#5),#6);
ENDSEC;
END-ISO-10303-21;
""",
        encoding="utf-8",
    )
    output = tmp_path / "derived"

    decision = authorize_user_owned_ifc_lite_derivation(source, confirmation_reference="TEST-IFC-OWNED-001")
    summary = derive_ifc_lite_building_candidate(source, output, compliance_decision=decision)

    candidate = yaml.safe_load((output / "smalloffice_ifc_lite_building_candidate.yaml").read_text(encoding="utf-8"))
    report = json.loads((output / "smalloffice_ifc_lite_gap_report.json").read_text(encoding="utf-8"))
    assert summary.ifc_schema == "IFC2X3"
    assert summary.usable_space_count == 1
    assert candidate["spaces"] == [
        {
            "space_id": "SPACE-IFC-000005",
            "name": "Buero",
            "storey_id": "STOREY-IFC-000004",
            "floor_area_m2": 20.0,
            "volume_m3": 60.0,
            "source_entity_id": 5,
        }
    ]
    assert candidate["storeys"][0]["height_m"] == 3.0
    assert {gap["location"] for gap in report["gaps"]} >= {"elements", "simple_envelope", "zones", "technical"}


def test_blocks_ifc_lite_derivation_without_a_local_decision(tmp_path) -> None:
    source = tmp_path / "small.ifc"
    source.write_text("ISO-10303-21;", encoding="utf-8")

    with pytest.raises(PermissionError, match="Compliance-UNKNOWN"):
        derive_ifc_lite_building_candidate(source, tmp_path / "derived")
