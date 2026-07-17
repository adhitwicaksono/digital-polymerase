"""Explicit atom references, covalent bonds, and PDB ``CONECT`` records.

PDB coordinates do not, by themselves, define a complete molecular topology.
This module provides a small target-independent representation that physical
readiness workflows can use without pretending to assign force-field atom
types, charges, or bond orders.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .atoms import ResidueKey, atom_sort_key
from .pdb_io import Residue, sort_residue_keys


@dataclass(frozen=True, order=True)
class AtomReference:
    """Identify one atom independently of its PDB serial number."""

    chain: str
    res_num: int
    insertion_code: str
    atom_name: str

    @classmethod
    def from_residue_key(cls, key: ResidueKey, atom_name: str) -> "AtomReference":
        return cls(key[0], key[1], key[2], atom_name)

    @property
    def residue_key(self) -> ResidueKey:
        return (self.chain, self.res_num, self.insertion_code)

    @property
    def label(self) -> str:
        insertion = self.insertion_code or ""
        return f"{self.chain}:{self.res_num}{insertion}:{self.atom_name}"


@dataclass(frozen=True)
class CovalentBond:
    """An undirected covalent connection without a force-field bond order."""

    left: AtomReference
    right: AtomReference
    category: str

    @property
    def key(self) -> tuple[AtomReference, AtomReference]:
        return tuple(sorted((self.left, self.right)))  # type: ignore[return-value]


def deduplicate_bonds(bonds: Sequence[CovalentBond]) -> list[CovalentBond]:
    """Return bonds in first-seen order with duplicate atom pairs removed."""

    seen: set[tuple[AtomReference, AtomReference]] = set()
    unique: list[CovalentBond] = []
    for bond in bonds:
        if bond.left == bond.right:
            raise ValueError(f"Self-bond is invalid: {bond.left.label}")
        if bond.key in seen:
            continue
        seen.add(bond.key)
        unique.append(bond)
    return unique


def build_serial_map(
    structure: Mapping[ResidueKey, Residue],
    *,
    preferred_atom_order: Sequence[str] | None = None,
) -> dict[AtomReference, int]:
    """Map atom references to the serial order used by ``write_pdb``."""

    serials: dict[AtomReference, int] = {}
    serial = 1
    order = list(preferred_atom_order) if preferred_atom_order is not None else None
    for key in sort_residue_keys(structure):
        for atom_name in sorted(
            structure[key], key=lambda name: atom_sort_key(name, order)
        ):
            serials[AtomReference.from_residue_key(key, atom_name)] = serial
            serial += 1
    return serials


def format_conect_records(
    structure: Mapping[ResidueKey, Residue],
    bonds: Sequence[CovalentBond],
    *,
    preferred_atom_order: Sequence[str] | None = None,
) -> list[str]:
    """Format a symmetric heavy-atom bond graph as PDB ``CONECT`` records.

    At most four partners are written per record, matching the traditional PDB
    fixed-width representation. Multiple records are emitted when necessary.
    """

    serials = build_serial_map(structure, preferred_atom_order=preferred_atom_order)
    adjacency: dict[int, set[int]] = {}
    for bond in deduplicate_bonds(bonds):
        try:
            left = serials[bond.left]
            right = serials[bond.right]
        except KeyError as exc:
            missing = exc.args[0]
            raise ValueError(
                f"Bond references an atom absent from the structure: {missing.label}"
            ) from exc
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)

    records: list[str] = []
    for serial in sorted(adjacency):
        partners = sorted(adjacency[serial])
        for offset in range(0, len(partners), 4):
            chunk = partners[offset : offset + 4]
            records.append(
                "CONECT" + f"{serial:5d}" + "".join(f"{value:5d}" for value in chunk)
            )
    return records
