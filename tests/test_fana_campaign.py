from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from digital_polymerase.core.atoms import Atom, clone_atom
from digital_polymerase.core.errors import ValidationError
from digital_polymerase.core.pdb_io import (
    parse_pdb,
    residue_name,
    sort_residue_keys,
    write_pdb,
)
from digital_polymerase.core.residues import base_of, source_sequence
from digital_polymerase.physical.fana_campaign import (
    AUDIT_FAIL_STATUS,
    AUDIT_PASS_STATUS,
    CAMPAIGN_STATUS,
    audit_fana_minimization,
    initialize_fana_minimization_campaign,
    parse_amber_minimization_output,
)


ROOT = Path(__file__).resolve().parents[1]
RNA_INPUT = ROOT / "benchmarks/ana_fragment_scaling/inputs/RNA-8mer.pdb"
FANA_TEMPLATE = ROOT / "benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb"


def _initialize(tmp_path: Path) -> Path:
    campaign = tmp_path / "campaign"
    initialize_fana_minimization_campaign(RNA_INPUT, FANA_TEMPLATE, campaign)
    return campaign


def _approve_synthetic_manifest(campaign: Path) -> dict[str, str]:
    manifest_path = campaign / "fana_parameters.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parameterization = manifest["parameterization"]
    code_by_base = {"A": "FAA", "C": "FCC", "G": "FGG", "U": "FUU"}
    for source_name, mapping in parameterization["residue_mappings"].items():
        mapping["internal_name"] = code_by_base[base_of(source_name)]

    terminal = parameterization["terminal_states"][0]
    terminal["five_prime"] = {
        "chemistry": "synthetic-test-5-prime",
        "residue_name": "5FC",
        "resolved": True,
    }
    terminal["three_prime"] = {
        "chemistry": "synthetic-test-3-prime",
        "residue_name": "3FC",
        "resolved": True,
    }
    parameterization["review"] = {
        "status": "approved",
        "reviewer": "Synthetic test fixture",
        "reviewed_on": "2026-01-01",
        "evidence": ["tests/test_fana_campaign.py"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return code_by_base


def _write_synthetic_minimized(
    campaign: Path,
    code_by_base: dict[str, str],
    *,
    remove_five_prime_atoms: tuple[str, ...] = (),
) -> Path:
    candidate_path = campaign / "candidate/candidate_fana.pdb"
    candidate = parse_pdb(candidate_path, strict=True)
    keys = sort_residue_keys(candidate)
    minimized = {}
    translation = np.asarray([3.0, -2.0, 1.0])
    for index, key in enumerate(keys):
        if index == 0:
            target_name = "5FC"
        elif index == len(keys) - 1:
            target_name = "3FC"
        else:
            target_name = code_by_base[base_of(residue_name(candidate[key]))]
        minimized[key] = {
            atom_name: clone_atom(
                atom,
                res_name=target_name,
                coords=atom.coords + translation,
            )
            for atom_name, atom in candidate[key].items()
            if index != 0 or atom_name not in remove_five_prime_atoms
        }
    water_key = ("Z", 1, "")
    minimized[water_key] = {
        "O": Atom("HETATM", "O", "WAT", "Z", 1, "", np.asarray([0.0, 0.0, 0.0]))
    }
    minimized_path = campaign / "synthetic_minimized.pdb"
    write_pdb(minimized, minimized_path)
    return minimized_path


def _write_amber_output(path: Path, *, energy: str = "-1.2345D+03") -> None:
    path.write_text(
        f"""Synthetic Amber test output
FINAL RESULTS
 NSTEP       ENERGY          RMS            GMAX         NAME    NUMBER
   5000  {energy}     1.2500D-04     2.5000D-03     C2       14
""",
        encoding="utf-8",
    )


def test_initialize_campaign_is_reproducible_and_blocked(tmp_path: Path):
    campaign = tmp_path / "campaign"

    result = initialize_fana_minimization_campaign(RNA_INPUT, FANA_TEMPLATE, campaign)

    source = parse_pdb(RNA_INPUT, strict=True)
    assert result.status == CAMPAIGN_STATUS
    assert result.sequence == source_sequence(source)
    assert result.residue_count == 8
    assert all(path.is_file() for path in result.generated_files)
    payload = json.loads((campaign / "campaign.json").read_text(encoding="utf-8"))
    assert payload["status"] == CAMPAIGN_STATUS
    assert payload["geometry_gate"] == "PASS"
    manifest = json.loads(
        (campaign / "fana_parameters.json").read_text(encoding="utf-8")
    )
    assert manifest["parameterization"]["artifacts"] == []
    assert not any(manifest["parameterization"]["coverage"].values())
    decisions = (campaign / "modxna_fragment_decisions.tsv").read_text(encoding="utf-8")
    assert decisions.count("\tA5L\t") == 4
    assert "EXPERT_DECISION_REQUIRED" in decisions
    assert list((campaign / "parameters").iterdir()) == [
        campaign / "parameters/README.md"
    ]


def test_parse_amber_final_results_and_reject_nonfinite_values(tmp_path: Path):
    valid = tmp_path / "valid.out"
    _write_amber_output(valid)

    result = parse_amber_minimization_output(valid)

    assert result.nstep == 5000
    assert result.energy == pytest.approx(-1234.5)
    assert result.rms_gradient == pytest.approx(1.25e-4)
    assert result.maximum_gradient == pytest.approx(2.5e-3)
    assert result.maximum_gradient_atom == "C2"
    assert result.maximum_gradient_atom_number == 14

    invalid = tmp_path / "invalid.out"
    _write_amber_output(invalid, energy="NaN")
    with pytest.raises(ValidationError, match="fatal marker"):
        parse_amber_minimization_output(invalid)


def test_post_minimization_audit_restores_solute_and_requires_expert_review(
    tmp_path: Path,
):
    campaign = _initialize(tmp_path)
    code_by_base = _approve_synthetic_manifest(campaign)
    minimized = _write_synthetic_minimized(campaign, code_by_base)
    preflight = campaign / "parameter_preflight.json"
    preflight.write_text(
        json.dumps(
            {
                "target": "FANA",
                "status": "PREPARED_NOT_EXECUTED",
                "executed": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    stage1 = campaign / "stage1.out"
    stage2 = campaign / "stage2.out"
    _write_amber_output(stage1, energy="-1.0000D+03")
    _write_amber_output(stage2, energy="-1.1000D+03")

    result = audit_fana_minimization(
        campaign / "candidate/candidate_fana.pdb",
        minimized,
        campaign / "inputs/2KP4_FANA_template.pdb",
        campaign / "fana_parameters.json",
        preflight,
        stage1,
        stage2,
        campaign / "post_audit",
        strict=True,
    )

    assert result.status == AUDIT_PASS_STATUS
    assert result.structurally_passed
    assert result.issues == []
    assert result.geometry_status == "PASS"
    assert result.residue_count == 8
    assert result.heavy_atom_count > 100
    assert result.heavy_atom_rmsd == pytest.approx(0.0, abs=1e-10)
    restored = parse_pdb(
        campaign / "post_audit/restored_minimized_solute.pdb", strict=True
    )
    assert source_sequence(restored) == source_sequence(
        parse_pdb(campaign / "candidate/candidate_fana.pdb", strict=True)
    )
    payload = json.loads(
        (campaign / "post_audit/minimization_audit.json").read_text(encoding="utf-8")
    )
    assert payload["expert_review_required"] is True
    assert payload["executed_by_digital_polymerase"] is False
    assert payload["stage2"]["energy"] == pytest.approx(-1100.0)


def test_post_minimization_audit_honors_terminal_atom_normalization(
    tmp_path: Path,
):
    campaign = _initialize(tmp_path)
    code_by_base = _approve_synthetic_manifest(campaign)
    manifest_path = campaign / "fana_parameters.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["parameterization"]["terminal_states"][0]["five_prime"]["remove_atoms"] = [
        "P",
        "OP1",
        "OP2",
    ]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    minimized = _write_synthetic_minimized(
        campaign,
        code_by_base,
        remove_five_prime_atoms=("P", "OP1", "OP2"),
    )
    preflight = campaign / "parameter_preflight.json"
    preflight.write_text(
        '{"target":"FANA","status":"PREPARED_NOT_EXECUTED","executed":false}\n',
        encoding="utf-8",
    )
    stage1 = campaign / "stage1.out"
    stage2 = campaign / "stage2.out"
    _write_amber_output(stage1)
    _write_amber_output(stage2)

    result = audit_fana_minimization(
        campaign / "candidate/candidate_fana.pdb",
        minimized,
        campaign / "inputs/2KP4_FANA_template.pdb",
        manifest_path,
        preflight,
        stage1,
        stage2,
        campaign / "terminal_audit",
        strict=True,
    )

    assert result.structurally_passed
    assert result.geometry_status == "PASS"
    restored = parse_pdb(
        campaign / "terminal_audit/restored_minimized_solute.pdb", strict=True
    )
    first_key = sort_residue_keys(restored)[0]
    assert not {"P", "OP1", "OP2"}.intersection(restored[first_key])


def test_post_minimization_audit_blocks_bad_amber_output(tmp_path: Path):
    campaign = _initialize(tmp_path)
    code_by_base = _approve_synthetic_manifest(campaign)
    minimized = _write_synthetic_minimized(campaign, code_by_base)
    preflight = campaign / "parameter_preflight.json"
    preflight.write_text(
        '{"target":"FANA","status":"PREPARED_NOT_EXECUTED","executed":false}\n',
        encoding="utf-8",
    )
    stage1 = campaign / "stage1.out"
    stage2 = campaign / "stage2.out"
    _write_amber_output(stage1)
    _write_amber_output(stage2, energy="NaN")

    result = audit_fana_minimization(
        campaign / "candidate/candidate_fana.pdb",
        minimized,
        campaign / "inputs/2KP4_FANA_template.pdb",
        campaign / "fana_parameters.json",
        preflight,
        stage1,
        stage2,
        campaign / "failed_audit",
    )

    assert result.status == AUDIT_FAIL_STATUS
    assert not result.structurally_passed
    assert any(
        "Stage 2" in issue and "fatal marker" in issue for issue in result.issues
    )
    assert (campaign / "failed_audit/minimization_audit.json").is_file()
