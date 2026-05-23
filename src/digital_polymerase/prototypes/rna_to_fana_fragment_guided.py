#!/usr/bin/env python3
"""
Prototype 003A: Chain-Preserving RNA to FANA Converter

Digital Polymerase / XNA World Project

This script generates a FANA-like candidate PDB from an RNA PDB using a FANA
template or fragment as a local sugar/substituent geometry donor.

Core idea:
- Preserve the RNA polymer chain atoms that define backbone continuity.
- Replace the RNA 2'-OH chemistry with FANA-like 2'-fluoro geometry.
- Preserve RNA nucleobase atoms and sequence.
- Validate chain continuity and C2'-F geometry.

Important:
- This is NOT a chemically or physically validated FANA modeling package.
- This is an experimental chain-preserving candidate-structure generator.
- The output requires visual inspection, geometry checks, energy minimization,
  force-field support, and expert chemical review before scientific use.

Default mode:
    chain-preserving

For each RNA residue:
1. Choose a FANA residue template by base class.
2. Align template local frame onto source RNA local frame using Kabsch alignment.
3. Preserve chain-continuity atoms from the RNA residue:
   P, OP1/OP2/O1P/O2P, O5', C5', C4', O4', C3', O3', C1'
4. Replace local 2' chemistry with transformed FANA C2' and F/F2' atom.
5. Preserve RNA base atoms.
6. Export FANA-like candidate PDB.
7. Report chain-continuity and C2'-F validation.

Recommended interpretation:
    RNA chain/base framework + FANA local C2'/F geometry
    = exploratory FANA-like candidate structure, not a validated FANA polymer.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np


ResidueKey = Tuple[str, int, str]

RNA_BASES = {"A", "U", "G", "C"}

CHAIN_PRESERVE_ATOMS = {
    "P", "OP1", "OP2", "O1P", "O2P",
    "O5'", "C5'", "C4'", "O4'", "C3'", "O3'", "C1'",
}

# RNA O2' is intentionally not preserved for FANA.
FANA_LOCAL_ATOMS = {"C2'", "F2'", "F", "H2'"}

DEFAULT_ANCHORS = ["C1'", "C3'", "C4'", "O4'"]

BACKBONE_ORDER = [
    "P", "OP1", "OP2", "O1P", "O2P", "O5'", "C5'", "C4'", "O4'",
    "C3'", "O3'", "C2'", "F2'", "H2'", "C1'",
]


@dataclass
class Atom:
    record: str
    atom_name: str
    res_name: str
    chain: str
    res_num: int
    insertion_code: str
    coords: np.ndarray
    occupancy: float
    temp_factor: float
    element: str


@dataclass
class ConversionRecord:
    source_key: ResidueKey
    source_res_name: str
    source_base: str
    target_res_name: str
    template_key: ResidueKey
    template_res_name: str
    template_base_class: str
    anchor_atoms: List[str]
    anchor_rmsd: float
    c2f_distance: Optional[float]
    note: str


@dataclass
class DistanceRecord:
    label: str
    chain: str
    left_res_num: int
    left_icode: str
    left_atom: str
    right_res_num: int
    right_icode: str
    right_atom: str
    distance: float
    expected_min: float
    expected_max: float
    status: str
    note: str = ""


@dataclass
class DistanceSummary:
    label: str
    expected_min: float
    expected_max: float
    measured: int
    missing: int
    failed: int
    mean: float
    minimum: float
    maximum: float
    records: List[DistanceRecord]


def infer_element(atom_name: str, pdb_element: str = "") -> str:
    elem = (pdb_element or "").strip()
    if elem and re.match(r"^[A-Za-z]{1,2}$", elem):
        elem = elem.upper()
        if elem in {"C", "N", "O", "P", "H", "S", "F", "CL", "BR", "I"}:
            return elem[0] + elem[1:].lower()

    cleaned = re.sub(r"[^A-Za-z]", "", atom_name)
    if not cleaned:
        return ""
    if atom_name.strip().upper().startswith("F"):
        return "F"
    first = cleaned[0].upper()
    if first in {"C", "N", "O", "P", "H", "S", "F"}:
        return first
    return first


def parse_pdb(path: Path) -> Dict[ResidueKey, Dict[str, Atom]]:
    residues: Dict[ResidueKey, Dict[str, Atom]] = defaultdict(dict)

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue

        try:
            record = line[0:6].strip()
            atom_name = line[12:16].strip()
            res_name = line[17:20].strip()
            chain = line[21].strip() if len(line) > 21 and line[21].strip() else "A"
            res_num = int(line[22:26].strip())
            insertion_code = line[26].strip() if len(line) > 26 else ""

            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())

            occ_str = line[54:60].strip() if len(line) >= 60 else ""
            temp_str = line[60:66].strip() if len(line) >= 66 else ""
            elem_str = line[76:78].strip() if len(line) >= 78 else ""

            occupancy = float(occ_str) if occ_str else 1.0
            temp_factor = float(temp_str) if temp_str else 0.0
            element = infer_element(atom_name, elem_str)

            key = (chain, res_num, insertion_code)
            residues[key][atom_name] = Atom(
                record=record,
                atom_name=atom_name,
                res_name=res_name,
                chain=chain,
                res_num=res_num,
                insertion_code=insertion_code,
                coords=np.array([x, y, z], dtype=float),
                occupancy=occupancy,
                temp_factor=temp_factor,
                element=element,
            )
        except Exception:
            continue

    return dict(residues)


def sorted_residue_keys(residues: Dict[ResidueKey, Dict[str, Atom]]) -> List[ResidueKey]:
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def residue_name(residue: Dict[str, Atom]) -> str:
    return next(iter(residue.values())).res_name


def normalize_base_from_residue_name(res_name: str) -> str:
    res = res_name.strip().upper()
    if res in RNA_BASES:
        return res

    # Known FANA residues in 2KP4: GFL, CFL, TAF, A5L.
    if res.startswith("G"):
        return "G"
    if res.startswith("A"):
        return "A"
    if res.startswith("C"):
        return "C"
    if res.startswith("U") or res.startswith("T"):
        return "U"

    return res[0] if res else "N"


def residue_sequence(residues: Dict[ResidueKey, Dict[str, Atom]]) -> str:
    return "".join(normalize_base_from_residue_name(residue_name(residues[k])) for k in sorted_residue_keys(residues))


def is_backbone_atom(atom_name: str) -> bool:
    if atom_name in CHAIN_PRESERVE_ATOMS or atom_name in {"C2'", "O2'", "F2'", "F", "H2'"}:
        return True
    if "'" in atom_name:
        return True
    return False


def split_backbone_base(residue: Dict[str, Atom]) -> Tuple[Dict[str, Atom], Dict[str, Atom]]:
    backbone = {name: atom for name, atom in residue.items() if is_backbone_atom(name)}
    base = {name: atom for name, atom in residue.items() if not is_backbone_atom(name)}
    return backbone, base


def kabsch(mobile: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    if mobile.shape != target.shape:
        raise ValueError("mobile and target must have the same shape")
    if mobile.ndim != 2 or mobile.shape[1] != 3:
        raise ValueError("coordinate arrays must be N x 3")
    if mobile.shape[0] < 3:
        raise ValueError("at least three anchor atoms are required")

    mobile_center = mobile.mean(axis=0)
    target_center = target.mean(axis=0)
    m = mobile - mobile_center
    t = target - target_center

    cov = m.T @ t
    u, _s, vt = np.linalg.svd(cov)
    r = vt.T @ u.T

    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T

    trans = target_center - r @ mobile_center
    transformed = (r @ mobile.T).T + trans
    rmsd = float(np.sqrt(np.mean(np.sum((transformed - target) ** 2, axis=1))))
    return r, trans, rmsd


def apply_transform(coords: np.ndarray, r: np.ndarray, t: np.ndarray) -> np.ndarray:
    return r @ coords + t


def clone_atom(
    atom: Atom,
    *,
    coords: Optional[np.ndarray] = None,
    atom_name: Optional[str] = None,
    res_name: Optional[str] = None,
    chain: Optional[str] = None,
    res_num: Optional[int] = None,
    insertion_code: Optional[str] = None,
    record: str = "HETATM",
    element: Optional[str] = None,
) -> Atom:
    out_atom_name = atom_name if atom_name is not None else atom.atom_name
    return Atom(
        record=record if record is not None else atom.record,
        atom_name=out_atom_name,
        res_name=res_name if res_name is not None else atom.res_name,
        chain=chain if chain is not None else atom.chain,
        res_num=res_num if res_num is not None else atom.res_num,
        insertion_code=insertion_code if insertion_code is not None else atom.insertion_code,
        coords=np.array(coords if coords is not None else atom.coords, dtype=float),
        occupancy=atom.occupancy,
        temp_factor=atom.temp_factor,
        element=element if element is not None else infer_element(out_atom_name, atom.element),
    )


def build_template_index(template: Dict[ResidueKey, Dict[str, Atom]]) -> Dict[str, Tuple[ResidueKey, Dict[str, Atom]]]:
    index: Dict[str, Tuple[ResidueKey, Dict[str, Atom]]] = {}
    for key in sorted_residue_keys(template):
        res = template[key]
        base = normalize_base_from_residue_name(residue_name(res))
        index.setdefault(base, (key, res))
    return index


def select_template_for_base(
    source_base: str,
    template_index: Dict[str, Tuple[ResidueKey, Dict[str, Atom]]],
) -> Tuple[ResidueKey, Dict[str, Atom], str, str]:
    source_base = source_base.upper()

    if source_base in template_index:
        key, res = template_index[source_base]
        return key, res, source_base, "exact base-class template"

    # RNA U uses T-like FANA geometry if no U-like FANA template exists.
    if source_base == "U" and "U" in template_index:
        key, res = template_index["U"]
        return key, res, "U", "U/T-like FANA template used for RNA U"

    if source_base == "U" and "T" in template_index:
        key, res = template_index["T"]
        return key, res, "T", "T-like FANA geometry donor used for RNA U"

    # Because normalize maps T to U, this usually catches TAF as U already.

    if source_base == "A" and "G" in template_index:
        key, res = template_index["G"]
        return key, res, "G", "purine fallback: A uses G-like FANA template"

    if source_base == "G" and "A" in template_index:
        key, res = template_index["A"]
        return key, res, "A", "purine fallback: G uses A-like FANA template"

    if source_base == "C" and "U" in template_index:
        key, res = template_index["U"]
        return key, res, "U", "pyrimidine fallback: C uses U/T-like FANA template"

    if source_base == "U" and "C" in template_index:
        key, res = template_index["C"]
        return key, res, "C", "pyrimidine fallback: U uses C-like FANA template"

    first = sorted(template_index.keys())[0]
    key, res = template_index[first]
    return key, res, first, f"last-resort fallback: uses {first}-like FANA template"


def target_fana_residue_name(source_base: str, naming_policy: str = "template-observed") -> str:
    source_base = source_base.upper()

    if naming_policy == "template-observed":
        return {"A": "A5L", "U": "UFL", "G": "GFL", "C": "CFL"}.get(source_base, "FNA")

    if naming_policy == "provisional":
        return {"A": "AFL", "U": "UFL", "G": "GFL", "C": "CFL"}.get(source_base, "FNA")

    raise ValueError(f"Unsupported naming policy: {naming_policy}")


def available_anchors(source: Dict[str, Atom], template: Dict[str, Atom], requested: Iterable[str]) -> List[str]:
    return [a for a in requested if a in source and a in template]


def find_template_fluorine(template_residue: Dict[str, Atom]) -> Optional[str]:
    for name in ["F2'", "F", "2F", "F2*"]:
        if name in template_residue:
            return name
    # last-resort: any atom that starts with F and is element F
    for name, atom in template_residue.items():
        if name.upper().startswith("F") or atom.element.upper() == "F":
            return name
    return None


def convert_residue_chain_preserving(
    source_key: ResidueKey,
    source_residue: Dict[str, Atom],
    template_key: ResidueKey,
    template_residue: Dict[str, Atom],
    *,
    target_res_name: str,
    anchors: List[str],
) -> Tuple[Dict[str, Atom], float, List[str], Optional[float]]:
    """
    Chain-preserving RNA -> FANA local conversion.

    Preserves source RNA chain atoms and bases.
    Replaces C2' and adds F2' from locally aligned FANA template.
    Removes RNA O2'.
    """
    source_chain, source_res_num, source_icode = source_key

    used_anchors = available_anchors(source_residue, template_residue, anchors)
    if len(used_anchors) < 3:
        raise ValueError(f"Not enough anchors for {source_key}: {used_anchors}")

    mobile = np.array([template_residue[a].coords for a in used_anchors])
    target = np.array([source_residue[a].coords for a in used_anchors])
    r, t, rmsd = kabsch(mobile, target)

    output: Dict[str, Atom] = {}

    source_backbone, source_base = split_backbone_base(source_residue)

    # Preserve source RNA chain atoms, but drop O2' and C2' because FANA local 2' geometry is template-derived.
    for atom_name, atom in source_backbone.items():
        if atom_name in {"O2'", "C2'", "H2'"}:
            continue
        if atom_name in CHAIN_PRESERVE_ATOMS:
            output[atom_name] = clone_atom(
                atom,
                res_name=target_res_name,
                chain=source_chain,
                res_num=source_res_num,
                insertion_code=source_icode,
                record="HETATM",
            )

    # Preserve source RNA nucleobases.
    for atom_name, atom in source_base.items():
        output[atom_name] = clone_atom(
            atom,
            res_name=target_res_name,
            chain=source_chain,
            res_num=source_res_num,
            insertion_code=source_icode,
            record="HETATM",
        )

    # Add transformed FANA C2'.
    if "C2'" not in template_residue:
        raise ValueError(f"Template residue {template_key} lacks C2'")

    c2_atom = template_residue["C2'"]
    c2_coords = apply_transform(c2_atom.coords, r, t)
    output["C2'"] = clone_atom(
        c2_atom,
        coords=c2_coords,
        atom_name="C2'",
        res_name=target_res_name,
        chain=source_chain,
        res_num=source_res_num,
        insertion_code=source_icode,
        record="HETATM",
        element="C",
    )

    # Add transformed FANA fluorine, standardized as F2'.
    f_name = find_template_fluorine(template_residue)
    c2f_distance = None
    if f_name:
        f_atom = template_residue[f_name]
        f_coords = apply_transform(f_atom.coords, r, t)
        output["F2'"] = clone_atom(
            f_atom,
            coords=f_coords,
            atom_name="F2'",
            res_name=target_res_name,
            chain=source_chain,
            res_num=source_res_num,
            insertion_code=source_icode,
            record="HETATM",
            element="F",
        )
        c2f_distance = float(np.linalg.norm(output["C2'"].coords - output["F2'"].coords))

    # Add transformed H2' if available and not already present.
    if "H2'" in template_residue:
        h2_atom = template_residue["H2'"]
        h2_coords = apply_transform(h2_atom.coords, r, t)
        output["H2'"] = clone_atom(
            h2_atom,
            coords=h2_coords,
            atom_name="H2'",
            res_name=target_res_name,
            chain=source_chain,
            res_num=source_res_num,
            insertion_code=source_icode,
            record="HETATM",
            element="H",
        )

    return output, rmsd, used_anchors, c2f_distance


def atom_sort_key(atom_name: str) -> Tuple[int, str]:
    if atom_name in BACKBONE_ORDER:
        return (BACKBONE_ORDER.index(atom_name), atom_name)
    return (100, atom_name)


def format_pdb_atom_line(serial: int, atom: Atom) -> str:
    record = atom.record or "HETATM"
    atom_name = atom.atom_name[:4]
    res_name = atom.res_name[:3]
    chain = (atom.chain or "A")[:1]
    icode = (atom.insertion_code or " ")[:1]
    elem = (atom.element or infer_element(atom_name))[:2].rjust(2)

    return (
        f"{record:<6s}"
        f"{serial:5d} "
        f"{atom_name:>4s} "
        f"{res_name:>3s} "
        f"{chain:1s}"
        f"{atom.res_num:4d}"
        f"{icode:1s}   "
        f"{atom.coords[0]:8.3f}"
        f"{atom.coords[1]:8.3f}"
        f"{atom.coords[2]:8.3f}"
        f"{atom.occupancy:6.2f}"
        f"{atom.temp_factor:6.2f}"
        f"{'':>10s}"
        f"{elem:>2s}"
    )


def write_pdb(residues: Dict[ResidueKey, Dict[str, Atom]], output_path: Path, *, source_sequence: str, template_summary: str) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        f.write("REMARK   Digital Polymerase Prototype 003A\n")
        f.write("REMARK   Chain-preserving RNA to FANA candidate reconstruction\n")
        f.write(f"REMARK   Source RNA sequence: {source_sequence}\n")
        f.write(f"REMARK   FANA template summary: {template_summary}\n")
        f.write("REMARK   Method: RNA chain/base geometry preserved; FANA C2'/F geometry introduced\n")
        f.write("REMARK   WARNING: Computational candidate only\n")
        f.write("REMARK   WARNING: Not energy-minimized, force-field-validated, or experimentally verified\n")
        f.write("REMARK   WARNING: FANA residue names are provisional and may need adjustment\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")

        serial = 1
        for key in sorted_residue_keys(residues):
            residue = residues[key]
            for atom_name in sorted(residue.keys(), key=atom_sort_key):
                f.write(format_pdb_atom_line(serial, residue[atom_name]) + "\n")
                serial += 1
        f.write("END\n")


def _summarize(label: str, records: List[DistanceRecord], missing: int, expected_min: float, expected_max: float) -> DistanceSummary:
    distances = [r.distance for r in records]
    failed = sum(1 for r in records if r.status == "FAIL")
    if distances:
        mean = float(np.mean(distances))
        minimum = float(np.min(distances))
        maximum = float(np.max(distances))
    else:
        mean = minimum = maximum = float("nan")
    return DistanceSummary(label, expected_min, expected_max, len(records), missing, failed, mean, minimum, maximum, records)


def validate_inter_residue_distance(
    residues: Dict[ResidueKey, Dict[str, Atom]],
    *,
    atom_left: str,
    atom_right: str,
    expected_min: float,
    expected_max: float,
    label: str,
    skip_numbering_gaps: bool = True,
) -> DistanceSummary:
    records: List[DistanceRecord] = []
    missing = 0
    keys = sorted_residue_keys(residues)

    for lk, rk in zip(keys[:-1], keys[1:]):
        lc, ln, li = lk
        rc, rn, ri = rk
        if lc != rc:
            continue
        if skip_numbering_gaps and (rn != ln + 1 or li or ri):
            continue

        left = residues[lk]
        right = residues[rk]
        if atom_left not in left or atom_right not in right:
            missing += 1
            continue

        d = float(np.linalg.norm(left[atom_left].coords - right[atom_right].coords))
        status = "PASS" if expected_min <= d <= expected_max else "FAIL"
        records.append(DistanceRecord(label, lc, ln, li, atom_left, rn, ri, atom_right, d, expected_min, expected_max, status))

    return _summarize(label, records, missing, expected_min, expected_max)


def validate_intra_residue_distance(
    residues: Dict[ResidueKey, Dict[str, Atom]],
    *,
    atom_a: str,
    atom_b: str,
    expected_min: float,
    expected_max: float,
    label: str,
) -> DistanceSummary:
    records: List[DistanceRecord] = []
    missing = 0

    for key in sorted_residue_keys(residues):
        chain, resnum, icode = key
        residue = residues[key]
        if atom_a not in residue or atom_b not in residue:
            missing += 1
            continue
        d = float(np.linalg.norm(residue[atom_a].coords - residue[atom_b].coords))
        status = "PASS" if expected_min <= d <= expected_max else "FAIL"
        records.append(DistanceRecord(label, chain, resnum, icode, atom_a, resnum, icode, atom_b, d, expected_min, expected_max, status))

    return _summarize(label, records, missing, expected_min, expected_max)


def validation_status(summary: DistanceSummary) -> str:
    if summary.measured == 0:
        return "NO_DATA"
    return "PASS" if summary.failed == 0 else "FAIL"


def distance_summary_table(source_summaries: Dict[str, DistanceSummary], output_summaries: Dict[str, DistanceSummary]) -> str:
    labels = sorted(set(source_summaries) | set(output_summaries))
    lines = [
        "| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for label in labels:
        for name, dct in [("source", source_summaries), ("output", output_summaries)]:
            summary = dct.get(label)
            if summary is None:
                continue
            lines.append(
                f"| {label} | {name} | {summary.measured} | {summary.missing} | {summary.failed} | "
                f"{summary.mean:.3f} | {summary.minimum:.3f} | {summary.maximum:.3f} | "
                f"{summary.expected_min:.2f}–{summary.expected_max:.2f} | {validation_status(summary)} |"
            )
    return "\n".join(lines)


def failed_link_table(summary: DistanceSummary, n: int = 20) -> str:
    failed = [r for r in summary.records if r.status == "FAIL"]
    if not failed:
        return "No failed links detected."

    def deviation(r: DistanceRecord) -> float:
        if r.distance < r.expected_min:
            return r.expected_min - r.distance
        if r.distance > r.expected_max:
            return r.distance - r.expected_max
        return 0.0

    failed = sorted(failed, key=deviation, reverse=True)[:n]
    lines = [
        "| Rank | Link | Distance (Å) | Expected range (Å) | Status |",
        "|---:|---|---:|---|---|",
    ]
    for i, r in enumerate(failed, start=1):
        link = f"{r.chain}{r.left_res_num}{r.left_icode}:{r.left_atom} → {r.chain}{r.right_res_num}{r.right_icode}:{r.right_atom}"
        lines.append(f"| {i} | `{link}` | {r.distance:.3f} | {r.expected_min:.2f}–{r.expected_max:.2f} | {r.status} |")
    return "\n".join(lines)


def build_validation_summaries(
    source: Dict[ResidueKey, Dict[str, Atom]],
    output: Dict[ResidueKey, Dict[str, Atom]],
    *,
    skip_numbering_gaps: bool = True,
) -> Tuple[Dict[str, DistanceSummary], Dict[str, DistanceSummary]]:
    source_summaries = {
        "O3'(i)→P(i+1)": validate_inter_residue_distance(source, atom_left="O3'", atom_right="P", expected_min=1.4, expected_max=1.8, label="O3'(i)→P(i+1)", skip_numbering_gaps=skip_numbering_gaps),
        "P(i)→O5'(i)": validate_intra_residue_distance(source, atom_a="P", atom_b="O5'", expected_min=1.4, expected_max=1.8, label="P(i)→O5'(i)"),
        "C1'→C2'": validate_intra_residue_distance(source, atom_a="C1'", atom_b="C2'", expected_min=1.35, expected_max=1.75, label="C1'→C2'"),
        "C2'→C3'": validate_intra_residue_distance(source, atom_a="C2'", atom_b="C3'", expected_min=1.35, expected_max=1.75, label="C2'→C3'"),
    }

    output_summaries = {
        "O3'(i)→P(i+1)": validate_inter_residue_distance(output, atom_left="O3'", atom_right="P", expected_min=1.4, expected_max=1.8, label="O3'(i)→P(i+1)", skip_numbering_gaps=skip_numbering_gaps),
        "P(i)→O5'(i)": validate_intra_residue_distance(output, atom_a="P", atom_b="O5'", expected_min=1.4, expected_max=1.8, label="P(i)→O5'(i)"),
        "C1'→C2'": validate_intra_residue_distance(output, atom_a="C1'", atom_b="C2'", expected_min=1.35, expected_max=1.75, label="C1'→C2'"),
        "C2'→C3'": validate_intra_residue_distance(output, atom_a="C2'", atom_b="C3'", expected_min=1.35, expected_max=1.75, label="C2'→C3'"),
        "C2'→F2'": validate_intra_residue_distance(output, atom_a="C2'", atom_b="F2'", expected_min=1.25, expected_max=1.50, label="C2'→F2'"),
    }

    return source_summaries, output_summaries


def write_report(
    report_path: Path,
    *,
    source_path: Path,
    template_path: Path,
    output_path: Path,
    source_sequence: str,
    template_index: Dict[str, Tuple[ResidueKey, Dict[str, Atom]]],
    records: List[ConversionRecord],
    anchors: List[str],
    naming_policy: str,
    source_validation: Dict[str, DistanceSummary],
    output_validation: Dict[str, DistanceSummary],
    skip_numbering_gaps: bool,
) -> None:
    rmsds = [r.anchor_rmsd for r in records]
    c2f = [r.c2f_distance for r in records if r.c2f_distance is not None]

    template_lines = []
    for base, (key, res) in sorted(template_index.items()):
        template_lines.append(f"- `{base}` → `{residue_name(res)}` at chain `{key[0]}`, residue `{key[1]}{key[2]}`")

    record_lines = []
    for i, rec in enumerate(records, start=1):
        c2f_str = f"{rec.c2f_distance:.4f}" if rec.c2f_distance is not None else "NA"
        record_lines.append(
            f"| {i} | {rec.source_key[0]}{rec.source_key[1]}{rec.source_key[2]} | {rec.source_base} | "
            f"{rec.target_res_name} | {rec.template_res_name} {rec.template_key[0]}{rec.template_key[1]}{rec.template_key[2]} | "
            f"{rec.anchor_rmsd:.4f} | {c2f_str} | {rec.note} |"
        )

    chain_status = validation_status(output_validation["O3'(i)→P(i+1)"])
    f_status = validation_status(output_validation["C2'→F2'"])

    report = f"""# RNA → FANA Chain-Preserving Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 003A  
**Method:** Chain-preserving RNA → FANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `{chain_status}`  
**C2′–F status:** `{f_status}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- FANA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source Sequence

```text
{source_sequence}
```

---

## Template Index

The FANA template provides local sugar/substituent geometry donors.

{chr(10).join(template_lines)}

Notes:

- RNA `U` is mapped to a U/T-like FANA geometry donor when the template uses thymine-like FANA residues.
- RNA bases are preserved by default; residue labels are provisional.

---

## Method Summary

This prototype uses a **chain-preserving** strategy.

For each RNA residue:

1. determine source RNA base identity
2. select the best available FANA template residue
3. align FANA template anchor atoms onto RNA anchor atoms using Kabsch alignment
4. preserve RNA chain-continuity atoms and RNA nucleobase atoms
5. replace RNA 2′ chemistry by introducing FANA-like `C2′` and `F2′`
6. remove RNA `O2′`
7. export a FANA-like candidate residue
8. validate inter-residue chain continuity and C2′–F geometry

This is **not** a full-template reconstruction.

---

## Settings

- Anchor atoms: `{", ".join(anchors)}`
- Residue naming policy: `{naming_policy}`
- Skip residue-numbering gaps in inter-residue validation: `{skip_numbering_gaps}`

---

## Alignment Summary

- Converted residues: `{len(records)}`
- Mean anchor RMSD: `{np.mean(rmsds):.4f} Å`
- Maximum anchor RMSD: `{np.max(rmsds):.4f} Å`
- Mean C2′–F distance: `{np.mean(c2f) if c2f else float('nan'):.4f} Å`
- Maximum C2′–F distance: `{np.max(c2f) if c2f else float('nan'):.4f} Å`

Important:

> Chain continuity is preserved by keeping the RNA polymer-chain atoms. FANA-like local 2′ geometry is introduced from the FANA template.

---

## Structural Validation

{distance_summary_table(source_validation, output_validation)}

### Worst output O3′–P links

{failed_link_table(output_validation["O3'(i)→P(i+1)"], n=20)}

### Worst output C2′–F2′ distances

{failed_link_table(output_validation["C2'→F2'"], n=20)}

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | C2′–F (Å) | Note |
|---:|---|---|---|---|---:|---:|---|
{chr(10).join(record_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a FANA-like candidate structure generated using chain-preserving local reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed FANA structure.

---

## Important Limitations

- This is not energy-minimized.
- No force-field parameters are generated.
- RNA bases are preserved.
- RNA chain atoms are preserved to maintain polymer continuity.
- FANA-like C2′ and F2′ geometry is introduced from a template, but stereochemistry still needs expert review.
- Connectivity is not explicitly written with `CONECT` records.
- Residue names are provisional and may need adjustment for downstream tools.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect the output in PyMOL, ChimeraX, VMD, or Mol*.
2. Check residue completeness and atom naming.
3. Inspect base-backbone attachment geometry.
4. Review O3′–P and C2′–F validation tables.
5. Compare local C2′/F geometry with the FANA template.
6. Add explicit topology/connectivity in future versions.
7. Perform energy minimization with appropriate force-field support.
8. Run short MD only after force-field/topology validation.

---

## Development Note

Prototype 003A applies the successful ANA 002A.2 lesson:

```text
Do not sacrifice chain continuity for local XNA geometry.
```

The strategy is therefore:

```text
preserve chain first
introduce XNA-local chemistry second
validate explicitly
```
"""
    report_path.write_text(report, encoding="utf-8")


def convert(
    source_rna_path: Path,
    fana_template_path: Path,
    output_path: Path,
    *,
    report_path: Optional[Path] = None,
    anchors: List[str] = DEFAULT_ANCHORS,
    naming_policy: str = "template-observed",
    skip_numbering_gaps: bool = True,
) -> List[ConversionRecord]:
    source = parse_pdb(source_rna_path)
    template = parse_pdb(fana_template_path)

    if not source:
        raise ValueError(f"No atoms/residues parsed from source RNA PDB: {source_rna_path}")
    if not template:
        raise ValueError(f"No atoms/residues parsed from FANA template PDB: {fana_template_path}")

    template_index = build_template_index(template)
    if not template_index:
        raise ValueError("Could not build FANA template index")

    output_residues: Dict[ResidueKey, Dict[str, Atom]] = {}
    records: List[ConversionRecord] = []
    source_sequence = residue_sequence(source)

    for skey in sorted_residue_keys(source):
        sres = source[skey]
        sres_name = residue_name(sres)
        sbase = normalize_base_from_residue_name(sres_name)

        tkey, tres, tbase, note = select_template_for_base(sbase, template_index)
        tres_name = residue_name(tres)
        target_name = target_fana_residue_name(sbase, naming_policy=naming_policy)

        out_res, rmsd, used_anchors, c2f_distance = convert_residue_chain_preserving(
            skey,
            sres,
            tkey,
            tres,
            target_res_name=target_name,
            anchors=anchors,
        )

        output_residues[skey] = out_res

        records.append(
            ConversionRecord(
                source_key=skey,
                source_res_name=sres_name,
                source_base=sbase,
                target_res_name=target_name,
                template_key=tkey,
                template_res_name=tres_name,
                template_base_class=tbase,
                anchor_atoms=used_anchors,
                anchor_rmsd=rmsd,
                c2f_distance=c2f_distance,
                note=note,
            )
        )

    template_summary = ", ".join(
        f"{base}:{residue_name(res)}@{key[0]}{key[1]}{key[2]}"
        for base, (key, res) in sorted(template_index.items())
    )

    write_pdb(output_residues, output_path, source_sequence=source_sequence, template_summary=template_summary)

    source_validation, output_validation = build_validation_summaries(
        source,
        output_residues,
        skip_numbering_gaps=skip_numbering_gaps,
    )

    if report_path:
        write_report(
            report_path,
            source_path=source_rna_path,
            template_path=fana_template_path,
            output_path=output_path,
            source_sequence=source_sequence,
            template_index=template_index,
            records=records,
            anchors=anchors,
            naming_policy=naming_policy,
            source_validation=source_validation,
            output_validation=output_validation,
            skip_numbering_gaps=skip_numbering_gaps,
        )

    o3p = output_validation["O3'(i)→P(i+1)"]
    c2f = output_validation["C2'→F2'"]
    rmsds = [r.anchor_rmsd for r in records]

    print("=" * 80)
    print("Digital Polymerase Prototype 003A")
    print("Chain-preserving RNA → FANA candidate reconstruction")
    print("=" * 80)
    print(f"Source RNA: {source_rna_path}")
    print(f"FANA template: {fana_template_path}")
    print(f"Output PDB: {output_path}")
    if report_path:
        print(f"Report: {report_path}")
    print(f"Converted residues: {len(records)}")
    print(f"Source sequence: {source_sequence}")
    print(f"Mean anchor RMSD: {np.mean(rmsds):.4f} Å")
    print(f"Max anchor RMSD: {np.max(rmsds):.4f} Å")
    print("-" * 80)
    print("Validation:")
    print(f"  O3′(i)→P(i+1): {validation_status(o3p)} "
          f"(measured={o3p.measured}, failed={o3p.failed}, mean={o3p.mean:.3f} Å)")
    print(f"  C2′→F2′: {validation_status(c2f)} "
          f"(measured={c2f.measured}, failed={c2f.failed}, mean={c2f.mean:.3f} Å)")
    print("=" * 80)

    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prototype 003A: chain-preserving RNA to FANA converter.")
    parser.add_argument("--rna", "--source", dest="rna", required=True, type=Path, help="Source RNA PDB file")
    parser.add_argument("--template", required=True, type=Path, help="FANA template PDB file")
    parser.add_argument("--output", required=True, type=Path, help="Output FANA-like candidate PDB")
    parser.add_argument("--report", type=Path, default=None, help="Optional Markdown report output")
    parser.add_argument("--anchors", nargs="+", default=DEFAULT_ANCHORS, help="Anchor atoms for Kabsch alignment")
    parser.add_argument("--naming-policy", choices=["template-observed", "provisional"], default="template-observed")
    parser.add_argument("--include-numbering-gaps", action="store_true", help="Validate inter-residue links across residue numbering gaps")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    convert(
        args.rna,
        args.template,
        args.output,
        report_path=args.report,
        anchors=args.anchors,
        naming_policy=args.naming_policy,
        skip_numbering_gaps=not args.include_numbering_gaps,
    )


if __name__ == "__main__":
    main()
