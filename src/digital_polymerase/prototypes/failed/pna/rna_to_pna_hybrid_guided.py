#!/usr/bin/env python3
"""
Prototype 008D: RNA-informed PNA Hybrid-Guided Builder

Digital Polymerase / XNA World Project

PNA is the chimaera. Earlier stages taught three lessons:
- 008A.1: forcing a PNA pseudopeptide chain onto an RNA fold collapses/tangles.
- 008B: template-primary PNA scaffold-first conversion works cleanly, but does not preserve RNA fold.
- 008C: sequence-primary PNA generation is useful, but it is a sequence-carrier generator.

Prototype 008D tries a hybrid compromise:

    RNA base frames guide placement
    +
    PNA template chemistry provides local scaffold
    +
    bounded pairwise smoothing nudges C'(i)->N1'(i+1)
    +
    movement caps prevent 008A.1-style collapse

This is a boundary-test prototype. It is not expected to fully solve PNA fold
preservation, and it is not physically validated.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional
import numpy as np


ResidueKey = Tuple[str, int, str]

PNA_BACKBONE_ATOMS = ["C8'", "C7'", "O7'", "N4'", "C3'", "C2'", "N1'", "C5'", "C'", "O1'"]
BACKBONE_ORDER = ["N1'", "C2'", "C3'", "N4'", "C7'", "O7'", "C8'", "C5'", "C'", "O1'"]

RNA_NONBASE_ATOMS = {
    "P", "OP1", "OP2", "O1P", "O2P",
    "O5'", "C5'", "C4'", "O4'", "C3'", "O3'",
    "C2'", "O2'", "C1'",
}

BASE_CORE_ATOMS = {
    "A": ["N9", "C8", "N7", "C5", "C6", "N6", "N1", "C2", "N3", "C4"],
    "G": ["N9", "C8", "N7", "C5", "C6", "O6", "N1", "C2", "N2", "N3", "C4"],
    "C": ["N1", "C2", "O2", "N3", "C4", "N4", "C5", "C6"],
    "U": ["N1", "C2", "O2", "N3", "C4", "O4", "C5", "C6"],
}

BASE_REQUIRED_OXYGENS = {
    "A": [],
    "G": ["O6"],
    "C": ["O2"],
    "U": ["O2", "O4"],
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
    output_res_name: str
    template_key: ResidueKey
    template_res_name: str
    base_fit_rmsd: float
    total_shift: float
    c8_to_n: Optional[float]
    next_link: Optional[float]
    missing_required_base_atoms: List[str]
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


def usable_template_keys(template):
    return [k for k in keys(template) if all(a in template[k] for a in PNA_BACKBONE_ATOMS)]


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


def source_keys(source):
    return [k for k in keys(source) if base_of(resname(source[k])) in {"A", "U", "G", "C"}]


def source_sequence(source):
    return "".join(base_of(resname(source[k])) for k in source_keys(source))


def template_sequence(template):
    return "".join(base_of(resname(template[k])) for k in usable_template_keys(template))


def target_res_name(base: str, policy="preserve"):
    if policy == "dna-like":
        return {"A": "APN", "U": "TPN", "G": "GPN", "C": "CPN"}.get(base, "PNN")
    return {"A": "APN", "U": "UPN", "G": "GPN", "C": "CPN"}.get(base, "PNN")


def gly_atom(base: str) -> str:
    return "N9" if base in {"A", "G"} else "N1"


def source_base_atoms(residue):
    return {n: a for n, a in residue.items() if n not in RNA_NONBASE_ATOMS and "'" not in n and not n.startswith("H")}


def is_pna_base_atom(name: str) -> bool:
    if name in PNA_BACKBONE_ATOMS:
        return False
    if name.startswith("H"):
        return False
    return name not in {"N", "CA", "C", "O"}


def pna_base_atoms(residue):
    return {n: a for n, a in residue.items() if is_pna_base_atom(n)}


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
        raise ValueError("Kabsch alignment requires at least 3 paired anchors")
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


def build_template_index(template):
    idx = defaultdict(list)
    for k in usable_template_keys(template):
        idx[base_of(resname(template[k]))].append(k)
    return dict(idx)


def select_template(base, idx):
    if base in idx and idx[base]:
        return idx[base][0], "exact base-class donor"
    if base == "U" and "T" in idx and idx["T"]:
        return idx["T"][0], "T-like donor for U"
    # base_of maps TPN to U in most templates, so this usually works.
    if base == "U" and "U" in idx and idx["U"]:
        return idx["U"][0], "U/T-like donor for U"
    for alt in (["A", "G"] if base in {"A", "G"} else ["C", "U", "T"]):
        if alt in idx and idx[alt]:
            return idx[alt][0], f"fallback donor {alt}"
    first = sorted(idx)[0]
    return idx[first][0], "last-resort donor"


def base_fit_transform(pna_res, rna_res, base):
    common = [a for a in BASE_CORE_ATOMS.get(base, []) if a in pna_res and a in rna_res]
    if base == "U":
        # T donor may contain the same ring atoms as U.
        common = [a for a in BASE_CORE_ATOMS["U"] if a in pna_res and a in rna_res]
    if len(common) < 3:
        common = [a for a in ["N9", "N1", "C2", "C4", "C5", "C6"] if a in pna_res and a in rna_res]
    if len(common) < 3:
        raise ValueError(f"Not enough common base atoms for base-frame alignment: {common}")
    mobile = np.array([pna_res[a].coords for a in common])
    target = np.array([rna_res[a].coords for a in common])
    return kabsch(mobile, target), common


def build_initial_residues(source, template):
    idx = build_template_index(template)
    out = {}
    records = []
    initial_centers = {}
    skeys = source_keys(source)

    for skey in skeys:
        sres = source[skey]
        base = base_of(resname(sres))
        tkey, note = select_template(base, idx)
        tres = template[tkey]
        (r, tr, rmsd), common = base_fit_transform(tres, sres, base)

        out_name = target_res_name(base)
        out_res = {}

        # Transform PNA backbone into RNA base frame.
        for a in PNA_BACKBONE_ATOMS:
            out_res[a] = clone(
                tres[a],
                coords=apply(tres[a].coords, r, tr),
                atom_name=a,
                res_name=out_name,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                element=infer_element(a),
            )

        # Transform donor base into RNA base frame.
        for name, atom in pna_base_atoms(tres).items():
            if base == "U" and name == "C5M":
                continue
            out_res[name] = clone(
                atom,
                coords=apply(atom.coords, r, tr),
                atom_name=name,
                res_name=out_name,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                element=infer_element(name, atom.element),
            )

        # Record initial center for bounded movement.
        all_coords = np.array([a.coords for a in out_res.values()])
        initial_centers[skey] = all_coords.mean(axis=0)

        out[skey] = out_res
        records.append(
            ConversionRecord(
                source_key=skey,
                source_base=base,
                output_res_name=out_name,
                template_key=tkey,
                template_res_name=resname(tres),
                base_fit_rmsd=rmsd,
                total_shift=0.0,
                c8_to_n=None,
                next_link=None,
                missing_required_base_atoms=[],
                note=f"{note}; RNA base-frame placement; bounded hybrid smoothing pending",
            )
        )

    return out, records, initial_centers


def residue_center(res):
    return np.array([a.coords for a in res.values()]).mean(axis=0)


def translate_residue(res, delta):
    for atom in res.values():
        atom.coords = atom.coords + delta


def bounded_hybrid_smooth(out, initial_centers, *, iterations=60, link_target=1.34, step_cap=0.08, max_total_shift=2.5, spring=0.015):
    """
    Bounded pairwise smoothing.

    It nudges C'(i) and N1'(i+1) toward peptide-like continuity while preventing
    the catastrophic global collapse seen in 008A.1.
    """
    ks = keys(out)
    total_shift = {k: np.zeros(3, dtype=float) for k in ks}

    def can_pair(a, b):
        return a[0] == b[0] and b[1] == a[1] + 1 and not a[2] and not b[2]

    for _ in range(iterations):
        # Pairwise linkage nudges.
        for lk, rk in zip(ks[:-1], ks[1:]):
            if not can_pair(lk, rk):
                continue
            if "C'" not in out[lk] or "N1'" not in out[rk]:
                continue
            v = out[rk]["N1'"].coords - out[lk]["C'"].coords
            d = float(np.linalg.norm(v))
            if d < 1e-8:
                continue
            unit = v / d
            err = d - link_target

            # Move only a capped amount. If distance is too long, bring closer;
            # if too short, push apart.
            move_mag = min(abs(err) * 0.10, step_cap)
            move = move_mag * unit * (1.0 if err > 0 else -1.0)

            # Current residue moves toward next N1'; next moves toward previous C' in opposite direction.
            proposals = [(lk, +0.5 * move), (rk, -0.5 * move)]
            for k, delta in proposals:
                proposed_total = total_shift[k] + delta
                if float(np.linalg.norm(proposed_total)) <= max_total_shift:
                    translate_residue(out[k], delta)
                    total_shift[k] = proposed_total

        # Weak spring back toward initial RNA base-frame placement.
        for k in ks:
            center = residue_center(out[k])
            back = initial_centers[k] - center
            delta = spring * back
            proposed_total = total_shift[k] + delta
            if float(np.linalg.norm(proposed_total)) <= max_total_shift:
                translate_residue(out[k], delta)
                total_shift[k] = proposed_total

    return total_shift


def finalize_records(out, records, total_shift):
    rec_by_key = {r.source_key: r for r in records}
    oks = keys(out)

    for k in oks:
        rec = rec_by_key[k]
        base = rec.source_base
        g = gly_atom(base)
        if "C8'" in out[k] and g in out[k]:
            rec.c8_to_n = float(np.linalg.norm(out[k]["C8'"].coords - out[k][g].coords))
        rec.total_shift = float(np.linalg.norm(total_shift.get(k, np.zeros(3))))
        rec.missing_required_base_atoms = [a for a in BASE_REQUIRED_OXYGENS.get(base, []) if a not in out[k]]
        rec.note = rec.note.replace("bounded hybrid smoothing pending", "bounded hybrid smoothing applied")

    for lk, rk in zip(oks[:-1], oks[1:]):
        if lk[0] == rk[0] and rk[1] == lk[1] + 1 and not lk[2] and not rk[2]:
            if "C'" in out[lk] and "N1'" in out[rk]:
                rec_by_key[lk].next_link = float(np.linalg.norm(out[lk]["C'"].coords - out[rk]["N1'"].coords))

    return records


def convert(source, template, *, iterations=60, step_cap=0.08, max_total_shift=2.5, spring=0.015):
    out, records, initial_centers = build_initial_residues(source, template)
    total_shift = bounded_hybrid_smooth(
        out,
        initial_centers,
        iterations=iterations,
        step_cap=step_cap,
        max_total_shift=max_total_shift,
        spring=spring,
    )
    records = finalize_records(out, records, total_shift)
    return out, records


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
        f.write("REMARK   Digital Polymerase Prototype 008D\n")
        f.write("REMARK   RNA-informed PNA hybrid-guided candidate reconstruction\n")
        f.write(f"REMARK   Source RNA sequence: {src_seq}\n")
        f.write(f"REMARK   PNA template base-class sequence: {tmpl_seq}\n")
        f.write("REMARK   Strategy: RNA base-frame placement + bounded PNA linkage smoothing\n")
        f.write("REMARK   WARNING: Experimental boundary-test prototype; not physically validated\n")
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
    failed = sum(1 for v in vals if not (1.20 <= v <= 1.85))
    return DistanceSummary("C8'→glycosidic N", len(vals), missing, failed, float(np.mean(vals)) if vals else float("nan"), float(np.min(vals)) if vals else float("nan"), float(np.max(vals)) if vals else float("nan"), 1.20, 1.85)


def validate_base_oxygens(residues):
    missing = 0
    measured = 0
    for k in keys(residues):
        base = base_of(resname(residues[k]))
        required = BASE_REQUIRED_OXYGENS.get(base, [])
        measured += len(required)
        for atom in required:
            if atom not in residues[k]:
                missing += 1
    failed = missing
    ok = measured - missing
    return DistanceSummary("required base oxygens present", ok, missing, failed, float(ok), float(ok), float(ok), 1.0, float(measured) if measured else 1.0)


def clash_summary(residues, cutoff=1.00):
    # Crude heavy-atom clash count across different residues only.
    atoms = []
    for k in keys(residues):
        for name, atom in residues[k].items():
            if atom.element != "H":
                atoms.append((k, name, atom.coords))
    count = 0
    min_d = float("inf")
    for i in range(len(atoms)):
        ki, ni, ci = atoms[i]
        for j in range(i + 1, len(atoms)):
            kj, nj, cj = atoms[j]
            if ki == kj:
                continue
            d = float(np.linalg.norm(ci - cj))
            min_d = min(min_d, d)
            if d < cutoff:
                count += 1
    return count, min_d if min_d < float("inf") else float("nan")


def status(s):
    return "NO_DATA" if s.measured == 0 and s.missing == 0 else ("PASS" if s.failed == 0 else "FAIL")


def build_validation(output):
    return {
        "PNA C'(i)→N1'(i+1)": validate_inter(output, "C'", "N1'", 1.15, 2.80, "PNA C'(i)→N1'(i+1)"),
        "C8'→glycosidic N": validate_base_attachment(output),
        "C8'→C7'": validate_intra(output, "C8'", "C7'", 1.30, 1.85, "C8'→C7'"),
        "C7'→O7'": validate_intra(output, "C7'", "O7'", 1.10, 1.40, "C7'→O7'"),
        "C7'→N4'": validate_intra(output, "C7'", "N4'", 1.15, 1.60, "C7'→N4'"),
        "N4'→C3'": validate_intra(output, "N4'", "C3'", 1.25, 1.80, "N4'→C3'"),
        "C3'→C2'": validate_intra(output, "C3'", "C2'", 1.25, 1.90, "C3'→C2'"),
        "C2'→N1'": validate_intra(output, "C2'", "N1'", 1.20, 1.80, "C2'→N1'"),
        "N4'→C5'": validate_intra(output, "N4'", "C5'", 1.25, 1.80, "N4'→C5'"),
        "C5'→C'": validate_intra(output, "C5'", "C'", 1.25, 1.90, "C5'→C'"),
        "C'→O1'": validate_intra(output, "C'", "O1'", 1.10, 1.40, "C'→O1'"),
        "required base oxygens present": validate_base_oxygens(output),
    }


def validation_table(checks):
    lines = [
        "| Metric | Measured | Missing | Failed | Mean | Min | Max | Expected | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for label, s in checks.items():
        lines.append(f"| {label} | {s.measured} | {s.missing} | {s.failed} | {s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | {s.lo:.2f}–{s.hi:.2f} | {status(s)} |")
    return "\n".join(lines)


def classify_008d(output, records, checks, clash_count):
    # Conservative boundary-test classification.
    link = checks["PNA C'(i)→N1'(i+1)"]
    base = checks["C8'→glycosidic N"]
    oxy = checks["required base oxygens present"]
    max_shift = max((r.total_shift for r in records), default=0.0)
    if base.failed == 0 and oxy.failed == 0 and max_shift <= 2.6 and clash_count < max(10, len(records) * 4):
        if link.failed == 0:
            return "PASS_BOUNDARY_TEST"
        return "PARTIAL_PASS_LINKAGE_NOT_FULLY_SOLVED"
    return "FAIL_OR_TOO_ROUGH"


def write_report(path, source_path, template_path, output_path, source, template, output, records, params):
    checks = build_validation(output)
    clash_count, min_clash_distance = clash_summary(output)
    classification = classify_008d(output, records, checks, clash_count)

    c8n = [r.c8_to_n for r in records if r.c8_to_n is not None]
    links = [r.next_link for r in records if r.next_link is not None]
    shifts = [r.total_shift for r in records]
    rmsds = [r.base_fit_rmsd for r in records]

    rec_lines = []
    for i, r in enumerate(records, 1):
        rec_lines.append(
            f"| {i} | {r.source_key[0]}{r.source_key[1]}{r.source_key[2]} | {r.source_base} | {r.output_res_name} | "
            f"{r.template_res_name} {r.template_key[0]}{r.template_key[1]}{r.template_key[2]} | "
            f"{r.base_fit_rmsd:.4f} | {r.total_shift:.4f} | {r.c8_to_n if r.c8_to_n is not None else 'NA'} | "
            f"{r.next_link if r.next_link is not None else 'NA'} | "
            f"{','.join(r.missing_required_base_atoms) if r.missing_required_base_atoms else 'none'} | {r.note} |"
        )

    md = f"""# RNA → PNA Hybrid-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 008D  
**Method:** RNA-informed PNA hybrid-guided reconstruction  
**Status:** Experimental boundary-test candidate; not physically validated  
**Classification:** `{classification}`  
**PNA chain-continuity status:** `C′(i)→N1′(i+1) {status(checks["PNA C'(i)→N1'(i+1)"])}`  
**Base-attachment status:** `{status(checks["C8'→glycosidic N"])}`  
**Base-oxygen audit:** `{status(checks["required base oxygens present"])}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- PNA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source and Template

- Source RNA sequence: `{source_sequence(source)}`
- PNA template base-class sequence: `{template_sequence(template)}`
- Source residue count: `{len(source_keys(source))}`
- Usable template residue count: `{len(usable_template_keys(template))}`
- Converted residues: `{len(records)}`

---

## 008D Strategy

Prototype 008D is a hybrid boundary-test.

It uses:

```text
RNA base-frame alignment
+
PNA local pseudopeptide scaffold
+
bounded C′(i)→N1′(i+1) smoothing
+
movement caps to prevent collapse
```

This is intentionally different from:

```text
008A.1 → aggressive RNA-fold forcing
008B   → template-primary scaffold-first generation
008C   → sequence-primary generation
```

008D asks:

```text
Can PNA be nudged toward RNA-informed geometry without collapsing?
```

---

## Parameters

```text
iterations       = {params["iterations"]}
step_cap         = {params["step_cap"]}
max_total_shift  = {params["max_total_shift"]}
spring           = {params["spring"]}
```

---

## Structural Validation

{validation_table(checks)}

---

## Global Sanity Diagnostics

- Mean base-fit RMSD: `{np.mean(rmsds) if rmsds else float('nan'):.4f} Å`
- Maximum base-fit RMSD: `{np.max(rmsds) if rmsds else float('nan'):.4f} Å`
- Mean total residue shift: `{np.mean(shifts) if shifts else float('nan'):.4f} Å`
- Maximum total residue shift: `{np.max(shifts) if shifts else float('nan'):.4f} Å`
- Mean C8′→glycosidic N distance: `{np.mean(c8n) if c8n else float('nan'):.4f} Å`
- Mean C′(i)→N1′(i+1) distance: `{np.mean(links) if links else float('nan'):.4f} Å`
- Heavy-atom inter-residue clashes below 1.00 Å: `{clash_count}`
- Minimum inter-residue heavy-atom distance: `{min_clash_distance:.4f} Å`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Base-fit RMSD (Å) | Total shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|
{chr(10).join(rec_lines)}

---

## Interpretation

Correct description:

> a PNA-like computational candidate generated by RNA base-frame guidance plus bounded PNA linkage smoothing.

Incorrect description:

> a solved, physically validated, RNA-fold-preserving PNA analog.

The classification should be interpreted conservatively. If `C′(i)→N1′(i+1)` remains failed while the visual model is not tangled, that is still valuable: it indicates where PNA resists RNA-informed conversion.
"""
    path.write_text(md, encoding="utf-8")


def run(source_path: Path, template_path: Path, output_path: Path, report_path: Path, iterations=60, step_cap=0.08, max_total_shift=2.5, spring=0.015):
    source = parse_pdb(source_path)
    template = parse_pdb(template_path)
    output, records = convert(source, template, iterations=iterations, step_cap=step_cap, max_total_shift=max_total_shift, spring=spring)
    write_pdb(output, output_path, source_sequence(source), template_sequence(template))
    write_report(
        report_path, source_path, template_path, output_path, source, template, output, records,
        {"iterations": iterations, "step_cap": step_cap, "max_total_shift": max_total_shift, "spring": spring},
    )

    checks = build_validation(output)
    clash_count, min_clash_distance = clash_summary(output)
    classification = classify_008d(output, records, checks, clash_count)

    print("=" * 80)
    print("Digital Polymerase Prototype 008D")
    print("RNA-informed PNA hybrid-guided candidate reconstruction")
    print("=" * 80)
    print(f"Source RNA: {source_path}")
    print(f"PNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    print(f"Report: {report_path}")
    print(f"Source sequence: {source_sequence(source)}")
    print(f"Converted residues: {len(records)}")
    print(f"Classification: {classification}")
    print("-" * 80)
    for label in ["PNA C'(i)→N1'(i+1)", "C8'→glycosidic N", "C8'→C7'", "C7'→O7'", "C7'→N4'", "C'→O1'", "required base oxygens present"]:
        s = checks[label]
        print(f"{label}: {status(s)} (measured={s.measured}, missing={s.missing}, failed={s.failed}, mean={s.mean:.3f})")
    print(f"Clashes <1.00 Å: {clash_count}; min inter-residue heavy atom distance: {min_clash_distance:.3f} Å")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Prototype 008D: RNA-informed PNA hybrid-guided builder.")
    parser.add_argument("--rna", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--iterations", default=60, type=int)
    parser.add_argument("--step-cap", default=0.08, type=float)
    parser.add_argument("--max-total-shift", default=2.5, type=float)
    parser.add_argument("--spring", default=0.015, type=float)
    args = parser.parse_args()
    run(
        args.rna, args.template, args.output, args.report,
        iterations=args.iterations,
        step_cap=args.step_cap,
        max_total_shift=args.max_total_shift,
        spring=args.spring,
    )


if __name__ == "__main__":
    main()
