#!/usr/bin/env python3
"""
Prototype 004A: RNA to CeNA Converter

Digital Polymerase / XNA World Project

This script generates CeNA-like candidate PDB structures from RNA PDB inputs
using a CeNA template.

Supported modes:

1. full-template
   - Used when the CeNA template is at least as long as the RNA input.
   - Takes the CeNA backbone/scaffold directly from the template.
   - Transforms and transplants RNA bases onto the CeNA scaffold.

2. chain-preserving
   - Used when the RNA input is longer than the CeNA template.
   - Preserves source RNA chain-continuity atoms.
   - Inserts local CeNA cyclohexenyl scaffold atoms from the CeNA template.
   - Removes RNA O4' and introduces CeNA-like C6' and C7' geometry.
   - Transforms RNA bases onto the new CeNA-like local scaffold.

Default mode:
    auto

In auto mode:
    if CeNA template length >= RNA length: use full-template
    else: use chain-preserving

Important:
- This is NOT a chemically or physically validated CeNA modeling package.
- Outputs are computational candidate structures.
- They require visual inspection, stereochemical review, topology/force-field
  review, energy minimization, and expert chemical validation before use in
  scientific conclusions.
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

# CeNA template residues observed in 2H0N-like templates:
# XGL, XTL, XAL, XCL.

# Full CeNA scaffold/backbone atom recognition.
CENA_BACKBONE_ATOMS = {
    "P", "OP1", "OP2", "O1P", "O2P",
    "O5'", "C5'", "C4'", "C6'", "C7'",
    "C3'", "O3'", "C2'", "C1'",
}

# In chain-preserving mode, these are kept directly from the RNA source
# to preserve polymer continuity and the source chain path.
CHAIN_PRESERVE_ATOMS = {
    "P", "OP1", "OP2", "O1P", "O2P",
    "O5'", "C5'", "C4'", "C3'", "O3'",
}

# In chain-preserving mode, these are inserted from the CeNA template.
# RNA O4' is not preserved because CeNA has a cyclohexenyl-like scaffold.
CENA_LOCAL_ATOMS = {
    "C1'", "C2'", "C6'", "C7'",
}

BACKBONE_ORDER = [
    "P", "OP1", "OP2", "O1P", "O2P",
    "O5'", "C5'", "C4'",
    "C6'", "C7'", "C1'", "C2'",
    "C3'", "O3'",
]

FULL_TEMPLATE_ANCHORS = ["C1'", "C2'", "C3'", "C4'"]
CHAIN_TEMPLATE_ANCHORS = ["O5'", "C5'", "C4'", "C3'", "O3'"]
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

            atom = Atom(
                record=record,
                atom_name=atom_name,
                res_name=res_name,
                chain=chain,
                res_num=res_num,
                insertion_code=insertion_code,
                coords=np.array([x, y, z], dtype=float),
                occupancy=float(occ_str) if occ_str else 1.0,
                temp_factor=float(temp_str) if temp_str else 0.0,
                element=infer_element(atom_name, elem_str),
            )
            residues[(chain, res_num, insertion_code)][atom_name] = atom
        except Exception:
            continue

    return dict(residues)


def sorted_residue_keys(residues: Dict[ResidueKey, Dict[str, Atom]]) -> List[ResidueKey]:
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def residue_name(residue: Dict[str, Atom]) -> str:
    return next(iter(residue.values())).res_name


def normalize_base(res_name: str) -> str:
    r = res_name.strip().upper()

    if r in RNA_BASES:
        return r

    # CeNA templates: XAL, XCL, XGL, XTL.
    if r in {"XAL", "CNA", "CEA"} or r.endswith("A"):
        return "A"
    if r in {"XGL", "CEG"} or r.endswith("G"):
        return "G"
    if r in {"XCL", "CEC"} or r.endswith("C"):
        return "C"
    if r in {"XTL", "XUL", "CET", "CEU"} or r.endswith("T") or r.endswith("U"):
        return "U"

    if r.startswith("A"):
        return "A"
    if r.startswith("G"):
        return "G"
    if r.startswith("C"):
        return "C"
    if r.startswith("T") or r.startswith("U"):
        return "U"

    return r[0] if r else "N"


def sequence(residues: Dict[ResidueKey, Dict[str, Atom]]) -> str:
    return "".join(normalize_base(residue_name(residues[k])) for k in sorted_residue_keys(residues))


def is_backbone_atom(atom_name: str) -> bool:
    if atom_name in CENA_BACKBONE_ATOMS:
        return True
    if "'" in atom_name:
        return True
    return False


def split_backbone_base(residue: Dict[str, Atom]) -> Tuple[Dict[str, Atom], Dict[str, Atom]]:
    backbone = {n: a for n, a in residue.items() if is_backbone_atom(n)}
    base = {n: a for n, a in residue.items() if not is_backbone_atom(n)}
    return backbone, base


def kabsch(mobile: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    if mobile.shape != target.shape:
        raise ValueError("mobile and target arrays must have same shape")
    if mobile.ndim != 2 or mobile.shape[1] != 3:
        raise ValueError("coordinates must be N x 3")
    if mobile.shape[0] < 3:
        raise ValueError("at least 3 anchors are required")

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


def apply_transform(coord: np.ndarray, r: np.ndarray, t: np.ndarray) -> np.ndarray:
    return r @ coord + t


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
    out_name = atom_name if atom_name is not None else atom.atom_name
    return Atom(
        record=record if record is not None else atom.record,
        atom_name=out_name,
        res_name=res_name if res_name is not None else atom.res_name,
        chain=chain if chain is not None else atom.chain,
        res_num=res_num if res_num is not None else atom.res_num,
        insertion_code=insertion_code if insertion_code is not None else atom.insertion_code,
        coords=np.array(coords if coords is not None else atom.coords, dtype=float),
        occupancy=atom.occupancy,
        temp_factor=atom.temp_factor,
        element=element if element is not None else infer_element(out_name, atom.element),
    )


def target_cena_residue_name(source_base: str, base_label_policy: str = "preserve") -> str:
    b = source_base.upper()
    if base_label_policy == "preserve":
        return {"A": "XAL", "U": "XUL", "G": "XGL", "C": "XCL"}.get(b, "XNL")
    if base_label_policy == "dna-like":
        return {"A": "XAL", "U": "XTL", "G": "XGL", "C": "XCL"}.get(b, "XNL")
    raise ValueError(f"Unsupported base label policy: {base_label_policy}")


def glycosidic_atom_for_base(base: str) -> str:
    return "N9" if base.upper() in {"A", "G"} else "N1"


def template_glycosidic_distance(template_residue: Dict[str, Atom], source_base: str) -> Optional[float]:
    gly_atom = glycosidic_atom_for_base(source_base)
    if "C1'" in template_residue and gly_atom in template_residue:
        d = float(np.linalg.norm(template_residue[gly_atom].coords - template_residue["C1'"].coords))
        if 1.20 <= d <= 1.80:
            return d
    return None


def adjust_base_attachment(
    residue: Dict[str, Atom],
    base_atom_names: Iterable[str],
    source_base: str,
    desired_distance: Optional[float],
) -> Optional[float]:
    gly_atom = glycosidic_atom_for_base(source_base)
    if desired_distance is None:
        desired_distance = 1.48

    if "C1'" not in residue or gly_atom not in residue:
        return None

    c1 = residue["C1'"].coords
    n = residue[gly_atom].coords
    vec = n - c1
    current = float(np.linalg.norm(vec))
    if current < 1e-6:
        return None

    unit = vec / current
    shift = (desired_distance - current) * unit

    for atom_name in base_atom_names:
        if atom_name in residue:
            residue[atom_name].coords = residue[atom_name].coords + shift

    return float(np.linalg.norm(residue[gly_atom].coords - residue["C1'"].coords))


def available_anchors(source_residue, template_residue, anchors) -> List[str]:
    return [a for a in anchors if a in source_residue and a in template_residue]


def build_template_index(template: Dict[ResidueKey, Dict[str, Atom]]) -> Dict[str, List[Tuple[ResidueKey, Dict[str, Atom]]]]:
    index: Dict[str, List[Tuple[ResidueKey, Dict[str, Atom]]]] = defaultdict(list)
    for key in sorted_residue_keys(template):
        res = template[key]
        if len(res) < 6:
            continue
        base = normalize_base(residue_name(res))
        index[base].append((key, res))
    return dict(index)


def select_template_for_base(
    source_base: str,
    template_index: Dict[str, List[Tuple[ResidueKey, Dict[str, Atom]]]],
    occurrence_counter: Dict[str, int],
) -> Tuple[ResidueKey, Dict[str, Atom], str, str]:
    base = source_base.upper()

    if base in template_index and template_index[base]:
        i = occurrence_counter.get(base, 0)
        occurrence_counter[base] = i + 1
        pool = template_index[base]
        key, res = pool[i % len(pool)]
        return key, res, base, "exact base-class CeNA template"

    if base == "U" and "T" in template_index and template_index["T"]:
        i = occurrence_counter.get("T", 0)
        occurrence_counter["T"] = i + 1
        pool = template_index["T"]
        key, res = pool[i % len(pool)]
        return key, res, "T", "T-like CeNA geometry donor used for RNA U"

    if base == "A" and "G" in template_index:
        i = occurrence_counter.get("G", 0)
        occurrence_counter["G"] = i + 1
        pool = template_index["G"]
        key, res = pool[i % len(pool)]
        return key, res, "G", "purine fallback: A uses G-like CeNA template"

    if base == "G" and "A" in template_index:
        i = occurrence_counter.get("A", 0)
        occurrence_counter["A"] = i + 1
        pool = template_index["A"]
        key, res = pool[i % len(pool)]
        return key, res, "A", "purine fallback: G uses A-like CeNA template"

    if base == "C" and "U" in template_index:
        i = occurrence_counter.get("U", 0)
        occurrence_counter["U"] = i + 1
        pool = template_index["U"]
        key, res = pool[i % len(pool)]
        return key, res, "U", "pyrimidine fallback: C uses U/T-like CeNA template"

    if base == "U" and "C" in template_index:
        i = occurrence_counter.get("C", 0)
        occurrence_counter["C"] = i + 1
        pool = template_index["C"]
        key, res = pool[i % len(pool)]
        return key, res, "C", "pyrimidine fallback: U uses C-like CeNA template"

    first = sorted(template_index.keys())[0]
    i = occurrence_counter.get(first, 0)
    occurrence_counter[first] = i + 1
    pool = template_index[first]
    key, res = pool[i % len(pool)]
    return key, res, first, f"last-resort fallback: uses {first}-like CeNA template"


def convert_full_template(
    source: Dict[ResidueKey, Dict[str, Atom]],
    template: Dict[ResidueKey, Dict[str, Atom]],
    *,
    anchors: List[str],
    base_label_policy: str,
) -> Tuple[Dict[ResidueKey, Dict[str, Atom]], List[ConversionRecord]]:
    source_keys = sorted_residue_keys(source)
    template_keys = sorted_residue_keys(template)

    if len(template_keys) < len(source_keys):
        raise ValueError(
            f"CeNA template has fewer residues ({len(template_keys)}) than source RNA ({len(source_keys)}). "
            "Use auto/chain-preserving mode for longer RNA inputs."
        )

    output: Dict[ResidueKey, Dict[str, Atom]] = {}
    records: List[ConversionRecord] = []

    for idx, skey in enumerate(source_keys):
        tkey = template_keys[idx]
        sres = source[skey]
        tres = template[tkey]
        source_base = normalize_base(residue_name(sres))
        target_name = target_cena_residue_name(source_base, base_label_policy)

        used = available_anchors(sres, tres, anchors)
        if len(used) < 3:
            raise ValueError(f"Not enough anchors for source {skey} and template {tkey}: {used}")

        # Transform source RNA base into CeNA template local frame.
        mobile = np.array([sres[a].coords for a in used])
        target = np.array([tres[a].coords for a in used])
        r, trans, rmsd = kabsch(mobile, target)

        cena_backbone, _cena_base = split_backbone_base(tres)
        _rna_backbone, rna_base_atoms = split_backbone_base(sres)

        out_res: Dict[str, Atom] = {}

        for atom_name, atom in cena_backbone.items():
            out_res[atom_name] = clone_atom(
                atom,
                res_name=target_name,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                record="HETATM",
            )

        transplanted_base_names = []
        for atom_name, atom in rna_base_atoms.items():
            new_coord = apply_transform(atom.coords, r, trans)
            out_res[atom_name] = clone_atom(
                atom,
                coords=new_coord,
                res_name=target_name,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                record="HETATM",
            )
            transplanted_base_names.append(atom_name)

        desired_gly = template_glycosidic_distance(tres, source_base)
        gly = adjust_base_attachment(out_res, transplanted_base_names, source_base, desired_gly)

        output[skey] = out_res
        records.append(
            ConversionRecord(
                source_key=skey,
                source_res_name=residue_name(sres),
                source_base=source_base,
                target_res_name=target_name,
                template_key=tkey,
                template_res_name=residue_name(tres),
                mode="full-template",
                anchor_atoms=used,
                anchor_rmsd=rmsd,
                base_anchor_rmsd=None,
                glycosidic_distance=gly,
                note="full CeNA scaffold from corresponding template residue; transformed source RNA base",
            )
        )

    return output, records


def convert_chain_preserving(
    source: Dict[ResidueKey, Dict[str, Atom]],
    template: Dict[ResidueKey, Dict[str, Atom]],
    *,
    chain_anchors: List[str],
    base_anchors: List[str],
    base_label_policy: str,
) -> Tuple[Dict[ResidueKey, Dict[str, Atom]], List[ConversionRecord]]:
    template_index = build_template_index(template)
    if not template_index:
        raise ValueError("Could not build usable CeNA template index")

    output: Dict[ResidueKey, Dict[str, Atom]] = {}
    records: List[ConversionRecord] = []
    occurrence_counter: Dict[str, int] = {}

    for skey in sorted_residue_keys(source):
        sres = source[skey]
        source_base = normalize_base(residue_name(sres))
        target_name = target_cena_residue_name(source_base, base_label_policy)

        tkey, tres, template_base, selection_note = select_template_for_base(
            source_base, template_index, occurrence_counter
        )

        used_chain_anchors = available_anchors(sres, tres, chain_anchors)
        if len(used_chain_anchors) < 3:
            used_chain_anchors = available_anchors(sres, tres, ["C3'", "C4'", "C5'"])

        if len(used_chain_anchors) < 3:
            raise ValueError(f"Not enough chain anchors for source {skey} and template {tkey}: {used_chain_anchors}")

        mobile = np.array([tres[a].coords for a in used_chain_anchors])
        target = np.array([sres[a].coords for a in used_chain_anchors])
        r_chain, t_chain, chain_rmsd = kabsch(mobile, target)

        out_res: Dict[str, Atom] = {}

        source_backbone, source_base_atoms = split_backbone_base(sres)

        # Preserve RNA chain-continuity atoms. RNA O4' is intentionally dropped.
        for atom_name, atom in source_backbone.items():
            if atom_name in CHAIN_PRESERVE_ATOMS:
                out_res[atom_name] = clone_atom(
                    atom,
                    res_name=target_name,
                    chain=skey[0],
                    res_num=skey[1],
                    insertion_code=skey[2],
                    record="HETATM",
                )

        # Insert local CeNA scaffold atoms transformed into RNA chain frame.
        for atom_name, atom in tres.items():
            if atom_name in CENA_LOCAL_ATOMS:
                new_coord = apply_transform(atom.coords, r_chain, t_chain)
                out_res[atom_name] = clone_atom(
                    atom,
                    coords=new_coord,
                    res_name=target_name,
                    chain=skey[0],
                    res_num=skey[1],
                    insertion_code=skey[2],
                    record="HETATM",
                )

        required = ["C1'", "C2'", "C3'", "C4'", "C6'", "C7'"]
        missing = [a for a in required if a not in out_res]
        if missing:
            raise ValueError(f"Converted residue {skey} missing required local CeNA atoms: {missing}")

        # Transform RNA base atoms from source local frame onto new CeNA-like local frame.
        used_base_anchors = [a for a in base_anchors if a in sres and a in out_res]
        if len(used_base_anchors) < 3:
            raise ValueError(f"Not enough base transplant anchors for {skey}: {used_base_anchors}")

        mobile_base = np.array([sres[a].coords for a in used_base_anchors])
        target_base = np.array([out_res[a].coords for a in used_base_anchors])
        r_base, t_base, base_rmsd = kabsch(mobile_base, target_base)

        transplanted_base_names = []
        for atom_name, atom in source_base_atoms.items():
            new_coord = apply_transform(atom.coords, r_base, t_base)
            out_res[atom_name] = clone_atom(
                atom,
                coords=new_coord,
                res_name=target_name,
                chain=skey[0],
                res_num=skey[1],
                insertion_code=skey[2],
                record="HETATM",
            )
            transplanted_base_names.append(atom_name)

        desired_gly = template_glycosidic_distance(tres, source_base)
        gly = adjust_base_attachment(out_res, transplanted_base_names, source_base, desired_gly)

        output[skey] = out_res
        records.append(
            ConversionRecord(
                source_key=skey,
                source_res_name=residue_name(sres),
                source_base=source_base,
                target_res_name=target_name,
                template_key=tkey,
                template_res_name=residue_name(tres),
                mode="chain-preserving",
                anchor_atoms=used_chain_anchors,
                anchor_rmsd=chain_rmsd,
                base_anchor_rmsd=base_rmsd,
                glycosidic_distance=gly,
                note=selection_note + "; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed",
            )
        )

    return output, records


def format_atom_line(serial: int, atom: Atom) -> str:
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


def atom_sort_key(name: str):
    if name in BACKBONE_ORDER:
        return (BACKBONE_ORDER.index(name), name)
    return (100, name)


def write_pdb(
    residues: Dict[ResidueKey, Dict[str, Atom]],
    output_path: Path,
    *,
    source_sequence: str,
    template_sequence: str,
    mode: str,
    base_label_policy: str,
) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        f.write("REMARK   Digital Polymerase Prototype 004A\n")
        f.write("REMARK   RNA to CeNA candidate reconstruction\n")
        f.write(f"REMARK   Mode: {mode}\n")
        f.write(f"REMARK   Source RNA sequence: {source_sequence}\n")
        f.write(f"REMARK   CeNA template base-class sequence: {template_sequence}\n")
        f.write(f"REMARK   Base label policy: {base_label_policy}\n")
        if mode == "full-template":
            f.write("REMARK   Method: CeNA scaffold from full template; RNA bases transformed and transplanted\n")
        else:
            f.write("REMARK   Method: RNA chain atoms preserved; CeNA local scaffold inserted; RNA bases transformed\n")
        f.write("REMARK   WARNING: Computational candidate only\n")
        f.write("REMARK   WARNING: Not energy-minimized, force-field-validated, or experimentally verified\n")
        f.write("REMARK   WARNING: CeNA residue names may be provisional, especially XUL if preserve policy is used\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")
        serial = 1
        for key in sorted_residue_keys(residues):
            res = residues[key]
            for name in sorted(res.keys(), key=atom_sort_key):
                f.write(format_atom_line(serial, res[name]) + "\n")
                serial += 1
        f.write("END\n")


def summarize_distances(label, records, missing, expected_min, expected_max):
    dists = [r.distance for r in records]
    failed = sum(1 for r in records if r.status == "FAIL")
    if dists:
        mean = float(np.mean(dists))
        minimum = float(np.min(dists))
        maximum = float(np.max(dists))
    else:
        mean = minimum = maximum = float("nan")
    return DistanceSummary(label, expected_min, expected_max, len(records), missing, failed, mean, minimum, maximum, records)


def validate_inter(residues, atom_left, atom_right, expected_min, expected_max, label, skip_numbering_gaps=True):
    keys = sorted_residue_keys(residues)
    records = []
    missing = 0
    for lk, rk in zip(keys[:-1], keys[1:]):
        if lk[0] != rk[0]:
            continue
        if skip_numbering_gaps and (rk[1] != lk[1] + 1 or lk[2] or rk[2]):
            continue
        lres = residues[lk]
        rres = residues[rk]
        if atom_left not in lres or atom_right not in rres:
            missing += 1
            continue
        d = float(np.linalg.norm(lres[atom_left].coords - rres[atom_right].coords))
        status = "PASS" if expected_min <= d <= expected_max else "FAIL"
        records.append(DistanceRecord(label, lk[0], lk[1], lk[2], atom_left, rk[1], rk[2], atom_right, d, expected_min, expected_max, status))
    return summarize_distances(label, records, missing, expected_min, expected_max)


def validate_intra(residues, atom_a, atom_b, expected_min, expected_max, label):
    records = []
    missing = 0
    for k in sorted_residue_keys(residues):
        res = residues[k]
        if atom_a not in res or atom_b not in res:
            missing += 1
            continue
        d = float(np.linalg.norm(res[atom_a].coords - res[atom_b].coords))
        status = "PASS" if expected_min <= d <= expected_max else "FAIL"
        records.append(DistanceRecord(label, k[0], k[1], k[2], atom_a, k[1], k[2], atom_b, d, expected_min, expected_max, status))
    return summarize_distances(label, records, missing, expected_min, expected_max)


def validate_glycosidic(residues):
    records = []
    missing = 0
    for k in sorted_residue_keys(residues):
        res = residues[k]
        base = normalize_base(residue_name(res))
        atom_b = glycosidic_atom_for_base(base)
        if "C1'" not in res or atom_b not in res:
            missing += 1
            continue
        d = float(np.linalg.norm(res["C1'"].coords - res[atom_b].coords))
        status = "PASS" if 1.30 <= d <= 1.75 else "FAIL"
        records.append(DistanceRecord("C1'→glycosidic N", k[0], k[1], k[2], "C1'", k[1], k[2], atom_b, d, 1.30, 1.75, status))
    return summarize_distances("C1'→glycosidic N", records, missing, 1.30, 1.75)


def validation_status(s: DistanceSummary) -> str:
    if s.measured == 0:
        return "NO_DATA"
    return "PASS" if s.failed == 0 else "FAIL"


def distance_summary_table(summaries_by_structure: Dict[str, Dict[str, DistanceSummary]]) -> str:
    labels = sorted({label for dct in summaries_by_structure.values() for label in dct})
    lines = [
        "| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for label in labels:
        for struct, dct in summaries_by_structure.items():
            if label not in dct:
                continue
            s = dct[label]
            lines.append(
                f"| {label} | {struct} | {s.measured} | {s.missing} | {s.failed} | "
                f"{s.mean:.3f} | {s.minimum:.3f} | {s.maximum:.3f} | "
                f"{s.expected_min:.2f}–{s.expected_max:.2f} | {validation_status(s)} |"
            )
    return "\n".join(lines)


def failed_table(summary: DistanceSummary, n=20) -> str:
    failed = [r for r in summary.records if r.status == "FAIL"]
    if not failed:
        return "No failed links detected."

    def deviation(r):
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
    for i, r in enumerate(failed, 1):
        link = f"{r.chain}{r.left_res_num}{r.left_icode}:{r.left_atom} → {r.chain}{r.right_res_num}{r.right_icode}:{r.right_atom}"
        lines.append(f"| {i} | `{link}` | {r.distance:.3f} | {r.expected_min:.2f}–{r.expected_max:.2f} | {r.status} |")
    return "\n".join(lines)


def build_validations(source, template, output, *, skip_numbering_gaps=True):
    def common(residues):
        return {
            "O3'(i)→P(i+1)": validate_inter(residues, "O3'", "P", 1.40, 1.80, "O3'(i)→P(i+1)", skip_numbering_gaps),
            "P(i)→O5'(i)": validate_intra(residues, "P", "O5'", 1.35, 1.90, "P(i)→O5'(i)"),
            "C1'→glycosidic N": validate_glycosidic(residues),
            "C1'→C2'": validate_intra(residues, "C1'", "C2'", 1.35, 1.85, "C1'→C2'"),
            "C2'→C3'": validate_intra(residues, "C2'", "C3'", 1.35, 1.85, "C2'→C3'"),
            "C3'→C4'": validate_intra(residues, "C3'", "C4'", 1.35, 1.85, "C3'→C4'"),
            "C4'→C5'": validate_intra(residues, "C4'", "C5'", 1.30, 1.80, "C4'→C5'"),
            "C3'→O3'": validate_intra(residues, "C3'", "O3'", 1.20, 1.65, "C3'→O3'"),
            "C5'→O5'": validate_intra(residues, "C5'", "O5'", 1.20, 1.75, "C5'→O5'"),
        }

    output_checks = common(output)
    output_checks.update({
        "C4'→C6'": validate_intra(output, "C4'", "C6'", 1.20, 1.70, "C4'→C6'"),
        "C6'→C7'": validate_intra(output, "C6'", "C7'", 1.15, 1.50, "C6'→C7'"),
        "C7'→C1'": validate_intra(output, "C7'", "C1'", 1.30, 1.85, "C7'→C1'"),
    })

    template_checks = common(template)
    template_checks.update({
        "C4'→C6'": validate_intra(template, "C4'", "C6'", 1.20, 1.70, "C4'→C6'"),
        "C6'→C7'": validate_intra(template, "C6'", "C7'", 1.15, 1.50, "C6'→C7'"),
        "C7'→C1'": validate_intra(template, "C7'", "C1'", 1.30, 1.85, "C7'→C1'"),
    })

    return {
        "source RNA": common(source),
        "CeNA template": template_checks,
        "output": output_checks,
    }


def write_report(
    report_path: Path,
    *,
    source_path: Path,
    template_path: Path,
    output_path: Path,
    source,
    template,
    output,
    records: List[ConversionRecord],
    requested_mode: str,
    actual_mode: str,
    base_label_policy: str,
    validations,
) -> None:
    src_seq = sequence(source)
    tmpl_seq = sequence(template)
    rmsd = [r.anchor_rmsd for r in records]
    base_rmsd = [r.base_anchor_rmsd for r in records if r.base_anchor_rmsd is not None]
    gly = [r.glycosidic_distance for r in records if r.glycosidic_distance is not None]

    o3p = validations["output"]["O3'(i)→P(i+1)"]
    glysum = validations["output"]["C1'→glycosidic N"]
    c4c6 = validations["output"]["C4'→C6'"]
    c6c7 = validations["output"]["C6'→C7'"]
    c7c1 = validations["output"]["C7'→C1'"]

    rec_lines = []
    for i, rec in enumerate(records, 1):
        gly_s = f"{rec.glycosidic_distance:.4f}" if rec.glycosidic_distance is not None else "NA"
        base_s = f"{rec.base_anchor_rmsd:.4f}" if rec.base_anchor_rmsd is not None else "NA"
        rec_lines.append(
            f"| {i} | {rec.source_key[0]}{rec.source_key[1]}{rec.source_key[2]} | {rec.source_base} | "
            f"{rec.target_res_name} | {rec.template_res_name} {rec.template_key[0]}{rec.template_key[1]}{rec.template_key[2]} | "
            f"{rec.mode} | {rec.anchor_rmsd:.4f} | {base_s} | {gly_s} | {rec.note} |"
        )

    report = f"""# RNA → CeNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 004A  
**Requested mode:** `{requested_mode}`  
**Actual mode:** `{actual_mode}`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `{validation_status(o3p)}`  
**Base-attachment status:** `{validation_status(glysum)}`  
**CeNA local scaffold status:** `C4′→C6′ {validation_status(c4c6)}`, `C6′→C7′ {validation_status(c6c7)}`, `C7′→C1′ {validation_status(c7c1)}`

---

## Inputs

- Source RNA PDB: `{source_path}`
- CeNA template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source and Template

- Source RNA sequence: `{src_seq}`
- CeNA template base-class sequence: `{tmpl_seq}`
- Source residue count: `{len(sorted_residue_keys(source))}`
- Template residue count: `{len(sorted_residue_keys(template))}`
- Converted residues: `{len(records)}`
- Base label policy: `{base_label_policy}`

---

## Method Summary

This converter supports two RNA → CeNA modes.

### Full-template mode

Used when the CeNA template is at least as long as the source RNA.

```text
CeNA full scaffold donor + transformed RNA bases
```

### Chain-preserving mode

Used when the source RNA is longer than the CeNA template.

```text
RNA chain atoms preserved
+
CeNA local cyclohexenyl scaffold atoms inserted from template
+
RNA bases transformed onto the new CeNA-like local scaffold
```

In `auto` mode, the script chooses full-template mode when possible and chain-preserving mode when the source RNA is longer than the template.

---

## Settings

- Requested mode: `{requested_mode}`
- Actual mode: `{actual_mode}`
- Full-template anchors: `{", ".join(FULL_TEMPLATE_ANCHORS)}`
- Chain-preserving CeNA-template anchors: `{", ".join(CHAIN_TEMPLATE_ANCHORS)}`
- Base-transplant anchors: `{", ".join(BASE_TRANSPLANT_ANCHORS)}`
- Base label policy: `{base_label_policy}`

---

## Alignment Summary

- Mean template/local anchor RMSD: `{np.mean(rmsd):.4f} Å`
- Maximum template/local anchor RMSD: `{np.max(rmsd):.4f} Å`
- Mean base-transplant anchor RMSD: `{np.mean(base_rmsd) if base_rmsd else float('nan'):.4f} Å`
- Maximum base-transplant anchor RMSD: `{np.max(base_rmsd) if base_rmsd else float('nan'):.4f} Å`
- Mean C1′→glycosidic N distance: `{np.mean(gly) if gly else float('nan'):.4f} Å`
- Maximum C1′→glycosidic N distance: `{np.max(gly) if gly else float('nan'):.4f} Å`

---

## Structural Validation

{distance_summary_table(validations)}

### Worst output O3′–P links

{failed_table(validations["output"]["O3'(i)→P(i+1)"], n=20)}

### Worst output CeNA C4′–C6′ links

{failed_table(validations["output"]["C4'→C6'"], n=20)}

### Worst output CeNA C6′–C7′ links

{failed_table(validations["output"]["C6'→C7'"], n=20)}

### Worst output CeNA C7′–C1′ links

{failed_table(validations["output"]["C7'→C1'"], n=20)}

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Template/local RMSD (Å) | Base RMSD (Å) | C1′–N (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
{chr(10).join(rec_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> a CeNA-like computational candidate generated by template-guided or chain-preserving reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed CeNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- `XUL` residue labels are provisional when RNA `U` is preserved.
- Chain-preserving mode preserves the RNA chain path and inserts local CeNA-like scaffold atoms; it is not a fully de novo CeNA fold prediction.
- CeNA stereochemistry requires expert review.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect in PyMOL, ChimeraX, Discovery Studio, VMD, or Mol*.
2. Inspect CeNA cyclohexenyl scaffold geometry.
3. Compare local scaffold geometry against the 2H0N CeNA template.
4. Check C1′→glycosidic N and CeNA local scaffold distances.
5. Add topology/connectivity support in future versions.
6. Perform energy minimization only with appropriate CeNA parameters.
7. Treat large RNA outputs as candidate geometry, not validated CeNA folds.
"""
    report_path.write_text(report, encoding="utf-8")


def convert(
    source_path: Path,
    template_path: Path,
    output_path: Path,
    *,
    report_path: Optional[Path] = None,
    mode: str = "auto",
    base_label_policy: str = "preserve",
    skip_numbering_gaps: bool = True,
):
    source = parse_pdb(source_path)
    template = parse_pdb(template_path)

    if not source:
        raise ValueError(f"No residues parsed from source RNA PDB: {source_path}")
    if not template:
        raise ValueError(f"No residues parsed from CeNA template PDB: {template_path}")

    n_source = len(sorted_residue_keys(source))
    n_template = len(sorted_residue_keys(template))

    if mode == "auto":
        actual_mode = "full-template" if n_template >= n_source else "chain-preserving"
    else:
        actual_mode = mode

    if actual_mode == "full-template":
        output, records = convert_full_template(
            source,
            template,
            anchors=FULL_TEMPLATE_ANCHORS,
            base_label_policy=base_label_policy,
        )
    elif actual_mode == "chain-preserving":
        output, records = convert_chain_preserving(
            source,
            template,
            chain_anchors=CHAIN_TEMPLATE_ANCHORS,
            base_anchors=BASE_TRANSPLANT_ANCHORS,
            base_label_policy=base_label_policy,
        )
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    write_pdb(
        output,
        output_path,
        source_sequence=sequence(source),
        template_sequence=sequence(template),
        mode=actual_mode,
        base_label_policy=base_label_policy,
    )

    validations = build_validations(
        source,
        template,
        output,
        skip_numbering_gaps=skip_numbering_gaps,
    )

    if report_path:
        write_report(
            report_path,
            source_path=source_path,
            template_path=template_path,
            output_path=output_path,
            source=source,
            template=template,
            output=output,
            records=records,
            requested_mode=mode,
            actual_mode=actual_mode,
            base_label_policy=base_label_policy,
            validations=validations,
        )

    rmsd = [r.anchor_rmsd for r in records]
    brmsd = [r.base_anchor_rmsd for r in records if r.base_anchor_rmsd is not None]
    o3p = validations["output"]["O3'(i)→P(i+1)"]
    gly = validations["output"]["C1'→glycosidic N"]
    c4c6 = validations["output"]["C4'→C6'"]
    c6c7 = validations["output"]["C6'→C7'"]
    c7c1 = validations["output"]["C7'→C1'"]

    print("=" * 80)
    print("Digital Polymerase Prototype 004A")
    print("RNA → CeNA candidate reconstruction")
    print("=" * 80)
    print(f"Source RNA: {source_path}")
    print(f"CeNA template: {template_path}")
    print(f"Output PDB: {output_path}")
    if report_path:
        print(f"Report: {report_path}")
    print(f"Requested mode: {mode}")
    print(f"Actual mode: {actual_mode}")
    print(f"Source sequence: {sequence(source)}")
    print(f"Template base classes: {sequence(template)}")
    print(f"Converted residues: {len(records)}")
    print(f"Mean template/local anchor RMSD: {np.mean(rmsd):.4f} Å")
    print(f"Max template/local anchor RMSD: {np.max(rmsd):.4f} Å")
    if brmsd:
        print(f"Mean base anchor RMSD: {np.mean(brmsd):.4f} Å")
        print(f"Max base anchor RMSD: {np.max(brmsd):.4f} Å")
    print("-" * 80)
    print(f"O3′(i)→P(i+1): {validation_status(o3p)} "
          f"(measured={o3p.measured}, failed={o3p.failed}, mean={o3p.mean:.3f} Å)")
    print(f"C1′→glycosidic N: {validation_status(gly)} "
          f"(measured={gly.measured}, failed={gly.failed}, mean={gly.mean:.3f} Å)")
    print(f"C4′→C6′: {validation_status(c4c6)} "
          f"(measured={c4c6.measured}, failed={c4c6.failed}, mean={c4c6.mean:.3f} Å)")
    print(f"C6′→C7′: {validation_status(c6c7)} "
          f"(measured={c6c7.measured}, failed={c6c7.failed}, mean={c6c7.mean:.3f} Å)")
    print(f"C7′→C1′: {validation_status(c7c1)} "
          f"(measured={c7c1.measured}, failed={c7c1.failed}, mean={c7c1.mean:.3f} Å)")
    print("=" * 80)

    return records


def parse_args():
    parser = argparse.ArgumentParser(description="Prototype 004A: RNA to CeNA converter.")
    parser.add_argument("--rna", "--source", dest="rna", required=True, type=Path, help="Source RNA PDB file")
    parser.add_argument("--template", required=True, type=Path, help="CeNA template PDB file")
    parser.add_argument("--output", required=True, type=Path, help="Output CeNA-like candidate PDB")
    parser.add_argument("--report", type=Path, default=None, help="Optional Markdown report")
    parser.add_argument("--mode", choices=["auto", "full-template", "chain-preserving"], default="auto")
    parser.add_argument("--base-label-policy", choices=["preserve", "dna-like"], default="preserve")
    parser.add_argument("--include-numbering-gaps", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    convert(
        args.rna,
        args.template,
        args.output,
        report_path=args.report,
        mode=args.mode,
        base_label_policy=args.base_label_policy,
        skip_numbering_gaps=not args.include_numbering_gaps,
    )


if __name__ == "__main__":
    main()
