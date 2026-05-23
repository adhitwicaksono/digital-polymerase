#!/usr/bin/env python3
"""
Prototype 005A: RNA to XyNA Converter

Digital Polymerase / XNA World Project

This script generates XyNA-like candidate PDB structures from RNA PDB inputs
using an experimental XyNA template.

XyNA is pentose-based, so this prototype uses a conservative chain-preserving
strategy by default:

    preserve RNA chain/base framework
    +
    introduce XyNA-like local C2'/O2' geometry from template
    +
    validate polymer continuity and local sugar geometry

Supported modes:
    auto              -> currently uses chain-preserving mode by default
    chain-preserving  -> preserve RNA chain/base atoms; replace C2'/O2' locally
    full-template     -> use full XyNA template scaffold; transplant RNA bases

Important:
- This is NOT a chemically or physically validated XyNA modeling package.
- Outputs are computational candidate structures.
- They require visual inspection, stereochemical review, topology/force-field
  review, energy minimization, and expert chemical validation before use.
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

XYNA_LOCAL_ATOMS = {"C2'", "O2'"}

BACKBONE_ORDER = [
    "P", "OP1", "OP2", "O1P", "O2P",
    "O5'", "C5'", "C4'", "O4'", "C3'", "O3'",
    "C1'", "C2'", "O2'",
]

LOCAL_ANCHORS = ["C1'", "C3'", "C4'", "O4'"]
FULL_TEMPLATE_ANCHORS = ["C1'", "C2'", "C3'", "C4'"]
BASE_TRANSPLANT_ANCHORS = ["C1'", "C2'", "C3'", "C4'"]


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
    mode: str
    anchor_atoms: List[str]
    anchor_rmsd: float
    base_anchor_rmsd: Optional[float]
    glycosidic_distance: Optional[float]
    c2o2_distance: Optional[float]
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
    return cleaned[0].upper() if cleaned else ""


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
            coords = np.array([
                float(line[30:38].strip()),
                float(line[38:46].strip()),
                float(line[46:54].strip()),
            ], dtype=float)
            occ = float(line[54:60].strip()) if len(line) >= 60 and line[54:60].strip() else 1.0
            temp = float(line[60:66].strip()) if len(line) >= 66 and line[60:66].strip() else 0.0
            elem = line[76:78].strip() if len(line) >= 78 else ""
            residues[(chain, res_num, insertion_code)][atom_name] = Atom(
                record, atom_name, res_name, chain, res_num, insertion_code,
                coords, occ, temp, infer_element(atom_name, elem)
            )
        except Exception:
            continue
    return dict(residues)


def sorted_keys(residues):
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def residue_name(residue):
    return next(iter(residue.values())).res_name


def normalize_base(res_name: str) -> str:
    r = res_name.strip().upper()
    if r in RNA_BASES:
        return r
    # XyNA template residues: 8XA, 8XG, 8XC, 8XU.
    if "8XA" in r or r.endswith("A"):
        return "A"
    if "8XG" in r or r.endswith("G"):
        return "G"
    if "8XC" in r or r.endswith("C"):
        return "C"
    if "8XU" in r or "8XT" in r or r.endswith("U") or r.endswith("T"):
        return "U"
    if r.startswith("A"):
        return "A"
    if r.startswith("G"):
        return "G"
    if r.startswith("C"):
        return "C"
    if r.startswith(("U", "T")):
        return "U"
    return r[0] if r else "N"


def sequence(residues):
    return "".join(normalize_base(residue_name(residues[k])) for k in sorted_keys(residues))


def is_backbone_atom(atom_name: str) -> bool:
    if atom_name in CHAIN_PRESERVE_ATOMS or atom_name in XYNA_LOCAL_ATOMS:
        return True
    if "'" in atom_name:
        return True
    return False


def split_backbone_base(residue):
    backbone = {n: a for n, a in residue.items() if is_backbone_atom(n)}
    base = {n: a for n, a in residue.items() if not is_backbone_atom(n)}
    return backbone, base


def kabsch(mobile: np.ndarray, target: np.ndarray):
    if mobile.shape != target.shape or mobile.shape[0] < 3:
        raise ValueError("Kabsch alignment requires matching arrays with at least 3 anchors")
    mc = mobile.mean(axis=0)
    tc = target.mean(axis=0)
    m = mobile - mc
    t = target - tc
    cov = m.T @ t
    u, _s, vt = np.linalg.svd(cov)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T
    trans = tc - r @ mc
    transformed = (r @ mobile.T).T + trans
    rmsd = float(np.sqrt(np.mean(np.sum((transformed - target) ** 2, axis=1))))
    return r, trans, rmsd


def apply_transform(coord, r, t):
    return r @ coord + t


def clone_atom(atom, *, coords=None, atom_name=None, res_name=None, chain=None, res_num=None, insertion_code=None, record="HETATM", element=None):
    out_name = atom_name if atom_name is not None else atom.atom_name
    return Atom(
        record if record is not None else atom.record,
        out_name,
        res_name if res_name is not None else atom.res_name,
        chain if chain is not None else atom.chain,
        res_num if res_num is not None else atom.res_num,
        insertion_code if insertion_code is not None else atom.insertion_code,
        np.array(coords if coords is not None else atom.coords, dtype=float),
        atom.occupancy,
        atom.temp_factor,
        element if element is not None else infer_element(out_name, atom.element),
    )


def target_xyna_residue_name(source_base: str, base_label_policy: str = "preserve") -> str:
    b = source_base.upper()
    if base_label_policy == "preserve":
        return {"A": "8XA", "U": "8XU", "G": "8XG", "C": "8XC"}.get(b, "8XN")
    if base_label_policy == "dna-like":
        return {"A": "8XA", "U": "8XT", "G": "8XG", "C": "8XC"}.get(b, "8XN")
    raise ValueError(f"Unsupported base label policy: {base_label_policy}")


def glycosidic_atom_for_base(base: str) -> str:
    return "N9" if base.upper() in {"A", "G"} else "N1"


def template_glycosidic_distance(template_residue, source_base: str) -> Optional[float]:
    gly_atom = glycosidic_atom_for_base(source_base)
    if "C1'" in template_residue and gly_atom in template_residue:
        d = float(np.linalg.norm(template_residue[gly_atom].coords - template_residue["C1'"].coords))
        if 1.20 <= d <= 1.80:
            return d
    return None


def adjust_base_attachment(residue, base_atom_names, source_base: str, desired_distance: Optional[float]) -> Optional[float]:
    gly_atom = glycosidic_atom_for_base(source_base)
    if desired_distance is None:
        desired_distance = 1.47
    if "C1'" not in residue or gly_atom not in residue:
        return None
    c1 = residue["C1'"].coords
    n = residue[gly_atom].coords
    vec = n - c1
    current = float(np.linalg.norm(vec))
    if current < 1e-6:
        return None
    shift = (desired_distance - current) * (vec / current)
    for atom_name in base_atom_names:
        if atom_name in residue:
            residue[atom_name].coords = residue[atom_name].coords + shift
    return float(np.linalg.norm(residue[gly_atom].coords - residue["C1'"].coords))


def available_anchors(a, b, anchors):
    return [x for x in anchors if x in a and x in b]


def build_template_index(template):
    index = defaultdict(list)
    for key in sorted_keys(template):
        res = template[key]
        if len(res) < 6:
            continue
        index[normalize_base(residue_name(res))].append((key, res))
    return dict(index)


def select_template_for_base(source_base, template_index, counter):
    base = source_base.upper()
    if base in template_index and template_index[base]:
        i = counter.get(base, 0)
        counter[base] = i + 1
        key, res = template_index[base][i % len(template_index[base])]
        return key, res, base, "exact base-class XyNA template"
    if base == "U" and "T" in template_index and template_index["T"]:
        i = counter.get("T", 0)
        counter["T"] = i + 1
        key, res = template_index["T"][i % len(template_index["T"])]
        return key, res, "T", "T-like XyNA donor used for RNA U"
    if base == "A" and "G" in template_index:
        i = counter.get("G", 0); counter["G"] = i + 1
        key, res = template_index["G"][i % len(template_index["G"])]
        return key, res, "G", "purine fallback"
    if base == "G" and "A" in template_index:
        i = counter.get("A", 0); counter["A"] = i + 1
        key, res = template_index["A"][i % len(template_index["A"])]
        return key, res, "A", "purine fallback"
    if base == "C" and "U" in template_index:
        i = counter.get("U", 0); counter["U"] = i + 1
        key, res = template_index["U"][i % len(template_index["U"])]
        return key, res, "U", "pyrimidine fallback"
    if base == "U" and "C" in template_index:
        i = counter.get("C", 0); counter["C"] = i + 1
        key, res = template_index["C"][i % len(template_index["C"])]
        return key, res, "C", "pyrimidine fallback"
    first = sorted(template_index)[0]
    i = counter.get(first, 0); counter[first] = i + 1
    key, res = template_index[first][i % len(template_index[first])]
    return key, res, first, "last-resort fallback"


def convert_chain_preserving(source, template, *, base_label_policy):
    template_index = build_template_index(template)
    if not template_index:
        raise ValueError("Could not build usable XyNA template index")
    output = {}
    records = []
    counter = {}
    for skey in sorted_keys(source):
        sres = source[skey]
        sbase = normalize_base(residue_name(sres))
        target_name = target_xyna_residue_name(sbase, base_label_policy)
        tkey, tres, tbase, note = select_template_for_base(sbase, template_index, counter)

        anchors = available_anchors(sres, tres, LOCAL_ANCHORS)
        if len(anchors) < 3:
            anchors = available_anchors(sres, tres, ["C1'", "C3'", "C4'"])
        if len(anchors) < 3:
            raise ValueError(f"Not enough local anchors for {skey}: {anchors}")

        mobile = np.array([tres[a].coords for a in anchors])
        target = np.array([sres[a].coords for a in anchors])
        r, t, rmsd = kabsch(mobile, target)

        out_res = {}
        source_backbone, source_base_atoms = split_backbone_base(sres)

        # Preserve RNA chain atoms and base framework, but replace C2'/O2' with XyNA template-derived geometry.
        for atom_name, atom in source_backbone.items():
            if atom_name in CHAIN_PRESERVE_ATOMS:
                out_res[atom_name] = clone_atom(atom, res_name=target_name, chain=skey[0], res_num=skey[1], insertion_code=skey[2])

        for atom_name in ["C2'", "O2'"]:
            if atom_name in tres:
                new_coord = apply_transform(tres[atom_name].coords, r, t)
                out_res[atom_name] = clone_atom(
                    tres[atom_name],
                    coords=new_coord,
                    atom_name=atom_name,
                    res_name=target_name,
                    chain=skey[0],
                    res_num=skey[1],
                    insertion_code=skey[2],
                    element=infer_element(atom_name)
                )

        for atom_name, atom in source_base_atoms.items():
            out_res[atom_name] = clone_atom(atom, res_name=target_name, chain=skey[0], res_num=skey[1], insertion_code=skey[2])

        gly_atom = glycosidic_atom_for_base(sbase)
        gly = float(np.linalg.norm(out_res["C1'"].coords - out_res[gly_atom].coords)) if "C1'" in out_res and gly_atom in out_res else None
        c2o2 = float(np.linalg.norm(out_res["C2'"].coords - out_res["O2'"].coords)) if "C2'" in out_res and "O2'" in out_res else None

        output[skey] = out_res
        records.append(ConversionRecord(skey, residue_name(sres), sbase, target_name, tkey, residue_name(tres), "chain-preserving", anchors, rmsd, None, gly, c2o2, note + "; RNA chain/base preserved; XyNA C2'/O2' inserted"))
    return output, records


def convert_full_template(source, template, *, base_label_policy):
    source_keys = sorted_keys(source)
    template_keys = sorted_keys(template)
    if len(template_keys) < len(source_keys):
        raise ValueError("XyNA template is shorter than source RNA; use chain-preserving mode")
    output = {}
    records = []
    for i, skey in enumerate(source_keys):
        tkey = template_keys[i]
        sres = source[skey]
        tres = template[tkey]
        sbase = normalize_base(residue_name(sres))
        target_name = target_xyna_residue_name(sbase, base_label_policy)
        anchors = available_anchors(sres, tres, FULL_TEMPLATE_ANCHORS)
        if len(anchors) < 3:
            raise ValueError(f"Not enough full-template anchors for {skey}: {anchors}")
        mobile = np.array([sres[a].coords for a in anchors])
        target = np.array([tres[a].coords for a in anchors])
        r, t, rmsd = kabsch(mobile, target)

        xyna_backbone, _ = split_backbone_base(tres)
        _, source_base_atoms = split_backbone_base(sres)
        out_res = {}

        for atom_name, atom in xyna_backbone.items():
            out_res[atom_name] = clone_atom(atom, res_name=target_name, chain=skey[0], res_num=skey[1], insertion_code=skey[2])

        transplanted = []
        for atom_name, atom in source_base_atoms.items():
            new_coord = apply_transform(atom.coords, r, t)
            out_res[atom_name] = clone_atom(atom, coords=new_coord, res_name=target_name, chain=skey[0], res_num=skey[1], insertion_code=skey[2])
            transplanted.append(atom_name)

        gly = adjust_base_attachment(out_res, transplanted, sbase, template_glycosidic_distance(tres, sbase))
        c2o2 = float(np.linalg.norm(out_res["C2'"].coords - out_res["O2'"].coords)) if "C2'" in out_res and "O2'" in out_res else None

        output[skey] = out_res
        records.append(ConversionRecord(skey, residue_name(sres), sbase, target_name, tkey, residue_name(tres), "full-template", anchors, rmsd, None, gly, c2o2, "full XyNA scaffold; transformed RNA base"))
    return output, records


def atom_sort_key(name):
    if name in BACKBONE_ORDER:
        return (BACKBONE_ORDER.index(name), name)
    return (100, name)


def format_atom_line(serial, atom):
    elem = (atom.element or infer_element(atom.atom_name))[:2].rjust(2)
    chain = (atom.chain or "A")[:1]
    icode = (atom.insertion_code or " ")[:1]
    return (
        f"{atom.record:<6s}{serial:5d} "
        f"{atom.atom_name[:4]:>4s} "
        f"{atom.res_name[:3]:>3s} "
        f"{chain}{atom.res_num:4d}{icode}   "
        f"{atom.coords[0]:8.3f}{atom.coords[1]:8.3f}{atom.coords[2]:8.3f}"
        f"{atom.occupancy:6.2f}{atom.temp_factor:6.2f}"
        f"{'':>10s}{elem:>2s}"
    )


def write_pdb(residues, output_path, *, source_sequence, template_sequence, mode, base_label_policy):
    with output_path.open("w", encoding="utf-8") as f:
        f.write("REMARK   Digital Polymerase Prototype 005A\n")
        f.write("REMARK   RNA to XyNA candidate reconstruction\n")
        f.write(f"REMARK   Mode: {mode}\n")
        f.write(f"REMARK   Source RNA sequence: {source_sequence}\n")
        f.write(f"REMARK   XyNA template base-class sequence: {template_sequence}\n")
        f.write(f"REMARK   Base label policy: {base_label_policy}\n")
        f.write("REMARK   WARNING: Computational candidate only\n")
        f.write("REMARK   WARNING: Not energy-minimized, force-field-validated, or experimentally verified\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")
        serial = 1
        for key in sorted_keys(residues):
            for name in sorted(residues[key].keys(), key=atom_sort_key):
                f.write(format_atom_line(serial, residues[key][name]) + "\n")
                serial += 1
        f.write("END\n")


def summarize(label, records, missing, expected_min, expected_max):
    vals = [r.distance for r in records]
    failed = sum(1 for r in records if r.status == "FAIL")
    if vals:
        mean = float(np.mean(vals)); mn = float(np.min(vals)); mx = float(np.max(vals))
    else:
        mean = mn = mx = float("nan")
    return DistanceSummary(label, expected_min, expected_max, len(records), missing, failed, mean, mn, mx, records)


def validate_inter(residues, a, b, lo, hi, label, skip_numbering_gaps=True):
    keys = sorted_keys(residues); recs = []; missing = 0
    for lk, rk in zip(keys[:-1], keys[1:]):
        if lk[0] != rk[0]: continue
        if skip_numbering_gaps and (rk[1] != lk[1] + 1 or lk[2] or rk[2]): continue
        if a not in residues[lk] or b not in residues[rk]:
            missing += 1; continue
        d = float(np.linalg.norm(residues[lk][a].coords - residues[rk][b].coords))
        recs.append(DistanceRecord(label, lk[0], lk[1], lk[2], a, rk[1], rk[2], b, d, lo, hi, "PASS" if lo <= d <= hi else "FAIL"))
    return summarize(label, recs, missing, lo, hi)


def validate_intra(residues, a, b, lo, hi, label):
    recs = []; missing = 0
    for k in sorted_keys(residues):
        if a not in residues[k] or b not in residues[k]:
            missing += 1; continue
        d = float(np.linalg.norm(residues[k][a].coords - residues[k][b].coords))
        recs.append(DistanceRecord(label, k[0], k[1], k[2], a, k[1], k[2], b, d, lo, hi, "PASS" if lo <= d <= hi else "FAIL"))
    return summarize(label, recs, missing, lo, hi)


def validate_gly(residues):
    recs = []; missing = 0
    for k in sorted_keys(residues):
        base = normalize_base(residue_name(residues[k]))
        gly = glycosidic_atom_for_base(base)
        if "C1'" not in residues[k] or gly not in residues[k]:
            missing += 1; continue
        d = float(np.linalg.norm(residues[k]["C1'"].coords - residues[k][gly].coords))
        recs.append(DistanceRecord("C1'→glycosidic N", k[0], k[1], k[2], "C1'", k[1], k[2], gly, d, 1.30, 1.75, "PASS" if 1.30 <= d <= 1.75 else "FAIL"))
    return summarize("C1'→glycosidic N", recs, missing, 1.30, 1.75)


def status(s):
    return "NO_DATA" if s.measured == 0 else ("PASS" if s.failed == 0 else "FAIL")


def validations(source, template, output, *, skip_numbering_gaps=True):
    def common(r):
        return {
            "O3'(i)→P(i+1)": validate_inter(r, "O3'", "P", 1.40, 1.85, "O3'(i)→P(i+1)", skip_numbering_gaps),
            "P(i)→O5'(i)": validate_intra(r, "P", "O5'", 1.35, 1.90, "P(i)→O5'(i)"),
            "C1'→glycosidic N": validate_gly(r),
            "C1'→C2'": validate_intra(r, "C1'", "C2'", 1.35, 1.75, "C1'→C2'"),
            "C2'→O2'": validate_intra(r, "C2'", "O2'", 1.25, 1.60, "C2'→O2'"),
            "C2'→C3'": validate_intra(r, "C2'", "C3'", 1.35, 1.75, "C2'→C3'"),
            "C3'→C4'": validate_intra(r, "C3'", "C4'", 1.35, 1.75, "C3'→C4'"),
            "C4'→O4'": validate_intra(r, "C4'", "O4'", 1.20, 1.60, "C4'→O4'"),
            "C1'→O4'": validate_intra(r, "C1'", "O4'", 1.20, 1.60, "C1'→O4'"),
        }
    return {"source RNA": common(source), "XyNA template": common(template), "output": common(output)}


def table(v):
    labels = sorted({x for d in v.values() for x in d})
    lines = ["| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |",
             "|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for label in labels:
        for struct, dct in v.items():
            s = dct[label]
            lines.append(f"| {label} | {struct} | {s.measured} | {s.missing} | {s.failed} | {s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | {s.expected_min:.2f}–{s.expected_max:.2f} | {status(s)} |")
    return "\n".join(lines)


def failed_table(s, n=20):
    failed = [r for r in s.records if r.status == "FAIL"]
    if not failed: return "No failed links detected."
    def dev(r):
        return max(r.expected_min - r.distance, r.distance - r.expected_max, 0)
    failed = sorted(failed, key=dev, reverse=True)[:n]
    lines = ["| Rank | Link | Distance (Å) | Expected range (Å) | Status |", "|---:|---|---:|---|---|"]
    for i, r in enumerate(failed, 1):
        link = f"{r.chain}{r.left_res_num}{r.left_icode}:{r.left_atom} → {r.chain}{r.right_res_num}{r.right_icode}:{r.right_atom}"
        lines.append(f"| {i} | `{link}` | {r.distance:.3f} | {r.expected_min:.2f}–{r.expected_max:.2f} | {r.status} |")
    return "\n".join(lines)


def write_report(report_path, *, source_path, template_path, output_path, source, template, output, records, requested_mode, actual_mode, base_label_policy, v):
    rmsd = [r.anchor_rmsd for r in records]
    gly = [r.glycosidic_distance for r in records if r.glycosidic_distance is not None]
    c2o2 = [r.c2o2_distance for r in records if r.c2o2_distance is not None]
    rec_lines = []
    for i, r in enumerate(records, 1):
        rec_lines.append(f"| {i} | {r.source_key[0]}{r.source_key[1]}{r.source_key[2]} | {r.source_base} | {r.target_res_name} | {r.template_res_name} {r.template_key[0]}{r.template_key[1]}{r.template_key[2]} | {r.mode} | {r.anchor_rmsd:.4f} | {r.glycosidic_distance if r.glycosidic_distance is not None else 'NA'} | {r.c2o2_distance if r.c2o2_distance is not None else 'NA'} | {r.note} |")

    out = v["output"]
    report = f"""# RNA → XyNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 005A  
**Requested mode:** `{requested_mode}`  
**Actual mode:** `{actual_mode}`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `{status(out["O3'(i)→P(i+1)"])}`  
**Base-attachment status:** `{status(out["C1'→glycosidic N"])}`  
**XyNA local sugar status:** `C2′→O2′ {status(out["C2'→O2'"])}`, `C1′→O4′ {status(out["C1'→O4'"])}`, `C4′→O4′ {status(out["C4'→O4'"])}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- XyNA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source and Template

- Source RNA sequence: `{sequence(source)}`
- XyNA template base-class sequence: `{sequence(template)}`
- Source residue count: `{len(sorted_keys(source))}`
- Template residue count: `{len(sorted_keys(template))}`
- Converted residues: `{len(records)}`
- Base label policy: `{base_label_policy}`

---

## Method Summary

Prototype 005A supports two RNA → XyNA modes.

### Chain-preserving mode

This is the default in `auto` mode because XyNA is pentose-based and close enough to RNA-like chain geometry for a conservative local sugar replacement strategy.

```text
RNA chain/base framework preserved
+
XyNA-like C2′/O2′ geometry inserted from template
```

### Full-template mode

This mode uses the full XyNA scaffold as donor and transforms RNA bases onto the XyNA template. It is available for short RNA inputs when a full-length XyNA template exists.

---

## Alignment Summary

- Mean local/template anchor RMSD: `{np.mean(rmsd):.4f} Å`
- Maximum local/template anchor RMSD: `{np.max(rmsd):.4f} Å`
- Mean C1′→glycosidic N distance: `{np.mean(gly) if gly else float('nan'):.4f} Å`
- Maximum C1′→glycosidic N distance: `{np.max(gly) if gly else float('nan'):.4f} Å`
- Mean C2′→O2′ distance: `{np.mean(c2o2) if c2o2 else float('nan'):.4f} Å`
- Maximum C2′→O2′ distance: `{np.max(c2o2) if c2o2 else float('nan'):.4f} Å`

---

## Structural Validation

{table(v)}

### Worst output O3′–P links

{failed_table(out["O3'(i)→P(i+1)"], n=20)}

### Worst output C2′–O2′ distances

{failed_table(out["C2'→O2'"], n=20)}

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Anchor RMSD (Å) | C1′–N (Å) | C2′–O2′ (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
{chr(10).join(rec_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a XyNA-like computational candidate generated by template-guided or chain-preserving local sugar reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed XyNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- XyNA stereochemistry requires expert inspection.
- Chain-preserving mode preserves the RNA chain path and replaces local C2′/O2′ geometry; it is not de novo XyNA folding.
- Biological function, stability, replication, or catalytic activity is not implied.
"""
    report_path.write_text(report, encoding="utf-8")


def convert(source_path, template_path, output_path, *, report_path=None, mode="auto", base_label_policy="preserve", skip_numbering_gaps=True):
    source = parse_pdb(source_path)
    template = parse_pdb(template_path)
    if not source:
        raise ValueError(f"No residues parsed from source: {source_path}")
    if not template:
        raise ValueError(f"No residues parsed from template: {template_path}")

    if mode == "auto":
        actual_mode = "chain-preserving"
    else:
        actual_mode = mode

    if actual_mode == "chain-preserving":
        output, records = convert_chain_preserving(source, template, base_label_policy=base_label_policy)
    elif actual_mode == "full-template":
        output, records = convert_full_template(source, template, base_label_policy=base_label_policy)
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    write_pdb(output, output_path, source_sequence=sequence(source), template_sequence=sequence(template), mode=actual_mode, base_label_policy=base_label_policy)
    v = validations(source, template, output, skip_numbering_gaps=skip_numbering_gaps)

    if report_path:
        write_report(report_path, source_path=source_path, template_path=template_path, output_path=output_path, source=source, template=template, output=output, records=records, requested_mode=mode, actual_mode=actual_mode, base_label_policy=base_label_policy, v=v)

    rmsd = [r.anchor_rmsd for r in records]
    out = v["output"]
    print("=" * 80)
    print("Digital Polymerase Prototype 005A")
    print("RNA → XyNA candidate reconstruction")
    print("=" * 80)
    print(f"Source RNA: {source_path}")
    print(f"XyNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    if report_path:
        print(f"Report: {report_path}")
    print(f"Requested mode: {mode}")
    print(f"Actual mode: {actual_mode}")
    print(f"Source sequence: {sequence(source)}")
    print(f"Template base classes: {sequence(template)}")
    print(f"Converted residues: {len(records)}")
    print(f"Mean local/template RMSD: {np.mean(rmsd):.4f} Å")
    print(f"Max local/template RMSD: {np.max(rmsd):.4f} Å")
    print("-" * 80)
    for label in ["O3'(i)→P(i+1)", "C1'→glycosidic N", "C2'→O2'", "C1'→O4'", "C4'→O4'"]:
        s = out[label]
        print(f"{label}: {status(s)} (measured={s.measured}, failed={s.failed}, mean={s.mean:.3f} Å)")
    print("=" * 80)
    return records


def parse_args():
    p = argparse.ArgumentParser(description="Prototype 005A: RNA to XyNA converter.")
    p.add_argument("--rna", "--source", dest="rna", required=True, type=Path)
    p.add_argument("--template", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--report", type=Path, default=None)
    p.add_argument("--mode", choices=["auto", "chain-preserving", "full-template"], default="auto")
    p.add_argument("--base-label-policy", choices=["preserve", "dna-like"], default="preserve")
    p.add_argument("--include-numbering-gaps", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    convert(args.rna, args.template, args.output, report_path=args.report, mode=args.mode, base_label_policy=args.base_label_policy, skip_numbering_gaps=not args.include_numbering_gaps)


if __name__ == "__main__":
    main()
