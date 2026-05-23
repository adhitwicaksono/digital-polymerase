#!/usr/bin/env python3
"""
Prototype 002A: Fragment-Guided RNA to ANA Converter

Digital Polymerase / XNA World Project

This script generates an ANA-like candidate PDB from an RNA PDB using a shorter
ANA fragment as a local geometry template.

Important:
- This is NOT a chemically or physically validated ANA modeling package.
- This is an experimental fragment-guided candidate-structure generator.
- The output requires visual inspection, geometry checks, energy minimization,
  and expert chemical review before scientific interpretation.

Strategy:
1. Parse source RNA PDB.
2. Parse ANA fragment/template PDB.
3. For each RNA residue, select an ANA local template residue:
   - G -> observed G-like ANA template (e.g., GAO)
   - U -> observed U-like ANA template (e.g., UAR)
   - C -> observed C-like ANA template (e.g., CAR)
   - A -> purine fallback, usually G-like ANA template, because this 4-mer
          template may not contain an A-like ANA residue.
4. Rigidly align the ANA template residue frame onto the RNA residue frame using
   local anchor atoms and Kabsch alignment.
5. Use the transformed ANA backbone and preserve the RNA nucleobase atoms.
6. Export a candidate ANA-like PDB.

Recommended interpretation:
    RNA global/base geometry + ANA local backbone fragment geometry
    = exploratory ANA-like candidate structure
"""

from __future__ import annotations

import argparse
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Optional

import numpy as np


ResidueKey = Tuple[str, int, str]


# Standard / common nucleic acid backbone atoms.
# Prime-containing hydrogens are classified as backbone/sugar hydrogens separately.
BACKBONE_ATOMS = {
    "P", "OP1", "OP2", "O5'", "C5'", "C4'", "O4'",
    "C3'", "O3'", "C2'", "O2'", "C1'",
}

BACKBONE_ORDER = [
    "P", "OP1", "OP2", "O5'", "C5'", "C4'", "O4'",
    "C3'", "O3'", "C2'", "O2'", "C1'",
    "H5'", "'H5'", "H4'", "H3'", "H2'", "'HO2", "H1'", "'HO3",
]


# Default alignment anchors. These exist in the RNA and the uploaded ANA fragment.
DEFAULT_ANCHORS = ["C1'", "C2'", "C3'", "C4'", "O4'"]


RNA_BASES = {"A", "U", "G", "C"}


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
    backbone_atom_count: int
    base_atom_count: int
    note: str


def infer_element(atom_name: str, pdb_element: str = "") -> str:
    """Infer chemical element from PDB element column or atom name."""
    elem = (pdb_element or "").strip()
    if elem and re.match(r"^[A-Za-z]{1,2}$", elem):
        # Handle odd cases like O1- by falling back below.
        if elem.upper() not in {"O1", "O1-", "C1", "N1"}:
            return elem.upper() if len(elem) == 1 else elem.title()

    cleaned = re.sub(r"[^A-Za-z]", "", atom_name)
    if not cleaned:
        return ""
    # PDB atom names for nucleic acids are normally C/N/O/P/H.
    first = cleaned[0].upper()
    if first in {"C", "N", "O", "P", "H", "S"}:
        return first
    return first


def parse_pdb(path: Path) -> Dict[ResidueKey, Dict[str, Atom]]:
    """Parse a PDB file into chain-aware residues."""
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
            # Prototype behavior: skip malformed atoms.
            # Future versions should report skipped lines.
            continue

    return dict(residues)


def sorted_residue_keys(residues: Dict[ResidueKey, Dict[str, Atom]]) -> List[ResidueKey]:
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))


def residue_name(residue: Dict[str, Atom]) -> str:
    return next(iter(residue.values())).res_name


def normalize_base_from_residue_name(res_name: str) -> str:
    """Infer base identity/class from residue name."""
    res = res_name.strip().upper()

    if res in RNA_BASES:
        return res

    # Common XNA/nonstandard residue naming in the current templates:
    # GAO = G-like ANA residue, UAR = U-like ANA residue, CAR = C-like ANA residue.
    if res.startswith("G"):
        return "G"
    if res.startswith("A"):
        return "A"
    if res.startswith("U") or res.startswith("T"):
        return "U"
    if res.startswith("C"):
        return "C"

    return res[0] if res else "N"


def is_backbone_atom(atom_name: str) -> bool:
    """Classify sugar/phosphate backbone atoms and sugar hydrogens."""
    if atom_name in BACKBONE_ATOMS:
        return True

    # Prime-containing hydrogens or hydroxyl labels from BIOVIA-style PDB output.
    # Examples observed: H1', H2', H3', H4', H5', 'H5', 'HO2, 'HO3.
    if "'" in atom_name:
        return True

    return False


def is_base_atom(atom_name: str) -> bool:
    return not is_backbone_atom(atom_name)


def split_backbone_base(residue: Dict[str, Atom]) -> Tuple[Dict[str, Atom], Dict[str, Atom]]:
    backbone = {name: atom for name, atom in residue.items() if is_backbone_atom(name)}
    base = {name: atom for name, atom in residue.items() if is_base_atom(name)}
    return backbone, base


def kabsch(mobile: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Return rotation R and translation t that best align mobile onto target.

    Applying:
        transformed = (R @ mobile_point) + t
    """
    if mobile.shape != target.shape:
        raise ValueError("mobile and target coordinate arrays must have the same shape")
    if mobile.ndim != 2 or mobile.shape[1] != 3:
        raise ValueError("coordinate arrays must be N x 3")
    if mobile.shape[0] < 3:
        raise ValueError("at least three anchor atoms are recommended for stable alignment")

    mobile_center = mobile.mean(axis=0)
    target_center = target.mean(axis=0)

    mobile_centered = mobile - mobile_center
    target_centered = target - target_center

    covariance = mobile_centered.T @ target_centered
    u, _s, vt = np.linalg.svd(covariance)
    r = vt.T @ u.T

    # Prevent reflection.
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T

    t = target_center - r @ mobile_center
    transformed = (r @ mobile.T).T + t
    rmsd = float(np.sqrt(np.mean(np.sum((transformed - target) ** 2, axis=1))))

    return r, t, rmsd


def transform_atom(atom: Atom, r: np.ndarray, t: np.ndarray) -> Atom:
    new_atom = Atom(**atom.__dict__)
    new_atom.coords = r @ atom.coords + t
    return new_atom


def clone_atom_with_updates(
    atom: Atom,
    *,
    coords: Optional[np.ndarray] = None,
    res_name: Optional[str] = None,
    chain: Optional[str] = None,
    res_num: Optional[int] = None,
    insertion_code: Optional[str] = None,
    record: Optional[str] = "HETATM",
) -> Atom:
    new_atom = Atom(**atom.__dict__)
    if coords is not None:
        new_atom.coords = coords
    if res_name is not None:
        new_atom.res_name = res_name
    if chain is not None:
        new_atom.chain = chain
    if res_num is not None:
        new_atom.res_num = res_num
    if insertion_code is not None:
        new_atom.insertion_code = insertion_code
    if record is not None:
        new_atom.record = record
    return new_atom


def build_template_index(
    template_residues: Dict[ResidueKey, Dict[str, Atom]]
) -> Dict[str, Tuple[ResidueKey, Dict[str, Atom]]]:
    """
    Build a base-class index from template residues.
    Keeps the first residue found for each base class.
    """
    index: Dict[str, Tuple[ResidueKey, Dict[str, Atom]]] = {}
    for key in sorted_residue_keys(template_residues):
        res = template_residues[key]
        base_class = normalize_base_from_residue_name(residue_name(res))
        index.setdefault(base_class, (key, res))
    return index


def select_template_for_base(
    source_base: str,
    template_index: Dict[str, Tuple[ResidueKey, Dict[str, Atom]]],
) -> Tuple[ResidueKey, Dict[str, Atom], str, str]:
    """
    Select the best available ANA fragment template for a source RNA base.

    If exact A template is absent, use a purine fallback (G).
    If exact C/U template is absent, use another pyrimidine fallback.
    """
    source_base = source_base.upper()

    if source_base in template_index:
        key, res = template_index[source_base]
        return key, res, source_base, "exact base-class template"

    if source_base == "A" and "G" in template_index:
        key, res = template_index["G"]
        return key, res, "G", "purine fallback: A uses G-like ANA backbone template"

    if source_base == "G" and "A" in template_index:
        key, res = template_index["A"]
        return key, res, "A", "purine fallback: G uses A-like ANA backbone template"

    if source_base == "U" and "C" in template_index:
        key, res = template_index["C"]
        return key, res, "C", "pyrimidine fallback: U uses C-like ANA backbone template"

    if source_base == "C" and "U" in template_index:
        key, res = template_index["U"]
        return key, res, "U", "pyrimidine fallback: C uses U-like ANA backbone template"

    # Last-resort fallback: first available template.
    first_base = sorted(template_index.keys())[0]
    key, res = template_index[first_base]
    return key, res, first_base, f"last-resort fallback: uses {first_base}-like ANA template"


def target_ana_residue_name(source_base: str, naming_policy: str = "provisional") -> str:
    """
    Assign output residue names for ANA candidate residues.

    The uploaded ANA template uses GAO, UAR, and CAR. An A-like ANA residue is absent,
    so AAR is used as a provisional A-like ANA residue name.
    """
    source_base = source_base.upper()

    if naming_policy == "template-observed":
        # Use observed where known, provisional where absent.
        return {"A": "AAR", "U": "UAR", "G": "GAO", "C": "CAR"}.get(source_base, "ANA")

    # Provisional uniform-ish style.
    return {"A": "AAR", "U": "UAR", "G": "GAR", "C": "CAR"}.get(source_base, "ANA")


def available_anchors(source: Dict[str, Atom], template: Dict[str, Atom], requested: Iterable[str]) -> List[str]:
    return [a for a in requested if a in source and a in template]


def convert_residue_fragment_guided(
    source_key: ResidueKey,
    source_residue: Dict[str, Atom],
    template_key: ResidueKey,
    template_residue: Dict[str, Atom],
    *,
    target_res_name: str,
    anchors: List[str],
    fix_c1: bool = True,
) -> Tuple[Dict[str, Atom], float, List[str]]:
    """
    Convert one RNA residue into an ANA-like candidate residue.

    The template ANA backbone is transformed into the source RNA local frame.
    RNA nucleobase atoms are preserved in their original source coordinates.
    """
    used_anchors = available_anchors(source_residue, template_residue, anchors)
    if len(used_anchors) < 3:
        raise ValueError(
            f"Need at least 3 shared anchor atoms, found {len(used_anchors)}: {used_anchors}"
        )

    mobile = np.array([template_residue[a].coords for a in used_anchors], dtype=float)
    target = np.array([source_residue[a].coords for a in used_anchors], dtype=float)

    r, t, rmsd = kabsch(mobile, target)

    source_backbone, source_base = split_backbone_base(source_residue)
    template_backbone, _template_base = split_backbone_base(template_residue)

    # Transform ANA template backbone into source local/global frame.
    transformed_backbone: Dict[str, Atom] = {}
    for atom_name, atom in template_backbone.items():
        transformed = transform_atom(atom, r, t)
        transformed_backbone[atom_name] = transformed

    # Optional translation to pin template C1' exactly to the source C1'
    # for better base-backbone attachment consistency.
    if fix_c1 and "C1'" in transformed_backbone and "C1'" in source_residue:
        delta = source_residue["C1'"].coords - transformed_backbone["C1'"].coords
        for atom_name in transformed_backbone:
            transformed_backbone[atom_name].coords = transformed_backbone[atom_name].coords + delta

    chain, res_num, icode = source_key
    output: Dict[str, Atom] = {}

    for atom_name, atom in transformed_backbone.items():
        output[atom_name] = clone_atom_with_updates(
            atom,
            res_name=target_res_name,
            chain=chain,
            res_num=res_num,
            insertion_code=icode,
            record="HETATM",
        )

    # Preserve RNA base atoms in the original source position.
    for atom_name, atom in source_base.items():
        output[atom_name] = clone_atom_with_updates(
            atom,
            res_name=target_res_name,
            chain=chain,
            res_num=res_num,
            insertion_code=icode,
            record="HETATM",
        )

    return output, rmsd, used_anchors


def atom_sort_key(atom_name: str) -> Tuple[int, int, str]:
    if atom_name in BACKBONE_ORDER:
        return (0, BACKBONE_ORDER.index(atom_name), atom_name)
    if is_backbone_atom(atom_name):
        return (1, 999, atom_name)
    return (2, 999, atom_name)


def format_pdb_atom_line(serial: int, atom: Atom) -> str:
    record = "HETATM"
    atom_name = atom.atom_name
    res_name = atom.res_name[:3]
    chain = (atom.chain or "A")[:1]
    icode = atom.insertion_code[:1] if atom.insertion_code else " "
    elem = (atom.element or infer_element(atom_name))[:2].rjust(2)

    return (
        f"{record:<6}{serial:5d} "
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


def write_pdb(
    residues: Dict[ResidueKey, Dict[str, Atom]],
    output_path: Path,
    *,
    source_sequence: str,
    template_summary: str,
    records: List[ConversionRecord],
) -> None:
    with output_path.open("w", encoding="utf-8") as f:
        f.write("REMARK   Digital Polymerase Prototype 002A\n")
        f.write("REMARK   Fragment-guided RNA to ANA candidate reconstruction\n")
        f.write(f"REMARK   Source RNA sequence: {source_sequence}\n")
        f.write(f"REMARK   ANA template summary: {template_summary}\n")
        f.write("REMARK   Method: ANA fragment backbone transformed into RNA local frames\n")
        f.write("REMARK   RNA nucleobase atoms preserved; ANA backbone atoms are template-derived\n")
        f.write("REMARK   WARNING: Computational candidate only\n")
        f.write("REMARK   WARNING: Not energy-minimized, force-field-validated, or experimentally verified\n")
        f.write("REMARK   WARNING: ANA residue names are provisional and may need adjustment\n")
        f.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")

        serial = 1
        for key in sorted_residue_keys(residues):
            residue = residues[key]
            for atom_name in sorted(residue.keys(), key=atom_sort_key):
                f.write(format_pdb_atom_line(serial, residue[atom_name]) + "\n")
                serial += 1

        f.write("END\n")


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
    fix_c1: bool,
    naming_policy: str,
) -> None:
    rmsds = [r.anchor_rmsd for r in records]
    mean_rmsd = sum(rmsds) / len(rmsds) if rmsds else float("nan")
    max_rmsd = max(rmsds) if rmsds else float("nan")

    template_lines = []
    for base_class, (key, residue) in sorted(template_index.items()):
        template_lines.append(
            f"- `{base_class}` → `{residue_name(residue)}` at chain `{key[0]}`, residue `{key[1]}`"
        )

    record_lines = []
    for i, rec in enumerate(records, start=1):
        record_lines.append(
            "| {i} | {chain}{resnum}{icode} | {src} | {target} | {tmpl} {tchain}{tresnum}{ticode} | {rmsd:.4f} | {note} |".format(
                i=i,
                chain=rec.source_key[0],
                resnum=rec.source_key[1],
                icode=rec.source_key[2],
                src=rec.source_res_name,
                target=rec.target_res_name,
                tmpl=rec.template_res_name,
                tchain=rec.template_key[0],
                tresnum=rec.template_key[1],
                ticode=rec.template_key[2],
                rmsd=rec.anchor_rmsd,
                note=rec.note,
            )
        )

    report = f"""# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A  
**Method:** Fragment-guided RNA → ANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated

---

## Inputs

- Source RNA PDB: `{source_path}`
- ANA fragment template PDB: `{template_path}`
- Output PDB: `{output_path}`

---

## Source Sequence

```text
{source_sequence}
```

---

## Template Index

The ANA template is shorter than the RNA input, so template residues are used as local geometry donors.

{chr(10).join(template_lines)}

---

## Method Summary

This prototype uses a local ANA fragment as a residue-level backbone geometry donor.

For each RNA residue:

1. determine source RNA base identity
2. select the best available ANA template residue
3. align ANA template anchor atoms onto RNA anchor atoms using Kabsch alignment
4. transform the ANA backbone into the RNA local frame
5. preserve RNA nucleobase atoms in their original coordinates
6. combine transformed ANA backbone + preserved RNA base atoms
7. export an ANA-like candidate residue

This is **not** a full-template reconstruction because the ANA template contains only 4 residues.

---

## Settings

- Anchor atoms: `{", ".join(anchors)}`
- Pin C1' after alignment: `{fix_c1}`
- Residue naming policy: `{naming_policy}`

---

## Alignment Summary

- Converted residues: `{len(records)}`
- Mean anchor RMSD: `{mean_rmsd:.4f} Å`
- Maximum anchor RMSD: `{max_rmsd:.4f} Å`

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
{chr(10).join(record_lines)}

---

## Scientific Interpretation

This output should be interpreted as:

> an ANA-like candidate structure generated using fragment-guided local backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed ANA structure.

---

## Important Limitations

- The ANA template contains only a 4-mer fragment.
- A-like ANA geometry is absent in the uploaded template; A residues may use a purine fallback template.
- RNA nucleobase atoms are preserved, but backbone geometry is template-derived.
- The output is not energy-minimized.
- No force-field parameters are generated.
- Connectivity is not explicitly written with `CONECT` records.
- Molecular viewers may infer nonstandard residue bonds differently.
- Residue names are provisional and may need adjustment for downstream tools.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect the output in PyMOL, ChimeraX, VMD, or Mol*.
2. Check residue completeness and atom naming.
3. Inspect base-backbone attachment geometry.
4. Check bond lengths, angles, torsions, and clashes.
5. Compare local ANA backbone geometry with the original 4-mer ANA template.
6. Add explicit connectivity records or topology files in future versions.
7. Perform energy minimization with appropriate force-field support.
8. Repeat the prototype when a full ANA 8-mer template becomes available.

---

## Development Note

This prototype introduces a second Digital Polymerase mode:

```text
Prototype 001: full-template reconstruction
Prototype 002A: fragment-guided local reconstruction
```

This is useful because many XNA systems may not have full-length templates matching the desired source molecule.
"""
    report_path.write_text(report, encoding="utf-8")


def convert(
    source_rna_path: Path,
    ana_template_path: Path,
    output_path: Path,
    *,
    report_path: Optional[Path] = None,
    anchors: List[str] = DEFAULT_ANCHORS,
    fix_c1: bool = True,
    naming_policy: str = "template-observed",
) -> List[ConversionRecord]:
    source = parse_pdb(source_rna_path)
    template = parse_pdb(ana_template_path)

    if not source:
        raise ValueError(f"No atoms/residues parsed from source RNA PDB: {source_rna_path}")
    if not template:
        raise ValueError(f"No atoms/residues parsed from ANA template PDB: {ana_template_path}")

    template_index = build_template_index(template)
    if not template_index:
        raise ValueError("Could not build ANA template index")

    output_residues: Dict[ResidueKey, Dict[str, Atom]] = {}
    records: List[ConversionRecord] = []

    source_keys = sorted_residue_keys(source)
    source_sequence = ""

    for source_key in source_keys:
        source_residue = source[source_key]
        source_res_name = residue_name(source_residue)
        source_base = normalize_base_from_residue_name(source_res_name)
        source_sequence += source_base

        template_key, template_residue, template_base_class, note = select_template_for_base(
            source_base, template_index
        )
        template_res_name = residue_name(template_residue)
        target_res_name = target_ana_residue_name(source_base, naming_policy=naming_policy)

        converted_residue, rmsd, used_anchors = convert_residue_fragment_guided(
            source_key,
            source_residue,
            template_key,
            template_residue,
            target_res_name=target_res_name,
            anchors=anchors,
            fix_c1=fix_c1,
        )

        output_residues[source_key] = converted_residue

        backbone, base = split_backbone_base(converted_residue)
        records.append(
            ConversionRecord(
                source_key=source_key,
                source_res_name=source_res_name,
                source_base=source_base,
                target_res_name=target_res_name,
                template_key=template_key,
                template_res_name=template_res_name,
                template_base_class=template_base_class,
                anchor_atoms=used_anchors,
                anchor_rmsd=rmsd,
                backbone_atom_count=len(backbone),
                base_atom_count=len(base),
                note=note,
            )
        )

    template_summary = ", ".join(
        f"{base}:{residue_name(res)}@{key[0]}{key[1]}{key[2]}"
        for base, (key, res) in sorted(template_index.items())
    )

    write_pdb(
        output_residues,
        output_path,
        source_sequence=source_sequence,
        template_summary=template_summary,
        records=records,
    )

    if report_path:
        write_report(
            report_path,
            source_path=source_rna_path,
            template_path=ana_template_path,
            output_path=output_path,
            source_sequence=source_sequence,
            template_index=template_index,
            records=records,
            anchors=anchors,
            fix_c1=fix_c1,
            naming_policy=naming_policy,
        )

    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prototype 002A: fragment-guided RNA to ANA candidate reconstruction"
    )
    parser.add_argument("--rna", required=True, type=Path, help="Input RNA PDB")
    parser.add_argument("--template", required=True, type=Path, help="ANA fragment/template PDB")
    parser.add_argument("--output", required=True, type=Path, help="Output ANA-like candidate PDB")
    parser.add_argument("--report", type=Path, default=None, help="Optional Markdown conversion report")
    parser.add_argument(
        "--anchors",
        nargs="+",
        default=DEFAULT_ANCHORS,
        help="Shared local anchor atoms for Kabsch alignment",
    )
    parser.add_argument(
        "--no-fix-c1",
        action="store_true",
        help="Do not translate transformed ANA backbone to pin C1' to source RNA C1'",
    )
    parser.add_argument(
        "--naming-policy",
        choices=["template-observed", "provisional"],
        default="template-observed",
        help="Residue naming policy for output ANA-like residues",
    )

    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)

    records = convert(
        args.rna,
        args.template,
        args.output,
        report_path=args.report,
        anchors=args.anchors,
        fix_c1=not args.no_fix_c1,
        naming_policy=args.naming_policy,
    )

    rmsds = [r.anchor_rmsd for r in records]
    print("=" * 80)
    print("Digital Polymerase Prototype 002A")
    print("Fragment-guided RNA -> ANA candidate reconstruction")
    print("=" * 80)
    print(f"Converted residues: {len(records)}")
    print(f"Mean anchor RMSD: {sum(rmsds) / len(rmsds):.4f} Å")
    print(f"Max anchor RMSD:  {max(rmsds):.4f} Å")
    print(f"Output PDB:       {args.output}")
    if args.report:
        print(f"Report:           {args.report}")
    print("")
    print("WARNING: This is a computational candidate only.")
    print("WARNING: Not energy-minimized, force-field-validated, or experimentally verified.")
    print("=" * 80)


if __name__ == "__main__":
    main()
