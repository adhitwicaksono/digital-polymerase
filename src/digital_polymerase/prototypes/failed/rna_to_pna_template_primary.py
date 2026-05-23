#!/usr/bin/env python3
"""
Prototype 008B: RNA to PNA Template-Primary Converter

Digital Polymerase / XNA World Project

PNA is the chimaera. Prototype 008A.1 failed because it tried to force a
pseudopeptide PNA backbone onto an RNA fold. Prototype 008B reverses the logic:

    PNA scaffold first
    +
    RNA sequence/base identity second

This converter preserves/tiles a clean PNA template scaffold and replaces the
nucleobases according to the RNA sequence.

Important:
- This is a computational candidate generator only.
- It does NOT preserve the RNA 3D fold.
- It is intended to produce a clean PNA-like candidate scaffold first.
- Outputs are not energy-minimized, MD-ready, or physically validated.
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

BASE_CORE_ATOMS = {
    "A": ["N9", "C8", "N7", "C5", "C6", "N6", "N1", "C2", "N3", "C4"],
    "G": ["N9", "C8", "N7", "C5", "C6", "O6", "N1", "C2", "N2", "N3", "C4"],
    "C": ["N1", "C2", "O2", "N3", "C4", "N4", "C5", "C6"],
    "U": ["N1", "C2", "O2", "N3", "C4", "O4", "C5", "C6"],  # donor may be TPN; C5M is removed
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
    scaffold_template_key: ResidueKey
    scaffold_template_res_name: str
    base_donor_key: ResidueKey
    base_donor_res_name: str
    tile_index: int
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
            residues[(chain, rn, ic)][name] = Atom("HETATM", name, resn, chain, rn, ic, xyz, occ, temp, infer_element(name, elem))
        except Exception:
            continue
    return dict(residues)


def keys(residues):
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def usable_template_keys(residues):
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


def source_sequence(residues):
    return "".join(base_of(resname(residues[k])) for k in keys(residues) if base_of(resname(residues[k])) in {"A", "U", "G", "C"})


def template_sequence(template):
    return "".join(base_of(resname(template[k])) for k in usable_template_keys(template))


def target_res_name(base: str, policy="preserve"):
    if policy == "dna-like":
        return {"A": "APN", "U": "TPN", "G": "GPN", "C": "CPN"}.get(base, "PNN")
    return {"A": "APN", "U": "UPN", "G": "GPN", "C": "CPN"}.get(base, "PNN")


def gly_atom(base: str) -> str:
    return "N9" if base in {"A", "G"} else "N1"


def is_base_atom(name: str) -> bool:
    if name in PNA_BACKBONE_ATOMS:
        return False
    if name.startswith("H"):
        return False
    return name not in {"N", "CA", "C", "O"}


def base_atoms(residue):
    return {n: a for n, a in residue.items() if is_base_atom(n)}


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


def build_base_donor_index(template):
    index = defaultdict(list)
    for k in usable_template_keys(template):
        index[base_of(resname(template[k]))].append(k)
    return dict(index)


def select_base_donor(base, donor_index):
    if base in donor_index and donor_index[base]:
        return donor_index[base][0], "exact base donor"
    if base == "U" and "T" in donor_index and donor_index["T"]:
        return donor_index["T"][0], "T-like donor used for RNA U"
    # Because base_of maps TPN to U, this usually catches RNA U already.
    if base == "U" and "U" in donor_index and donor_index["U"]:
        return donor_index["U"][0], "U/T-like donor used for RNA U"
    for alt in (["A", "G"] if base in {"A", "G"} else ["C", "U", "T"]):
        if alt in donor_index and donor_index[alt]:
            return donor_index[alt][0], f"fallback donor {alt}"
    first = sorted(donor_index)[0]
    return donor_index[first][0], "last-resort donor"


def tile_translation_vector(template, tkeys):
    if len(tkeys) < 2:
        return np.array([8.0, 0.0, 0.0])
    first = template[tkeys[0]]
    last = template[tkeys[-1]]
    penult = template[tkeys[-2]]
    # Choose the next-tile N1' so it continues from last C' at a peptide-like distance.
    direction = last["C'"].coords - penult["C'"].coords
    norm = float(np.linalg.norm(direction))
    if norm < 1e-8:
        direction = last["C8'"].coords - first["C8'"].coords
        norm = float(np.linalg.norm(direction))
    if norm < 1e-8:
        direction = np.array([1.0, 0.0, 0.0])
        norm = 1.0
    direction = direction / norm
    return last["C'"].coords + 1.34 * direction - first["N1'"].coords


def backbone_transform_from_acceptor_to_donor(acceptor_res, donor_res, acceptor_shift):
    anchors = [a for a in ["C8'", "C7'", "N4'", "C3'", "C2'", "N1'", "C5'", "C'"] if a in donor_res and a in acceptor_res]
    if len(anchors) < 3:
        raise ValueError("Not enough PNA backbone anchors")
    mobile = np.array([donor_res[a].coords for a in anchors])
    target = np.array([acceptor_res[a].coords + acceptor_shift for a in anchors])
    r, t, rmsd = kabsch(mobile, target)
    return r, t, rmsd


def convert(source, template, *, base_label_policy="preserve", mode="template-primary"):
    src_keys = [k for k in keys(source) if base_of(resname(source[k])) in {"A", "U", "G", "C"}]
    src_seq = [base_of(resname(source[k])) for k in src_keys]
    tkeys = usable_template_keys(template)
    donor_index = build_base_donor_index(template)
    if not tkeys:
        raise ValueError("No usable PNA template residues found")

    tile_vec = tile_translation_vector(template, tkeys)
    output = {}
    records = []

    for i, (skey, base) in enumerate(zip(src_keys, src_seq)):
        tile = i // len(tkeys)
        local_i = i % len(tkeys)
        scaffold_key = tkeys[local_i]
        scaffold_res = template[scaffold_key]
        shift = tile * tile_vec

        donor_key, donor_note = select_base_donor(base, donor_index)
        donor_res = template[donor_key]
        r, tr, _rmsd = backbone_transform_from_acceptor_to_donor(scaffold_res, donor_res, shift)

        out_name = target_res_name(base, base_label_policy)
        out_res = {}

        # Scaffold first: copy PNA backbone from template/tile.
        for a in PNA_BACKBONE_ATOMS:
            out_res[a] = clone(
                scaffold_res[a],
                coords=scaffold_res[a].coords + shift,
                atom_name=a,
                res_name=out_name,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                element=infer_element(a),
            )

        # Base second: copy donor base transformed into scaffold frame.
        donor_base_atoms = base_atoms(donor_res)
        copied = []
        for name, atom in donor_base_atoms.items():
            if base == "U" and name == "C5M":
                continue  # convert thymine donor to uracil-like base by omitting methyl group
            if name in PNA_BACKBONE_ATOMS:
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
            copied.append(name)

        c8n = None
        g = gly_atom(base)
        if "C8'" in out_res and g in out_res:
            c8n = float(np.linalg.norm(out_res["C8'"].coords - out_res[g].coords))

        next_link = None
        # compute after all residues? approximate if next acceptor scaffold exists
        output[skey] = out_res

        missing = [a for a in BASE_REQUIRED_OXYGENS.get(base, []) if a not in out_res]
        records.append(
            ConversionRecord(
                source_key=skey,
                source_base=base,
                output_res_name=out_name,
                scaffold_template_key=scaffold_key,
                scaffold_template_res_name=resname(scaffold_res),
                base_donor_key=donor_key,
                base_donor_res_name=resname(donor_res),
                tile_index=tile,
                c8_to_n=c8n,
                next_link=None,
                missing_required_base_atoms=missing,
                note=f"{donor_note}; template-primary PNA scaffold; RNA fold not preserved",
            )
        )

    # Fill next-link values.
    out_keys = keys(output)
    rec_by_key = {r.source_key: r for r in records}
    for lk, rk in zip(out_keys[:-1], out_keys[1:]):
        if lk[0] == rk[0] and rk[1] == lk[1] + 1 and not lk[2] and not rk[2]:
            if "C'" in output[lk] and "N1'" in output[rk]:
                rec_by_key[lk].inter_c_to_n1_next = float(np.linalg.norm(output[lk]["C'"].coords - output[rk]["N1'"].coords))

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
        f.write("REMARK   Digital Polymerase Prototype 008B\n")
        f.write("REMARK   RNA to PNA template-primary base-replacement candidate\n")
        f.write(f"REMARK   Source RNA sequence: {src_seq}\n")
        f.write(f"REMARK   PNA template base-class sequence: {tmpl_seq}\n")
        f.write("REMARK   Strategy: preserve/tile PNA template scaffold; replace bases by RNA sequence\n")
        f.write("REMARK   WARNING: RNA fold is NOT preserved\n")
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


def validate_base_oxygens(residues):
    missing = 0
    measured = 0
    for k in keys(residues):
        base = base_of(resname(residues[k]))
        required = BASE_REQUIRED_OXYGENS.get(base, [])
        if not required:
            continue
        measured += len(required)
        for atom in required:
            if atom not in residues[k]:
                missing += 1
    failed = missing
    ok_count = measured - missing
    return DistanceSummary("required base oxygens present", ok_count, missing, failed, float(ok_count), float(ok_count), float(ok_count), 1.0, float(measured) if measured else 1.0)


def status(s):
    return "NO_DATA" if s.measured == 0 and s.missing == 0 else ("PASS" if s.failed == 0 else "FAIL")


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
        "required base oxygens present": validate_base_oxygens(output),
    }


def validation_table(checks):
    lines = [
        "| Metric | Measured | Missing | Failed | Mean (Å/count) | Min | Max | Expected | Status |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for label, s in checks.items():
        lines.append(f"| {label} | {s.measured} | {s.missing} | {s.failed} | {s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | {s.lo:.2f}–{s.hi:.2f} | {status(s)} |")
    return "\n".join(lines)


def write_report(path, source_path, template_path, output_path, source, template, output, records):
    checks = build_validation(output)
    c8n = [r.c8_to_n for r in records if r.c8_to_n is not None]
    links = [r.inter_c_to_n1_next for r in records if r.inter_c_to_n1_next is not None]
    missing_count = sum(len(r.missing_required_base_atoms) for r in records)

    rec_lines = []
    for i, r in enumerate(records, 1):
        rec_lines.append(
            f"| {i} | {r.source_key[0]}{r.source_key[1]}{r.source_key[2]} | {r.source_base} | {r.output_res_name} | "
            f"{r.scaffold_template_res_name} {r.scaffold_template_key[0]}{r.scaffold_template_key[1]}{r.scaffold_template_key[2]} | "
            f"{r.base_donor_res_name} {r.base_donor_key[0]}{r.base_donor_key[1]}{r.base_donor_key[2]} | "
            f"{r.tile_index} | {r.c8_to_n if r.c8_to_n is not None else 'NA'} | "
            f"{r.inter_c_to_n1_next if r.inter_c_to_n1_next is not None else 'NA'} | "
            f"{','.join(r.missing_required_base_atoms) if r.missing_required_base_atoms else 'none'} | {r.note} |"
        )

    md = f"""# RNA → PNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 008B  
**Method:** PNA template-primary base replacement  
**Status:** Experimental candidate, not physically validated  
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
- Source residue count: `{len([k for k in keys(source) if base_of(resname(source[k])) in {"A", "U", "G", "C"}])}`
- Usable template residue count: `{len(usable_template_keys(template))}`
- Converted residues: `{len(records)}`

---

## Why Prototype 008B Exists

Prototype 008A.1 tried to force a PNA pseudopeptide backbone onto an RNA fold and produced a tangled 8-mer.

Prototype 008B reverses the logic:

```text
PNA scaffold first
RNA sequence/base identity second
```

This means the RNA fold is not preserved. The priority is to produce a clean PNA-like candidate scaffold.

---

## Method Summary

Prototype 008B performs template-primary PNA reconstruction:

1. read the RNA sequence from the source PDB
2. preserve or tile the PNA template scaffold
3. select a PNA base donor by target RNA base identity
4. transform the donor base onto the scaffold residue
5. remove thymine `C5M` when using T-like donor for RNA U
6. validate PNA backbone geometry
7. validate `C8′→glycosidic N`
8. audit expected base oxygens

---

## Structural Validation

{validation_table(checks)}

---

## Summary Metrics

- Mean C8′→glycosidic N distance: `{np.mean(c8n) if c8n else float('nan'):.4f} Å`
- Mean C′(i)→N1′(i+1) distance: `{np.mean(links) if links else float('nan'):.4f} Å`
- Missing required base oxygen atoms: `{missing_count}`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Scaffold template | Base donor | Tile | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|---|
{chr(10).join(rec_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a PNA-like computational candidate generated by template-primary base replacement.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready PNA structure.

---

## Important Limitation

Prototype 008B does **not** preserve the RNA 3D fold. This is intentional.

It is designed to answer a narrower question:

```text
Can we produce a clean PNA-like candidate with the same base sequence?
```

not:

```text
Can we force PNA to adopt the original RNA tertiary structure?
```
"""
    path.write_text(md, encoding="utf-8")


def run(source_path: Path, template_path: Path, output_path: Path, report_path: Path):
    source = parse_pdb(source_path)
    template = parse_pdb(template_path)
    output, records = convert(source, template)
    write_pdb(output, output_path, source_sequence(source), template_sequence(template))
    write_report(report_path, source_path, template_path, output_path, source, template, output, records)

    checks = build_validation(output)
    print("=" * 80)
    print("Digital Polymerase Prototype 008B")
    print("RNA → PNA template-primary base replacement")
    print("=" * 80)
    print(f"Source RNA: {source_path}")
    print(f"PNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    print(f"Report: {report_path}")
    print(f"Source sequence: {source_sequence(source)}")
    print(f"Template sequence: {template_sequence(template)}")
    print(f"Converted residues: {len(records)}")
    print("-" * 80)
    for label in ["PNA C'(i)→N1'(i+1)", "C8'→glycosidic N", "C8'→C7'", "C7'→O7'", "C7'→N4'", "C'→O1'", "required base oxygens present"]:
        s = checks[label]
        print(f"{label}: {status(s)} (measured={s.measured}, missing={s.missing}, failed={s.failed}, mean={s.mean:.3f})")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Prototype 008B: RNA to PNA template-primary converter.")
    parser.add_argument("--rna", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    run(args.rna, args.template, args.output, args.report)


if __name__ == "__main__":
    main()
