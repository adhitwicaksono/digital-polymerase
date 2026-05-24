"""XNA target registry for atom grammar and validation defaults."""
from __future__ import annotations
from copy import deepcopy
from typing import Any
from .errors import RegistryError

XNA_REGISTRY: dict[str, dict[str, Any]] = {
 "RNA": {"family":"canonical", "backbone_atoms":["P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.85}], "base_attachment_range":[1.25,1.75], "strategy_default":"canonical"},
 "HNA": {"family":"hexitol", "backbone_atoms":["P","O5'","C5'","C4'","C3'","O3'","C2'","C1'","C6'","O4'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.90}], "base_attachment_range":[1.25,1.80], "distance_checks":{"C1'→C6'":["C1'","C6'",1.25,1.90], "C6'→O4'":["C6'","O4'",1.20,1.80]}, "strategy_default":"chain_preserving"},
 "ANA": {"family":"arabino", "backbone_atoms":["P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.90}], "base_attachment_range":[1.25,1.80], "strategy_default":"chain_preserving"},
 "FANA": {"family":"fluoroarabino", "backbone_atoms":["P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","F2'","C1'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.90}], "base_attachment_range":[1.25,1.80], "distance_checks":{"C2'→F2'":["C2'","F2'",1.25,1.55], "C1'→C2'":["C1'","C2'",1.25,1.75]}, "strategy_default":"chain_preserving"},
 "CeNA": {"family":"cyclohexenyl", "backbone_atoms":["P","O5'","C5'","C4'","C3'","O3'","C2'","C1'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.95}], "base_attachment_range":[1.25,1.85], "strategy_default":"template_guided"},
 "XyNA": {"family":"xylo", "backbone_atoms":["P","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.90}], "base_attachment_range":[1.25,1.80], "strategy_default":"template_guided"},
 "TNA": {"family":"threose", "backbone_atoms":["P","O5'","C4'","C3'","O3'","C2'","C1'"], "base_attachment_atom":"C1'", "linkage":[{"left":"O3'","right":"P","lo":1.45,"hi":1.95}], "base_attachment_range":[1.25,1.85], "strategy_default":"linkage_remapped"},
 "GNA": {"family":"glycerol", "backbone_atoms":["P","O3G","C3G","C2G","O2G","C1G"], "base_attachment_atom":"C1G", "linkage":[{"left":"P","right":"O3G","same_residue":True,"lo":1.35,"hi":1.85}, {"left":"O2G","right":"P","lo":1.35,"hi":1.95}], "base_attachment_range":[1.20,1.90], "strategy_default":"linkage_optimized"},
 "PNA": {"family":"pseudopeptide", "backbone_atoms":["C8'","C7'","O7'","N4'","C3'","C2'","N1'","C5'","C'","O1'"], "base_attachment_atom":"C8'", "linkage":[{"left":"C'","right":"N1'","lo":1.15,"hi":1.60}], "base_attachment_range":[1.20,1.85], "distance_checks":{"C8'→C7'":["C8'","C7'",1.30,1.85], "C7'→O7'":["C7'","O7'",1.10,1.40], "C7'→N4'":["C7'","N4'",1.15,1.60], "C'→O1'":["C'","O1'",1.10,1.40]}, "strategy_default":"template_primary"},
}

def normalize_target_name(target: str) -> str: return (target or "").upper().strip()
def get_target_spec(target: str) -> dict[str, Any]:
    key = normalize_target_name(target)
    if key not in XNA_REGISTRY: raise RegistryError(f"Unknown target: {target!r}. Available: {', '.join(sorted(XNA_REGISTRY))}")
    return deepcopy(XNA_REGISTRY[key])
def available_targets() -> list[str]: return sorted(XNA_REGISTRY)
def required_backbone_atoms(target: str) -> list[str]: return list(get_target_spec(target).get('backbone_atoms', []))
def default_strategy(target: str) -> str: return str(get_target_spec(target).get('strategy_default', 'template_guided'))
