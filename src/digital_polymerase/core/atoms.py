"""Atom-level data structures and helpers."""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Tuple, Optional
import re
import numpy as np

ResidueKey = Tuple[str, int, str]

@dataclass
class Atom:
    """Lightweight PDB atom record."""
    record: str
    atom_name: str
    res_name: str
    chain: str
    res_num: int
    insertion_code: str
    coords: np.ndarray
    occupancy: float = 1.0
    temp_factor: float = 0.0
    element: str = ""

    def __post_init__(self) -> None:
        self.coords = np.asarray(self.coords, dtype=float)
        if self.coords.shape != (3,):
            raise ValueError(f"Atom coordinates must have shape (3,), got {self.coords.shape}")
        self.record = self.record if self.record in {"ATOM", "HETATM"} else "HETATM"
        self.chain = (self.chain or "A")[:1]
        self.insertion_code = (self.insertion_code or "")[:1]
        if not self.element:
            self.element = infer_element(self.atom_name)

    @property
    def residue_key(self) -> ResidueKey:
        return (self.chain, self.res_num, self.insertion_code)

    def copy_with(self, **kwargs) -> "Atom":
        new_name = kwargs.get("atom_name", self.atom_name)
        if "element" not in kwargs or kwargs.get("element") is None:
            kwargs["element"] = infer_element(new_name, self.element)
        if "coords" in kwargs and kwargs["coords"] is not None:
            kwargs["coords"] = np.asarray(kwargs["coords"], dtype=float)
        return replace(self, **{k:v for k,v in kwargs.items() if v is not None})

def infer_element(atom_name: str, pdb_element: str = "") -> str:
    elem = (pdb_element or "").strip()
    if elem and re.fullmatch(r"[A-Za-z]{1,2}", elem):
        return elem[0].upper() + elem[1:].lower()
    cleaned = re.sub(r"[^A-Za-z]", "", atom_name or "")
    if not cleaned: return ""
    two = {"CL","BR","NA","MG","ZN","FE","CA","MN","CU","CO","NI","SE"}
    cand = cleaned[:2].upper()
    return cand[0] + cand[1].lower() if cand in two else cleaned[0].upper()

def clone_atom(atom: Atom, **kwargs) -> Atom:
    return atom.copy_with(**kwargs)

def atom_sort_key(atom_name: str, preferred_order: Optional[list[str]] = None) -> tuple[int, str]:
    if preferred_order and atom_name in preferred_order:
        return (preferred_order.index(atom_name), atom_name)
    return (10000, atom_name)

def is_hydrogen(atom: Atom) -> bool:
    return (atom.element or infer_element(atom.atom_name)).upper() == "H" or atom.atom_name.upper().startswith("H")
