"""External FANA parameter gate and Amber minimization-bundle preparation.

This module validates a provenance-rich parameter manifest against a specific
FANA candidate and its Level 4 readiness manifest. It can then prepare, but
never execute, a conservative two-stage Amber minimization bundle.

Structural validation of a manifest cannot prove that a force field is
scientifically accurate. Approval, derivation evidence, and external review
remain explicit parts of the contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

from digital_polymerase.core.atoms import ResidueKey, clone_atom
from digital_polymerase.core.errors import ValidationError
from digital_polymerase.core.pdb_io import (
    Structure,
    parse_pdb,
    residue_name,
    sort_residue_keys,
    write_pdb,
)
from digital_polymerase.core.residues import base_of


SCHEMA_VERSION = "0.1"
TARGET = "FANA"
UNRESOLVED = "UNRESOLVED"
AMBER_NAME_PATTERN = re.compile(r"^[A-Z0-9]{1,3}$")
SAFE_COMMAND_PATTERN = re.compile(r"^[A-Za-z0-9_.+-]+$")

REQUIRED_COVERAGE = (
    "atom_names",
    "atom_types",
    "partial_charges",
    "bonds",
    "angles",
    "dihedrals",
    "impropers",
    "nonbonded",
)

REQUIRED_ARTIFACT_ROLES = ("frcmod", "residue_library")
ALLOWED_ARTIFACT_ROLES = {
    "frcmod",
    "residue_library",
    "additional_leap_parameters",
}

ALLOWED_TERMINAL_REMOVALS = {
    "five_prime": frozenset({"P", "OP1", "OP2"}),
    "three_prime": frozenset(),
}

PRIMARY_REFERENCES = (
    "https://doi.org/10.1021/acs.jctc.4c01164",
    "https://doi.org/10.33011/livecoms.6.1.4545",
    "https://modxna.chpc.utah.edu/catalog/",
    "https://www.rcsb.org/structure/2KP4",
)


@dataclass(frozen=True)
class ValidatedArtifact:
    role: str
    source_path: Path
    bundle_name: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class ResolvedTerminalState:
    """Amber terminal template plus atoms removed from the source candidate."""

    residue_name: str
    remove_atoms: tuple[str, ...]


@dataclass
class FANAParameterGateResult:
    """Outcome of parameter-manifest validation and bundle preparation."""

    status: str
    ready: bool
    output_dir: Path
    issues: list[str]
    warnings: list[str]
    artifacts: list[ValidatedArtifact]
    generated_files: list[Path]


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
    insertion = key[2] or ""
    return f"{key[0]}:{key[1]}{insertion}"


def _consecutive_segments(keys: Sequence[ResidueKey]) -> list[list[ResidueKey]]:
    if not keys:
        return []
    segments: list[list[ResidueKey]] = [[keys[0]]]
    for key in keys[1:]:
        previous = segments[-1][-1]
        consecutive = (
            key[0] == previous[0]
            and key[1] == previous[1] + 1
            and not key[2]
            and not previous[2]
        )
        if consecutive:
            segments[-1].append(key)
        else:
            segments.append([key])
    return segments


def _candidate_inventory(structure: Structure) -> dict[str, list[str]]:
    inventory: dict[str, set[str]] = {}
    for key in sort_residue_keys(structure):
        name = residue_name(structure[key])
        inventory.setdefault(name, set()).update(structure[key])
    return {name: sorted(atoms) for name, atoms in sorted(inventory.items())}


def _validate_readiness_manifest(
    *,
    candidate_path: Path,
    readiness_path: Path,
    readiness: Mapping[str, Any],
    issues: list[str],
) -> None:
    if readiness.get("schema_version") != "0.1":
        issues.append("Readiness manifest schema_version must be 0.1.")
    if readiness.get("target") != TARGET:
        issues.append("Readiness manifest target must be FANA.")
    if readiness.get("status") != "PARAMETERIZATION_REQUIRED":
        issues.append("Readiness manifest status must be PARAMETERIZATION_REQUIRED.")
    geometry = readiness.get("geometry_gate")
    if not isinstance(geometry, dict) or geometry.get("status") != "PASS":
        issues.append("The FANA geometry gate must be PASS before parameterization.")
    candidate = readiness.get("candidate")
    expected_sha = candidate.get("sha256") if isinstance(candidate, dict) else None
    actual_sha = _sha256(candidate_path)
    if expected_sha != actual_sha:
        issues.append(
            "Candidate SHA-256 does not match the Level 4 readiness manifest."
        )
    if not readiness_path.is_file():
        issues.append(f"Readiness manifest does not exist: {readiness_path}")


def initialize_fana_parameter_manifest(
    candidate_pdb: str | Path,
    readiness_manifest: str | Path,
    output_json: str | Path,
) -> Path:
    """Write a candidate-specific, intentionally blocked parameter template."""

    candidate_path = Path(candidate_pdb)
    readiness_path = Path(readiness_manifest)
    output_path = Path(output_json)
    structure = parse_pdb(candidate_path, strict=True)
    readiness = _load_json(readiness_path, "readiness manifest")
    issues: list[str] = []
    _validate_readiness_manifest(
        candidate_path=candidate_path,
        readiness_path=readiness_path,
        readiness=readiness,
        issues=issues,
    )
    if issues:
        raise ValidationError(" ".join(issues))

    keys = sort_residue_keys(structure)
    if not keys:
        raise ValueError(f"No candidate residues found in {candidate_path}.")
    inventory = _candidate_inventory(structure)
    bases = sorted(
        {
            base_of(residue_name(structure[key]))
            for key in keys
            if base_of(residue_name(structure[key])) in {"A", "C", "G", "U"}
        }
    )
    mappings = {
        name: {
            "internal_name": UNRESOLVED,
            "input_atom_names": atoms,
        }
        for name, atoms in inventory.items()
    }
    terminal_states = []
    for segment in _consecutive_segments(keys):
        terminal_states.append(
            {
                "first_residue": _residue_label(segment[0]),
                "last_residue": _residue_label(segment[-1]),
                "five_prime": {
                    "chemistry": UNRESOLVED,
                    "residue_name": UNRESOLVED,
                    "remove_atoms": [],
                    "resolved": False,
                },
                "three_prime": {
                    "chemistry": UNRESOLVED,
                    "residue_name": UNRESOLVED,
                    "remove_atoms": [],
                    "resolved": False,
                },
            }
        )

    template = {
        "schema_version": SCHEMA_VERSION,
        "target": TARGET,
        "candidate_sha256": _sha256(candidate_path),
        "readiness_manifest_sha256": _sha256(readiness_path),
        "parameterization": {
            "engine": "Amber",
            "parent_force_field": {
                "name": UNRESOLVED,
                "version": UNRESOLVED,
                "leaprc": UNRESOLVED,
            },
            "generator": {
                "name": "modXNA",
                "version": UNRESOLVED,
                "command": UNRESOLVED,
                "fragments_by_base": {
                    base: {
                        "backbone": UNRESOLVED,
                        "sugar_linker": "A5L",
                        "base": UNRESOLVED,
                    }
                    for base in bases
                },
            },
            "residue_mappings": mappings,
            "terminal_states": terminal_states,
            "artifacts": [],
            "coverage": {name: False for name in REQUIRED_COVERAGE},
            "charge_model": {
                "method": UNRESOLVED,
                "quantum_method": UNRESOLVED,
                "expected_total_charge": None,
                "validated": False,
            },
            "review": {
                "status": "pending",
                "reviewer": UNRESOLVED,
                "reviewed_on": UNRESOLVED,
                "evidence": [],
                "notes": "",
            },
            "solvation": {
                "water_leaprc": "leaprc.water.opc",
                "water_box": "OPCBOX",
                "buffer_angstrom": 10.0,
                "neutralizing_ion": "Na+",
            },
            "minimization": {
                "cutoff_angstrom": 10.0,
                "stage1": {
                    "maxcyc": 5000,
                    "ncyc": 2500,
                    "restraint_wt": 10.0,
                    "restraint_mask": "!:WAT,Na+,Cl-",
                },
                "stage2": {
                    "maxcyc": 10000,
                    "ncyc": 5000,
                },
            },
            "references": list(PRIMARY_REFERENCES),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
    return output_path


def _valid_amber_name(value: Any) -> bool:
    return isinstance(value, str) and bool(AMBER_NAME_PATTERN.fullmatch(value))


def _validate_parent_force_field(
    parameterization: Mapping[str, Any], issues: list[str]
) -> None:
    parent = parameterization.get("parent_force_field")
    if not isinstance(parent, dict):
        issues.append("parameterization.parent_force_field must be an object.")
        return
    for field in ("name", "version", "leaprc"):
        value = parent.get(field)
        if not isinstance(value, str) or not value.strip() or value == UNRESOLVED:
            issues.append(f"parent_force_field.{field} must be resolved.")
    leaprc = parent.get("leaprc")
    if isinstance(leaprc, str) and not SAFE_COMMAND_PATTERN.fullmatch(leaprc):
        issues.append("parent_force_field.leaprc contains unsafe characters.")


def _validate_generator(
    parameterization: Mapping[str, Any], bases: set[str], issues: list[str]
) -> None:
    generator = parameterization.get("generator")
    if not isinstance(generator, dict):
        issues.append("parameterization.generator must be an object.")
        return
    for field in ("name", "version", "command"):
        value = generator.get(field)
        if not isinstance(value, str) or not value.strip() or value == UNRESOLVED:
            issues.append(f"generator.{field} must be resolved.")
    if str(generator.get("name", "")).lower() == "modxna":
        fragments = generator.get("fragments_by_base")
        if not isinstance(fragments, dict):
            issues.append("modXNA requires fragments_by_base provenance.")
            return
        for base in sorted(bases):
            selection = fragments.get(base)
            if not isinstance(selection, dict):
                issues.append(f"modXNA fragment selection is missing for base {base}.")
                continue
            for field in ("backbone", "sugar_linker", "base"):
                value = selection.get(field)
                if (
                    not isinstance(value, str)
                    or not value.strip()
                    or value == UNRESOLVED
                ):
                    issues.append(
                        f"modXNA {base} fragment field {field} must be resolved."
                    )
            if selection.get("sugar_linker") != "A5L":
                issues.append(
                    f"modXNA {base} sugar_linker must be A5L for this FANA gate."
                )


def _validate_residue_mappings(
    *,
    parameterization: Mapping[str, Any],
    inventory: Mapping[str, list[str]],
    issues: list[str],
) -> dict[str, str]:
    mappings = parameterization.get("residue_mappings")
    resolved: dict[str, str] = {}
    if not isinstance(mappings, dict):
        issues.append("parameterization.residue_mappings must be an object.")
        return resolved
    extra = sorted(set(mappings) - set(inventory))
    if extra:
        issues.append(
            "Residue mappings contain unused source names: " + ", ".join(extra)
        )
    for source_name, atom_names in inventory.items():
        mapping = mappings.get(source_name)
        if not isinstance(mapping, dict):
            issues.append(f"Residue mapping is missing for {source_name}.")
            continue
        internal_name = mapping.get("internal_name")
        if not _valid_amber_name(internal_name):
            issues.append(
                f"Residue mapping {source_name}.internal_name must be 1–3 uppercase alphanumerics."
            )
        else:
            resolved[source_name] = str(internal_name)
        declared_atoms = mapping.get("input_atom_names")
        if not isinstance(declared_atoms, list) or not all(
            isinstance(item, str) for item in declared_atoms
        ):
            issues.append(
                f"Residue mapping {source_name}.input_atom_names must be a string list."
            )
        elif sorted(set(declared_atoms)) != sorted(set(atom_names)):
            issues.append(
                f"Residue mapping {source_name} does not exactly cover candidate atom names."
            )
    if len(set(resolved.values())) != len(resolved):
        issues.append(
            "Internal Amber residue names must be unique by source chemistry."
        )
    return resolved


def _validate_terminal_states(
    *,
    structure: Structure,
    parameterization: Mapping[str, Any],
    segments: Sequence[Sequence[ResidueKey]],
    issues: list[str],
) -> dict[tuple[str, str], dict[str, ResolvedTerminalState]]:
    states = parameterization.get("terminal_states")
    resolved: dict[tuple[str, str], dict[str, ResolvedTerminalState]] = {}
    if not isinstance(states, list):
        issues.append("parameterization.terminal_states must be a list.")
        return resolved
    expected = {
        (_residue_label(segment[0]), _residue_label(segment[-1]))
        for segment in segments
    }
    for item in states:
        if not isinstance(item, dict):
            issues.append("Each terminal state must be an object.")
            continue
        pair = (str(item.get("first_residue", "")), str(item.get("last_residue", "")))
        if pair in resolved:
            issues.append(f"Duplicate terminal state for segment {pair[0]}–{pair[1]}.")
            continue
        terminal_names: dict[str, ResolvedTerminalState] = {}
        for end in ("five_prime", "three_prime"):
            value = item.get(end)
            if not isinstance(value, dict):
                issues.append(f"Terminal state {pair[0]}–{pair[1]} lacks {end}.")
                continue
            if value.get("resolved") is not True:
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} {end} is unresolved."
                )
            chemistry = value.get("chemistry")
            if (
                not isinstance(chemistry, str)
                or not chemistry.strip()
                or chemistry == UNRESOLVED
            ):
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} {end} chemistry is unresolved."
                )
            residue_code = value.get("residue_name")
            if not _valid_amber_name(residue_code):
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} {end} residue_name is invalid."
                )
                continue
            remove_atoms = value.get("remove_atoms", [])
            if not isinstance(remove_atoms, list) or not all(
                isinstance(atom_name, str) and atom_name.strip()
                for atom_name in remove_atoms
            ):
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} {end} remove_atoms "
                    "must be a string list."
                )
                continue
            if len(set(remove_atoms)) != len(remove_atoms):
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} {end} remove_atoms "
                    "contains duplicates."
                )
                continue
            unsupported = sorted(set(remove_atoms) - ALLOWED_TERMINAL_REMOVALS[end])
            if unsupported:
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} {end} cannot remove: "
                    + ", ".join(unsupported)
                )
                continue
            if (
                end == "five_prime"
                and remove_atoms
                and set(remove_atoms) != ALLOWED_TERMINAL_REMOVALS[end]
            ):
                issues.append(
                    f"Terminal state {pair[0]}–{pair[1]} five_prime must remove "
                    "P, OP1, and OP2 together."
                )
                continue
            if pair in expected:
                segment = next(
                    candidate_segment
                    for candidate_segment in segments
                    if (
                        _residue_label(candidate_segment[0]),
                        _residue_label(candidate_segment[-1]),
                    )
                    == pair
                )
                terminal_key = segment[0] if end == "five_prime" else segment[-1]
                absent = sorted(set(remove_atoms) - set(structure[terminal_key]))
                if absent:
                    issues.append(
                        f"Terminal state {pair[0]}–{pair[1]} {end} remove_atoms "
                        "are absent from the candidate: " + ", ".join(absent)
                    )
                    continue
            terminal_names[end] = ResolvedTerminalState(
                residue_name=str(residue_code),
                remove_atoms=tuple(remove_atoms),
            )
        resolved[pair] = terminal_names
    found = set(resolved)
    for pair in sorted(expected - found):
        issues.append(f"Terminal state is missing for segment {pair[0]}–{pair[1]}.")
    for pair in sorted(found - expected):
        issues.append(f"Terminal state references unknown segment {pair[0]}–{pair[1]}.")
    return resolved


def _safe_artifact_path(
    manifest_dir: Path, value: Any, *, label: str, issues: list[str]
) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        issues.append(f"{label} path must be a non-empty relative path.")
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        issues.append(f"{label} path must stay inside the manifest directory.")
        return None
    resolved = (manifest_dir / relative).resolve()
    root = manifest_dir.resolve()
    if resolved != root and root not in resolved.parents:
        issues.append(f"{label} resolves outside the manifest directory.")
        return None
    return resolved


def _validate_artifacts(
    *,
    parameterization: Mapping[str, Any],
    manifest_dir: Path,
    issues: list[str],
) -> list[ValidatedArtifact]:
    entries = parameterization.get("artifacts")
    validated: list[ValidatedArtifact] = []
    if not isinstance(entries, list) or not entries:
        issues.append("parameterization.artifacts must contain parameter files.")
        return validated
    bundle_names: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"artifacts[{index}]"
        if not isinstance(entry, dict):
            issues.append(f"{label} must be an object.")
            continue
        role = entry.get("role")
        if role not in ALLOWED_ARTIFACT_ROLES:
            issues.append(f"{label}.role is unsupported: {role!r}.")
            continue
        source_path = _safe_artifact_path(
            manifest_dir, entry.get("path"), label=label, issues=issues
        )
        expected_sha = entry.get("sha256")
        if not isinstance(expected_sha, str) or not re.fullmatch(
            r"[0-9a-f]{64}", expected_sha
        ):
            issues.append(
                f"{label}.sha256 must be 64 lowercase hexadecimal characters."
            )
            continue
        if source_path is None:
            continue
        if not source_path.is_file():
            issues.append(f"{label} file does not exist: {source_path}")
            continue
        if source_path.stat().st_size == 0:
            issues.append(f"{label} file is empty: {source_path}")
            continue
        actual_sha = _sha256(source_path)
        if actual_sha != expected_sha:
            issues.append(f"{label} SHA-256 mismatch for {source_path.name}.")
            continue
        bundle_name = source_path.name
        if not SAFE_COMMAND_PATTERN.fullmatch(bundle_name):
            issues.append(
                f"{label} filename contains characters that are unsafe in LEaP: "
                f"{bundle_name!r}."
            )
            continue
        if bundle_name in bundle_names:
            issues.append(f"Parameter artifact filenames collide: {bundle_name}.")
            continue
        bundle_names.add(bundle_name)
        validated.append(
            ValidatedArtifact(
                role=str(role),
                source_path=source_path,
                bundle_name=bundle_name,
                sha256=actual_sha,
                size_bytes=source_path.stat().st_size,
            )
        )
    roles = {item.role for item in validated}
    for role in REQUIRED_ARTIFACT_ROLES:
        if role not in roles:
            issues.append(f"At least one validated {role} artifact is required.")
    return validated


def _validate_library_names(
    *,
    artifacts: Sequence[ValidatedArtifact],
    required_names: set[str],
    issues: list[str],
) -> None:
    library_text = "\n".join(
        artifact.source_path.read_text(encoding="utf-8", errors="replace")
        for artifact in artifacts
        if artifact.role == "residue_library"
    )
    for name in sorted(required_names):
        token = re.compile(rf"(?<![A-Z0-9]){re.escape(name)}(?![A-Z0-9])")
        if token.search(library_text) is None:
            issues.append(
                f"Amber residue name {name} was not found in any residue-library artifact."
            )


def _validate_coverage(parameterization: Mapping[str, Any], issues: list[str]) -> None:
    coverage = parameterization.get("coverage")
    if not isinstance(coverage, dict):
        issues.append("parameterization.coverage must be an object.")
        return
    for field in REQUIRED_COVERAGE:
        if coverage.get(field) is not True:
            issues.append(f"Parameter coverage {field} must be explicitly true.")


def _validate_charge_and_review(
    parameterization: Mapping[str, Any], issues: list[str]
) -> None:
    charge = parameterization.get("charge_model")
    if not isinstance(charge, dict):
        issues.append("parameterization.charge_model must be an object.")
    else:
        for field in ("method", "quantum_method"):
            value = charge.get(field)
            if not isinstance(value, str) or not value.strip() or value == UNRESOLVED:
                issues.append(f"charge_model.{field} must be resolved.")
        expected_charge = charge.get("expected_total_charge")
        if not isinstance(expected_charge, int) or isinstance(expected_charge, bool):
            issues.append("charge_model.expected_total_charge must be an integer.")
        if charge.get("validated") is not True:
            issues.append("charge_model.validated must be explicitly true.")

    review = parameterization.get("review")
    if not isinstance(review, dict):
        issues.append("parameterization.review must be an object.")
        return
    if review.get("status") != "approved":
        issues.append("Parameter review status must be approved.")
    reviewer = review.get("reviewer")
    if not isinstance(reviewer, str) or not reviewer.strip() or reviewer == UNRESOLVED:
        issues.append("Parameter review requires a named reviewer.")
    reviewed_on = review.get("reviewed_on")
    try:
        review_date = date.fromisoformat(str(reviewed_on))
    except ValueError:
        issues.append("Parameter review reviewed_on must be an ISO date (YYYY-MM-DD).")
    else:
        if review_date > date.today():
            issues.append("Parameter review reviewed_on cannot be in the future.")
    evidence = review.get("evidence")
    if (
        not isinstance(evidence, list)
        or not evidence
        or not all(isinstance(item, str) and item.strip() for item in evidence)
    ):
        issues.append("Parameter review requires at least one evidence reference.")


def _validate_protocol(parameterization: Mapping[str, Any], issues: list[str]) -> None:
    solvation = parameterization.get("solvation")
    if not isinstance(solvation, dict):
        issues.append("parameterization.solvation must be an object.")
    else:
        for field in ("water_leaprc", "water_box", "neutralizing_ion"):
            value = solvation.get(field)
            if not isinstance(value, str) or not SAFE_COMMAND_PATTERN.fullmatch(value):
                issues.append(
                    f"solvation.{field} is missing or contains unsafe characters."
                )
        buffer_value = solvation.get("buffer_angstrom")
        if (
            not isinstance(buffer_value, (int, float))
            or isinstance(buffer_value, bool)
            or not 6.0 <= float(buffer_value) <= 30.0
        ):
            issues.append("solvation.buffer_angstrom must be between 6 and 30 Å.")

    minimization = parameterization.get("minimization")
    if not isinstance(minimization, dict):
        issues.append("parameterization.minimization must be an object.")
        return
    cutoff = minimization.get("cutoff_angstrom")
    if (
        not isinstance(cutoff, (int, float))
        or isinstance(cutoff, bool)
        or not 6.0 <= float(cutoff) <= 15.0
    ):
        issues.append("minimization.cutoff_angstrom must be between 6 and 15 Å.")
    for name in ("stage1", "stage2"):
        stage = minimization.get(name)
        if not isinstance(stage, dict):
            issues.append(f"minimization.{name} must be an object.")
            continue
        maxcyc = stage.get("maxcyc")
        ncyc = stage.get("ncyc")
        if (
            not isinstance(maxcyc, int)
            or isinstance(maxcyc, bool)
            or not 100 <= maxcyc <= 200000
        ):
            issues.append(f"minimization.{name}.maxcyc must be 100–200000.")
        if (
            not isinstance(ncyc, int)
            or isinstance(ncyc, bool)
            or not isinstance(maxcyc, int)
            or not 0 <= ncyc <= maxcyc
        ):
            issues.append(f"minimization.{name}.ncyc must be between 0 and maxcyc.")
    stage1 = minimization.get("stage1")
    if isinstance(stage1, dict):
        weight = stage1.get("restraint_wt")
        if (
            not isinstance(weight, (int, float))
            or isinstance(weight, bool)
            or not 0.1 <= float(weight) <= 100.0
        ):
            issues.append("minimization.stage1.restraint_wt must be 0.1–100.")
        mask = stage1.get("restraint_mask")
        if not isinstance(mask, str) or not mask.strip() or "'" in mask or "\n" in mask:
            issues.append("minimization.stage1.restraint_mask is missing or unsafe.")


def _write_preflight(
    *,
    output_dir: Path,
    status: str,
    issues: Sequence[str],
    warnings: Sequence[str],
    artifacts: Sequence[ValidatedArtifact],
    generated_files: Sequence[Path],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "parameter_preflight.json"
    report_path = output_dir / "parameter_preflight.md"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "target": TARGET,
        "stage": "external_parameter_gate",
        "status": status,
        "issues": list(issues),
        "warnings": list(warnings),
        "artifacts": [
            {
                "role": artifact.role,
                "source_path": str(artifact.source_path),
                "bundle_name": artifact.bundle_name,
                "sha256": artifact.sha256,
                "size_bytes": artifact.size_bytes,
            }
            for artifact in artifacts
        ],
        "generated_files": [str(path) for path in generated_files],
        "executed": False,
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    issue_lines = "\n".join(f"- {item}" for item in issues) if issues else "- None."
    warning_lines = (
        "\n".join(f"- {item}" for item in warnings) if warnings else "- None."
    )
    artifact_lines = (
        "\n".join(
            f"- `{item.bundle_name}` — `{item.role}` — `{item.sha256}`"
            for item in artifacts
        )
        if artifacts
        else "- None validated."
    )
    report = f"""# FANA External-Parameter Preflight

**Status:** `{status}`
**Execution:** Not run

## Blocking issues

{issue_lines}

## Warnings

{warning_lines}

## Validated artifacts

{artifact_lines}

This gate validates identity, hashes, declared coverage, residue-name coverage,
terminal-state resolution, and review provenance. It does not independently
prove the scientific accuracy of the supplied force field.
"""
    report_path.write_text(report, encoding="utf-8")
    return json_path, report_path


def _rename_candidate(
    *,
    structure: Structure,
    internal_mappings: Mapping[str, str],
    terminal_states: Mapping[tuple[str, str], Mapping[str, ResolvedTerminalState]],
) -> Structure:
    renamed: Structure = {}
    segments = _consecutive_segments(sort_residue_keys(structure))
    terminal_by_key: dict[ResidueKey, ResolvedTerminalState] = {}
    for segment in segments:
        pair = (_residue_label(segment[0]), _residue_label(segment[-1]))
        state = terminal_states[pair]
        if len(segment) == 1:
            raise ValidationError(
                "Single-residue segments require a dedicated terminal template and "
                "are not supported by this minimization preparer."
            )
        terminal_by_key[segment[0]] = state["five_prime"]
        terminal_by_key[segment[-1]] = state["three_prime"]
    for key in sort_residue_keys(structure):
        source_name = residue_name(structure[key])
        terminal = terminal_by_key.get(key)
        target_name = (
            terminal.residue_name
            if terminal is not None
            else internal_mappings[source_name]
        )
        remove_atoms = set(terminal.remove_atoms) if terminal is not None else set()
        renamed[key] = {
            atom_name: clone_atom(atom, res_name=target_name)
            for atom_name, atom in structure[key].items()
            if atom_name not in remove_atoms
        }
    return renamed


def _planned_bundle_paths(output_dir: Path) -> list[Path]:
    return [
        output_dir / "candidate_amber_names.pdb",
        output_dir / "tleap.in",
        output_dir / "minimize_stage1.in",
        output_dir / "minimize_stage2.in",
        output_dir / "run_minimization.sh",
        output_dir / "PREPARATION_README.md",
        output_dir / "parameter_manifest.snapshot.json",
        output_dir / "readiness_manifest.snapshot.json",
    ]


def _write_minimization_bundle(
    *,
    structure: Structure,
    parameterization: Mapping[str, Any],
    internal_mappings: Mapping[str, str],
    terminal_states: Mapping[tuple[str, str], Mapping[str, ResolvedTerminalState]],
    artifacts: Sequence[ValidatedArtifact],
    candidate_path: Path,
    parameter_manifest_path: Path,
    readiness_manifest_path: Path,
    output_dir: Path,
    overwrite: bool,
) -> list[Path]:
    planned = _planned_bundle_paths(output_dir)
    parameter_dir = output_dir / "parameters"
    artifact_targets = [parameter_dir / item.bundle_name for item in artifacts]
    protected_sources = {
        candidate_path.resolve(),
        readiness_manifest_path.resolve(),
        parameter_manifest_path.resolve(),
        *(item.source_path.resolve() for item in artifacts),
    }
    collisions = [
        path
        for path in [*planned, *artifact_targets]
        if path.resolve() in protected_sources
    ]
    if collisions:
        labels = ", ".join(str(path) for path in collisions)
        raise ValidationError(
            "Output paths collide with source inputs; choose a separate bundle directory: "
            + labels
        )
    existing = [path for path in [*planned, *artifact_targets] if path.exists()]
    if existing and not overwrite:
        labels = ", ".join(str(path) for path in existing)
        raise FileExistsError(
            "Refusing to overwrite existing minimization-bundle files: " + labels
        )

    renamed = _rename_candidate(
        structure=structure,
        internal_mappings=internal_mappings,
        terminal_states=terminal_states,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    parameter_dir.mkdir(parents=True, exist_ok=True)
    for artifact, target in zip(artifacts, artifact_targets):
        shutil.copy2(artifact.source_path, target)

    candidate_output = output_dir / "candidate_amber_names.pdb"
    write_pdb(
        renamed,
        candidate_output,
        remarks=(
            "Digital Polymerase FANA Amber minimization preparation",
            "Residue names mapped from an approved external parameter manifest",
            "WARNING: bundle prepared but not executed or scientifically validated by this tool",
        ),
    )

    parent = parameterization["parent_force_field"]
    solvation = parameterization["solvation"]
    frcmods = [item for item in artifacts if item.role != "residue_library"]
    libraries = [item for item in artifacts if item.role == "residue_library"]
    leap_lines = [
        f"source {parent['leaprc']}",
        f"source {solvation['water_leaprc']}",
    ]
    leap_lines.extend(
        f'loadAmberParams "parameters/{item.bundle_name}"' for item in frcmods
    )
    leap_lines.extend(f'loadoff "parameters/{item.bundle_name}"' for item in libraries)
    leap_lines.extend(
        [
            'fana = loadPdb "candidate_amber_names.pdb"',
            "check fana",
            "charge fana",
            f"solvateOct fana {solvation['water_box']} {float(solvation['buffer_angstrom']):.3f}",
            f"addIons fana {solvation['neutralizing_ion']} 0",
            "saveAmberParm fana fana_system.prmtop fana_system.inpcrd",
            'savePdb fana "fana_system_solvated.pdb"',
            "quit",
        ]
    )
    (output_dir / "tleap.in").write_text("\n".join(leap_lines) + "\n", encoding="utf-8")

    minimization = parameterization["minimization"]
    cutoff = float(minimization["cutoff_angstrom"])
    stage1 = minimization["stage1"]
    stage2 = minimization["stage2"]
    stage1_text = f"""FANA restrained solvent minimization
&cntrl
  imin=1,
  maxcyc={int(stage1["maxcyc"])},
  ncyc={int(stage1["ncyc"])},
  ntb=1,
  cut={cutoff:.3f},
  ntpr=100,
  ntr=1,
  restraint_wt={float(stage1["restraint_wt"]):.3f},
  restraintmask='{stage1["restraint_mask"]}',
/
"""
    stage2_text = f"""FANA unrestrained minimization
&cntrl
  imin=1,
  maxcyc={int(stage2["maxcyc"])},
  ncyc={int(stage2["ncyc"])},
  ntb=1,
  cut={cutoff:.3f},
  ntpr=100,
  ntr=0,
/
"""
    (output_dir / "minimize_stage1.in").write_text(stage1_text, encoding="utf-8")
    (output_dir / "minimize_stage2.in").write_text(stage2_text, encoding="utf-8")

    run_script = """#!/usr/bin/env bash
set -euo pipefail

# Generated by Digital Polymerase. Review every file before running.
command -v tleap >/dev/null
command -v sander >/dev/null
command -v ambpdb >/dev/null

tleap -f tleap.in > tleap.log
sander -O -i minimize_stage1.in -o minimize_stage1.out -p fana_system.prmtop -c fana_system.inpcrd -r minimize_stage1.rst7 -ref fana_system.inpcrd
sander -O -i minimize_stage2.in -o minimize_stage2.out -p fana_system.prmtop -c minimize_stage1.rst7 -r minimize_stage2.rst7
ambpdb -p fana_system.prmtop -c minimize_stage2.rst7 > fana_minimized.pdb
"""
    run_path = output_dir / "run_minimization.sh"
    run_path.write_text(run_script, encoding="utf-8")
    run_path.chmod(0o644)
    shutil.copy2(
        parameter_manifest_path, output_dir / "parameter_manifest.snapshot.json"
    )
    shutil.copy2(
        readiness_manifest_path, output_dir / "readiness_manifest.snapshot.json"
    )

    readme = """# Prepared FANA Amber minimization bundle

This directory was generated only after the external-parameter manifest passed
Digital Polymerase's structural and provenance checks. No Amber command has
been executed.

Before running anything:

1. inspect `parameter_preflight.md` and both manifest snapshots;
2. confirm the copied parameter-file hashes;
3. inspect residue names and atom coverage in `candidate_amber_names.pdb`;
4. review `tleap.in`, both minimization control files, solvent, ions, cutoffs,
   restraints, terminal chemistry, and expected total charge;
5. run LEaP manually and reject any warning about unknown atoms, missing atom
   types, missing parameters, duplicate parameters, or charge inconsistency;
6. inspect energy, maximum gradient, structural drift, covalent geometry,
   C2′ stereochemistry, and sugar pucker after each minimization stage.

`run_minimization.sh` is intentionally written as a non-executed review
artifact. Run it manually only in an AmberTools environment after expert review.
"""
    (output_dir / "PREPARATION_README.md").write_text(readme, encoding="utf-8")
    return [*planned, *artifact_targets]


def prepare_fana_amber_minimization(
    candidate_pdb: str | Path,
    readiness_manifest: str | Path,
    parameter_manifest: str | Path,
    output_dir: str | Path,
    *,
    strict: bool = False,
    overwrite: bool = False,
) -> FANAParameterGateResult:
    """Validate external parameters and prepare an unexecuted Amber bundle."""

    candidate_path = Path(candidate_pdb)
    readiness_path = Path(readiness_manifest)
    parameter_path = Path(parameter_manifest)
    destination = Path(output_dir)
    structure = parse_pdb(candidate_path, strict=True)
    readiness = _load_json(readiness_path, "readiness manifest")
    manifest = _load_json(parameter_path, "parameter manifest")

    issues: list[str] = []
    warnings: list[str] = []
    _validate_readiness_manifest(
        candidate_path=candidate_path,
        readiness_path=readiness_path,
        readiness=readiness,
        issues=issues,
    )
    if manifest.get("schema_version") != SCHEMA_VERSION:
        issues.append(f"Parameter manifest schema_version must be {SCHEMA_VERSION}.")
    if manifest.get("target") != TARGET:
        issues.append("Parameter manifest target must be FANA.")
    if manifest.get("candidate_sha256") != _sha256(candidate_path):
        issues.append(
            "Parameter manifest candidate_sha256 does not match the candidate."
        )
    if manifest.get("readiness_manifest_sha256") != _sha256(readiness_path):
        issues.append(
            "Parameter manifest readiness_manifest_sha256 does not match the readiness manifest."
        )

    parameterization = manifest.get("parameterization")
    if not isinstance(parameterization, dict):
        parameterization = {}
        issues.append("parameterization must be an object.")
    if parameterization.get("engine") != "Amber":
        issues.append("parameterization.engine must be Amber.")

    protected_sources = {
        candidate_path.resolve(),
        readiness_path.resolve(),
        parameter_path.resolve(),
    }
    artifact_entries = parameterization.get("artifacts")
    if isinstance(artifact_entries, list):
        for entry in artifact_entries:
            if not isinstance(entry, dict):
                continue
            value = entry.get("path")
            if not isinstance(value, str) or not value.strip():
                continue
            declared = Path(value)
            if not declared.is_absolute():
                declared = parameter_path.parent / declared
            protected_sources.add(declared.resolve())
    preflight_targets = {
        (destination / "parameter_preflight.json").resolve(),
        (destination / "parameter_preflight.md").resolve(),
    }
    preflight_collisions = sorted(protected_sources & preflight_targets)
    if preflight_collisions:
        labels = ", ".join(str(path) for path in preflight_collisions)
        raise ValidationError(
            "Preflight output would overwrite an input; choose a separate output "
            "directory: " + labels
        )

    inventory = _candidate_inventory(structure)
    keys = sort_residue_keys(structure)
    segments = _consecutive_segments(keys)
    bases = {
        base_of(residue_name(structure[key]))
        for key in keys
        if base_of(residue_name(structure[key])) in {"A", "C", "G", "U"}
    }
    _validate_parent_force_field(parameterization, issues)
    _validate_generator(parameterization, bases, issues)
    internal_mappings = _validate_residue_mappings(
        parameterization=parameterization,
        inventory=inventory,
        issues=issues,
    )
    terminal_states = _validate_terminal_states(
        structure=structure,
        parameterization=parameterization,
        segments=segments,
        issues=issues,
    )
    artifacts = _validate_artifacts(
        parameterization=parameterization,
        manifest_dir=parameter_path.parent,
        issues=issues,
    )
    required_library_names = set(internal_mappings.values())
    for value in terminal_states.values():
        required_library_names.update(
            terminal.residue_name for terminal in value.values()
        )
    _validate_library_names(
        artifacts=artifacts,
        required_names=required_library_names,
        issues=issues,
    )
    _validate_coverage(parameterization, issues)
    _validate_charge_and_review(parameterization, issues)
    _validate_protocol(parameterization, issues)

    references = parameterization.get("references")
    if (
        not isinstance(references, list)
        or not references
        or not all(isinstance(item, str) and item.strip() for item in references)
    ):
        issues.append("parameterization.references must contain provenance links.")

    if any(len(segment) == 1 for segment in segments):
        issues.append(
            "Single-residue chain segments are not supported by this minimization "
            "preparer."
        )

    for command in ("tleap", "sander", "ambpdb"):
        if shutil.which(command) is None:
            warnings.append(
                f"Amber command {command!r} is unavailable; the bundle cannot run here."
            )

    generated_files: list[Path] = []
    status = "BLOCKED"
    if not issues:
        try:
            generated_files = _write_minimization_bundle(
                structure=structure,
                parameterization=parameterization,
                internal_mappings=internal_mappings,
                terminal_states=terminal_states,
                artifacts=artifacts,
                candidate_path=candidate_path,
                parameter_manifest_path=parameter_path,
                readiness_manifest_path=readiness_path,
                output_dir=destination,
                overwrite=overwrite,
            )
        except (OSError, ValidationError) as exc:
            issues.append(str(exc))
        else:
            status = "PREPARED_NOT_EXECUTED"

    preflight_json, preflight_report = _write_preflight(
        output_dir=destination,
        status=status,
        issues=issues,
        warnings=warnings,
        artifacts=artifacts,
        generated_files=generated_files,
    )
    generated_files.extend((preflight_json, preflight_report))
    result = FANAParameterGateResult(
        status=status,
        ready=status == "PREPARED_NOT_EXECUTED",
        output_dir=destination,
        issues=issues,
        warnings=warnings,
        artifacts=artifacts,
        generated_files=generated_files,
    )
    if strict and issues:
        raise ValidationError(
            "FANA external-parameter gate is blocked: " + " ".join(issues)
        )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize or validate a FANA external-parameter manifest."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    initialize = subparsers.add_parser(
        "init", help="Write a candidate-specific unresolved manifest template."
    )
    initialize.add_argument("--candidate", required=True, type=Path)
    initialize.add_argument("--readiness", required=True, type=Path)
    initialize.add_argument("--output", required=True, type=Path)

    prepare = subparsers.add_parser(
        "prepare", help="Validate external parameters and prepare Amber inputs."
    )
    prepare.add_argument("--candidate", required=True, type=Path)
    prepare.add_argument("--readiness", required=True, type=Path)
    prepare.add_argument("--parameters", required=True, type=Path)
    prepare.add_argument("--output-dir", required=True, type=Path)
    prepare.add_argument("--strict", action="store_true")
    prepare.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        path = initialize_fana_parameter_manifest(
            args.candidate, args.readiness, args.output
        )
        print(f"Wrote unresolved FANA parameter-manifest template: {path}")
        return 0
    result = prepare_fana_amber_minimization(
        args.candidate,
        args.readiness,
        args.parameters,
        args.output_dir,
        strict=args.strict,
        overwrite=args.overwrite,
    )
    print(
        f"FANA external-parameter gate: {result.status}; "
        f"{len(result.issues)} blockers, {len(result.warnings)} warnings"
    )
    return 0 if result.ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
