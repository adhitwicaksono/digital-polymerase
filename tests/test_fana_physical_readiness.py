from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from digital_polymerase.converters.rna_to_fana import convert_rna_to_fana
from digital_polymerase.core.atoms import clone_atom
from digital_polymerase.core.pdb_io import parse_pdb, sort_residue_keys, write_pdb
from digital_polymerase.physical.fana import audit_fana_physical_readiness


ROOT = Path(__file__).resolve().parents[1]
RNA_INPUTS = ROOT / "benchmarks/ana_fragment_scaling/inputs"
FANA_TEMPLATE = ROOT / "benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb"


def _build_candidate(tmp_path: Path, input_name: str) -> Path:
    candidate = tmp_path / f"{Path(input_name).stem}_fana.pdb"
    convert_rna_to_fana(
        RNA_INPUTS / input_name,
        FANA_TEMPLATE,
        candidate,
        tmp_path / f"{Path(input_name).stem}_conversion.md",
        tmp_path / f"{Path(input_name).stem}_conversion.json",
        strict=True,
    )
    return candidate


@pytest.mark.parametrize(
    ("input_name", "residue_count"),
    [
        ("RNA-8mer.pdb", 8),
        ("RNA-34mer.pdb", 34),
        ("8t5o-HH-typeI-111mer-full.pdb", 111),
    ],
)
def test_fana_level4_geometry_gate_scales(
    tmp_path: Path, input_name: str, residue_count: int
):
    candidate = _build_candidate(tmp_path, input_name)
    report = tmp_path / f"{Path(input_name).stem}_readiness.md"
    manifest = tmp_path / f"{Path(input_name).stem}_readiness.json"

    result = audit_fana_physical_readiness(
        candidate,
        FANA_TEMPLATE,
        report,
        manifest,
        strict=True,
    )

    assert result.geometry_ok
    assert result.geometry_status == "PASS"
    assert result.status == "PARAMETERIZATION_REQUIRED"
    assert result.residue_count == residue_count
    assert result.bond_count > residue_count * 20
    assert result.missing_atoms == []
    assert result.distance_failures == []
    assert len(result.pucker_observations) == residue_count
    assert len(result.chirality_observations) == residue_count
    assert all(item.status == "PASS" for item in result.pucker_observations)
    assert all(item.status == "PASS" for item in result.chirality_observations)
    assert report.exists() and manifest.exists()

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "0.1"
    assert payload["geometry_gate"]["status"] == "PASS"
    assert payload["parameterization"]["status"] == "REQUIRED"
    assert payload["parameterization"]["md_ready"] is False
    assert (
        payload["parameterization"]["suggested_route"]["catalog_sugar_linker_fragment"]
        == "A5L"
    )
    assert len(payload["parameterization"]["blockers"]) == 6


def test_fana_level4_writes_explicit_connectivity_pdb(tmp_path: Path):
    candidate = _build_candidate(tmp_path, "RNA-8mer.pdb")
    conect_pdb = tmp_path / "fana_with_connectivity.pdb"

    result = audit_fana_physical_readiness(
        candidate,
        FANA_TEMPLATE,
        tmp_path / "readiness.md",
        tmp_path / "readiness.json",
        conect_pdb=conect_pdb,
        strict=True,
    )

    assert result.bond_count == 194
    text = conect_pdb.read_text(encoding="utf-8")
    assert "CONECT" in text
    assert "not bond orders" in text
    assert (
        parse_pdb(conect_pdb, strict=True).keys()
        == parse_pdb(candidate, strict=True).keys()
    )


def test_fana_level4_accepts_a_complete_neutral_five_prime_hydroxyl(
    tmp_path: Path,
):
    candidate = _build_candidate(tmp_path, "RNA-8mer.pdb")
    structure = parse_pdb(candidate, strict=True)
    first_key = sort_residue_keys(structure)[0]
    for atom_name in ("P", "OP1", "OP2"):
        del structure[first_key][atom_name]
    normalized = tmp_path / "fana_5oh.pdb"
    write_pdb(structure, normalized)

    result = audit_fana_physical_readiness(
        normalized,
        FANA_TEMPLATE,
        tmp_path / "fana_5oh_readiness.md",
        tmp_path / "fana_5oh_readiness.json",
        strict=True,
    )

    assert result.geometry_ok
    assert result.missing_atoms == []
    assert result.distance_failures == []
    assert result.bond_count == 191
    payload = json.loads(
        (tmp_path / "fana_5oh_readiness.json").read_text(encoding="utf-8")
    )
    segment = payload["topology_handoff"]["chain_segments"][0]
    assert segment["five_prime_phosphorus_present"] is False


def test_fana_level4_rejects_inverted_c2_fluorine_stereochemistry(
    tmp_path: Path,
):
    candidate = _build_candidate(tmp_path, "RNA-8mer.pdb")
    structure = parse_pdb(candidate, strict=True)
    first_key = sort_residue_keys(structure)[0]
    residue = structure[first_key]

    center = residue["C2'"].coords
    c1_vector = residue["C1'"].coords - center
    c3_vector = residue["C3'"].coords - center
    normal = np.cross(c1_vector, c3_vector)
    normal = normal / np.linalg.norm(normal)
    fluorine_vector = residue["F2'"].coords - center
    reflected = fluorine_vector - 2.0 * np.dot(fluorine_vector, normal) * normal
    residue["F2'"] = clone_atom(residue["F2'"], coords=center + reflected)

    inverted = tmp_path / "inverted_fana.pdb"
    write_pdb(structure, inverted)
    result = audit_fana_physical_readiness(
        inverted,
        FANA_TEMPLATE,
        tmp_path / "inverted_readiness.md",
        tmp_path / "inverted_readiness.json",
    )

    assert not result.geometry_ok
    assert result.status == "GEOMETRY_GATE_FAILED"
    assert result.distance_failures == []
    assert sum(item.status == "FAIL" for item in result.chirality_observations) == 1
