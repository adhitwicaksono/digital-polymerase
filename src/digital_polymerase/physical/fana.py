"""FANA Level 4 physical-modeling readiness gate.

The gate turns a Level 3 geometric FANA candidate into an auditable handoff for
external parameterization. It builds an explicit covalent graph, checks bond
distances, compares C2' stereochemistry and sugar pucker against an experimental
FANA template, records unresolved termini, and emits an optional ``CONECT`` PDB.

It deliberately does *not* invent force-field atom types, partial charges, or
parameters. A passing result is therefore ``PARAMETERIZATION_REQUIRED``, never
``MD_READY``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from math import atan2, degrees, hypot, pi
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np

from digital_polymerase.converters.rna_to_fana import PREFERRED_ATOM_ORDER
from digital_polymerase.core.atoms import Atom, ResidueKey, is_hydrogen
from digital_polymerase.core.connectivity import (
    AtomReference,
    CovalentBond,
    deduplicate_bonds,
    format_conect_records,
)
from digital_polymerase.core.errors import (
    TemplateError,
    UnsupportedResidueError,
    ValidationError,
)
from digital_polymerase.core.geometry import dihedral, distance
from digital_polymerase.core.pdb_io import (
    Structure,
    parse_pdb,
    residue_name,
    sort_residue_keys,
    write_pdb,
)
from digital_polymerase.core.residues import base_of, glycosidic_atom


SCHEMA_VERSION = "0.1"
TARGET = "FANA"
RING_ATOMS = ("O4'", "C1'", "C2'", "C3'", "C4'")
FIVE_PRIME_PHOSPHATE_ATOMS = frozenset({"P", "OP1", "OP2"})


@dataclass(frozen=True)
class BondRule:
    left: str
    right: str
    minimum: float
    maximum: float
    category: str


@dataclass(frozen=True)
class BondDistanceFailure:
    left: str
    right: str
    category: str
    measured: float
    minimum: float
    maximum: float


@dataclass(frozen=True)
class PuckerObservation:
    residue: str
    base: str
    phase_degrees: float
    amplitude_degrees: float
    fit_rms_degrees: float
    reference_residue: str
    reference_phase_degrees: float
    reference_amplitude_degrees: float
    phase_delta_degrees: float
    amplitude_delta_degrees: float
    status: str


@dataclass(frozen=True)
class ChiralityObservation:
    residue: str
    base: str
    signed_volume: float
    observed_sign: int
    reference_sign: int
    status: str


@dataclass
class FANAReadinessResult:
    """Result returned by the FANA physical-readiness audit."""

    status: str
    geometry_status: str
    residue_count: int
    bond_count: int
    report_path: Path
    manifest_path: Path
    conect_pdb_path: Path | None
    missing_atoms: list[dict[str, str]]
    distance_failures: list[BondDistanceFailure]
    pucker_observations: list[PuckerObservation]
    chirality_observations: list[ChiralityObservation]
    parameterization_blockers: list[str]

    @property
    def geometry_ok(self) -> bool:
        return self.geometry_status == "PASS"


BACKBONE_RULES = (
    BondRule("P", "OP1", 1.35, 1.75, "phosphate"),
    BondRule("P", "OP2", 1.35, 1.75, "phosphate"),
    BondRule("P", "O5'", 1.40, 1.85, "phosphate_ester"),
    BondRule("O5'", "C5'", 1.25, 1.70, "sugar_backbone"),
    BondRule("C5'", "C4'", 1.25, 1.80, "sugar_backbone"),
    BondRule("C4'", "O4'", 1.20, 1.70, "sugar_ring"),
    BondRule("O4'", "C1'", 1.20, 1.70, "sugar_ring"),
    BondRule("C1'", "C2'", 1.25, 1.75, "sugar_ring"),
    BondRule("C2'", "C3'", 1.25, 1.80, "sugar_ring"),
    BondRule("C3'", "C4'", 1.25, 1.80, "sugar_ring"),
    BondRule("C3'", "O3'", 1.20, 1.70, "sugar_backbone"),
    BondRule("C2'", "F2'", 1.20, 1.60, "fana_substituent"),
)

BASE_BONDS: dict[str, tuple[tuple[str, str], ...]] = {
    "A": (
        ("N9", "C8"),
        ("C8", "N7"),
        ("N7", "C5"),
        ("C5", "C6"),
        ("C6", "N6"),
        ("C6", "N1"),
        ("N1", "C2"),
        ("C2", "N3"),
        ("N3", "C4"),
        ("C4", "C5"),
        ("C4", "N9"),
    ),
    "G": (
        ("N9", "C8"),
        ("C8", "N7"),
        ("N7", "C5"),
        ("C5", "C6"),
        ("C6", "O6"),
        ("C6", "N1"),
        ("N1", "C2"),
        ("C2", "N2"),
        ("C2", "N3"),
        ("N3", "C4"),
        ("C4", "C5"),
        ("C4", "N9"),
    ),
    "C": (
        ("N1", "C2"),
        ("C2", "O2"),
        ("C2", "N3"),
        ("N3", "C4"),
        ("C4", "N4"),
        ("C4", "C5"),
        ("C5", "C6"),
        ("C6", "N1"),
    ),
    "U": (
        ("N1", "C2"),
        ("C2", "O2"),
        ("C2", "N3"),
        ("N3", "C4"),
        ("C4", "O4"),
        ("C4", "C5"),
        ("C5", "C6"),
        ("C6", "N1"),
    ),
}


def _residue_label(key: ResidueKey) -> str:
    insertion = key[2] or ""
    return f"{key[0]}:{key[1]}{insertion}"


def _find_fluorine(residue: Mapping[str, Atom]) -> str | None:
    for name in ("F2'", "F", "2F", "F2*"):
        if name in residue:
            return name
    for name, atom in residue.items():
        if name.upper().startswith("F") or atom.element.upper() == "F":
            return name
    return None


def _signed_c2_volume(residue: Mapping[str, Atom], fluorine_name: str) -> float:
    center = residue["C2'"].coords
    c1_vector = residue["C1'"].coords - center
    c3_vector = residue["C3'"].coords - center
    fluorine_vector = residue[fluorine_name].coords - center
    return float(np.dot(np.cross(c1_vector, c3_vector), fluorine_vector))


def _sign(value: float, *, tolerance: float = 1e-3) -> int:
    if value > tolerance:
        return 1
    if value < -tolerance:
        return -1
    return 0


def _pseudorotation(residue: Mapping[str, Atom]) -> tuple[float, float, float]:
    """Fit the five ring torsions to a pseudorotation phase and amplitude.

    The phase is used only for comparison with the supplied template under the
    same convention. No north/south label is assigned from the numeric phase.
    """

    torsions: list[float] = []
    for index in range(5):
        names = (
            RING_ATOMS[(index - 1) % 5],
            RING_ATOMS[index],
            RING_ATOMS[(index + 1) % 5],
            RING_ATOMS[(index + 2) % 5],
        )
        torsions.append(dihedral(*(residue[name].coords for name in names)))

    angles = np.asarray([4.0 * pi * index / 5.0 for index in range(5)])
    design = np.column_stack((np.cos(angles), np.sin(angles)))
    cosine_coefficient, sine_coefficient = np.linalg.lstsq(
        design, np.asarray(torsions), rcond=None
    )[0]
    fitted = design @ np.asarray([cosine_coefficient, sine_coefficient])
    phase = degrees(atan2(-sine_coefficient, cosine_coefficient)) % 360.0
    amplitude = hypot(cosine_coefficient, sine_coefficient)
    fit_rms = float(np.sqrt(np.mean((np.asarray(torsions, dtype=float) - fitted) ** 2)))
    return float(phase), float(amplitude), fit_rms


def _circular_delta(left: float, right: float) -> float:
    return abs((left - right + 180.0) % 360.0 - 180.0)


def _consecutive_segments(keys: Sequence[ResidueKey]) -> list[list[ResidueKey]]:
    if not keys:
        return []
    segments: list[list[ResidueKey]] = [[keys[0]]]
    for key in keys[1:]:
        previous = segments[-1][-1]
        consecutive = (
            key[0] == previous[0]
            and key[1] == previous[1] + 1
            and not key[2]
            and not previous[2]
        )
        if consecutive:
            segments[-1].append(key)
        else:
            segments.append([key])
    return segments


def _add_bond_observation(
    *,
    structure: Structure,
    left_key: ResidueKey,
    right_key: ResidueKey,
    rule: BondRule,
    bonds: list[CovalentBond],
    distances: list[float],
    missing_atoms: list[dict[str, str]],
    failures: list[BondDistanceFailure],
) -> None:
    left_residue = structure[left_key]
    right_residue = structure[right_key]
    missing = []
    if rule.left not in left_residue:
        missing.append(f"{_residue_label(left_key)}:{rule.left}")
    if rule.right not in right_residue:
        missing.append(f"{_residue_label(right_key)}:{rule.right}")
    if missing:
        missing_atoms.append(
            {
                "category": rule.category,
                "bond": "—".join(missing),
            }
        )
        return

    left_ref = AtomReference.from_residue_key(left_key, rule.left)
    right_ref = AtomReference.from_residue_key(right_key, rule.right)
    bonds.append(CovalentBond(left_ref, right_ref, rule.category))
    measured = distance(
        left_residue[rule.left].coords, right_residue[rule.right].coords
    )
    distances.append(measured)
    if not rule.minimum <= measured <= rule.maximum:
        failures.append(
            BondDistanceFailure(
                left=left_ref.label,
                right=right_ref.label,
                category=rule.category,
                measured=measured,
                minimum=rule.minimum,
                maximum=rule.maximum,
            )
        )


def _template_references(
    template: Structure,
) -> dict[str, list[dict[str, float | str | int]]]:
    references: dict[str, list[dict[str, float | str | int]]] = {}
    for key in sort_residue_keys(template):
        residue = template[key]
        fluorine_name = _find_fluorine(residue)
        if fluorine_name is None or not set(RING_ATOMS).issubset(residue):
            continue
        if not {"C1'", "C2'", "C3'"}.issubset(residue):
            continue
        base = base_of(residue_name(residue))
        if base not in BASE_BONDS:
            continue
        phase, amplitude, fit_rms = _pseudorotation(residue)
        volume = _signed_c2_volume(residue, fluorine_name)
        references.setdefault(base, []).append(
            {
                "residue": _residue_label(key),
                "phase": phase,
                "amplitude": amplitude,
                "fit_rms": fit_rms,
                "chirality_sign": _sign(volume),
            }
        )
    if not references:
        raise TemplateError(
            "The FANA template has no fluorinated residue with a complete "
            "O4'/C1'/C2'/C3'/C4' ring."
        )
    return references


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_report(
    *,
    path: Path,
    candidate_path: Path,
    template_path: Path,
    result: FANAReadinessResult,
    distance_count: int,
    distance_mean: float,
    distance_minimum: float,
    distance_maximum: float,
    segment_count: int,
    hydrogen_count: int,
) -> None:
    failed_puckers = sum(
        observation.status != "PASS" for observation in result.pucker_observations
    )
    failed_chirality = sum(
        observation.status != "PASS" for observation in result.chirality_observations
    )
    blockers = "\n".join(
        f"{index}. {blocker}"
        for index, blocker in enumerate(result.parameterization_blockers, 1)
    )
    conect_line = (
        f"- Explicit-connectivity PDB: `{result.conect_pdb_path}`\n"
        if result.conect_pdb_path is not None
        else "- Explicit-connectivity PDB: not requested\n"
    )
    markdown = f"""# FANA Level 4 Physical-Readiness Report

**Overall status:** `{result.status}`
**Geometry gate:** `{result.geometry_status}`
**Interpretation:** This is a parameterization handoff, not an MD-ready system.

## Inputs and outputs

- Candidate PDB: `{candidate_path}`
- Experimental FANA template: `{template_path}`
- Machine-readable manifest: `{result.manifest_path}`
{conect_line}
## Topology and geometry

| Check | Result |
|---|---:|
| FANA residues | {result.residue_count} |
| Consecutive chain segments | {segment_count} |
| Explicit covalent bonds | {result.bond_count} |
| Bond distances measured | {distance_count} |
| Missing atoms in bond rules | {len(result.missing_atoms)} |
| Out-of-range covalent distances | {len(result.distance_failures)} |
| C2′ stereochemistry mismatches | {failed_chirality} |
| Template-relative pucker outliers | {failed_puckers} |
| Explicit hydrogens present | {hydrogen_count} |

Measured covalent-distance range: `{distance_minimum:.3f}–{distance_maximum:.3f} Å`; mean `{distance_mean:.3f} Å`.

Sugar-pucker phases are compared only with the supplied template using the same
five-torsion fitting convention. The phase values are not independently labeled
as north, south, east, or west by this gate.

## Parameterization blockers

{blockers}

## External parameterization handoff

The modXNA catalog identifies `A5L` as the 2′FANA sugar/linker fragment built in
a C2′-endo conformer. That catalog match is a starting point, not a complete
residue template. Backbone/base modules, terminal forms, atom naming, charges,
and all bonded and nonbonded parameters still require an explicit, versioned
parameterization workflow and expert review.

Primary references:

- Love et al., *J. Chem. Theory Comput.* (2024), DOI: https://doi.org/10.1021/acs.jctc.4c01164
- Galindo-Murillo et al., *Living J. Comput. Mol. Sci.* (2025), DOI: https://doi.org/10.33011/livecoms.6.1.4545
- modXNA fragment catalog: https://modxna.chpc.utah.edu/catalog/
- Experimental template 2KP4: https://www.rcsb.org/structure/2KP4
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")


def audit_fana_physical_readiness(
    candidate_pdb: str | Path,
    template_pdb: str | Path,
    report_md: str | Path,
    manifest_json: str | Path,
    *,
    conect_pdb: str | Path | None = None,
    strict: bool = False,
    max_pucker_phase_delta: float = 45.0,
    max_pucker_amplitude_delta: float = 10.0,
) -> FANAReadinessResult:
    """Audit a FANA candidate and write a Level 4 parameterization handoff.

    ``strict`` raises only when the geometry gate fails. A passing geometry gate
    still returns ``PARAMETERIZATION_REQUIRED`` because this function cannot
    validate absent force-field data.
    """

    candidate_path = Path(candidate_pdb)
    template_path = Path(template_pdb)
    report_path = Path(report_md)
    manifest_path = Path(manifest_json)
    conect_path = Path(conect_pdb) if conect_pdb is not None else None

    structure = parse_pdb(candidate_path, strict=True)
    template = parse_pdb(template_path, strict=True)
    keys = sort_residue_keys(structure)
    if not keys:
        raise ValueError(f"No candidate residues found in {candidate_path}.")

    for key in keys:
        base = base_of(residue_name(structure[key]))
        if base not in BASE_BONDS:
            raise UnsupportedResidueError(
                f"Residue {_residue_label(key)} ({residue_name(structure[key])}) "
                "does not map to canonical A/U/G/C FANA chemistry."
            )

    segments = _consecutive_segments(keys)
    five_prime_keys = {segment[0] for segment in segments}

    template_references = _template_references(template)
    bonds: list[CovalentBond] = []
    distances: list[float] = []
    missing_atoms: list[dict[str, str]] = []
    distance_failures: list[BondDistanceFailure] = []

    for key in keys:
        residue = structure[key]
        base = base_of(residue_name(residue))
        neutral_five_prime = (
            key in five_prime_keys
            and not FIVE_PRIME_PHOSPHATE_ATOMS.intersection(residue)
        )
        for rule in BACKBONE_RULES:
            if neutral_five_prime and FIVE_PRIME_PHOSPHATE_ATOMS.intersection(
                (rule.left, rule.right)
            ):
                continue
            _add_bond_observation(
                structure=structure,
                left_key=key,
                right_key=key,
                rule=rule,
                bonds=bonds,
                distances=distances,
                missing_atoms=missing_atoms,
                failures=distance_failures,
            )
        attachment_rule = BondRule(
            "C1'", glycosidic_atom(base), 1.20, 1.80, "glycosidic_attachment"
        )
        _add_bond_observation(
            structure=structure,
            left_key=key,
            right_key=key,
            rule=attachment_rule,
            bonds=bonds,
            distances=distances,
            missing_atoms=missing_atoms,
            failures=distance_failures,
        )
        for left, right in BASE_BONDS[base]:
            _add_bond_observation(
                structure=structure,
                left_key=key,
                right_key=key,
                rule=BondRule(left, right, 1.10, 1.75, "nucleobase"),
                bonds=bonds,
                distances=distances,
                missing_atoms=missing_atoms,
                failures=distance_failures,
            )
        if "H2'" in residue:
            _add_bond_observation(
                structure=structure,
                left_key=key,
                right_key=key,
                rule=BondRule("C2'", "H2'", 0.80, 1.25, "explicit_hydrogen"),
                bonds=bonds,
                distances=distances,
                missing_atoms=missing_atoms,
                failures=distance_failures,
            )

    for segment in segments:
        for left_key, right_key in zip(segment, segment[1:]):
            _add_bond_observation(
                structure=structure,
                left_key=left_key,
                right_key=right_key,
                rule=BondRule("O3'", "P", 1.35, 1.95, "phosphodiester_linkage"),
                bonds=bonds,
                distances=distances,
                missing_atoms=missing_atoms,
                failures=distance_failures,
            )

    pucker_observations: list[PuckerObservation] = []
    chirality_observations: list[ChiralityObservation] = []
    for key in keys:
        residue = structure[key]
        base = base_of(residue_name(residue))
        references = template_references.get(base)
        if not references:
            raise TemplateError(
                f"The FANA template has no fluorinated reference for base {base}."
            )

        if set(RING_ATOMS).issubset(residue):
            phase, amplitude, fit_rms = _pseudorotation(residue)
            reference = min(
                references,
                key=lambda item: _circular_delta(phase, float(item["phase"])),
            )
            phase_delta = _circular_delta(phase, float(reference["phase"]))
            amplitude_delta = abs(amplitude - float(reference["amplitude"]))
            pucker_status = (
                "PASS"
                if phase_delta <= max_pucker_phase_delta
                and amplitude_delta <= max_pucker_amplitude_delta
                else "FAIL"
            )
            pucker_observations.append(
                PuckerObservation(
                    residue=_residue_label(key),
                    base=base,
                    phase_degrees=phase,
                    amplitude_degrees=amplitude,
                    fit_rms_degrees=fit_rms,
                    reference_residue=str(reference["residue"]),
                    reference_phase_degrees=float(reference["phase"]),
                    reference_amplitude_degrees=float(reference["amplitude"]),
                    phase_delta_degrees=phase_delta,
                    amplitude_delta_degrees=amplitude_delta,
                    status=pucker_status,
                )
            )

        fluorine_name = _find_fluorine(residue)
        if fluorine_name is not None and {"C1'", "C2'", "C3'"}.issubset(residue):
            signed_volume = _signed_c2_volume(residue, fluorine_name)
            observed_sign = _sign(signed_volume)
            reference_signs = [int(item["chirality_sign"]) for item in references]
            reference_sign = max(set(reference_signs), key=reference_signs.count)
            chirality_observations.append(
                ChiralityObservation(
                    residue=_residue_label(key),
                    base=base,
                    signed_volume=signed_volume,
                    observed_sign=observed_sign,
                    reference_sign=reference_sign,
                    status=(
                        "PASS"
                        if observed_sign != 0 and observed_sign == reference_sign
                        else "FAIL"
                    ),
                )
            )

    missing_pucker = len(pucker_observations) != len(keys)
    missing_chirality = len(chirality_observations) != len(keys)
    failed_puckers = any(item.status != "PASS" for item in pucker_observations)
    failed_chirality = any(item.status != "PASS" for item in chirality_observations)
    geometry_ok = not (
        missing_atoms
        or distance_failures
        or missing_pucker
        or missing_chirality
        or failed_puckers
        or failed_chirality
    )
    geometry_status = "PASS" if geometry_ok else "FAIL"
    status = "PARAMETERIZATION_REQUIRED" if geometry_ok else "GEOMETRY_GATE_FAILED"

    unique_bonds = deduplicate_bonds(bonds)
    hydrogen_count = sum(
        is_hydrogen(atom) for key in keys for atom in structure[key].values()
    )
    parameterization_blockers = [
        "Complete hydrogen placement and protonation states are not verified.",
        "Force-field atom types are not assigned.",
        "Partial atomic charges are not assigned.",
        "Bonded and nonbonded parameters are not assigned or versioned.",
        "5′/3′ terminal protonation or capping states are unresolved for every chain segment.",
        "PDB residue names are not mapped to validated force-field residue templates.",
    ]

    result = FANAReadinessResult(
        status=status,
        geometry_status=geometry_status,
        residue_count=len(keys),
        bond_count=len(unique_bonds),
        report_path=report_path,
        manifest_path=manifest_path,
        conect_pdb_path=conect_path,
        missing_atoms=missing_atoms,
        distance_failures=distance_failures,
        pucker_observations=pucker_observations,
        chirality_observations=chirality_observations,
        parameterization_blockers=parameterization_blockers,
    )

    if conect_path is not None:
        conect_path.parent.mkdir(parents=True, exist_ok=True)
        write_pdb(
            structure,
            conect_path,
            preferred_atom_order=PREFERRED_ATOM_ORDER,
            conect_records=format_conect_records(
                structure,
                unique_bonds,
                preferred_atom_order=PREFERRED_ATOM_ORDER,
            ),
            remarks=(
                "Digital Polymerase FANA Level 4 readiness handoff",
                "CONECT records encode observed covalent connectivity, not bond orders",
                "WARNING: parameters, charges, terminal states, and hydrogens remain unresolved",
            ),
        )

    terminal_segments = [
        {
            "first_residue": _residue_label(segment[0]),
            "last_residue": _residue_label(segment[-1]),
            "residue_count": len(segment),
            "five_prime_phosphorus_present": "P" in structure[segment[0]],
            "three_prime_oxygen_present": "O3'" in structure[segment[-1]],
            "terminal_state": "UNRESOLVED",
        }
        for segment in segments
    ]
    observed_names = sorted({residue_name(structure[key]) for key in keys})
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "target": TARGET,
        "stage": "level4_physical_readiness_gate",
        "status": status,
        "candidate": {
            "path": str(candidate_path),
            "sha256": _file_sha256(candidate_path),
            "residue_count": len(keys),
            "observed_residue_names": observed_names,
            "explicit_hydrogen_count": hydrogen_count,
        },
        "template": {
            "path": str(template_path),
            "sha256": _file_sha256(template_path),
            "reference": "RCSB PDB 2KP4 when the repository template is used",
        },
        "geometry_gate": {
            "status": geometry_status,
            "covalent_bond_count": len(unique_bonds),
            "bond_distances_measured": len(distances),
            "bond_distance_mean": float(np.mean(distances)) if distances else None,
            "bond_distance_minimum": float(np.min(distances)) if distances else None,
            "bond_distance_maximum": float(np.max(distances)) if distances else None,
            "missing_atoms": missing_atoms,
            "distance_failures": [asdict(item) for item in distance_failures],
            "chirality": [asdict(item) for item in chirality_observations],
            "sugar_pucker": [asdict(item) for item in pucker_observations],
        },
        "topology_handoff": {
            "conect_pdb": str(conect_path) if conect_path is not None else None,
            "conect_scope": "observed covalent connectivity without bond orders",
            "chain_segments": terminal_segments,
        },
        "parameterization": {
            "status": "REQUIRED",
            "md_ready": False,
            "blockers": parameterization_blockers,
            "suggested_route": {
                "tool": "modXNA",
                "engine_family": "Amber",
                "catalog_sugar_linker_fragment": "A5L",
                "catalog_description": "2′FANA, built C2′-endo",
                "expert_selection_required": True,
                "note": (
                    "A5L is a fragment catalog match, not a complete or automatically "
                    "validated residue parameter set for this candidate."
                ),
            },
            "references": [
                "https://doi.org/10.1021/acs.jctc.4c01164",
                "https://doi.org/10.33011/livecoms.6.1.4545",
                "https://modxna.chpc.utah.edu/catalog/",
                "https://www.rcsb.org/structure/2KP4",
            ],
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    distance_mean = float(np.mean(distances)) if distances else float("nan")
    distance_minimum = float(np.min(distances)) if distances else float("nan")
    distance_maximum = float(np.max(distances)) if distances else float("nan")
    _write_report(
        path=report_path,
        candidate_path=candidate_path,
        template_path=template_path,
        result=result,
        distance_count=len(distances),
        distance_mean=distance_mean,
        distance_minimum=distance_minimum,
        distance_maximum=distance_maximum,
        segment_count=len(segments),
        hydrogen_count=hydrogen_count,
    )

    if strict and not geometry_ok:
        raise ValidationError(
            "FANA Level 4 geometry gate failed; inspect the readiness report and manifest."
        )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a FANA candidate for topology, stereochemistry, sugar pucker, "
            "and external parameterization readiness."
        )
    )
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--conect-output", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--max-pucker-phase-delta", type=float, default=45.0)
    parser.add_argument("--max-pucker-amplitude-delta", type=float, default=10.0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = audit_fana_physical_readiness(
        args.candidate,
        args.template,
        args.report,
        args.manifest,
        conect_pdb=args.conect_output,
        strict=args.strict,
        max_pucker_phase_delta=args.max_pucker_phase_delta,
        max_pucker_amplitude_delta=args.max_pucker_amplitude_delta,
    )
    print(
        f"FANA physical-readiness gate {result.geometry_status}: "
        f"{result.residue_count} residues, {result.bond_count} bonds; "
        f"overall status {result.status}"
    )
    return 0 if result.geometry_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
