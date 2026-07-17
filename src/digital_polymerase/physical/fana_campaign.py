"""Controlled FANA minimization campaign preparation and post-run audit.

The campaign initializer builds a reproducible 8-mer (or other supplied RNA)
handoff around the stable FANA converter, Level 4 readiness gate, and external
parameter manifest. The post-run audit consumes Amber outputs but never runs
Amber itself.

Neither a structurally passing audit nor a finite minimization energy proves
that an external force field is scientifically accurate. Final acceptance
remains an explicit expert-review step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from digital_polymerase.converters.rna_to_fana import convert_rna_to_fana
from digital_polymerase.core.atoms import ResidueKey, clone_atom, is_hydrogen
from digital_polymerase.core.errors import ValidationError
from digital_polymerase.core.geometry import kabsch
from digital_polymerase.core.pdb_io import (
    Structure,
    parse_pdb,
    residue_name,
    sort_residue_keys,
    write_pdb,
)
from digital_polymerase.physical.fana import audit_fana_physical_readiness
from digital_polymerase.physical.fana_parameters import (
    initialize_fana_parameter_manifest,
)


SCHEMA_VERSION = "0.1"
TARGET = "FANA"
CAMPAIGN_STATUS = "EXTERNAL_PARAMETERS_REQUIRED"
AUDIT_PASS_STATUS = "STRUCTURAL_PASS_EXPERT_REVIEW_REQUIRED"
AUDIT_FAIL_STATUS = "AUDIT_FAILED"

REFERENCES = (
    "https://doi.org/10.1021/acs.jctc.4c01164",
    "https://doi.org/10.33011/livecoms.6.1.4545",
    "https://modxna.chpc.utah.edu/catalog/",
    "https://modxna.chpc.utah.edu/generate-a-phosphothioate-backbone-residue/",
    "https://ambermd.org/AmberTools.php",
    "https://www.rcsb.org/structure/2KP4",
)


@dataclass(frozen=True)
class AmberFinalResult:
    """Final minimization row parsed from one Amber output file."""

    path: Path
    nstep: int
    energy: float
    rms_gradient: float
    maximum_gradient: float
    maximum_gradient_atom: str | None
    maximum_gradient_atom_number: int | None
    reached_maximum_cycles: bool


@dataclass
class FANACampaignResult:
    """Files produced for a candidate-bound FANA minimization campaign."""

    status: str
    output_dir: Path
    sequence: str
    residue_count: int
    generated_files: list[Path]


@dataclass
class FANAMinimizationAuditResult:
    """Outcome of a non-executing audit of externally produced Amber results."""

    status: str
    output_dir: Path
    issues: list[str]
    warnings: list[str]
    residue_count: int
    heavy_atom_count: int
    heavy_atom_rmsd: float | None
    maximum_heavy_atom_displacement: float | None
    geometry_status: str
    stage1: AmberFinalResult | None
    stage2: AmberFinalResult | None
    generated_files: list[Path]

    @property
    def structurally_passed(self) -> bool:
        return self.status == AUDIT_PASS_STATUS


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read {label} JSON: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must contain a JSON object: {path}")
    return value


def _residue_label(key: ResidueKey) -> str:
    return f"{key[0]}:{key[1]}{key[2] or ''}"


def _consecutive_segments(keys: Sequence[ResidueKey]) -> list[list[ResidueKey]]:
    if not keys:
        return []
    segments: list[list[ResidueKey]] = [[keys[0]]]
    for key in keys[1:]:
        previous = segments[-1][-1]
        if (
            key[0] == previous[0]
            and key[1] == previous[1] + 1
            and not key[2]
            and not previous[2]
        ):
            segments[-1].append(key)
        else:
            segments.append([key])
    return segments


def _ensure_writable_targets(
    targets: Sequence[Path], *, protected: Sequence[Path], overwrite: bool
) -> None:
    protected_resolved = {path.resolve() for path in protected}
    collisions = [path for path in targets if path.resolve() in protected_resolved]
    if collisions:
        raise ValidationError(
            "Campaign output would overwrite an input: "
            + ", ".join(str(path) for path in collisions)
        )
    existing = [path for path in targets if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "Refusing to overwrite existing campaign files: "
            + ", ".join(str(path) for path in existing)
        )


def _campaign_paths(output_dir: Path) -> dict[str, Path]:
    return {
        "source": output_dir / "inputs/source_rna.pdb",
        "template": output_dir / "inputs/2KP4_FANA_template.pdb",
        "candidate": output_dir / "candidate/candidate_fana.pdb",
        "conect": output_dir / "candidate/candidate_fana_conect.pdb",
        "conversion_report": output_dir / "reports/conversion.md",
        "conversion_json": output_dir / "reports/conversion.json",
        "readiness_report": output_dir / "reports/readiness.md",
        "readiness_json": output_dir / "fana_readiness.json",
        "parameters_json": output_dir / "fana_parameters.json",
        "fragment_decisions": output_dir / "modxna_fragment_decisions.tsv",
        "campaign_json": output_dir / "campaign.json",
        "campaign_readme": output_dir / "CAMPAIGN_README.md",
        "parameter_readme": output_dir / "parameters/README.md",
        "minimization_readme": output_dir / "minimization/README.md",
        "post_readme": output_dir / "post_minimization/README.md",
    }


def initialize_fana_minimization_campaign(
    source_rna_pdb: str | Path,
    template_pdb: str | Path,
    output_dir: str | Path,
    *,
    overwrite: bool = False,
) -> FANACampaignResult:
    """Build a reproducible, intentionally blocked FANA campaign directory."""

    source_path = Path(source_rna_pdb)
    template_path = Path(template_pdb)
    destination = Path(output_dir)
    paths = _campaign_paths(destination)
    _ensure_writable_targets(
        list(paths.values()),
        protected=(source_path, template_path),
        overwrite=overwrite,
    )

    paths["source"].parent.mkdir(parents=True, exist_ok=True)
    paths["template"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, paths["source"])
    shutil.copy2(template_path, paths["template"])

    conversion = convert_rna_to_fana(
        paths["source"],
        paths["template"],
        paths["candidate"],
        paths["conversion_report"],
        paths["conversion_json"],
        strict=True,
    )
    readiness = audit_fana_physical_readiness(
        paths["candidate"],
        paths["template"],
        paths["readiness_report"],
        paths["readiness_json"],
        conect_pdb=paths["conect"],
        strict=True,
    )
    initialize_fana_parameter_manifest(
        paths["candidate"], paths["readiness_json"], paths["parameters_json"]
    )

    decision_table = """base\tbackbone_fragment\tsugar_linker\tbase_fragment\tparent_force_field\tstatus\tnote
A\tUNRESOLVED (DPO or RPO)\tA5L\tUNRESOLVED (DAA or RAA)\tUNRESOLVED (OL15/21 or OL3)\tEXPERT_DECISION_REQUIRED\tKeep backbone, base variant, and parent force-field family consistent.
C\tUNRESOLVED (DPO or RPO)\tA5L\tUNRESOLVED (DCC or RCC)\tUNRESOLVED (OL15/21 or OL3)\tEXPERT_DECISION_REQUIRED\tKeep backbone, base variant, and parent force-field family consistent.
G\tUNRESOLVED (DPO or RPO)\tA5L\tUNRESOLVED (DGG or RGG)\tUNRESOLVED (OL15/21 or OL3)\tEXPERT_DECISION_REQUIRED\tKeep backbone, base variant, and parent force-field family consistent.
U\tUNRESOLVED (DPO or RPO)\tA5L\tUNRESOLVED (catalog exposes RUU)\tUNRESOLVED (OL15/21 or OL3)\tEXPERT_DECISION_REQUIRED\tUracil compatibility must be reviewed; do not silently substitute thymine or mix force-field families.
"""
    paths["fragment_decisions"].write_text(decision_table, encoding="utf-8")

    campaign_payload = {
        "schema_version": SCHEMA_VERSION,
        "target": TARGET,
        "stage": "controlled_minimization_campaign",
        "status": CAMPAIGN_STATUS,
        "sequence": conversion.sequence,
        "residue_count": conversion.residue_count,
        "geometry_gate": readiness.geometry_status,
        "inputs": {
            "source_rna": {
                "path": str(paths["source"].relative_to(destination)),
                "sha256": _sha256(paths["source"]),
            },
            "fana_template": {
                "path": str(paths["template"].relative_to(destination)),
                "sha256": _sha256(paths["template"]),
            },
            "candidate": {
                "path": str(paths["candidate"].relative_to(destination)),
                "sha256": _sha256(paths["candidate"]),
            },
            "readiness_manifest": {
                "path": str(paths["readiness_json"].relative_to(destination)),
                "sha256": _sha256(paths["readiness_json"]),
            },
            "parameter_manifest": {
                "path": str(paths["parameters_json"].relative_to(destination)),
                "initial_template_sha256": _sha256(paths["parameters_json"]),
            },
        },
        "external_requirements": [
            "AmberTools with current CPPTRAJ, LEaP, SANDER, and AMBPDB",
            "expert-selected, family-consistent modXNA fragments",
            "generated residue-library and frcmod artifacts",
            "resolved 5-prime and 3-prime terminal residue templates",
            "charge and parameter coverage evidence",
            "named parameter reviewer approval",
        ],
        "references": list(REFERENCES),
    }
    paths["campaign_json"].write_text(
        json.dumps(campaign_payload, indent=2) + "\n", encoding="utf-8"
    )

    paths["parameter_readme"].parent.mkdir(parents=True, exist_ok=True)
    paths["parameter_readme"].write_text(
        """# External parameter artifacts

Place only independently generated and reviewed FANA residue-library and
`frcmod` files here. Record their relative paths as `parameters/<filename>` and
their exact SHA-256 hashes in `../fana_parameters.json`.

This directory intentionally contains no force-field artifacts.
""",
        encoding="utf-8",
    )
    paths["minimization_readme"].parent.mkdir(parents=True, exist_ok=True)
    paths["minimization_readme"].write_text(
        """# Amber minimization bundle destination

Run `digital-polymerase-fana-parameters prepare` only after the external
parameter manifest is complete and reviewed. The preparer will write LEaP and
minimization inputs here without executing them.
""",
        encoding="utf-8",
    )
    paths["post_readme"].parent.mkdir(parents=True, exist_ok=True)
    paths["post_readme"].write_text(
        """# Post-minimization audit destination

After an independently reviewed Amber run, use
`digital-polymerase-fana-campaign audit` to restore FANA residue identities,
parse the final minimization rows, and rerun structural checks here.
""",
        encoding="utf-8",
    )

    campaign_readme = f"""# FANA controlled-minimization campaign

- **Status:** `{CAMPAIGN_STATUS}`
- **Sequence:** `{conversion.sequence}`
- **Residues:** `{conversion.residue_count}`
- **Initial geometry gate:** `{readiness.geometry_status}`

This campaign is candidate-bound and intentionally blocked until real external
parameters and named expert approval are supplied.

## 1. Resolve the chemistry

Review `modxna_fragment_decisions.tsv`. `A5L` is the cataloged FANA
sugar/linker. Do not select `DPO` versus `RPO`, DNA/RNA base variants, the
parent force field, uracil handling, or terminal templates without documenting
the compatibility rationale.

The modXNA input form is one line per residue chemistry:

```text
<backbone fragment> A5L <base fragment>
```

modXNA requires current AmberTools/CPPTRAJ, generates a random three-character
residue name, and does not build 5-prime or 3-prime terminal residues.

## 2. Add reviewed artifacts

Place generated libraries and `frcmod` files in `parameters/`. Complete
`fana_parameters.json`, including exact hashes, residue mappings, terminal
chemistry, charge evidence, coverage, and named review approval.

## 3. Prepare Amber inputs

From this campaign directory:

```bash
digital-polymerase-fana-parameters prepare \\
  --candidate candidate/candidate_fana.pdb \\
  --readiness fana_readiness.json \\
  --parameters fana_parameters.json \\
  --output-dir minimization \\
  --strict
```

Passing status is `PREPARED_NOT_EXECUTED`. Inspect every generated file and all
LEaP messages before manually running `minimization/run_minimization.sh` in an
AmberTools environment.

## 4. Audit the external run

```bash
digital-polymerase-fana-campaign audit \\
  --candidate candidate/candidate_fana.pdb \\
  --minimized minimization/fana_minimized.pdb \\
  --template inputs/2KP4_FANA_template.pdb \\
  --parameters fana_parameters.json \\
  --preflight minimization/parameter_preflight.json \\
  --stage1 minimization/minimize_stage1.out \\
  --stage2 minimization/minimize_stage2.out \\
  --output-dir post_minimization \\
  --strict
```

The strongest automated success status is
`{AUDIT_PASS_STATUS}`. Expert review is still required before dynamics or
before declaring the FANA physical-validation milestone complete.

## References

- modXNA paper: https://doi.org/10.1021/acs.jctc.4c01164
- modified-nucleotide parameterization tutorial:
  https://doi.org/10.33011/livecoms.6.1.4545
- fragment catalog: https://modxna.chpc.utah.edu/catalog/
- modXNA generation tutorial:
  https://modxna.chpc.utah.edu/generate-a-phosphothioate-backbone-residue/
- AmberTools: https://ambermd.org/AmberTools.php
"""
    paths["campaign_readme"].write_text(campaign_readme, encoding="utf-8")
    return FANACampaignResult(
        status=CAMPAIGN_STATUS,
        output_dir=destination,
        sequence=conversion.sequence,
        residue_count=conversion.residue_count,
        generated_files=list(paths.values()),
    )


_FLOAT_PATTERN = re.compile(
    r"^(?:[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?|[-+]?(?:nan|inf))$",
    re.IGNORECASE,
)


def _parse_float_token(value: str) -> float:
    if not _FLOAT_PATTERN.fullmatch(value):
        raise ValueError(value)
    return float(value.replace("D", "E").replace("d", "e"))


def parse_amber_minimization_output(path: str | Path) -> AmberFinalResult:
    """Parse the last Amber ``FINAL RESULTS`` minimization table."""

    output_path = Path(path)
    text = output_path.read_text(encoding="utf-8", errors="replace")
    upper = text.upper()
    fatal_patterns = {
        "NAN": r"\bNAN\b",
        "FATAL": r"\bFATAL\b",
        "ERROR:": r"\bERROR\s*:",
        "ABNORMAL TERMINATION": r"\bABNORMAL TERMINATION\b",
    }
    fatal_markers = [
        label
        for label, pattern in fatal_patterns.items()
        if re.search(pattern, upper) is not None
    ]
    if fatal_markers:
        raise ValidationError(
            f"Amber output {output_path} contains fatal marker(s): "
            + ", ".join(fatal_markers)
        )

    lines = text.splitlines()
    headers = [
        index
        for index, line in enumerate(lines)
        if all(token in line.upper() for token in ("NSTEP", "ENERGY", "RMS", "GMAX"))
    ]
    for header_index in reversed(headers):
        for line in lines[header_index + 1 : header_index + 9]:
            tokens = line.split()
            if len(tokens) < 4:
                continue
            try:
                nstep_value = _parse_float_token(tokens[0])
                energy = _parse_float_token(tokens[1])
                rms_gradient = _parse_float_token(tokens[2])
                maximum_gradient = _parse_float_token(tokens[3])
            except ValueError:
                continue
            if not nstep_value.is_integer():
                continue
            values = (energy, rms_gradient, maximum_gradient)
            if not all(math.isfinite(value) for value in values):
                raise ValidationError(
                    f"Amber output {output_path} has non-finite final results."
                )
            atom_name = tokens[4] if len(tokens) >= 5 else None
            atom_number: int | None = None
            if len(tokens) >= 6:
                try:
                    atom_number = int(tokens[5])
                except ValueError:
                    atom_number = None
            return AmberFinalResult(
                path=output_path,
                nstep=int(nstep_value),
                energy=energy,
                rms_gradient=rms_gradient,
                maximum_gradient=maximum_gradient,
                maximum_gradient_atom=atom_name,
                maximum_gradient_atom_number=atom_number,
                reached_maximum_cycles=(
                    "MAXIMUM NUMBER OF MINIMIZATION CYCLES REACHED" in upper
                ),
            )
    raise ValidationError(
        f"Could not find a finite Amber FINAL RESULTS minimization row in {output_path}."
    )


def _expected_amber_names(
    candidate: Structure,
    parameterization: Mapping[str, Any],
    issues: list[str],
) -> list[str]:
    mappings = parameterization.get("residue_mappings")
    states = parameterization.get("terminal_states")
    if not isinstance(mappings, dict) or not isinstance(states, list):
        issues.append("Parameter manifest lacks residue mappings or terminal states.")
        return []

    terminal_by_segment: dict[tuple[str, str], tuple[str, str]] = {}
    for state in states:
        if not isinstance(state, dict):
            continue
        pair = (str(state.get("first_residue", "")), str(state.get("last_residue", "")))
        five = state.get("five_prime")
        three = state.get("three_prime")
        if isinstance(five, dict) and isinstance(three, dict):
            five_name = five.get("residue_name")
            three_name = three.get("residue_name")
            if isinstance(five_name, str) and isinstance(three_name, str):
                terminal_by_segment[pair] = (five_name, three_name)

    expected_by_key: dict[ResidueKey, str] = {}
    for segment in _consecutive_segments(sort_residue_keys(candidate)):
        pair = (_residue_label(segment[0]), _residue_label(segment[-1]))
        terminal = terminal_by_segment.get(pair)
        if terminal is None:
            issues.append(
                f"No resolved terminal mapping for segment {pair[0]}–{pair[1]}."
            )
            continue
        if len(segment) == 1:
            issues.append(
                "Single-residue segments are unsupported in the campaign audit."
            )
            continue
        expected_by_key[segment[0]] = terminal[0]
        expected_by_key[segment[-1]] = terminal[1]

    names: list[str] = []
    for key in sort_residue_keys(candidate):
        if key in expected_by_key:
            names.append(expected_by_key[key])
            continue
        source_name = residue_name(candidate[key])
        mapping = mappings.get(source_name)
        internal_name = (
            mapping.get("internal_name") if isinstance(mapping, dict) else None
        )
        if not isinstance(internal_name, str):
            issues.append(f"No internal Amber residue mapping for {source_name}.")
            names.append("")
        else:
            names.append(internal_name)
    return names


def _restore_minimized_polymer(
    *,
    candidate: Structure,
    minimized: Structure,
    expected_amber_names: Sequence[str],
    issues: list[str],
) -> Structure:
    allowed = set(expected_amber_names)
    minimized_polymer_keys = [
        key
        for key in sort_residue_keys(minimized)
        if residue_name(minimized[key]) in allowed
    ]
    candidate_keys = sort_residue_keys(candidate)
    if len(minimized_polymer_keys) != len(candidate_keys):
        issues.append(
            "Minimized PDB contains "
            f"{len(minimized_polymer_keys)} recognized FANA residues; expected "
            f"{len(candidate_keys)}."
        )
        return {}

    restored: Structure = {}
    for index, (candidate_key, minimized_key) in enumerate(
        zip(candidate_keys, minimized_polymer_keys)
    ):
        actual_name = residue_name(minimized[minimized_key])
        expected_name = expected_amber_names[index]
        if actual_name != expected_name:
            issues.append(
                f"Minimized residue {index + 1} is {actual_name}; expected {expected_name}."
            )
        missing_atoms = sorted(
            set(candidate[candidate_key]) - set(minimized[minimized_key])
        )
        if missing_atoms:
            issues.append(
                f"Minimized residue {index + 1} lacks candidate atoms: "
                + ", ".join(missing_atoms)
            )
        source_name = residue_name(candidate[candidate_key])
        restored[candidate_key] = {
            atom_name: clone_atom(
                atom,
                res_name=source_name,
                chain=candidate_key[0],
                res_num=candidate_key[1],
                insertion_code=candidate_key[2],
            )
            for atom_name, atom in minimized[minimized_key].items()
        }
    return restored


def _heavy_atom_displacements(
    candidate: Structure, restored: Structure
) -> tuple[int, float, float]:
    reference_coordinates: list[np.ndarray] = []
    minimized_coordinates: list[np.ndarray] = []
    for key in sort_residue_keys(candidate):
        for atom_name, atom in candidate[key].items():
            if is_hydrogen(atom):
                continue
            reference_coordinates.append(atom.coords)
            minimized_coordinates.append(restored[key][atom_name].coords)
    if len(reference_coordinates) < 3:
        raise ValidationError(
            "At least three common heavy atoms are required for RMSD."
        )
    reference = np.asarray(reference_coordinates, dtype=float)
    minimized = np.asarray(minimized_coordinates, dtype=float)
    rotation, translation, fitted_rmsd = kabsch(minimized, reference)
    fitted = (rotation @ minimized.T).T + translation
    displacement = np.linalg.norm(fitted - reference, axis=1)
    return len(reference_coordinates), fitted_rmsd, float(np.max(displacement))


def _stage_payload(result: AmberFinalResult | None) -> dict[str, Any] | None:
    if result is None:
        return None
    payload = asdict(result)
    payload["path"] = str(result.path)
    payload["sha256"] = _sha256(result.path)
    return payload


def _write_audit_outputs(
    *,
    result: FANAMinimizationAuditResult,
    report_path: Path,
    json_path: Path,
    candidate_path: Path,
    minimized_path: Path,
    template_path: Path,
    parameter_path: Path,
    preflight_path: Path,
    max_heavy_atom_rmsd: float,
) -> None:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "target": TARGET,
        "stage": "post_minimization_audit",
        "status": result.status,
        "issues": result.issues,
        "warnings": result.warnings,
        "residue_count": result.residue_count,
        "heavy_atom_count": result.heavy_atom_count,
        "heavy_atom_rmsd": result.heavy_atom_rmsd,
        "maximum_heavy_atom_displacement": result.maximum_heavy_atom_displacement,
        "maximum_allowed_heavy_atom_rmsd": max_heavy_atom_rmsd,
        "geometry_status": result.geometry_status,
        "stage1": _stage_payload(result.stage1),
        "stage2": _stage_payload(result.stage2),
        "expert_review_required": True,
        "executed_by_digital_polymerase": False,
        "inputs": {
            "candidate": {
                "path": str(candidate_path),
                "sha256": _sha256(candidate_path),
            },
            "minimized": {
                "path": str(minimized_path),
                "sha256": _sha256(minimized_path),
            },
            "template": {
                "path": str(template_path),
                "sha256": _sha256(template_path),
            },
            "parameter_manifest": {
                "path": str(parameter_path),
                "sha256": _sha256(parameter_path),
            },
            "parameter_preflight": {
                "path": str(preflight_path),
                "sha256": _sha256(preflight_path),
            },
        },
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    issue_lines = "\n".join(f"- {item}" for item in result.issues) or "- None."
    warning_lines = "\n".join(f"- {item}" for item in result.warnings) or "- None."
    stage_lines = []
    for label, stage in (("Stage 1", result.stage1), ("Stage 2", result.stage2)):
        if stage is None:
            stage_lines.append(f"| {label} | not parsed | — | — | — |")
        else:
            stage_lines.append(
                f"| {label} | {stage.nstep} | {stage.energy:.8g} | "
                f"{stage.rms_gradient:.8g} | {stage.maximum_gradient:.8g} |"
            )
    rmsd_text = (
        f"{result.heavy_atom_rmsd:.4f} Å"
        if result.heavy_atom_rmsd is not None
        else "not computed"
    )
    maximum_text = (
        f"{result.maximum_heavy_atom_displacement:.4f} Å"
        if result.maximum_heavy_atom_displacement is not None
        else "not computed"
    )
    report = f"""# FANA Post-Minimization Audit

- **Status:** `{result.status}`
- **Digital Polymerase executed Amber:** No
- **Expert review still required:** Yes

## Inputs

- Original candidate: `{candidate_path}`
- Externally minimized PDB: `{minimized_path}`
- Approved parameter manifest: `{parameter_path}`
- Passing preparation preflight: `{preflight_path}`

## Structural checks

| Metric | Result |
|---|---:|
| Restored FANA residues | {result.residue_count} |
| Common heavy atoms | {result.heavy_atom_count} |
| Aligned heavy-atom RMSD | {rmsd_text} |
| Configured RMSD ceiling | {max_heavy_atom_rmsd:.4f} Å |
| Maximum aligned heavy-atom displacement | {maximum_text} |
| Level 4 geometry recheck | `{result.geometry_status}` |

The RMSD ceiling is a campaign safeguard, not a universal physical-validity
criterion. Bond geometry, C2-prime/F2-prime stereochemistry, and template-relative
sugar pucker are rechecked separately.

## Amber final rows

| Stage | NSTEP | Energy | RMS gradient | Maximum gradient |
|---|---:|---:|---:|---:|
{chr(10).join(stage_lines)}

## Blocking issues

{issue_lines}

## Warnings

{warning_lines}

Even a structural pass does not validate the force field. A named expert must
review parameter provenance, LEaP output, charges, final energies/gradients,
restraints, structural changes, and the intended downstream use before the
FANA physical-validation milestone can be closed.
"""
    report_path.write_text(report, encoding="utf-8")


def audit_fana_minimization(
    candidate_pdb: str | Path,
    minimized_pdb: str | Path,
    template_pdb: str | Path,
    parameter_manifest: str | Path,
    parameter_preflight: str | Path,
    stage1_output: str | Path,
    stage2_output: str | Path,
    output_dir: str | Path,
    *,
    max_heavy_atom_rmsd: float = 2.0,
    strict: bool = False,
    overwrite: bool = False,
) -> FANAMinimizationAuditResult:
    """Audit externally generated Amber minimization outputs without running Amber."""

    candidate_path = Path(candidate_pdb)
    minimized_path = Path(minimized_pdb)
    template_path = Path(template_pdb)
    parameter_path = Path(parameter_manifest)
    preflight_path = Path(parameter_preflight)
    stage1_path = Path(stage1_output)
    stage2_path = Path(stage2_output)
    destination = Path(output_dir)
    restored_path = destination / "restored_minimized_solute.pdb"
    geometry_report = destination / "restored_geometry_readiness.md"
    geometry_json = destination / "restored_geometry_readiness.json"
    report_path = destination / "minimization_audit.md"
    json_path = destination / "minimization_audit.json"
    targets = [restored_path, geometry_report, geometry_json, report_path, json_path]
    inputs = [
        candidate_path,
        minimized_path,
        template_path,
        parameter_path,
        preflight_path,
        stage1_path,
        stage2_path,
    ]
    _ensure_writable_targets(targets, protected=inputs, overwrite=overwrite)
    if not isinstance(max_heavy_atom_rmsd, (int, float)) or isinstance(
        max_heavy_atom_rmsd, bool
    ):
        raise ValueError("max_heavy_atom_rmsd must be numeric.")
    if not 0.0 < float(max_heavy_atom_rmsd) <= 20.0:
        raise ValueError("max_heavy_atom_rmsd must be greater than 0 and at most 20 Å.")

    candidate = parse_pdb(candidate_path, strict=True)
    minimized = parse_pdb(minimized_path, strict=True)
    manifest = _load_json(parameter_path, "parameter manifest")
    preflight = _load_json(preflight_path, "parameter preflight")
    issues: list[str] = []
    warnings: list[str] = []

    if (
        manifest.get("schema_version") != SCHEMA_VERSION
        or manifest.get("target") != TARGET
    ):
        issues.append("Parameter manifest must use FANA schema version 0.1.")
    if manifest.get("candidate_sha256") != _sha256(candidate_path):
        issues.append(
            "Parameter manifest candidate hash does not match the audit candidate."
        )
    parameterization = manifest.get("parameterization")
    if not isinstance(parameterization, dict):
        parameterization = {}
        issues.append("Parameter manifest parameterization must be an object.")
    review = parameterization.get("review")
    if not isinstance(review, dict) or review.get("status") != "approved":
        issues.append("Parameter manifest must retain approved external review status.")
    if (
        preflight.get("target") != TARGET
        or preflight.get("status") != "PREPARED_NOT_EXECUTED"
    ):
        issues.append("Parameter preflight must report PREPARED_NOT_EXECUTED for FANA.")
    if preflight.get("executed") is not False:
        issues.append("Parameter preflight must record executed as false.")

    expected_names = _expected_amber_names(candidate, parameterization, issues)
    restored = _restore_minimized_polymer(
        candidate=candidate,
        minimized=minimized,
        expected_amber_names=expected_names,
        issues=issues,
    )

    stage1: AmberFinalResult | None = None
    stage2: AmberFinalResult | None = None
    for label, path in (("Stage 1", stage1_path), ("Stage 2", stage2_path)):
        try:
            parsed = parse_amber_minimization_output(path)
        except (OSError, ValidationError) as exc:
            issues.append(f"{label} minimization output failed validation: {exc}")
            continue
        if parsed.reached_maximum_cycles:
            warnings.append(
                f"{label} reached its maximum minimization cycle count; expert "
                "gradient review is required."
            )
        if label == "Stage 1":
            stage1 = parsed
        else:
            stage2 = parsed

    heavy_atom_count = 0
    heavy_atom_rmsd: float | None = None
    maximum_displacement: float | None = None
    geometry_status = "NOT_RUN"
    if restored and not any("lacks candidate atoms" in issue for issue in issues):
        destination.mkdir(parents=True, exist_ok=True)
        write_pdb(
            restored,
            restored_path,
            remarks=(
                "Digital Polymerase post-minimization FANA solute restoration",
                "Coordinates came from an external Amber run; Digital Polymerase did not execute Amber",
            ),
        )
        try:
            heavy_atom_count, heavy_atom_rmsd, maximum_displacement = (
                _heavy_atom_displacements(candidate, restored)
            )
        except (KeyError, ValidationError) as exc:
            issues.append(f"Heavy-atom comparison failed: {exc}")
        else:
            if heavy_atom_rmsd > float(max_heavy_atom_rmsd):
                issues.append(
                    f"Aligned heavy-atom RMSD {heavy_atom_rmsd:.4f} Å exceeds "
                    f"the configured {float(max_heavy_atom_rmsd):.4f} Å ceiling."
                )
        geometry = audit_fana_physical_readiness(
            restored_path,
            template_path,
            geometry_report,
            geometry_json,
            strict=False,
        )
        geometry_status = geometry.geometry_status
        if not geometry.geometry_ok:
            issues.append(
                "Restored minimized FANA solute failed the Level 4 geometry recheck."
            )

    status = AUDIT_FAIL_STATUS if issues else AUDIT_PASS_STATUS
    generated = [
        path
        for path in (restored_path, geometry_report, geometry_json)
        if path.exists()
    ]
    result = FANAMinimizationAuditResult(
        status=status,
        output_dir=destination,
        issues=issues,
        warnings=warnings,
        residue_count=len(restored),
        heavy_atom_count=heavy_atom_count,
        heavy_atom_rmsd=heavy_atom_rmsd,
        maximum_heavy_atom_displacement=maximum_displacement,
        geometry_status=geometry_status,
        stage1=stage1,
        stage2=stage2,
        generated_files=generated,
    )
    _write_audit_outputs(
        result=result,
        report_path=report_path,
        json_path=json_path,
        candidate_path=candidate_path,
        minimized_path=minimized_path,
        template_path=template_path,
        parameter_path=parameter_path,
        preflight_path=preflight_path,
        max_heavy_atom_rmsd=float(max_heavy_atom_rmsd),
    )
    result.generated_files.extend((report_path, json_path))
    if strict and issues:
        raise ValidationError("FANA minimization audit failed: " + " ".join(issues))
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize or audit a controlled FANA minimization campaign."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    initialize = subparsers.add_parser(
        "init", help="Build an intentionally blocked, candidate-bound campaign."
    )
    initialize.add_argument("--rna", required=True, type=Path)
    initialize.add_argument("--template", required=True, type=Path)
    initialize.add_argument("--output-dir", required=True, type=Path)
    initialize.add_argument("--overwrite", action="store_true")

    audit = subparsers.add_parser(
        "audit", help="Audit externally generated Amber minimization outputs."
    )
    audit.add_argument("--candidate", required=True, type=Path)
    audit.add_argument("--minimized", required=True, type=Path)
    audit.add_argument("--template", required=True, type=Path)
    audit.add_argument("--parameters", required=True, type=Path)
    audit.add_argument("--preflight", required=True, type=Path)
    audit.add_argument("--stage1", required=True, type=Path)
    audit.add_argument("--stage2", required=True, type=Path)
    audit.add_argument("--output-dir", required=True, type=Path)
    audit.add_argument("--max-heavy-atom-rmsd", type=float, default=2.0)
    audit.add_argument("--strict", action="store_true")
    audit.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        result = initialize_fana_minimization_campaign(
            args.rna,
            args.template,
            args.output_dir,
            overwrite=args.overwrite,
        )
        print(
            f"FANA campaign {result.status}: {result.sequence} "
            f"({result.residue_count} residues) in {result.output_dir}"
        )
        return 0
    result = audit_fana_minimization(
        args.candidate,
        args.minimized,
        args.template,
        args.parameters,
        args.preflight,
        args.stage1,
        args.stage2,
        args.output_dir,
        max_heavy_atom_rmsd=args.max_heavy_atom_rmsd,
        strict=args.strict,
        overwrite=args.overwrite,
    )
    print(
        f"FANA minimization audit {result.status}: "
        f"{len(result.issues)} blockers, {len(result.warnings)} warnings"
    )
    return 0 if result.structurally_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
