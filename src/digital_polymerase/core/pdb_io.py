"""PDB parsing and writing utilities."""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from typing import Dict, Mapping, Iterable, Optional
import numpy as np
from .atoms import Atom, ResidueKey, infer_element, atom_sort_key
from .errors import PDBParseError

Residue = Dict[str, Atom]
Structure = Dict[ResidueKey, Residue]

def sort_residue_keys(residues: Mapping[ResidueKey, Residue]) -> list[ResidueKey]:
    return sorted(residues.keys(), key=lambda k: (k[0], k[1], k[2]))

def parse_pdb(path: str | Path, *, strict: bool = False) -> Structure:
    path = Path(path)
    residues: dict[ResidueKey, Residue] = defaultdict(dict)
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        raise PDBParseError(f"Could not read PDB file: {path}") from exc
    for lineno, line in enumerate(lines, 1):
        if not line.startswith(("ATOM", "HETATM")): continue
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
            atom = Atom("HETATM" if line.startswith("HETATM") else "ATOM", name, resn, chain, rn, ic, xyz, occ, temp, infer_element(name, elem))
            residues[atom.residue_key][atom.atom_name] = atom
        except Exception as exc:
            if strict: raise PDBParseError(f"Failed to parse line {lineno}: {line!r}") from exc
            continue
    return dict(residues)

def residue_name(residue: Mapping[str, Atom]) -> str:
    return next(iter(residue.values())).res_name

def format_atom_line(serial: int, atom: Atom) -> str:
    elem = (atom.element or infer_element(atom.atom_name))[:2].rjust(2)
    ic = (atom.insertion_code or " ")[:1]
    return (f"{atom.record:<6s}{serial:5d} {atom.atom_name[:4]:>4s} {atom.res_name[:3]:>3s} "
            f"{(atom.chain or 'A')[:1]}{atom.res_num:4d}{ic}   "
            f"{atom.coords[0]:8.3f}{atom.coords[1]:8.3f}{atom.coords[2]:8.3f}"
            f"{atom.occupancy:6.2f}{atom.temp_factor:6.2f}{'':>10s}{elem:>2s}")

def write_pdb(residues: Mapping[ResidueKey, Residue], path: str | Path, *, remarks: Optional[Iterable[str]] = None, preferred_atom_order: Optional[list[str]] = None, conect_records: Optional[Iterable[str]] = None) -> None:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as h:
        for remark in remarks or []: h.write(f"REMARK   {remark}\n")
        h.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1\n")
        serial = 1
        for key in sort_residue_keys(residues):
            for name in sorted(residues[key], key=lambda n: atom_sort_key(n, preferred_atom_order)):
                h.write(format_atom_line(serial, residues[key][name]) + "\n"); serial += 1
        for line in conect_records or []: h.write(line.rstrip('\n') + '\n')
        h.write("END\n")
