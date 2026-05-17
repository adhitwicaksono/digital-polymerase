#!/usr/bin/env python3
"""
Prototype 001: Template-guided RNA -> HNA candidate reconstruction

Digital Polymerase / XNA World Project

This script generates a candidate HNA-like PDB structure from:
  1. an input RNA PDB structure, and
  2. an experimental/template HNA PDB structure.

Core idea:
  - use the HNA template as the backbone geometry source,
  - preserve/transplant the source RNA base atoms,
  - align source base geometry onto the HNA template using local anchor atoms,
  - export a candidate PDB structure.

Important:
  This is NOT a chemically or experimentally validated converter.
  The output is a computational candidate model and should be inspected,
  energy-minimized, and validated by MD or other structural workflows.

Example:
  python rna_to_hna_template_based.py \
      --rna examples/rna_to_hna_8mer/input_rna_8mer.pdb \
      --template data/templates/hna_8mer.pdb \
      --output examples/rna_to_hna_8mer/converted_hna_candidate.pdb \
      --base-policy preserve \
      --report examples/rna_to_hna_8mer/conversion_report.md
"""

from __future__ import annotations

import argparse
import math
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

ResidueKey = Tuple[str, int, str]  # (chain_id, residue_number, insertion_code)


@dataclass
class Atom:
    """Minimal PDB atom representation."""

    record: str
    serial: int
    atom_name: str
    altloc: str
    res_name: str
    chain: str
    res_num: int
    insertion_code: str
    coords: np.ndarray
    occupancy: float
    temp_factor: float
    element: str
    charge: str = ""

    def copy(self) -> "Atom":
        return deepcopy(self)


Residue = OrderedDict[str, Atom]
Structure = OrderedDict[ResidueKey, Residue]


# ---------------------------------------------------------------------------
# Atom classification
# ---------------------------------------------------------------------------

# Exact heavy-atom names commonly considered nucleic-acid backbone/sugar atoms.
# Includes canonical phosphate naming variants.
BACKBONE_HEAVY_ATOMS = {
    "P",
    "OP1", "OP2", "OP3",
    "O1P", "O2P", "O3P",
    "O5'", "C5'",
    "C4'", "O4'",
    "C3'", "O3'",
    "C2'", "O2'",
    "C1'",
    "C6'",  # HNA-specific backbone/ring atom
}

# Common sugar/backbone hydrogen patterns. This is intentionally conservative.
BACKBONE_H_PREFIXES = (
    "H1'", "H2'", "H3'", "H4'", "H5'", "H6'",
    "1H1'", "2H1'", "1H2'", "2H2'", "1H3'", "2H3'",
    "1H4'", "2H4'", "1H5'", "2H5'", "1H6'", "2H6'",
    "HO2'", "HO3'", "HO5'", "HOP",
)


def is_backbone_atom(atom_name: str) -> bool:
    """
    Return True if atom_name is likely part of the sugar/phosphate backbone.

    This prototype uses a conservative exact-name approach for heavy atoms,
    plus common sugar/backbone hydrogen naming patterns.
    """
    name = atom_name.strip()
    if name in BACKBONE_HEAVY_ATOMS:
        return True
    if any(name.startswith(prefix) for prefix in BACKBONE_H_PREFIXES):
        return True
    return False


def is_base_atom(atom_name: str) -> bool:
    """Return True if atom_name is not classified as backbone/sugar/phosphate."""
    return not is_backbone_atom(atom_name)


# ---------------------------------------------------------------------------
# PDB parsing/writing
# ---------------------------------------------------------------------------

def _safe_float(text: str, default: float = 0.0) -> float:
    text = text.strip()
    if not text:
        return default
    return float(text)


def _safe_int(text: str, default: int = 0) -> int:
    text = text.strip()
    if not text:
        return default
    return int(text)


def infer_element(atom_name: str) -> str:
    """Infer element from PDB atom name when the element column is missing."""
    stripped = atom_name.strip()
    if not stripped:
        return ""
    # For typical PDB atom names: C1', N9, OP1, etc.
    # Strip leading digits and take first alphabetic character.
    for char in stripped:
        if char.isalpha():
            return char.upper()
    return stripped[0].upper()


def parse_pdb(path: Path) -> Structure:
    """
    Parse ATOM/HETATM records from a PDB file.

    Residues are keyed by (chain, residue number, insertion code) to avoid
    collisions in multi-chain structures.
    """
    residues: Structure = OrderedDict()

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not (line.startswith("ATOM") or line.startswith("HETATM")):
                continue

            record = line[0:6].strip()
            serial = _safe_int(line[6:11], default=0)
            atom_name = line[12:16].strip()
            altloc = line[16:17].strip()
            res_name = line[17:20].strip()
            chain = line[21:22].strip() or "A"
            res_num = _safe_int(line[22:26], default=0)
            insertion_code = line[26:27].strip()
            x = _safe_float(line[30:38])
            y = _safe_float(line[38:46])
            z = _safe_float(line[46:54])
            occupancy = _safe_float(line[54:60], default=1.0)
            temp_factor = _safe_float(line[60:66], default=0.0)
            element = line[76:78].strip() if len(line) >= 78 else ""
            charge = line[78:80].strip() if len(line) >= 80 else ""

            if not element:
                element = infer_element(atom_name)

            key: ResidueKey = (chain, res_num, insertion_code)
            if key not in residues:
                residues[key] = OrderedDict()

            # If altlocs are present, this prototype keeps the first atom name seen.
            # Later versions should handle altloc selection explicitly.
            if atom_name in residues[key]:
                continue

            residues[key][atom_name] = Atom(
                record=record,
                serial=serial,
                atom_name=atom_name,
                altloc=altloc,
                res_name=res_name,
                chain=chain,
                res_num=res_num,
                insertion_code=insertion_code,
                coords=np.array([x, y, z], dtype=float),
                occupancy=occupancy,
                temp_factor=temp_factor,
                element=element,
                charge=charge,
            )

    return residues


def format_pdb_atom_line(serial: int, atom: Atom, record: str = "HETATM") -> str:
    """Format one ATOM/HETATM line in standard PDB fixed-width style."""
    return (
        f"{record:<6s}"
        f"{serial:5d} "
        f"{atom.atom_name:>4s}"
        f"{atom.altloc:1s}"
        f"{atom.res_name:>3s} "
        f"{atom.chain:1s}"
        f"{atom.res_num:4d}"
        f"{atom.insertion_code:1s}"
        f"   "
        f"{atom.coords[0]:8.3f}"
        f"{atom.coords[1]:8.3f}"
        f"{atom.coords[2]:8.3f}"
        f"{atom.occupancy:6.2f}"
        f"{atom.temp_factor:6.2f}"
        f"          "
        f"{atom.element:>2s}"
        f"{atom.charge:>2s}"
    )


def write_pdb(
    residues: Structure,
    output_path: Path,
    source_sequence: str,
    base_policy: str,
    validation_summary: Optional[Dict[str, float]] = None,
) -> None:
    """Write candidate HNA PDB structure."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("REMARK   Digital Polymerase Prototype 001\n")
        handle.write("REMARK   Template-guided RNA to HNA candidate reconstruction\n")
        handle.write(f"REMARK   Original source sequence: {source_sequence}\n")
        handle.write(f"REMARK   Base policy: {base_policy}\n")
        handle.write("REMARK   HNA backbone geometry copied from template residues\n")
        handle.write("REMARK   Source RNA base atoms aligned/transplanted onto HNA backbone\n")
        handle.write("REMARK   WARNING: computational candidate only\n")
        handle.write("REMARK   WARNING: not energy-minimized, force-field-validated, or experimentally verified\n")

        if validation_summary:
            handle.write(
                f"REMARK   Mean anchor RMSD: {validation_summary.get('mean_anchor_rmsd', math.nan):.4f} A\n"
            )
            handle.write(
                f"REMARK   Max anchor RMSD: {validation_summary.get('max_anchor_rmsd', math.nan):.4f} A\n"
            )

        # Placeholder CRYST1 record. Keep as P1 because the output is a model, not a solved crystal.
        handle.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")

        serial = 1
        for _key, residue in residues.items():
            # Write backbone first, then base atoms for readability.
            atom_names = list(residue.keys())
            backbone_names = [name for name in atom_names if is_backbone_atom(name)]
            base_names = [name for name in atom_names if is_base_atom(name)]

            for atom_name in backbone_names + base_names:
                atom = residue[atom_name]
                handle.write(format_pdb_atom_line(serial, atom, record="HETATM") + "\n")
                serial += 1

        handle.write("END\n")


# ---------------------------------------------------------------------------
# Sequence and residue naming
# ---------------------------------------------------------------------------

RNA_BASES = {"A", "U", "G", "C"}
DNA_BASES = {"A", "T", "G", "C"}

# Default: preserve the source RNA base chemistry.
# This avoids silently calling a copied uracil atom set "thymine".
HNA_BASE_MAP_PRESERVE = {
    "A": "6HA",
    "U": "6HU",
    "G": "6HG",
    "C": "6HC",
}

# Optional label-only mapping for workflows where HNA residue naming follows DNA-like bases.
# Note: U->T here does NOT add the thymine methyl group.
HNA_BASE_MAP_RNA_TO_DNA_LABEL = {
    "A": "6HA",
    "U": "6HT",
    "G": "6HG",
    "C": "6HC",
}


def normalize_source_base(res_name: str) -> str:
    """
    Normalize a source RNA/DNA residue name to a one-letter base where possible.
    """
    name = res_name.strip().upper()

    # Canonical one-letter forms
    if name in RNA_BASES or name in DNA_BASES:
        return name

    # Common PDB residue variants
    mapping = {
        "ADE": "A",
        "GUA": "G",
        "CYT": "C",
        "URA": "U",
        "THY": "T",
        "DA": "A",
        "DG": "G",
        "DC": "C",
        "DT": "T",
        "RA": "A",
        "RG": "G",
        "RC": "C",
        "RU": "U",
    }
    return mapping.get(name, name)


def hna_residue_name(source_res_name: str, base_policy: str) -> str:
    """
    Convert source residue name to an HNA residue label.

    base_policy:
      preserve          -> U becomes 6HU
      rna-to-dna-label  -> U becomes 6HT, label-only; no methyl atom is added
    """
    base = normalize_source_base(source_res_name)

    if base_policy == "preserve":
        if base == "T":
            # If the source already uses T, preserve T.
            return "6HT"
        return HNA_BASE_MAP_PRESERVE.get(base, f"6H{base}")

    if base_policy == "rna-to-dna-label":
        if base == "T":
            return "6HT"
        return HNA_BASE_MAP_RNA_TO_DNA_LABEL.get(base, f"6H{base}")

    raise ValueError(f"Unknown base_policy: {base_policy}")


def residue_base_sequence(structure: Structure) -> str:
    """Return one-letter base sequence from residue names in structure order."""
    seq: List[str] = []
    for residue in structure.values():
        if not residue:
            continue
        first_atom = next(iter(residue.values()))
        seq.append(normalize_source_base(first_atom.res_name))
    return "".join(seq)


# ---------------------------------------------------------------------------
# Alignment
# ---------------------------------------------------------------------------

def kabsch_align(
    template_coords: np.ndarray,
    mobile_coords: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Compute optimal rotation and translation to align mobile onto template.

    Returns:
      R, t, rmsd
      transformed_mobile = R @ mobile + t
    """
    if template_coords.shape != mobile_coords.shape:
        raise ValueError("template_coords and mobile_coords must have the same shape")
    if template_coords.shape[0] < 3:
        raise ValueError("At least three anchor atoms are recommended for Kabsch alignment")

    template_center = np.mean(template_coords, axis=0)
    mobile_center = np.mean(mobile_coords, axis=0)

    template_centered = template_coords - template_center
    mobile_centered = mobile_coords - mobile_center

    covariance = mobile_centered.T @ template_centered
    u, _s, vt = np.linalg.svd(covariance)
    rotation = vt.T @ u.T

    # Avoid improper rotation/reflection.
    if np.linalg.det(rotation) < 0:
        vt[-1, :] *= -1
        rotation = vt.T @ u.T

    translation = template_center - rotation @ mobile_center
    transformed = (rotation @ mobile_coords.T).T + translation
    rmsd = float(np.sqrt(np.mean(np.sum((transformed - template_coords) ** 2, axis=1))))

    return rotation, translation, rmsd


def collect_anchor_coords(
    residue_a: Residue,
    residue_b: Residue,
    anchors: Iterable[str],
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Collect matching anchor coordinates from two residues.

    Returns coords_a, coords_b, used_anchor_names.
    """
    coords_a: List[np.ndarray] = []
    coords_b: List[np.ndarray] = []
    used: List[str] = []

    for anchor in anchors:
        if anchor in residue_a and anchor in residue_b:
            coords_a.append(residue_a[anchor].coords)
            coords_b.append(residue_b[anchor].coords)
            used.append(anchor)

    if not coords_a:
        return np.empty((0, 3)), np.empty((0, 3)), []

    return np.vstack(coords_a), np.vstack(coords_b), used


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------

def transform_residue(
    source_residue: Residue,
    template_residue: Residue,
    output_res_name: str,
    output_chain: str,
    output_res_num: int,
    output_insertion_code: str,
    anchors: Iterable[str] = ("C1'", "C2'", "C4'"),
) -> Tuple[Residue, Dict[str, object]]:
    """
    Build one candidate HNA residue:
      - copy backbone atoms from the HNA template residue
      - transform source base atoms into the HNA local coordinate frame
      - combine backbone + transformed base atoms
    """
    hna_backbone: Residue = OrderedDict()
    for atom_name, atom in template_residue.items():
        if is_backbone_atom(atom_name):
            copied = atom.copy()
            copied.res_name = output_res_name
            copied.chain = output_chain
            copied.res_num = output_res_num
            copied.insertion_code = output_insertion_code
            hna_backbone[atom_name] = copied

    source_base_atoms: Residue = OrderedDict()
    for atom_name, atom in source_residue.items():
        if is_base_atom(atom_name):
            source_base_atoms[atom_name] = atom.copy()

    template_coords, mobile_coords, used_anchors = collect_anchor_coords(
        template_residue,
        source_residue,
        anchors,
    )

    if len(used_anchors) >= 3:
        rotation, translation, anchor_rmsd = kabsch_align(template_coords, mobile_coords)
        method = "kabsch"
    elif "C1'" in template_residue and "C1'" in source_residue:
        # Fallback: translation using the base-attachment region only.
        rotation = np.eye(3)
        translation = template_residue["C1'"].coords - source_residue["C1'"].coords
        anchor_rmsd = float(np.linalg.norm(translation))
        method = "translation_fallback"
        used_anchors = ["C1'"]
    else:
        raise ValueError("Cannot align residue: no usable anchor atoms found")

    transformed_base: Residue = OrderedDict()
    for atom_name, atom in source_base_atoms.items():
        copied = atom.copy()
        copied.coords = rotation @ atom.coords + translation
        copied.res_name = output_res_name
        copied.chain = output_chain
        copied.res_num = output_res_num
        copied.insertion_code = output_insertion_code
        transformed_base[atom_name] = copied

    hybrid: Residue = OrderedDict()
    hybrid.update(hna_backbone)
    hybrid.update(transformed_base)

    stats: Dict[str, object] = {
        "method": method,
        "used_anchors": used_anchors,
        "anchor_rmsd": anchor_rmsd,
        "backbone_atom_count": len(hna_backbone),
        "base_atom_count": len(transformed_base),
    }

    return hybrid, stats


def convert_rna_to_hna(
    rna_structure: Structure,
    hna_template: Structure,
    base_policy: str = "preserve",
    anchors: Iterable[str] = ("C1'", "C2'", "C4'"),
) -> Tuple[Structure, List[Dict[str, object]]]:
    """
    Convert RNA structure to candidate HNA structure using sequential template mapping.

    The nth source residue is paired with the nth template residue.
    """
    if len(hna_template) < len(rna_structure):
        raise ValueError(
            f"HNA template has fewer residues ({len(hna_template)}) than RNA source ({len(rna_structure)})."
        )

    output: Structure = OrderedDict()
    report_rows: List[Dict[str, object]] = []

    template_items = list(hna_template.items())

    for index, (source_key, source_residue) in enumerate(rna_structure.items()):
        template_key, template_residue = template_items[index]

        source_first_atom = next(iter(source_residue.values()))
        output_res_name = hna_residue_name(source_first_atom.res_name, base_policy)

        source_chain, source_res_num, source_icode = source_key
        hybrid_residue, stats = transform_residue(
            source_residue=source_residue,
            template_residue=template_residue,
            output_res_name=output_res_name,
            output_chain=source_chain,
            output_res_num=source_res_num,
            output_insertion_code=source_icode,
            anchors=anchors,
        )

        output[source_key] = hybrid_residue

        row: Dict[str, object] = {
            "index": index + 1,
            "source_key": source_key,
            "template_key": template_key,
            "source_res_name": source_first_atom.res_name,
            "output_res_name": output_res_name,
        }
        row.update(stats)
        report_rows.append(row)

    return output, report_rows


def summarize_validation(report_rows: List[Dict[str, object]]) -> Dict[str, float]:
    """Summarize per-residue anchor RMSD values."""
    rmsds = [float(row["anchor_rmsd"]) for row in report_rows if "anchor_rmsd" in row]
    if not rmsds:
        return {"mean_anchor_rmsd": math.nan, "max_anchor_rmsd": math.nan}
    return {
        "mean_anchor_rmsd": float(np.mean(rmsds)),
        "max_anchor_rmsd": float(np.max(rmsds)),
    }


def write_markdown_report(
    report_path: Path,
    rna_path: Path,
    template_path: Path,
    output_path: Path,
    source_sequence: str,
    base_policy: str,
    report_rows: List[Dict[str, object]],
) -> None:
    """Write a simple Markdown conversion report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary = summarize_validation(report_rows)

    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("# Prototype 001: RNA → HNA template-guided reconstruction report\n\n")
        handle.write("## Input files\n\n")
        handle.write(f"- Source RNA PDB: `{rna_path}`\n")
        handle.write(f"- HNA template PDB: `{template_path}`\n")
        handle.write(f"- Output candidate PDB: `{output_path}`\n\n")

        handle.write("## Settings\n\n")
        handle.write(f"- Source sequence: `{source_sequence}`\n")
        handle.write(f"- Base policy: `{base_policy}`\n")
        handle.write("- Alignment anchors: `C1'`, `C2'`, `C4'`\n\n")

        if base_policy == "rna-to-dna-label":
            handle.write(
                "> Warning: `rna-to-dna-label` maps RNA `U` to HNA `T` as a residue label only. "
                "This script does not add a thymine methyl group.\n\n"
            )

        handle.write("## Validation summary\n\n")
        handle.write(f"- Residues converted: {len(report_rows)}\n")
        handle.write(f"- Mean anchor RMSD: {summary['mean_anchor_rmsd']:.4f} Å\n")
        handle.write(f"- Max anchor RMSD: {summary['max_anchor_rmsd']:.4f} Å\n\n")

        handle.write("## Per-residue report\n\n")
        handle.write("| Index | Source residue | Output residue | Template residue | Method | Anchors | Anchor RMSD (Å) | Backbone atoms | Base atoms |\n")
        handle.write("|---:|---|---|---|---|---|---:|---:|---:|\n")
        for row in report_rows:
            anchors = ", ".join(row.get("used_anchors", []))
            template_key = row["template_key"]
            source_res = f"{row['source_res_name']} {row['source_key'][0]}:{row['source_key'][1]}{row['source_key'][2]}"
            template_res = f"{template_key[0]}:{template_key[1]}{template_key[2]}"
            handle.write(
                f"| {row['index']} "
                f"| {source_res} "
                f"| {row['output_res_name']} "
                f"| {template_res} "
                f"| {row['method']} "
                f"| {anchors} "
                f"| {float(row['anchor_rmsd']):.4f} "
                f"| {row['backbone_atom_count']} "
                f"| {row['base_atom_count']} |\n"
            )

        handle.write("\n## Important note\n\n")
        handle.write(
            "This output is a computational candidate structure. It has not been energy-minimized, "
            "force-field-validated, or experimentally verified. Use downstream geometry checks, "
            "molecular mechanics, molecular dynamics, and expert chemical inspection before drawing "
            "research conclusions.\n"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prototype 001: template-guided RNA -> HNA candidate reconstruction."
    )
    parser.add_argument(
        "--rna",
        required=True,
        type=Path,
        help="Input source RNA PDB file.",
    )
    parser.add_argument(
        "--template",
        required=True,
        type=Path,
        help="Input experimental/template HNA PDB file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output candidate HNA PDB file.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Optional Markdown report output path.",
    )
    parser.add_argument(
        "--base-policy",
        choices=("preserve", "rna-to-dna-label"),
        default="preserve",
        help=(
            "Base-label policy. 'preserve' keeps U as 6HU. "
            "'rna-to-dna-label' maps U to 6HT as a label only; it does not add a methyl group."
        ),
    )
    parser.add_argument(
        "--anchors",
        nargs="+",
        default=["C1'", "C2'", "C4'"],
        help="Anchor atoms used for local Kabsch alignment.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    print("=" * 80)
    print("DIGITAL POLYMERASE - PROTOTYPE 001")
    print("Template-guided RNA -> HNA candidate reconstruction")
    print("=" * 80)

    print("\n[1] Loading structures...")
    rna_structure = parse_pdb(args.rna)
    hna_template = parse_pdb(args.template)

    if not rna_structure:
        raise ValueError(f"No ATOM/HETATM records found in RNA file: {args.rna}")
    if not hna_template:
        raise ValueError(f"No ATOM/HETATM records found in HNA template file: {args.template}")

    source_sequence = residue_base_sequence(rna_structure)

    print(f"    RNA source residues: {len(rna_structure)}")
    print(f"    HNA template residues: {len(hna_template)}")
    print(f"    Source sequence: {source_sequence}")
    print(f"    Base policy: {args.base_policy}")

    if args.base_policy == "rna-to-dna-label":
        print("    WARNING: U->T is label-only; no thymine methyl group is added.")

    print("\n[2] Reconstructing candidate HNA residues...")
    hna_candidate, report_rows = convert_rna_to_hna(
        rna_structure=rna_structure,
        hna_template=hna_template,
        base_policy=args.base_policy,
        anchors=args.anchors,
    )

    for row in report_rows:
        print(
            f"    {row['index']:>2}. {row['source_res_name']} -> {row['output_res_name']} "
            f"| method={row['method']} "
            f"| anchors={','.join(row['used_anchors'])} "
            f"| anchor RMSD={float(row['anchor_rmsd']):.4f} Å "
            f"| backbone={row['backbone_atom_count']} atoms "
            f"| base={row['base_atom_count']} atoms"
        )

    validation_summary = summarize_validation(report_rows)

    print("\n[3] Writing output PDB...")
    write_pdb(
        residues=hna_candidate,
        output_path=args.output,
        source_sequence=source_sequence,
        base_policy=args.base_policy,
        validation_summary=validation_summary,
    )
    print(f"    Wrote: {args.output}")

    if args.report:
        print("\n[4] Writing Markdown report...")
        write_markdown_report(
            report_path=args.report,
            rna_path=args.rna,
            template_path=args.template,
            output_path=args.output,
            source_sequence=source_sequence,
            base_policy=args.base_policy,
            report_rows=report_rows,
        )
        print(f"    Wrote: {args.report}")

    print("\nSummary")
    print("-------")
    print(f"Residues converted: {len(report_rows)}")
    print(f"Mean anchor RMSD: {validation_summary['mean_anchor_rmsd']:.4f} Å")
    print(f"Max anchor RMSD: {validation_summary['max_anchor_rmsd']:.4f} Å")
    print("\nWARNING: Output is a computational candidate only.")
    print("Use energy minimization, MD simulation, and expert inspection before research use.")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
