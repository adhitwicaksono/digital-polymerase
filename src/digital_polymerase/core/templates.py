"""Template selection and template-sequence helpers."""
from __future__ import annotations
from collections import defaultdict
from typing import Mapping
from .atoms import Atom, ResidueKey
from .pdb_io import sort_residue_keys, residue_name
from .residues import base_of
from .registry import required_backbone_atoms
from .errors import TemplateError

def usable_template_keys(template: Mapping[ResidueKey, Mapping[str, Atom]], *, required_atoms: list[str] | None = None, target: str | None = None) -> list[ResidueKey]:
    if required_atoms is None:
        if target is None: raise ValueError("Either required_atoms or target must be provided")
        required_atoms = required_backbone_atoms(target)
    return [k for k in sort_residue_keys(template) if all(a in template[k] for a in required_atoms)]

def template_sequence(template, *, required_atoms=None, target=None) -> str:
    return "".join(base_of(residue_name(template[k])) for k in usable_template_keys(template, required_atoms=required_atoms, target=target))

def build_template_index(template, *, required_atoms=None, target=None) -> dict[str, list[ResidueKey]]:
    idx = defaultdict(list)
    for k in usable_template_keys(template, required_atoms=required_atoms, target=target):
        b = base_of(residue_name(template[k]))
        if b in {"A","U","G","C"}: idx[b].append(k)
    return dict(idx)

def select_template_by_base(base: str, index: Mapping[str, list[ResidueKey]], *, counters: dict[str,int] | None = None) -> tuple[ResidueKey, str]:
    b = base_of(base); counters = counters if counters is not None else {}
    def pick(label, note):
        i = counters.get(label, 0); counters[label] = i+1
        return index[label][i % len(index[label])], note
    if b in index and index[b]: return pick(b, "exact base-class template")
    if b == "U" and "T" in index and index["T"]: return pick("T", "T-like donor for U")
    for alt in (["A","G"] if b in {"A","G"} else ["C","U","T"]):
        if alt in index and index[alt]: return pick(alt, f"fallback {alt}-like template")
    if not index: raise TemplateError("Template index is empty")
    first = sorted(index)[0]
    return pick(first, "last-resort template")

def assert_template_has_required_atoms(template, *, required_atoms=None, target=None) -> None:
    if not usable_template_keys(template, required_atoms=required_atoms, target=target):
        req = required_atoms if required_atoms is not None else required_backbone_atoms(target or "")
        raise TemplateError(f"No template residue contains all required atoms: {req}")
