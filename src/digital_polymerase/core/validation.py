"""Validation helpers for Digital Polymerase candidate structures."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import numpy as np
from .atoms import is_hydrogen
from .pdb_io import sort_residue_keys, residue_name
from .residues import base_of, glycosidic_atom, required_base_oxygens
from .geometry import distance
from .registry import get_target_spec


@dataclass
class DistanceSummary:
    label: str
    measured: int
    missing: int
    failed: int
    mean: float
    minimum: float
    maximum: float
    lo: float
    hi: float

    @property
    def status(self) -> str:
        if self.measured == 0:
            return "NO_DATA"
        return "PASS" if self.failed == 0 and self.missing == 0 else "FAIL"


@dataclass
class ClashSummary:
    cutoff: float
    count: int
    minimum_distance: float
    atom_pairs_checked: int


def _summary(label, vals, missing, lo, hi):
    failed = sum(1 for v in vals if not (lo <= v <= hi))
    if vals:
        mean, mn, mx = float(np.mean(vals)), float(np.min(vals)), float(np.max(vals))
    else:
        mean = mn = mx = float("nan")
    return DistanceSummary(label, len(vals), missing, failed, mean, mn, mx, lo, hi)


def validate_intra_residue_distance(structure, atom_a, atom_b, lo, hi, *, label=None):
    vals = []
    missing = 0
    for k in sort_residue_keys(structure):
        r = structure[k]
        if atom_a not in r or atom_b not in r:
            missing += 1
            continue
        vals.append(distance(r[atom_a].coords, r[atom_b].coords))
    return _summary(label or f"{atom_a}→{atom_b}", vals, missing, lo, hi)


def validate_inter_residue_distance(
    structure,
    atom_left,
    atom_right,
    lo,
    hi,
    *,
    same_chain_consecutive_only=True,
    label=None,
):
    vals = []
    missing = 0
    ks = sort_residue_keys(structure)
    for lk, rk in zip(ks[:-1], ks[1:]):
        if same_chain_consecutive_only and (
            lk[0] != rk[0] or rk[1] != lk[1] + 1 or lk[2] or rk[2]
        ):
            continue
        left, right = structure[lk], structure[rk]
        if atom_left not in left or atom_right not in right:
            missing += 1
            continue
        vals.append(distance(left[atom_left].coords, right[atom_right].coords))
    return _summary(label or f"{atom_left}(i)→{atom_right}(i+1)", vals, missing, lo, hi)


def validate_base_attachment(structure, *, attachment_atom, lo, hi, label=None):
    vals = []
    missing = 0
    for k in sort_residue_keys(structure):
        r = structure[k]
        b = base_of(residue_name(r))
        gly = glycosidic_atom(b)
        if attachment_atom not in r or gly not in r:
            missing += 1
            continue
        vals.append(distance(r[attachment_atom].coords, r[gly].coords))
    return _summary(label or f"{attachment_atom}→glycosidic N", vals, missing, lo, hi)


def validate_required_atoms(
    structure, required_atoms, *, label="required atoms present"
):
    missing = 0
    residues = 0
    for k in sort_residue_keys(structure):
        residues += 1
        missing += sum(1 for a in required_atoms if a not in structure[k])
    return {
        "label": label,
        "residues": residues,
        "required_per_residue": len(required_atoms),
        "missing": missing,
        "status": "PASS" if missing == 0 else "FAIL",
    }


def validate_required_base_oxygens(structure):
    expected = 0
    missing = 0
    for k in sort_residue_keys(structure):
        r = structure[k]
        b = base_of(residue_name(r))
        for a in required_base_oxygens(b):
            expected += 1
            if a not in r:
                missing += 1
    return {
        "label": "required base oxygens present",
        "expected": expected,
        "missing": missing,
        "status": "PASS" if missing == 0 else "FAIL",
    }


def validate_target_geometry(structure, target: str) -> dict[str, Any]:
    spec = get_target_spec(target)
    results = {}
    results["required_atoms"] = validate_required_atoms(
        structure,
        spec.get("backbone_atoms", []),
        label=f"{target} required backbone atoms present",
    )
    lo, hi = spec.get("base_attachment_range", [1.20, 1.90])
    results["base_attachment"] = validate_base_attachment(
        structure,
        attachment_atom=spec["base_attachment_atom"],
        lo=float(lo),
        hi=float(hi),
    )
    for link in spec.get("linkage", []):
        label = f"{link['left']}→{link['right']}"
        if link.get("same_residue", False):
            results[label] = validate_intra_residue_distance(
                structure,
                link["left"],
                link["right"],
                float(link["lo"]),
                float(link["hi"]),
                label=label,
            )
        else:
            results[label] = validate_inter_residue_distance(
                structure,
                link["left"],
                link["right"],
                float(link["lo"]),
                float(link["hi"]),
                label=label,
            )
    for label, check in spec.get("distance_checks", {}).items():
        a, b, lo, hi = check
        results[label] = validate_intra_residue_distance(
            structure, a, b, float(lo), float(hi), label=label
        )
    results["base_oxygen_audit"] = validate_required_base_oxygens(structure)
    return results


def clash_summary(structure, *, cutoff=1.00, skip_same_residue=True):
    atoms = []
    for k in sort_residue_keys(structure):
        for name, atom in structure[k].items():
            if not is_hydrogen(atom):
                atoms.append((k, name, atom))
    count = 0
    checked = 0
    mind = float("inf")
    for i, (ki, _, ai) in enumerate(atoms):
        for kj, _, aj in atoms[i + 1 :]:
            if skip_same_residue and ki == kj:
                continue
            checked += 1
            d = distance(ai.coords, aj.coords)
            mind = min(mind, d)
            if d < cutoff:
                count += 1
    return ClashSummary(
        cutoff, count, mind if mind < float("inf") else float("nan"), checked
    )
