#!/usr/bin/env python3
"""
Prototype 008A.1: RNA to PNA Chimaera-Guided Converter

Digital Polymerase / XNA World Project

PNA is the chimaera: it is not a sugar/phosphate XNA but a peptide-like
nucleic acid mimic. This first-pass converter generates PNA-like candidates
from RNA PDB inputs using a PNA template.

Observed PNA template logic:
    Base attachment: C8' -> glycosidic N
    Chain linkage:   C'(i) -> N1'(i+1)

Strategy:
    1. Select a PNA template residue by base class.
    2. Place the PNA pseudopeptide scaffold using neighboring RNA C1' positions
       as a guide.
    3. Apply a suffix-based linkage correction so C'(i)->N1'(i+1) is continuous.
    4. Attach source RNA bases to PNA C8'.

This is a computational candidate generator only, not a physical validator.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, Optional
import numpy as np


ResidueKey = Tuple[str, int, str]

PNA_BACKBONE_ATOMS = ["C8'", "C7'", "O7'", "N4'", "C3'", "C2'", "N1'", "C5'", "C'", "O1'"]
BACKBONE_ORDER = ["N1'", "C2'", "C3'", "N4'", "C7'", "O7'", "C8'", "C5'", "C'", "O1'"]

BASE_CORE_ATOMS = {
    "A": ["N9", "C8", "N7", "C5", "C6", "N1", "C2", "N3", "C4"],
    "G": ["N9", "C8", "N7", "C5", "C6", "O6", "N1", "C2", "N2", "N3", "C4"],
    "C": ["N1", "C2", "O2", "N3", "C4", "N4", "C5", "C6"],
    "U": ["N1", "C2", "O2", "N3", "C4", "O4", "C5", "C6"],
}


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
    source_base: str
    target_res_name: str
    template_key: ResidueKey
    template_res_name: str
    guide_rmsd: float
    suffix_shift: float
    base_shift: float
    c8_to_n: Optional[float]
    inter_c_to_n1_next: Optional[float]
    note: str


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


def infer_element(atom_name: str, pdb_element: str = "") -> str:
    elem = (pdb_element or "").strip()
    if elem and re.match(r"^[A-Za-z]{1,2}$", elem):
        return elem[0].upper() + elem[1:].lower()
    cleaned = re.sub(r"[^A-Za-z]", "", atom_name)
    return cleaned[0].upper() if cleaned else ""


def parse_pdb(path: Path) -> Dict[ResidueKey, Dict[str, Atom]]:
    residues = defaultdict(dict)
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        try:
            name = line[12:16].strip()
            resn = line[17:20].strip()
            chain = line[21].strip() or "A"
            rn = int(line[22:26].strip())
            ic = line[26].strip()
            xyz = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])], dtype=float)
            occ = float(line[54:60].strip()) if len(line) >= 60 and line[54:60].strip() else 1.0
            temp = float(line[60:66].strip()) if len(line) >= 66 and line[60:66].strip() else 0.0
            elem = line[76:78].strip() if len(line) >= 78 else ""
            residues[(chain, rn, ic)][name] = Atom(
                "HETATM", name, resn, chain, rn, ic, xyz, occ, temp, infer_element(name, elem)
            )
        except Exception:
            continue
    return dict(residues)


def keys(residues):
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def usable_keys(residues):
    return [k for k in keys(residues) if all(a in residues[k] for a in PNA_BACKBONE_ATOMS)]


def resname(residue):
    return next(iter(residue.values())).res_name


def base_of(name: str) -> str:
    r = name.upper().strip()
    if r in {"A", "U", "G", "C"}:
        return r
    if r == "APN" or r.endswith("A"):
        return "A"
    if r == "GPN" or r.endswith("G"):
        return "G"
    if r == "CPN" or r.endswith("C"):
        return "C"
    if r == "TPN" or r.endswith("T") or r.endswith("U"):
        return "U"
    if r.startswith("A"):
        return "A"
    if r.startswith("G"):
        return "G"
    if r.startswith("C"):
        return "C"
    if r.startswith(("T", "U")):
        return "U"
    return "N"


def sequence(residues, only_usable=False):
    ks = usable_keys(residues) if only_usable else [k for k in keys(residues) if base_of(resname(residues[k])) in {"A", "U", "G", "C"}]
    return "".join(base_of(resname(residues[k])) for k in ks)


def target_name(base: str, policy: str = "preserve") -> str:
    if policy == "dna-like":
        return {"A": "APN", "U": "TPN", "G": "GPN", "C": "CPN"}.get(base, "PNN")
    return {"A": "APN", "U": "UPN", "G": "GPN", "C": "CPN"}.get(base, "PNN")


def gly_atom(base: str) -> str:
    return "N9" if base in {"A", "G"} else "N1"


def source_base_atoms(residue):
    nonbase = {
        "P", "OP1", "OP2", "O1P", "O2P",
        "O5'", "C5'", "C4'", "O4'", "C3'", "O3'",
        "C2'", "O2'", "C1'",
    }
    return {n: a for n, a in residue.items() if n not in nonbase and "'" not in n}


def clone(atom, *, coords=None, atom_name=None, res_name=None, chain=None, res_num=None, insertion_code=None, element=None):
    name = atom_name if atom_name is not None else atom.atom_name
    return Atom(
        "HETATM",
        name,
        res_name if res_name is not None else atom.res_name,
        chain if chain is not None else atom.chain,
        res_num if res_num is not None else atom.res_num,
        insertion_code if insertion_code is not None else atom.insertion_code,
        np.array(coords if coords is not None else atom.coords, dtype=float),
        atom.occupancy,
        atom.temp_factor,
        element if element is not None else infer_element(name, atom.element),
    )


def kabsch(mobile, target):
    mobile = np.asarray(mobile, dtype=float)
    target = np.asarray(target, dtype=float)
    if mobile.shape != target.shape or mobile.shape[0] < 3:
        raise ValueError("Kabsch alignment requires matching arrays with at least 3 anchors")
    mc = mobile.mean(axis=0)
    tc = target.mean(axis=0)
    m = mobile - mc
    t = target - tc
    u, s, vt = np.linalg.svd(m.T @ t)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T
    trans = tc - r @ mc
    fitted = (r @ mobile.T).T + trans
    rmsd = float(np.sqrt(np.mean(np.sum((fitted - target) ** 2, axis=1))))
    return r, trans, rmsd


def apply(coord, r, t):
    return r @ coord + t


def distance(res_a, atom_a, res_b, atom_b, default):
    if res_a is not None and res_b is not None and atom_a in res_a and atom_b in res_b:
        return float(np.linalg.norm(res_a[atom_a].coords - res_b[atom_b].coords))
    return default


def build_template_index(template):
    idx = defaultdict(list)
    tks = usable_keys(template)
    for i, k in enumerate(tks):
        idx[base_of(resname(template[k]))].append((i, k, template[k]))
    return dict(idx), tks


def select_template(base, idx, counter):
    if base in idx and idx[base]:
        i = counter.get(base, 0)
        counter[base] = i + 1
        return idx[base][i % len(idx[base])], "exact base-class PNA template"
    if base == "U" and "T" in idx and idx["T"]:
        i = counter.get("T", 0)
        counter["T"] = i + 1
        return idx["T"][i % len(idx["T"])], "T-like donor for RNA U"
    for alt in (["A", "G"] if base in {"A", "G"} else ["C", "U", "T"]):
        if alt in idx and idx[alt]:
            i = counter.get(alt, 0)
            counter[alt] = i + 1
            return idx[alt][i % len(idx[alt])], f"fallback {alt}-like donor"
    first = sorted(idx)[0]
    i = counter.get(first, 0)
    counter[first] = i + 1
    return idx[first][i % len(idx[first])], "last-resort fallback"


def initial_scaffold_from_c1_path(template, template_keys, template_index, template_residue, source, source_keys, source_i, donor_i):
    skey = source_keys[source_i]
    sres = source[skey]

    mobile = []
    target = []
    used = []

    # Current base-bearing atom C8' to source C1'.
    if "C8'" in template_residue and "C1'" in sres:
        mobile.append(template_residue["C8'"].coords)
        target.append(sres["C1'"].coords)
        used.append("C8'→C1'")

    # Neighbor path anchors from template C8' positions to source C1' positions.
    if source_i + 1 < len(source_keys) and source_keys[source_i + 1][0] == skey[0] and source_keys[source_i + 1][1] == skey[1] + 1:
        tni = donor_i + 1 if donor_i + 1 < len(template_keys) else donor_i - 1
        if tni >= 0 and "C8'" in template[template_keys[tni]] and "C1'" in source[source_keys[source_i + 1]]:
            mobile.append(template[template_keys[tni]]["C8'"].coords)
            target.append(source[source_keys[source_i + 1]]["C1'"].coords)
            used.append("next C8'→next C1'")

    if source_i - 1 >= 0 and skey[1] == source_keys[source_i - 1][1] + 1:
        tpi = donor_i - 1 if donor_i - 1 >= 0 else donor_i + 1
        if tpi < len(template_keys) and "C8'" in template[template_keys[tpi]] and "C1'" in source[source_keys[source_i - 1]]:
            mobile.append(template[template_keys[tpi]]["C8'"].coords)
            target.append(source[source_keys[source_i - 1]]["C1'"].coords)
            used.append("prev C8'→prev C1'")

    # If still underdetermined, add glycosidic anchor/base atoms.
    base = base_of(resname(sres))
    g = gly_atom(base)
    if len(mobile) < 3 and g in template_residue and g in sres:
        mobile.append(template_residue[g].coords)
        target.append(sres[g].coords)
        used.append("glycosidic N")

    if len(mobile) < 3:
        for a in BASE_CORE_ATOMS.get(base, []):
            if a in template_residue and a in sres:
                mobile.append(template_residue[a].coords)
                target.append(sres[a].coords)
                used.append(a)
                if len(mobile) >= 3:
                    break

    if len(mobile) < 3:
        raise ValueError(f"Not enough PNA guide anchors for source {skey}: {used}")

    r, t, rmsd = kabsch(np.array(mobile), np.array(target))
    return {a: apply(template_residue[a].coords, r, t) for a in PNA_BACKBONE_ATOMS}, rmsd, used


def suffix_linkage_correction(scaffolds, source_keys, target=1.34):
    """
    Enforce PNA C'(i)->N1'(i+1) by shifting each downstream suffix.
    This preserves internal residue geometry while making the pseudopeptide
    chain continuous. It may increase base-shift values, so it is documented
    as first-pass chimaera handling, not final physical refinement.
    """
    n = len(scaffolds)
    suffix_shift_total = [0.0] * n
    for i in range(n - 1):
        if not (source_keys[i + 1][0] == source_keys[i][0] and source_keys[i + 1][1] == source_keys[i][1] + 1 and not source_keys[i][2] and not source_keys[i + 1][2]):
            continue
        v = scaffolds[i + 1]["N1'"] - scaffolds[i]["C'"]
        d = float(np.linalg.norm(v))
        if d < 1e-8:
            continue
        delta = (target - d) * (v / d)
        mag = float(np.linalg.norm(delta))
        for j in range(i + 1, n):
            for a in PNA_BACKBONE_ATOMS:
                scaffolds[j][a] = scaffolds[j][a] + delta
            suffix_shift_total[j] += mag
    return scaffolds, suffix_shift_total


def attach_base(out_res, source_base_atoms_, source_residue, base, target_distance):
    g = gly_atom(base)
    if "C8'" not in out_res or g not in source_base_atoms_:
        return None, 0.0

    source_g = source_base_atoms_[g].coords
    desired = target_distance if target_distance is not None else 1.46

    # Preserve source base orientation; translate the whole base to attach gly N to C8'.
    if "C1'" in source_residue:
        v = source_g - source_residue["C1'"].coords
    else:
        v = source_g - out_res["C8'"].coords

    norm = float(np.linalg.norm(v))
    if norm < 1e-8:
        v = source_g - out_res["C8'"].coords
        norm = float(np.linalg.norm(v))
    if norm < 1e-8:
        return None, 0.0

    new_g = out_res["C8'"].coords + desired * (v / norm)
    shift = new_g - source_g

    for name, atom in source_base_atoms_.items():
        out_res[name] = clone(
            atom,
            coords=atom.coords + shift,
            res_name=out_res["C8'"].res_name,
            chain=out_res["C8'"].chain,
            res_num=out_res["C8'"].res_num,
            insertion_code=out_res["C8'"].insertion_code,
        )

    return float(np.linalg.norm(out_res["C8'"].coords - out_res[g].coords)), float(np.linalg.norm(shift))


def convert(source, template, policy="preserve"):
    idx, tkeys = build_template_index(template)
    if not idx:
        raise ValueError("Could not build usable PNA template index")

    source_keys = [k for k in keys(source) if base_of(resname(source[k])) in {"A", "U", "G", "C"}]
    bases = [base_of(resname(source[k])) for k in source_keys]

    selected = []
    counter = {}
    for base in bases:
        (donor_i, tkey, tres), note = select_template(base, idx, counter)
        selected.append((donor_i, tkey, tres, note))

    scaffolds = []
    guide_rmsds = []
    for i, (skey, base, (donor_i, tkey, tres, note)) in enumerate(zip(source_keys, bases, selected)):
        scaf, rmsd, used = initial_scaffold_from_c1_path(template, tkeys, idx, tres, source, source_keys, i, donor_i)
        scaffolds.append(scaf)
        guide_rmsds.append(rmsd)

    scaffolds, suffix_shifts = suffix_linkage_correction(scaffolds, source_keys, target=1.34)

    output = {}
    records = []
    for i, (skey, base, (donor_i, tkey, tres, note)) in enumerate(zip(source_keys, bases, selected)):
        sres = source[skey]
        target_res = target_name(base, policy)
        out_res = {}

        for a in PNA_BACKBONE_ATOMS:
            out_res[a] = clone(
                tres[a],
                coords=scaffolds[i][a],
                atom_name=a,
                res_name=target_res,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                element=infer_element(a),
            )

        desired = distance(tres, "C8'", tres, gly_atom(base), 1.46)
        c8n, base_shift = attach_base(out_res, source_base_atoms(sres), sres, base, desired)

        next_link = None
        if i + 1 < len(source_keys) and source_keys[i + 1][0] == skey[0] and source_keys[i + 1][1] == skey[1] + 1 and not skey[2] and not source_keys[i + 1][2]:
            next_link = float(np.linalg.norm(out_res["C'"].coords - scaffolds[i + 1]["N1'"]))

        output[skey] = out_res
        records.append(
            ConversionRecord(
                source_key=skey,
                source_base=base,
                target_res_name=target_res,
                template_key=tkey,
                template_res_name=resname(tres),
                guide_rmsd=guide_rmsds[i],
                suffix_shift=suffix_shifts[i],
                base_shift=base_shift,
                c8_to_n=c8n,
                inter_c_to_n1_next=next_link,
                note=note + "; PNA chimaera-guided scaffold with suffix linkage correction",
            )
        )

    return output, records


def atom_order(name):
    return (BACKBONE_ORDER.index(name), name) if name in BACKBONE_ORDER else (100, name)


def fmt_atom(serial, atom):
    elem = (atom.element or infer_element(atom.atom_name))[:2].rjust(2)
    icode = (atom.insertion_code or " ")[:1]
    return (
        f"{atom.record:<6s}{serial:5d} {atom.atom_name[:4]:>4s} {atom.res_name[:3]:>3s} "
        f"{(atom.chain or 'A')[:1]}{atom.res_num:4d}{icode}   "
        f"{atom.coords[0]:8.3f}{atom.coords[1]:8.3f}{atom.coords[2]:8.3f}"
        f"{atom.occupancy:6.2f}{atom.temp_factor:6.2f}{'':>10s}{elem:>2s}"
    )


def write_pdb(residues, path, src_seq, tmpl_seq):
    with path.open("w", encoding="utf-8") as f:
        f.write("REMARK   Digital Polymerase Prototype 008A.1\n")
        f.write("REMARK   RNA to PNA chimaera-guided candidate reconstruction\n")
        f.write(f"REMARK   Source RNA sequence: {src_seq}\n")
        f.write(f"REMARK   PNA template base-class sequence: {tmpl_seq}\n")
        f.write("REMARK   PNA linkage model: C'(i)->N1'(i+1)\n")
        f.write("REMARK   PNA base attachment model: C8'(i)->glycosidic N\n")
        f.write("REMARK   WARNING: Computational candidate only; not physically validated\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")
        serial = 1
        for k in keys(residues):
            for name in sorted(residues[k], key=atom_order):
                f.write(fmt_atom(serial, residues[k][name]) + "\n")
                serial += 1
        f.write("END\n")


def validate_intra(residues, a, b, lo, hi, label):
    vals, missing = [], 0
    for k in keys(residues):
        if a not in residues[k] or b not in residues[k]:
            missing += 1
            continue
        vals.append(float(np.linalg.norm(residues[k][a].coords - residues[k][b].coords)))
    failed = sum(1 for v in vals if not (lo <= v <= hi))
    return DistanceSummary(label, len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), lo, hi)


def validate_inter(residues, a, b, lo, hi, label):
    ks = keys(residues)
    vals, missing = [], 0
    for lk, rk in zip(ks[:-1], ks[1:]):
        if lk[0] != rk[0] or rk[1] != lk[1] + 1 or lk[2] or rk[2]:
            continue
        if a not in residues[lk] or b not in residues[rk]:
            missing += 1
            continue
        vals.append(float(np.linalg.norm(residues[lk][a].coords - residues[rk][b].coords)))
    failed = sum(1 for v in vals if not (lo <= v <= hi))
    return DistanceSummary(label, len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), lo, hi)


def validate_base_attachment(residues):
    vals, missing = [], 0
    for k in keys(residues):
        base = base_of(resname(residues[k]))
        g = gly_atom(base)
        if "C8'" not in residues[k] or g not in residues[k]:
            missing += 1
            continue
        vals.append(float(np.linalg.norm(residues[k]["C8'"].coords - residues[k][g].coords)))
    failed = sum(1 for v in vals if not (1.25 <= v <= 1.75))
    return DistanceSummary("C8'→glycosidic N", len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), 1.25, 1.75)


def status(s):
    return "NO_DATA" if s.measured == 0 else ("PASS" if s.failed == 0 else "FAIL")


def build_validation(output):
    return {
        "PNA C'(i)→N1'(i+1)": validate_inter(output, "C'", "N1'", 1.15, 1.60, "PNA C'(i)→N1'(i+1)"),
        "C8'→glycosidic N": validate_base_attachment(output),
        "C8'→C7'": validate_intra(output, "C8'", "C7'", 1.30, 1.80, "C8'→C7'"),
        "C7'→O7'": validate_intra(output, "C7'", "O7'", 1.10, 1.40, "C7'→O7'"),
        "C7'→N4'": validate_intra(output, "C7'", "N4'", 1.15, 1.55, "C7'→N4'"),
        "N4'→C3'": validate_intra(output, "N4'", "C3'", 1.25, 1.75, "N4'→C3'"),
        "C3'→C2'": validate_intra(output, "C3'", "C2'", 1.25, 1.85, "C3'→C2'"),
        "C2'→N1'": validate_intra(output, "C2'", "N1'", 1.20, 1.75, "C2'→N1'"),
        "N4'→C5'": validate_intra(output, "N4'", "C5'", 1.25, 1.75, "N4'→C5'"),
        "C5'→C'": validate_intra(output, "C5'", "C'", 1.25, 1.85, "C5'→C'"),
        "C'→O1'": validate_intra(output, "C'", "O1'", 1.10, 1.40, "C'→O1'"),
    }


def validation_table(checks):
    lines = [
        "| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for label, s in checks.items():
        lines.append(f"| {label} | {s.measured} | {s.missing} | {s.failed} | {s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | {s.lo:.2f}–{s.hi:.2f} | {status(s)} |")
    return "\n".join(lines)


def write_report(path, source_path, template_path, output_path, source, template, output, records):
    checks = build_validation(output)
    rmsd = [r.guide_rmsd for r in records]
    shifts = [r.base_shift for r in records]
    suffix = [r.suffix_shift for r in records]
    c8n = [r.c8_to_n for r in records if r.c8_to_n is not None]
    links = [r.inter_c_to_n1_next for r in records if r.inter_c_to_n1_next is not None]

    rec_lines = []
    for i, r in enumerate(records, 1):
        rec_lines.append(
            f"| {i} | {r.source_key[0]}{r.source_key[1]}{r.source_key[2]} | {r.source_base} | "
            f"{r.target_res_name} | {r.template_res_name} {r.template_key[0]}{r.template_key[1]}{r.template_key[2]} | "
            f"{r.guide_rmsd:.4f} | {r.suffix_shift:.4f} | {r.base_shift:.4f} | "
            f"{r.c8_to_n if r.c8_to_n is not None else 'NA'} | "
            f"{r.inter_c_to_n1_next if r.inter_c_to_n1_next is not None else 'NA'} | {r.note} |"
        )

    md = f"""# RNA → PNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 008A.1  
**Method:** PNA chimaera-guided pseudopeptide-backbone reconstruction  
**Status:** Experimental candidate, not physically validated  
**PNA chain-continuity status:** `C′(i)→N1′(i+1) {status(checks["PNA C'(i)→N1'(i+1)"])}`  
**Base-attachment status:** `{status(checks["C8'→glycosidic N"])}`  
**PNA backbone status:** `C7′→N4′ {status(checks["C7'→N4'"])}`, `C′→O1′ {status(checks["C'→O1'"])}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- PNA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source and Template

- Source RNA sequence: `{sequence(source)}`
- PNA template base-class sequence: `{sequence(template, only_usable=True)}`
- Source residue count: `{len([k for k in keys(source) if base_of(resname(source[k])) in {"A", "U", "G", "C"}])}`
- Usable template residue count: `{len(usable_keys(template))}`
- Converted residues: `{len(records)}`

---

## Why PNA Is the Chimaera

PNA is not a sugar-modified nucleic acid. It abandons the sugar-phosphate backbone and uses a pseudopeptide backbone.

The uploaded template uses PNA-like residues:

```text
APN
TPN
GPN
CPN
```

Important PNA scaffold atoms include:

```text
C8'
C7'
O7'
N4'
C3'
C2'
N1'
C5'
C'
O1'
```

Observed linkage:

```text
C′(i) → N1′(i+1)
```

Observed base attachment:

```text
C8′ → glycosidic N
```

---

## Method Summary

Prototype 008A.1 performs PNA chimaera-guided pseudopeptide-backbone reconstruction:

1. infer source RNA base identity
2. select a PNA template residue by base class
3. place the PNA pseudopeptide scaffold using neighboring RNA `C1′` positions as a guide
4. enforce PNA `C′(i)→N1′(i+1)` continuity using suffix linkage correction
5. attach the source RNA base to PNA `C8′`
6. export a PNA-like candidate PDB
7. validate PNA-specific backbone and base-attachment geometry

---

## Alignment / Correction Summary

- Mean guide RMSD: `{np.mean(rmsd):.4f} Å`
- Maximum guide RMSD: `{np.max(rmsd):.4f} Å`
- Mean suffix-linkage shift: `{np.mean(suffix):.4f} Å`
- Maximum suffix-linkage shift: `{np.max(suffix):.4f} Å`
- Mean base shift: `{np.mean(shifts):.4f} Å`
- Maximum base shift: `{np.max(shifts):.4f} Å`
- Mean C8′→glycosidic N distance: `{np.mean(c8n) if c8n else float('nan'):.4f} Å`
- Mean C′(i)→N1′(i+1) distance: `{np.mean(links) if links else float('nan'):.4f} Å`

---

## Structural Validation

{validation_table(checks)}

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Guide RMSD (Å) | Suffix shift (Å) | Base shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
{chr(10).join(rec_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a PNA-like computational candidate generated by chimaera-guided pseudopeptide-backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready PNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- PNA stereochemistry and peptide-like backbone geometry require expert inspection.
- The suffix-linkage correction prioritizes PNA chain continuity and may increase base shifts.
- Molecular viewers may not render standard nucleic-acid cartoon paths for PNA.
- The output is a candidate geometry only; biological function, stability, binding, or catalytic activity is not implied.
"""
    path.write_text(md, encoding="utf-8")


def run(source_path: Path, template_path: Path, output_path: Path, report_path: Path):
    source = parse_pdb(source_path)
    template = parse_pdb(template_path)
    output, records = convert(source, template)
    write_pdb(output, output_path, sequence(source), sequence(template, only_usable=True))
    write_report(report_path, source_path, template_path, output_path, source, template, output, records)

    checks = build_validation(output)
    print("=" * 80)
    print("Digital Polymerase Prototype 008A.1")
    print("RNA → PNA chimaera-guided candidate reconstruction")
    print("=" * 80)
    print(f"Source RNA: {source_path}")
    print(f"PNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    print(f"Report: {report_path}")
    print(f"Source sequence: {sequence(source)}")
    print(f"Template sequence: {sequence(template, only_usable=True)}")
    print(f"Converted residues: {len(records)}")
    print("-" * 80)
    for label in ["PNA C'(i)→N1'(i+1)", "C8'→glycosidic N", "C8'→C7'", "C7'→O7'", "C7'→N4'", "N4'→C3'", "C'→O1'"]:
        s = checks[label]
        print(f"{label}: {status(s)} (measured={s.measured}, failed={s.failed}, mean={s.mean:.3f} Å)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Prototype 008A.1: RNA to PNA converter.")
    parser.add_argument("--rna", required=True, type=Path, help="Source RNA PDB")
    parser.add_argument("--template", required=True, type=Path, help="PNA template PDB")
    parser.add_argument("--output", required=True, type=Path, help="Output PNA-like candidate PDB")
    parser.add_argument("--report", required=True, type=Path, help="Output Markdown report")
    args = parser.parse_args()
    run(args.rna, args.template, args.output, args.report)


if __name__ == "__main__":
    main()
