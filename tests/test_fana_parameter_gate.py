from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import pytest

from digital_polymerase.converters.rna_to_fana import convert_rna_to_fana
from digital_polymerase.core.errors import ValidationError
from digital_polymerase.core.pdb_io import parse_pdb, residue_name, sort_residue_keys
from digital_polymerase.core.residues import base_of
from digital_polymerase.physical.fana import audit_fana_physical_readiness
from digital_polymerase.physical.fana_parameters import (
    initialize_fana_parameter_manifest,
    prepare_fana_amber_minimization,
)


ROOT = Path(__file__).resolve().parents[1]
RNA_INPUT = ROOT / "benchmarks/ana_fragment_scaling/inputs/RNA-8mer.pdb"
FANA_TEMPLATE = ROOT / "benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_gate_inputs(tmp_path: Path) -> tuple[Path, Path]:
    candidate = tmp_path / "candidate_fana.pdb"
    convert_rna_to_fana(
        RNA_INPUT,
        FANA_TEMPLATE,
        candidate,
        tmp_path / "conversion.md",
        tmp_path / "conversion.json",
        strict=True,
    )
    readiness = tmp_path / "fana_readiness.json"
    audit_fana_physical_readiness(
        candidate,
        FANA_TEMPLATE,
        tmp_path / "fana_readiness.md",
        readiness,
        strict=True,
    )
    return candidate, readiness


def _approved_fixture_manifest(
    tmp_path: Path, candidate: Path, readiness: Path
) -> Path:
    manifest_path = tmp_path / "fana_parameters.json"
    initialize_fana_parameter_manifest(candidate, readiness, manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parameterization = manifest["parameterization"]

    parameterization["parent_force_field"] = {
        "name": "OL15 test fixture",
        "version": "synthetic-test-only",
        "leaprc": "leaprc.DNA.OL15",
    }
    generator = parameterization["generator"]
    generator["version"] = "synthetic-test-only"
    generator["command"] = "modxna.sh synthetic test fixture"
    for base, fragments in generator["fragments_by_base"].items():
        fragments["backbone"] = "DPO"
        fragments["base"] = f"D{base}B"

    code_by_base = {"A": "FAA", "C": "FCC", "G": "FGG", "U": "FUU"}
    for source_name, mapping in parameterization["residue_mappings"].items():
        mapping["internal_name"] = code_by_base[base_of(source_name)]

    structure = parse_pdb(candidate, strict=True)
    keys = sort_residue_keys(structure)
    first_code = f"5{base_of(residue_name(structure[keys[0]]))}F"
    last_code = f"3{base_of(residue_name(structure[keys[-1]]))}F"
    terminal = parameterization["terminal_states"][0]
    terminal["five_prime"] = {
        "chemistry": "5'-phosphate",
        "residue_name": first_code,
        "resolved": True,
    }
    terminal["three_prime"] = {
        "chemistry": "3'-hydroxyl",
        "residue_name": last_code,
        "resolved": True,
    }

    parameter_dir = tmp_path / "params"
    parameter_dir.mkdir()
    frcmod = parameter_dir / "fana.frcmod"
    frcmod.write_text("SYNTHETIC TEST FIXTURE; NOT A FORCE FIELD\n", encoding="utf-8")
    library = parameter_dir / "fana.lib"
    library_names = {*code_by_base.values(), first_code, last_code}
    library.write_text(
        "\n".join(f"!entry.{name}.unit.atoms table" for name in sorted(library_names))
        + "\n",
        encoding="utf-8",
    )
    parameterization["artifacts"] = [
        {
            "role": "frcmod",
            "path": "params/fana.frcmod",
            "sha256": _sha256(frcmod),
        },
        {
            "role": "residue_library",
            "path": "params/fana.lib",
            "sha256": _sha256(library),
        },
    ]
    parameterization["coverage"] = {
        field: True for field in parameterization["coverage"]
    }
    parameterization["charge_model"] = {
        "method": "RESP synthetic test fixture",
        "quantum_method": "HF/6-31G* synthetic test fixture",
        "expected_total_charge": -8,
        "validated": True,
    }
    parameterization["review"] = {
        "status": "approved",
        "reviewer": "Synthetic test fixture",
        "reviewed_on": date.today().isoformat(),
        "evidence": ["tests/test_fana_parameter_gate.py"],
        "notes": "Exercises structural validation only; not scientific approval.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def test_initialize_fana_parameter_manifest_is_candidate_specific_and_blocked(
    tmp_path: Path,
):
    candidate, readiness = _build_gate_inputs(tmp_path)
    manifest_path = tmp_path / "fana_parameters.json"

    initialize_fana_parameter_manifest(candidate, readiness, manifest_path)

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    parameterization = payload["parameterization"]
    assert payload["schema_version"] == "0.1"
    assert payload["target"] == "FANA"
    assert payload["candidate_sha256"] == _sha256(candidate)
    assert payload["readiness_manifest_sha256"] == _sha256(readiness)
    assert parameterization["artifacts"] == []
    assert not any(parameterization["coverage"].values())
    assert all(
        item["sugar_linker"] == "A5L"
        for item in parameterization["generator"]["fragments_by_base"].values()
    )
    assert all(
        not terminal[end]["resolved"]
        for terminal in parameterization["terminal_states"]
        for end in ("five_prime", "three_prime")
    )


def test_unresolved_manifest_blocks_bundle_generation(tmp_path: Path):
    candidate, readiness = _build_gate_inputs(tmp_path)
    manifest_path = tmp_path / "fana_parameters.json"
    initialize_fana_parameter_manifest(candidate, readiness, manifest_path)

    result = prepare_fana_amber_minimization(
        candidate,
        readiness,
        manifest_path,
        tmp_path / "blocked_bundle",
    )

    assert result.status == "BLOCKED"
    assert not result.ready
    assert result.issues
    assert not (result.output_dir / "tleap.in").exists()
    assert not (result.output_dir / "run_minimization.sh").exists()
    preflight = json.loads(
        (result.output_dir / "parameter_preflight.json").read_text(encoding="utf-8")
    )
    assert preflight["status"] == "BLOCKED"
    assert preflight["executed"] is False


def test_approved_manifest_prepares_but_does_not_execute_amber(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    candidate, readiness = _build_gate_inputs(tmp_path)
    manifest_path = _approved_fixture_manifest(tmp_path, candidate, readiness)
    output_dir = tmp_path / "prepared_bundle"
    monkeypatch.setattr(
        "digital_polymerase.physical.fana_parameters.shutil.which",
        lambda _command: None,
    )

    result = prepare_fana_amber_minimization(
        candidate,
        readiness,
        manifest_path,
        output_dir,
        strict=True,
    )

    assert result.status == "PREPARED_NOT_EXECUTED"
    assert result.ready
    assert result.issues == []
    assert len(result.warnings) == 3
    assert all("unavailable" in warning for warning in result.warnings)
    for name in (
        "candidate_amber_names.pdb",
        "tleap.in",
        "minimize_stage1.in",
        "minimize_stage2.in",
        "run_minimization.sh",
        "PREPARATION_README.md",
        "parameter_manifest.snapshot.json",
        "readiness_manifest.snapshot.json",
        "parameter_preflight.json",
        "parameter_preflight.md",
    ):
        assert (output_dir / name).is_file()
    assert (output_dir / "parameters/fana.frcmod").is_file()
    assert (output_dir / "parameters/fana.lib").is_file()
    assert (output_dir / "run_minimization.sh").stat().st_mode & 0o111 == 0
    assert not (output_dir / "fana_system.prmtop").exists()
    assert not (output_dir / "minimize_stage1.out").exists()

    renamed = parse_pdb(output_dir / "candidate_amber_names.pdb", strict=True)
    renamed_keys = sort_residue_keys(renamed)
    assert residue_name(renamed[renamed_keys[0]]).startswith("5")
    assert residue_name(renamed[renamed_keys[-1]]).startswith("3")
    leap_text = (output_dir / "tleap.in").read_text(encoding="utf-8")
    assert "source leaprc.DNA.OL15" in leap_text
    assert 'loadAmberParams "parameters/fana.frcmod"' in leap_text
    assert 'loadoff "parameters/fana.lib"' in leap_text
    assert "solvateOct fana OPCBOX 10.000" in leap_text
    assert "addIons fana Na+ 0" in leap_text
    preflight = json.loads(
        (output_dir / "parameter_preflight.json").read_text(encoding="utf-8")
    )
    assert preflight["status"] == "PREPARED_NOT_EXECUTED"
    assert preflight["executed"] is False


def test_tampered_parameter_artifact_blocks_strict_preparation(tmp_path: Path):
    candidate, readiness = _build_gate_inputs(tmp_path)
    manifest_path = _approved_fixture_manifest(tmp_path, candidate, readiness)
    (tmp_path / "params/fana.frcmod").write_text(
        "TAMPERED AFTER MANIFEST HASH\n", encoding="utf-8"
    )
    output_dir = tmp_path / "tampered_bundle"

    with pytest.raises(ValidationError, match="SHA-256 mismatch"):
        prepare_fana_amber_minimization(
            candidate,
            readiness,
            manifest_path,
            output_dir,
            strict=True,
        )

    assert not (output_dir / "tleap.in").exists()
    preflight = json.loads(
        (output_dir / "parameter_preflight.json").read_text(encoding="utf-8")
    )
    assert preflight["status"] == "BLOCKED"
    assert any("SHA-256 mismatch" in issue for issue in preflight["issues"])


def test_preflight_refuses_to_overwrite_an_input_manifest(tmp_path: Path):
    candidate, readiness = _build_gate_inputs(tmp_path)
    manifest_path = tmp_path / "parameter_preflight.json"
    initialize_fana_parameter_manifest(candidate, readiness, manifest_path)
    original_hash = _sha256(manifest_path)

    with pytest.raises(ValidationError, match="would overwrite an input"):
        prepare_fana_amber_minimization(
            candidate,
            readiness,
            manifest_path,
            tmp_path,
        )

    assert _sha256(manifest_path) == original_hash
