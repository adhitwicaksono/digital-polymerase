from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from digital_polymerase.converters.rna_to_fana import convert_rna_to_fana
from digital_polymerase.core.errors import TemplateError, UnsupportedResidueError
from digital_polymerase.core.pdb_io import parse_pdb, sort_residue_keys
from digital_polymerase.core.residues import source_sequence


ROOT = Path(__file__).resolve().parents[1]
RNA_INPUTS = ROOT / "benchmarks/ana_fragment_scaling/inputs"
RNA_8MER = RNA_INPUTS / "RNA-8mer.pdb"
FANA_TEMPLATE = ROOT / "benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb"


@pytest.mark.parametrize(
    (
        "input_name",
        "residue_count",
        "expected_mean_rmsd",
        "expected_max_rmsd",
        "expected_mean_c2f",
    ),
    [
        ("RNA-8mer.pdb", 8, 0.0477, 0.0726, 1.3822),
        ("RNA-34mer.pdb", 34, 0.0535, 0.0939, 1.3822),
        ("8t5o-HH-typeI-111mer-full.pdb", 111, 0.0520, 0.0955, 1.3823),
    ],
)
def test_fana_converter_regression(
    tmp_path,
    input_name,
    residue_count,
    expected_mean_rmsd,
    expected_max_rmsd,
    expected_mean_c2f,
):
    source_path = RNA_INPUTS / input_name
    output = tmp_path / "converted_fana.pdb"
    report = tmp_path / "conversion_report.md"
    metrics = tmp_path / "metrics.json"

    result = convert_rna_to_fana(
        source_path,
        FANA_TEMPLATE,
        output,
        report,
        metrics,
        strict=True,
    )

    assert result.ok
    assert result.residue_count == residue_count
    assert output.exists() and report.exists() and metrics.exists()
    assert result.metadata["mean_anchor_rmsd"] == pytest.approx(
        expected_mean_rmsd, abs=1e-4
    )
    assert result.metadata["max_anchor_rmsd"] == pytest.approx(
        expected_max_rmsd, abs=1e-4
    )
    assert result.metadata["mean_c2f_distance"] == pytest.approx(
        expected_mean_c2f, abs=1e-4
    )

    source = parse_pdb(source_path, strict=True)
    converted = parse_pdb(output, strict=True)
    assert result.sequence == source_sequence(source)
    assert source_sequence(converted) == source_sequence(source)

    for key in sort_residue_keys(converted):
        residue = converted[key]
        assert "C2'" in residue
        assert "F2'" in residue
        assert "O2'" not in residue
        assert np.allclose(residue["C1'"].coords, source[key]["C1'"].coords)

    payload = json.loads(metrics.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "0.1"
    assert payload["status"] == "success"
    assert payload["validation"]["required_atoms"]["status"] == "PASS"
    assert payload["validation"]["C2'→F2'"]["status"] == "PASS"


def test_fana_converter_rejects_template_without_fluorine(tmp_path):
    broken_template = tmp_path / "template_without_fluorine.pdb"
    lines = FANA_TEMPLATE.read_text(encoding="utf-8").splitlines()
    broken_template.write_text(
        "\n".join(
            line
            for line in lines
            if not (
                line.startswith(("ATOM", "HETATM"))
                and (
                    line[12:16].strip().upper().startswith("F")
                    or line[76:78].strip().upper() == "F"
                )
            )
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(TemplateError, match="fluorine"):
        convert_rna_to_fana(
            RNA_8MER,
            broken_template,
            tmp_path / "output.pdb",
            tmp_path / "report.md",
        )


def test_fana_converter_rejects_unrecognized_nucleic_acid_residue(tmp_path):
    modified_source = tmp_path / "modified_rna.pdb"
    lines = RNA_8MER.read_text(encoding="utf-8").splitlines()
    first_residue_number = next(
        line[22:26] for line in lines if line.startswith(("ATOM", "HETATM"))
    )
    modified = []
    for line in lines:
        if line.startswith(("ATOM", "HETATM")) and line[22:26] == first_residue_number:
            line = f"{line[:17]}PSU{line[20:]}"
        modified.append(line)
    modified_source.write_text("\n".join(modified) + "\n", encoding="utf-8")

    with pytest.raises(UnsupportedResidueError, match="would be dropped"):
        convert_rna_to_fana(
            modified_source,
            FANA_TEMPLATE,
            tmp_path / "output.pdb",
            tmp_path / "report.md",
        )
