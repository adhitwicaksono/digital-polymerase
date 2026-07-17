# Digital Polymerase Converters

`converters/` is the semi-stable user-facing layer of Digital Polymerase.

This folder should contain cleaner converter wrappers that call the reusable
`digital_polymerase.core` engine.

## Relationship between folders

```text
prototypes/  = experimental battlefield scripts
core/        = reusable engine components
converters/  = stable or semi-stable user-facing wrappers
```

Prototype scripts should **not** be deleted after promotion. They remain useful
as historical benchmarks, failure records, and regression references.

## Current status

The converter layer now contains the first promoted stable candidate:

```text
converters/
├── README.md
├── __init__.py
├── base.py
└── rna_to_fana.py
```

`rna_to_fana.py` promotes Prototype 003A into a reusable Python API and CLI.

## First stable-candidate converter

First stable-candidate converter:

```text
RNA → FANA
```

Why FANA first?

- It is chain-preserving.
- It has a clear local target marker: `C2′→F2′`.
- It has already been benchmarked from 8 nt to 111 nt.
- It is less structurally unusual than TNA, GNA, or PNA.
- It is a good pilot for refactoring prototype logic into the shared core engine.

Module:

```text
converters/rna_to_fana.py
```

Public function:

```python
convert_rna_to_fana(
    input_pdb,
    template_pdb,
    output_pdb,
    report_md,
    metrics_json=None,
)
```

CLI:

```bash
digital-polymerase-fana \
  --rna input_rna.pdb \
  --template fana_template.pdb \
  --output candidate_fana.pdb \
  --report conversion_report.md \
  --metrics validation.json \
  --strict
```

## Promotion criteria

A prototype should only move into `converters/` after it has:

1. explicit input/output paths
2. no hardcoded local paths
3. standardized CLI and/or Python API
4. standardized PDB, Markdown report, and optional JSON metrics outputs
5. target-specific validation through `core.validation`
6. registry-aware target grammar through `core.registry`
7. clear failure behavior
8. benchmark regression tests
9. documented limitations
10. visual sanity on 8-mer and 34-mer benchmarks

## Recommended promotion order

```text
v0.1 candidate: RNA → FANA
v0.2 candidates: RNA → ANA, RNA → HNA
v0.3 candidates: RNA → XyNA, RNA → CeNA
v0.4 experimental-stable candidates: RNA → TNA, RNA → GNA
PNA: separate special module for template-primary and sequence-primary generation
```

## Design principle

A converter should not merely write a PDB.

It should:

```text
parse → reconstruct → validate → report → fail clearly when needed
```

All outputs remain computational candidate structures unless validated by
downstream stereochemical inspection, minimization, molecular dynamics, force
field/topology checks, and expert chemical review.
