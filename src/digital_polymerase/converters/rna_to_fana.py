"""Stable-candidate chain-preserving RNA to FANA reconstruction.

This module promotes the geometry-transfer logic from Prototype 003A into the
reusable converter layer. It preserves the source RNA chain and nucleobases,
removes the ribose 2'-oxygen, and introduces template-derived FANA C2'/F2'
coordinates. Outputs are computational candidates, not physically refined or
experimentally validated FANA structures.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from digital_polymerase.core.atoms import Atom, ResidueKey, clone_atom
from digital_polymerase.core.errors import (
    TemplateError,
    UnsupportedResidueError,
    ValidationError,
)
from digital_polymerase.core.geometry import apply_transform, distance, kabsch
from digital_polymerase.core.pdb_io import (
    Residue,
    Structure,
    parse_pdb,
    residue_name,
    sort_residue_keys,
    write_pdb,
)
from digital_polymerase.core.reporting import (
    write_basic_report,
    write_conversion_metrics,
)
from digital_polymerase.core.residues import (
    residue_base,
    source_sequence,
    split_base_backbone_atoms,
)
from digital_polymerase.core.templates import (
    build_template_index,
    select_template_by_base,
)
from digital_polymerase.core.validation import DistanceSummary, validate_target_geometry

from .base import ConversionResult, ConverterConfig, ConverterPaths, ensure_output_dirs


TARGET = "FANA"
STRATEGY = "chain_preserving"
DEFAULT_ANCHORS = ("C1'", "C3'", "C4'", "O4'")

CHAIN_PRESERVE_ATOMS = {
    "P",
    "OP1",
    "OP2",
    "O1P",
    "O2P",
    "O5'",
    "C5'",
    "C4'",
    "O4'",
    "C3'",
    "O3'",
    "C1'",
}

PREFERRED_ATOM_ORDER = [
    "P",
    "OP1",
    "OP2",
    "O1P",
    "O2P",
    "O5'",
    "C5'",
    "C4'",
    "O4'",
    "C3'",
    "O3'",
    "C2'",
    "F2'",
    "H2'",
    "C1'",
]


@dataclass(frozen=True)
class FANAResidueRecord:
    """Trace one source residue to the selected FANA geometry donor."""

    source_key: ResidueKey
    source_base: str
    target_res_name: str
    template_key: ResidueKey
    template_res_name: str
    anchor_atoms: tuple[str, ...]
    anchor_rmsd: float
    c2f_distance: float
    template_note: str


def _find_fluorine(residue: Mapping[str, Atom]) -> str | None:
    for name in ("F2'", "F", "2F", "F2*"):
        if name in residue:
            return name
    for name, atom in residue.items():
        if name.upper().startswith("F") or atom.element.upper() == "F":
            return name
    return None


def _target_residue_name(base: str, naming_policy: str) -> str:
    policies = {
        "template-observed": {"A": "A5L", "U": "UFL", "G": "GFL", "C": "CFL"},
        "provisional": {"A": "AFL", "U": "UFL", "G": "GFL", "C": "CFL"},
    }
    if naming_policy not in policies:
        raise ValueError(f"Unsupported FANA naming policy: {naming_policy!r}")
    try:
        return policies[naming_policy][base]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported source base for RNA to FANA conversion: {base!r}"
        ) from exc


def _build_fana_template_index(template: Structure, anchors: Sequence[str]):
    required = list(dict.fromkeys([*anchors, "C2'"]))
    index = build_template_index(template, required_atoms=required)
    filtered = {
        base: [key for key in keys if _find_fluorine(template[key]) is not None]
        for base, keys in index.items()
    }
    filtered = {base: keys for base, keys in filtered.items() if keys}
    if not filtered:
        raise TemplateError(
            "The FANA template has no residue containing at least three alignment "
            "anchors, C2', and a fluorine atom."
        )
    return filtered


def _convert_residue(
    *,
    source_key: ResidueKey,
    source_residue: Residue,
    template_key: ResidueKey,
    template_residue: Residue,
    anchors: Sequence[str],
    target_res_name: str,
    template_note: str,
) -> tuple[Residue, FANAResidueRecord]:
    available = tuple(
        name for name in anchors if name in source_residue and name in template_residue
    )
    if len(available) < 3:
        raise TemplateError(
            f"Residue {source_key!r} and donor {template_key!r} share fewer than "
            f"three alignment anchors: {available!r}"
        )

    mobile = np.asarray([template_residue[name].coords for name in available])
    target = np.asarray([source_residue[name].coords for name in available])
    rotation, translation, anchor_rmsd = kabsch(mobile, target)

    chain, res_num, insertion_code = source_key
    output: Residue = {}
    source_base_atoms, source_backbone_atoms = split_base_backbone_atoms(source_residue)

    for atom_name, atom in source_backbone_atoms.items():
        if atom_name in CHAIN_PRESERVE_ATOMS:
            output[atom_name] = clone_atom(
                atom,
                record="HETATM",
                res_name=target_res_name,
                chain=chain,
                res_num=res_num,
                insertion_code=insertion_code,
            )

    for atom_name, atom in source_base_atoms.items():
        output[atom_name] = clone_atom(
            atom,
            record="HETATM",
            res_name=target_res_name,
            chain=chain,
            res_num=res_num,
            insertion_code=insertion_code,
        )

    if "C2'" not in template_residue:
        raise TemplateError(f"FANA donor {template_key!r} lacks C2'.")
    fluorine_name = _find_fluorine(template_residue)
    if fluorine_name is None:
        raise TemplateError(f"FANA donor {template_key!r} lacks fluorine.")

    c2 = template_residue["C2'"]
    output["C2'"] = clone_atom(
        c2,
        coords=apply_transform(c2.coords, rotation, translation),
        atom_name="C2'",
        record="HETATM",
        res_name=target_res_name,
        chain=chain,
        res_num=res_num,
        insertion_code=insertion_code,
        element="C",
    )

    fluorine = template_residue[fluorine_name]
    output["F2'"] = clone_atom(
        fluorine,
        coords=apply_transform(fluorine.coords, rotation, translation),
        atom_name="F2'",
        record="HETATM",
        res_name=target_res_name,
        chain=chain,
        res_num=res_num,
        insertion_code=insertion_code,
        element="F",
    )

    if "H2'" in template_residue:
        hydrogen = template_residue["H2'"]
        output["H2'"] = clone_atom(
            hydrogen,
            coords=apply_transform(hydrogen.coords, rotation, translation),
            atom_name="H2'",
            record="HETATM",
            res_name=target_res_name,
            chain=chain,
            res_num=res_num,
            insertion_code=insertion_code,
            element="H",
        )

    record = FANAResidueRecord(
        source_key=source_key,
        source_base=residue_base(source_residue),
        target_res_name=target_res_name,
        template_key=template_key,
        template_res_name=residue_name(template_residue),
        anchor_atoms=available,
        anchor_rmsd=anchor_rmsd,
        c2f_distance=distance(output["C2'"].coords, output["F2'"].coords),
        template_note=template_note,
    )
    return output, record


def _validation_status(value: Any) -> str:
    if isinstance(value, DistanceSummary):
        return value.status
    if isinstance(value, dict):
        return str(value.get("status", "UNKNOWN"))
    return "UNKNOWN"


def _failed_checks(validation: Mapping[str, Any]) -> list[str]:
    return [
        name
        for name, value in validation.items()
        if _validation_status(value) != "PASS"
    ]


def _validate_source_residues(
    source: Structure, source_keys: Sequence[ResidueKey]
) -> None:
    recognized = set(source_keys)
    unknown_nucleic_acid = []
    for key, residue in source.items():
        looks_like_nucleic_acid = {"C1'", "C3'", "C4'"}.issubset(residue) and (
            "N1" in residue or "N9" in residue
        )
        if looks_like_nucleic_acid and key not in recognized:
            unknown_nucleic_acid.append((key, residue_name(residue)))
    if unknown_nucleic_acid:
        labels = ", ".join(
            f"{key[0]}{key[1]}{key[2]} ({name})" for key, name in unknown_nucleic_acid
        )
        raise UnsupportedResidueError(
            "Unrecognized nucleic-acid-like residues would be dropped: " + labels
        )


def _convert_with_paths(
    paths: ConverterPaths,
    config: ConverterConfig,
    *,
    anchors: Sequence[str],
    naming_policy: str,
) -> ConversionResult:
    if paths.template_pdb is None:
        raise ValueError("RNA to FANA conversion requires a FANA template PDB.")
    if len(anchors) < 3:
        raise ValueError("At least three alignment anchors are required.")

    source = parse_pdb(paths.input_pdb, strict=True)
    template = parse_pdb(paths.template_pdb, strict=True)
    source_keys = [
        key
        for key in sort_residue_keys(source)
        if residue_name(source[key]).upper().strip() in {"A", "U", "G", "C"}
    ]
    if not source_keys:
        raise ValueError(f"No canonical RNA residues found in {paths.input_pdb}.")
    _validate_source_residues(source, source_keys)
    if not template:
        raise TemplateError(f"No template residues found in {paths.template_pdb}.")

    template_index = _build_fana_template_index(template, anchors)
    output: Structure = {}
    records: list[FANAResidueRecord] = []

    for source_key in source_keys:
        source_residue = source[source_key]
        base = residue_base(source_residue)
        # Prototype 003A always used the first matching donor for a base class.
        # Preserve that choice so the promoted converter is a true regression
        # of the benchmarked geometry rather than a new donor-cycling method.
        template_key, note = select_template_by_base(base, template_index)
        target_name = _target_residue_name(base, naming_policy)
        converted, record = _convert_residue(
            source_key=source_key,
            source_residue=source_residue,
            template_key=template_key,
            template_residue=template[template_key],
            anchors=anchors,
            target_res_name=target_name,
            template_note=note,
        )
        output[source_key] = converted
        records.append(record)

    sequence = source_sequence(source)
    ensure_output_dirs(paths)
    write_pdb(
        output,
        paths.output_pdb,
        preferred_atom_order=PREFERRED_ATOM_ORDER,
        remarks=(
            "Digital Polymerase stable-candidate RNA to FANA converter",
            f"Source RNA sequence: {sequence}",
            "Method: preserve RNA chain/base geometry; introduce FANA C2'/F2' geometry",
            "WARNING: computational candidate; not physically or experimentally validated",
        ),
    )

    validation = validate_target_geometry(output, TARGET)
    failures = _failed_checks(validation)
    status = "success" if not failures else "partial"
    messages = [
        "The output is a geometric candidate and is not MD-ready without topology, "
        "parameter, stereochemical, and minimization checks."
    ]
    if failures:
        messages.append("Validation did not pass: " + ", ".join(failures))

    rmsds = [record.anchor_rmsd for record in records]
    c2f_distances = [record.c2f_distance for record in records]
    metadata = {
        "converter": "rna_to_fana",
        "version": "0.1.0",
        "naming_policy": naming_policy,
        "anchors": list(anchors),
        "mean_anchor_rmsd": float(np.mean(rmsds)),
        "max_anchor_rmsd": float(np.max(rmsds)),
        "mean_c2f_distance": float(np.mean(c2f_distances)),
        "max_c2f_distance": float(np.max(c2f_distances)),
        "residue_records": [asdict(record) for record in records],
    }

    report_notes = [
        *config.notes,
        f"Converted {len(records)} RNA residues using {len(template_index)} base-class donor groups.",
        f"Mean anchor RMSD: {metadata['mean_anchor_rmsd']:.4f} A; maximum: {metadata['max_anchor_rmsd']:.4f} A.",
        f"Mean C2'-F2' distance: {metadata['mean_c2f_distance']:.4f} A.",
        *messages,
    ]
    write_basic_report(
        path=paths.report_md,
        title="RNA to FANA Chain-Preserving Conversion Report",
        target=TARGET,
        method=STRATEGY,
        input_file=paths.input_pdb,
        template_file=paths.template_pdb,
        output_file=paths.output_pdb,
        sequence=sequence,
        validation_results=validation,
        notes=report_notes,
    )
    if config.write_json and paths.metrics_json is not None:
        write_conversion_metrics(
            results=validation,
            path=paths.metrics_json,
            metadata={
                "target": TARGET,
                "strategy": STRATEGY,
                "status": status,
                "sequence": sequence,
                "residue_count": len(records),
                "metrics": {
                    key: value
                    for key, value in metadata.items()
                    if key
                    in {
                        "mean_anchor_rmsd",
                        "max_anchor_rmsd",
                        "mean_c2f_distance",
                        "max_c2f_distance",
                    }
                },
                "residue_records": metadata["residue_records"],
            },
        )

    result = ConversionResult(
        target=TARGET,
        strategy=STRATEGY,
        status=status,
        sequence=sequence,
        residue_count=len(records),
        paths=paths,
        validation=validation,
        messages=messages,
        metadata=metadata,
    )
    if config.strict and failures:
        raise ValidationError("RNA to FANA validation failed: " + ", ".join(failures))
    return result


def convert_rna_to_fana(
    input_pdb: str | Path,
    template_pdb: str | Path,
    output_pdb: str | Path,
    report_md: str | Path,
    metrics_json: str | Path | None = None,
    *,
    strict: bool = False,
    anchors: Sequence[str] = DEFAULT_ANCHORS,
    naming_policy: str = "template-observed",
) -> ConversionResult:
    """Generate and validate a chain-preserving FANA-like candidate.

    The source sequence, RNA chain geometry, and nucleobase coordinates are
    preserved. FANA C2'/F2' local coordinates are transferred from a structural
    donor by local Kabsch alignment.
    """

    paths = ConverterPaths.from_strings(
        input_pdb=input_pdb,
        template_pdb=template_pdb,
        output_pdb=output_pdb,
        report_md=report_md,
        metrics_json=metrics_json,
    )
    config = ConverterConfig(
        target=TARGET,
        strategy=STRATEGY,
        strict=strict,
        write_json=metrics_json is not None,
    )
    return _convert_with_paths(
        paths,
        config,
        anchors=tuple(anchors),
        naming_policy=naming_policy,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a chain-preserving RNA to FANA computational candidate."
    )
    parser.add_argument("--rna", required=True, type=Path, help="Source RNA PDB")
    parser.add_argument("--template", required=True, type=Path, help="FANA donor PDB")
    parser.add_argument(
        "--output", required=True, type=Path, help="Output candidate PDB"
    )
    parser.add_argument("--report", required=True, type=Path, help="Markdown report")
    parser.add_argument("--metrics", type=Path, help="Optional JSON validation metrics")
    parser.add_argument(
        "--strict", action="store_true", help="Raise on validation failure"
    )
    parser.add_argument(
        "--anchors",
        nargs="+",
        default=list(DEFAULT_ANCHORS),
        help="At least three atom names used for local alignment",
    )
    parser.add_argument(
        "--naming-policy",
        choices=("template-observed", "provisional"),
        default="template-observed",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = convert_rna_to_fana(
        args.rna,
        args.template,
        args.output,
        args.report,
        args.metrics,
        strict=args.strict,
        anchors=args.anchors,
        naming_policy=args.naming_policy,
    )
    print(
        f"{result.target} conversion {result.status}: "
        f"{result.residue_count} residues written to {result.paths.output_pdb}"
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
