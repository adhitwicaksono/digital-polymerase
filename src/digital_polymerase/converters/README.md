# Digital Polymerase Converters

This directory is reserved for **stable or semi-stable converter modules** in Digital Polymerase.

At the current development stage, most RNA → XNA scripts should remain in:

```text
src/digital_polymerase/prototypes/
```

until they have passed basic validation, documentation, and reproducibility checks.

---

## Purpose

The `converters/` directory will eventually contain reusable conversion modules for transforming nucleic acid structures between canonical nucleic acids and XNA-like chemistries.

Examples of future supported directions include:

```text
RNA → HNA
RNA → ANA
RNA → FANA
RNA → TNA
RNA → CeNA
RNA → GNA
DNA/RNA → XNA
XNA → XNA
```

A file should only be promoted here when it is no longer just a one-off prototype.

---

## Current Policy

Prototype scripts should **not** be placed here yet if they are:

- experimental
- chemically incomplete
- missing validation reports
- hardcoded for a single example
- not chain-aware
- not tested on multiple inputs
- not documented with limitations

For example, the following currently belong under `prototypes/`:

```text
src/digital_polymerase/prototypes/rna_to_hna_template_based.py
src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py
```

---

## Promotion Criteria

A prototype can be promoted into `converters/` when it satisfies most of the following:

### 1. Reusable interface

The script or module should support command-line arguments or callable functions.

Minimum CLI requirements:

```text
--source / --rna
--template
--output
--report
--base-policy
```

### 2. No hardcoded paths

The converter should not depend on local machine paths, temporary upload folders, or project-specific absolute paths.

### 3. Explicit method classification

The converter should clearly state whether it performs:

```text
symbolic conversion
topological conversion
template-guided reconstruction
fragment-guided reconstruction
chain-aware reconstruction
```

### 4. Scientific warning

Outputs must clearly state that generated structures are computational candidates unless physically validated.

Recommended warning:

```text
This output is a computational candidate structure.
It is not energy-minimized, force-field-validated, experimentally verified, or proof of biological function.
```

### 5. Validation metrics

At minimum, reports should include:

- converted residue count
- source sequence
- template usage
- local alignment RMSD
- missing atoms
- residue completeness
- inter-residue chain-continuity checks
- warnings and limitations

### 6. Chain-continuity awareness

For polymeric structures, the converter should check relevant inter-residue connectivity, such as:

```text
O3′(i) → P(i+1)
P(i) → O5′(i)
```

Residue-local alignment alone is not sufficient.

### 7. Documentation

Each converter should have corresponding documentation in:

```text
docs/
examples/
benchmarks/
```

---

## Planned Converter Families

### Full-template reconstruction

Used when source and target structures have comparable residue count and geometry.

Example:

```text
RNA 8-mer + HNA 8-mer template → HNA-like candidate 8-mer
```

This is represented by Prototype 001.

### Fragment-guided reconstruction

Used when the available XNA template is shorter than the source structure.

Example:

```text
RNA 8-mer / 12-mer / 34-mer + ANA 4-mer template → ANA-like candidate
```

This is represented by Prototype 002A.

### Chain-aware fragment reconstruction

Future method.

Instead of transforming residues independently, the converter should preserve or reconstruct inter-residue connectivity using connected fragments and/or overlapping windows.

### De novo / idealized XNA building

Future method.

This would build XNA structures from sequence and polymer definitions rather than from full experimental templates.

This is not yet implemented.

---

## Suggested Future Layout

```text
converters/
├── README.md
├── base.py
├── template_guided.py
├── fragment_guided.py
├── chain_validator.py
├── rna_to_hna.py
├── rna_to_ana.py
└── registry.py
```

---

## Relationship to Prototypes

`prototypes/` is where exploratory scripts live.

`converters/` is where reusable converter logic should live.

The recommended flow is:

```text
prototype script
↓
documented benchmark
↓
validation metrics
↓
refactor shared logic into core/
↓
promote stable logic into converters/
```

---

## Current Status

No converter in this directory should be considered production-ready yet.

Digital Polymerase is currently building and testing the foundation through:

```text
Prototype 001: RNA → HNA template-guided reconstruction
Benchmark 002: HH ribozyme RNA → HNA failure / stress-test benchmark
Prototype 002A: RNA → ANA fragment-guided reconstruction
Benchmark 003: ANA fragment-guided scaling benchmark
```

The next major requirement before promotion is:

```text
chain-continuity validation
```

---

## Development Reminder

Do not promote a converter only because it produces a PDB.

A Digital Polymerase converter should produce:

```text
candidate structure
+
transparent method description
+
validation metrics
+
explicit limitations
```

Scientific honesty is part of the tool.
