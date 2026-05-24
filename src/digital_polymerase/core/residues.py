"""Residue and base-identity helpers."""
from __future__ import annotations
from typing import Mapping, Iterable
import numpy as np
from .atoms import Atom, ResidueKey
from .pdb_io import sort_residue_keys, residue_name

CANONICAL_RNA_BASES = {"A", "U", "G", "C"}
DNA_TO_RNA = {"DA":"A", "DT":"U", "DG":"G", "DC":"C"}
RNA_BACKBONE_ATOMS = {"P","OP1","OP2","O1P","O2P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'"}
BASE_CORE_ATOMS = {
    "A": ["N9","C8","N7","C5","C6","N6","N1","C2","N3","C4"],
    "G": ["N9","C8","N7","C5","C6","O6","N1","C2","N2","N3","C4"],
    "C": ["N1","C2","O2","N3","C4","N4","C5","C6"],
    "U": ["N1","C2","O2","N3","C4","O4","C5","C6"],
}
BASE_REQUIRED_OXYGENS = {"A": [], "G": ["O6"], "C": ["O2"], "U": ["O2", "O4"]}

def normalize_base_symbol(symbol: str) -> str:
    s = (symbol or "").upper().strip()
    return "U" if s == "T" else s

def base_of(res_name: str) -> str:
    r = (res_name or "").upper().strip()
    if r in {"A","U","G","C"}: return r
    if r in DNA_TO_RNA: return DNA_TO_RNA[r]
    if r == "APN" or r.endswith("A") or r.startswith("A"): return "A"
    if r == "GPN" or r.endswith("G") or r.startswith("G"): return "G"
    if r == "CPN" or r.endswith("C") or r.startswith("C"): return "C"
    if r == "TPN" or r.endswith("T") or r.endswith("U") or r.startswith(("T","U")): return "U"
    return "N"

def glycosidic_atom(base: str) -> str:
    return "N9" if normalize_base_symbol(base) in {"A", "G"} else "N1"

def residue_base(residue: Mapping[str, Atom]) -> str:
    return base_of(residue_name(residue))

def is_base_atom(atom_name: str, *, backbone_atoms: Iterable[str] = RNA_BACKBONE_ATOMS) -> bool:
    return atom_name not in set(backbone_atoms) and "'" not in atom_name and not atom_name.startswith("H") and not atom_name.startswith("OP")

def split_base_backbone_atoms(residue: Mapping[str, Atom], *, backbone_atoms: Iterable[str] = RNA_BACKBONE_ATOMS) -> tuple[dict[str,Atom], dict[str,Atom]]:
    base, back = {}, {}
    bset = set(backbone_atoms)
    for name, atom in residue.items():
        if name in bset or "'" in name or name == "P" or name.startswith("OP"): back[name] = atom
        elif not name.startswith("H"): base[name] = atom
    return base, back

def source_base_keys(structure: Mapping[ResidueKey, Mapping[str, Atom]]) -> list[ResidueKey]:
    return [k for k in sort_residue_keys(structure) if residue_base(structure[k]) in CANONICAL_RNA_BASES]

def source_sequence(structure: Mapping[ResidueKey, Mapping[str, Atom]]) -> str:
    return "".join(residue_base(structure[k]) for k in source_base_keys(structure))

def base_centroid(residue: Mapping[str, Atom], base: str | None = None) -> np.ndarray:
    b = base or residue_base(residue)
    names = [n for n in BASE_CORE_ATOMS.get(b, []) if n in residue]
    if not names: names = [n for n in residue if is_base_atom(n)]
    if not names: raise ValueError("Cannot compute base centroid: no base atoms found")
    return np.mean([residue[n].coords for n in names], axis=0)

def required_base_atoms(base: str) -> list[str]: return BASE_CORE_ATOMS.get(normalize_base_symbol(base), [])
def required_base_oxygens(base: str) -> list[str]: return BASE_REQUIRED_OXYGENS.get(normalize_base_symbol(base), [])
