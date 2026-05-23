# Prototype 008B: RNA → PNA Template-Primary Base Replacement

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype:** 008B  
**Conversion:** RNA → PNA  
**Method:** Template-primary PNA scaffold with RNA-sequence base replacement  
**Status:** Successful scalable candidate generator; not physically validated

---

## Summary

Prototype 008B is the successful Digital Polymerase prototype for generating PNA-like candidate structures from RNA PDB inputs.

PNA, or peptide nucleic acid, is fundamentally different from the earlier XNA targets. It does not use a sugar-phosphate backbone. Instead, it uses a pseudopeptide backbone with nucleobases attached as side-chain-like groups.

Prototype 008A.1 attempted to force a PNA pseudopeptide backbone onto an RNA fold and produced a tangled 8-mer. Prototype 008B fixes this by reversing the conversion philosophy:

```text
PNA scaffold first
RNA sequence/base identity second
```

This means Prototype 008B does not preserve the RNA 3D fold. It generates a clean PNA-like molecule carrying the same base sequence.

---

## Current Script

Recommended path:

```text
src/digital_polymerase/prototypes/rna_to_pna_template_primary.py
```

Example command:

```bash
python src/digital_polymerase/prototypes/rna_to_pna_template_primary.py \
  --rna benchmarks/pna_scaling/inputs/RNA-34mer.pdb \
  --template benchmarks/pna_scaling/templates/3mbs_PNA-1mer-8.pdb \
  --output benchmarks/pna_scaling/outputs/converted_pna_RNA-34mer_template_primary_008B.pdb \
  --report benchmarks/pna_scaling/reports/conversion_report_RNA-34mer_template_primary_008B.md
```

---

## Template Used

Primary template:

```text
3mbs_PNA-1mer-8.pdb
```

Observed PNA-like residues:

```text
APN
TPN
GPN
CPN
```

Important PNA scaffold atoms:

```text
C8'
C7'
O7'
N4'
C3'
C2'
N1'
C5'
C'
O1'
```

Observed PNA-like linkage:

```text
C′(i) → N1′(i+1)
```

Observed base attachment:

```text
C8′ → glycosidic N
```

---

## Why Prototype 008B Was Needed

Prototype 008A.1 attempted:

```text
RNA fold → force PNA backbone onto it
```

This failed because PNA is too chemically different from RNA. The 8-mer output became severely tangled.

Prototype 008B instead attempts:

```text
PNA scaffold → replace bases by RNA sequence
```

This approach produced a clean 8-mer and scaled to 34-mer and 111-mer outputs.

---

## Method

For each source RNA residue, Prototype 008B:

1. reads RNA base identity from the source PDB
2. preserves or tiles the PNA template scaffold
3. selects a PNA base donor by target base identity
4. transforms donor base atoms onto the selected scaffold residue
5. removes thymine `C5M` when using T-like donor for RNA U
6. assigns output PNA-like residue names
7. validates PNA chain continuity
8. validates base attachment
9. audits expected base oxygen atoms
10. writes a PNA-like candidate PDB and Markdown report

---

## What Prototype 008B Preserves

Prototype 008B preserves:

```text
RNA base sequence
PNA-like scaffold grammar
PNA-like base attachment
PNA-like C′→N1′ chain continuity
```

Prototype 008B does **not** preserve:

```text
RNA tertiary fold
RNA sugar-phosphate geometry
RNA local backbone orientation
RNA-style cartoon/ribbon identity
```

This is intentional.

---

## Example Usage

### 8-mer test

```bash
python src/digital_polymerase/prototypes/rna_to_pna_template_primary.py \
  --rna benchmarks/pna_scaling/inputs/RNA-8mer.pdb \
  --template benchmarks/pna_scaling/templates/3mbs_PNA-1mer-8.pdb \
  --output benchmarks/pna_scaling/outputs/converted_pna_RNA-8mer_template_primary_008B.pdb \
  --report benchmarks/pna_scaling/reports/conversion_report_RNA-8mer_template_primary_008B.md
```

### 111-mer test

```bash
python src/digital_polymerase/prototypes/rna_to_pna_template_primary.py \
  --rna benchmarks/pna_scaling/inputs/8t5o-HH-typeI-111mer-full.pdb \
  --template benchmarks/pna_scaling/templates/3mbs_PNA-1mer-8.pdb \
  --output benchmarks/pna_scaling/outputs/converted_pna_8t5o-HH-typeI-111mer-full_template_primary_008B.pdb \
  --report benchmarks/pna_scaling/reports/conversion_report_8t5o-HH-typeI-111mer-full_template_primary_008B.md
```

---

## Benchmark Results

Prototype 008B was tested on six RNA inputs.

| Input | Residues | C′→N1′ next | C8′→gly N | Backbone C8′→C7′ | C7′→N4′ | C′→O1′ | Base oxygen audit | Mean C8′→N / C′→N1′ next (Å) | Missing base oxygens |
|---|---:|---|---|---|---|---|---|---:|---:|
| `RNA-8mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-12mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-16mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-22mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-34mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `HH-111mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |

All tested outputs passed the main report-level validation checks.

---

## Validation Metrics

Prototype 008B reports:

- converted residue count
- source RNA sequence
- PNA template sequence
- PNA `C′(i)→N1′(i+1)` chain continuity
- `C8′→glycosidic N` base attachment
- PNA backbone geometry checks
- expected base oxygen audit
- per-residue scaffold template and base donor
- tile index

---

## Visual Inspection

The following outputs were inspected visually:

```text
converted_pna_RNA-8mer_template_primary_008B.pdb
converted_pna_RNA-34mer_template_primary_008B.pdb
converted_pna_8t5o-HH-typeI-111mer-full_template_primary_008B.pdb
```

Observed:

```text
8-mer  → clean and coherent PNA-like molecule
34-mer → elongated, continuous PNA-like strand
111-mer → long clean sequence-preserving PNA-like chain
```

The 111-mer does not resemble the hammerhead ribozyme tertiary fold. This is expected and correct for Prototype 008B.

---

## Scientific Interpretation

Correct description:

```text
PNA-like candidate structures generated through template-primary base replacement.
```

Incorrect descriptions:

```text
validated PNA structures
experimentally confirmed PNA ribozymes
MD-ready PNA polymers
RNA-fold-preserving PNA analogs
proof of PNA biological function
```

The outputs are computational candidates only.

---

## Known Limitations

- Does not preserve RNA 3D fold.
- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- PNA stereochemistry requires expert inspection.
- Long outputs are tiled/scaffold-primary candidates.
- Molecular viewers may not recognize the output as a canonical nucleic-acid polymer.
- Biological function, stability, binding, or catalytic activity is not implied.

---

## Relationship to Other XNA Prototypes

Current working candidate-generation families:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
XyNA  → Prototype 005A
TNA   → Prototype 006B.4
GNA   → Prototype 007A
PNA   → Prototype 008B
```

Prototype 008B establishes a new Digital Polymerase strategy class:

```text
template-primary scaffold-first sequence remapping
```

This class is distinct from:

```text
fold-preserving conversion
chain-preserving conversion
linkage-remapped conversion
```

---

## Recommended Repository Placement

```text
src/digital_polymerase/prototypes/rna_to_pna_template_primary.py
docs/prototype_008B_rna_to_pna_template_primary.md
benchmarks/pna_scaling/
```

---

## Recommended Future Work

Future PNA development should add:

```text
template tiling controls
PNA stereochemistry checks
optional helical PNA scaffold generation
clash scoring
force-field/topology notes
PNA-specific residue naming options
CONECT/topology export
```

A possible future Prototype 008C could explore:

```text
PNA scaffold generation from sequence without relying on a finite template
```

or:

```text
template-primary PNA with controllable helical pitch and rise
```

---

## Current Status

Prototype 008B is a successful scalable PNA-like candidate generator.

It should remain under:

```text
src/digital_polymerase/prototypes/
```

until the project adds shared infrastructure and validation layers.

---

## Final Note

Prototype 008B marks the point where PNA joins the Digital Polymerase working prototype roster.

The chimaera was not defeated by forcing it into RNA shape. It was defeated by letting it remain PNA.
