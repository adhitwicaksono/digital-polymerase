# Prototype 006B: RNA → TNA Linkage-Optimized Reconstruction

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype:** 006B.4  
**Conversion:** RNA → TNA  
**Method:** Linkage-optimized TNA reconstruction  
**Status:** Successful scalable candidate generator; not physically validated

---

## Summary

Prototype 006B.4 is the Digital Polymerase prototype for generating TNA-like candidate structures from RNA PDB inputs.

TNA, or threose nucleic acid, required a more specialized approach than the earlier XNA targets. Unlike ANA, FANA, or XyNA, TNA cannot be handled safely by simply preserving RNA-like O3′→P chain geometry.

The core reason is that TNA uses a different linkage pattern:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
```

Prototype 006B.4 therefore performs **linkage-optimized reconstruction** rather than simple local sugar replacement.

---

## Current Script

Recommended path:

```text
src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py
```

The script generates TNA-like candidates from RNA PDB input and a TNA template:

```bash
python src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py \
  --rna benchmarks/tna_scaling/inputs/RNA-34mer.pdb \
  --template benchmarks/tna_scaling/templates/6MU5_TNA_13mer.pdb \
  --output benchmarks/tna_scaling/outputs/converted_tna_RNA-34mer_auto_006B4.pdb \
  --report benchmarks/tna_scaling/reports/conversion_report_RNA-34mer_auto_006B4.md
```

---

## Template Used

Primary template:

```text
6MU5_TNA_13mer.pdb
```

The uploaded template required atom-name normalization because some TNA atoms used TNA-specific names.

Internal normalization includes:

```text
C1T → C1′
C2T → C2′
C3T → C3′
C4T → C4′
O2T → O2′
O3T → O3′
O4T → O4′
O1P → OP1
O2P → OP2
```

Key normalized TNA atoms:

```text
P
OP1
OP2
C1'
C2'
C3'
C4'
O2'
O3'
O4'
```

---

## Why TNA Needed a New Algorithm

Earlier XNA prototypes used one of two broad strategies:

```text
full-template reconstruction
chain-preserving local scaffold reconstruction
```

These worked for HNA, ANA, FANA, CeNA, and XyNA.

TNA broke this pattern because its linkage is not RNA-like.

If the RNA chain were preserved directly, the converter would preserve:

```text
O3′(i) → P(i+1)
```

but the TNA template indicates:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
```

So TNA needed explicit linkage remapping and local optimization.

---

## Prototype Development Path

Development moved through several stages:

```text
006A   → first linkage-remapped reconstruction
006A.1 → direct O2′/O3′ bond correction
006B   → local TNA sugar optimization
006B.1 → stronger internal sugar constraints
006B.2 → improved terminal/gap-adjacent behavior
006B.3 → terminal rescue behavior
006B.4 → numbering-gap-aware next-residue handling
```

The archived working version is:

```text
Prototype 006B.4
```

---

## Method

For each source RNA residue, Prototype 006B.4:

1. parses and normalizes the TNA template
2. infers the source RNA base identity
3. selects a TNA template residue by base class or fallback logic
4. uses source RNA phosphate positions as a global chain guide
5. creates an initial TNA-like sugar placement from the template
6. locally optimizes sugar geometry using TNA-specific distance constraints
7. transforms source RNA bases onto the optimized TNA-like sugar
8. corrects C1′→glycosidic-N attachment
9. exports a TNA-like candidate PDB
10. validates TNA-specific linkages and local sugar geometry

---

## Optimization Targets

Prototype 006B.4 optimizes or checks the following geometry:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
C1′    → C2′
C2′    → C3′
C3′    → C4′
C2′    → O2′
C3′    → O3′
C1′    → glycosidic N
```

This makes the converter more suitable for TNA than a pure chain-preserving algorithm.

---

## Example Usage

### 34-mer test

```bash
python src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py \
  --rna benchmarks/tna_scaling/inputs/RNA-34mer.pdb \
  --template benchmarks/tna_scaling/templates/6MU5_TNA_13mer.pdb \
  --output benchmarks/tna_scaling/outputs/converted_tna_RNA-34mer_auto_006B4.pdb \
  --report benchmarks/tna_scaling/reports/conversion_report_RNA-34mer_auto_006B4.md
```

### 111-mer HH ribozyme-derived test

```bash
python src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py \
  --rna benchmarks/tna_scaling/inputs/8t5o-HH-typeI-111mer-full.pdb \
  --template benchmarks/tna_scaling/templates/6MU5_TNA_13mer.pdb \
  --output benchmarks/tna_scaling/outputs/converted_tna_8t5o-HH-typeI-111mer-full_auto_006B4.pdb \
  --report benchmarks/tna_scaling/reports/conversion_report_8t5o-HH-typeI-111mer-full_auto_006B4.md
```

---

## Benchmark Results

Prototype 006B.4 was tested on six RNA inputs.

| Input | Residues | O2′→P(next) | P→O3′ | Base attach | C2′→O2′ | C3′→O3′ | Segment RMSD mean/max (Å) | Base RMSD mean/max (Å) | Mean P→O3′ / O2′→P(next) (Å) |
|---|---:|---|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9191 / 1.2477 | 0.0674 / 0.0936 | 1.6026 / 1.6106 |
| `RNA-12mer` | 12 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9397 / 1.2477 | 0.0682 / 0.0922 | 1.6041 / 1.5809 |
| `RNA-16mer` | 16 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9598 / 1.2477 | 0.0724 / 0.1307 | 1.6031 / 1.5871 |
| `RNA-22mer` | 22 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9425 / 1.2907 | 0.1199 / 0.3648 | 1.6038 / 1.5794 |
| `RNA-34mer` | 34 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9575 / 1.5504 | 0.0995 / 0.3348 | 1.6026 / 1.5722 |
| `HH-111mer` | 111 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9595 / 1.3923 | 0.0987 / 0.3689 | 1.6032 / 1.5752 |

All tested outputs passed the main validation checks.

---

## Validation Metrics

Prototype 006B.4 reports:

- converted residue count
- source sequence
- template sequence
- initial segment RMSD
- base-transplant RMSD
- local optimization cost
- TNA O2′(i)→P(i+1) linkage
- TNA P(i)→O3′(i) linkage
- C1′→glycosidic-N base attachment
- C1′→C2′ local sugar distance
- C2′→C3′ local sugar distance
- C3′→C4′ local sugar distance
- C2′→O2′ local linkage distance
- C3′→O3′ local linkage distance
- per-residue template usage

---

## Visual Inspection

The following outputs were inspected visually:

```text
converted_tna_RNA-8mer_auto_006B4.pdb
converted_tna_RNA-34mer_auto_006B4.pdb
converted_tna_8t5o-HH-typeI-111mer-full_auto_006B4.pdb
```

Observed:

- coherent atom/stick structures
- no obvious residue explosion
- dense but connected macromolecular output for the 111-mer
- PyMOL did not render the same ribbon/cartoon style used for RNA-like XNAs

Important visualization note:

```text
For TNA, stick representation is more reliable than PyMOL nucleic-acid cartoon rendering.
```

PyMOL's standard nucleic-acid cartoon logic expects canonical DNA/RNA-style atom and linkage patterns. TNA does not follow that grammar, so ribbon absence is expected.

---

## Scientific Interpretation

Correct description:

```text
TNA-like candidate structures generated through linkage-optimized reconstruction.
```

Incorrect descriptions:

```text
validated TNA structures
experimentally confirmed TNA ribozymes
MD-ready TNA polymers
proof of TNA biological function
```

The outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- TNA stereochemistry requires expert inspection.
- PyMOL cartoon/ribbon rendering may fail or be uninformative.
- The 111-mer output is a geometry candidate, not proof that TNA can adopt or maintain that fold experimentally.
- Biological function, stability, replication, or catalytic activity is not implied.

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
```

Development pattern learned from TNA:

```text
some XNAs require changing the polymer-linkage model itself
local sugar edits are not always enough
validation must match the target XNA chemistry
visualization tools may not understand noncanonical polymers
```

---

## Recommended Repository Placement

```text
src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py
docs/prototype_006B_rna_to_tna_linkage_optimized.md
benchmarks/tna_scaling/
```

---

## Current Status

Prototype 006B.4 is a successful scalable TNA-like candidate generator.

It should remain under:

```text
src/digital_polymerase/prototypes/
```

until the project adds:

- shared core parser/alignment/validation modules
- explicit topology/connectivity support
- stronger stereochemical validation
- force-field or minimization workflows

---

## Final Note

Prototype 006B.4 marks the point where TNA joined HNA, ANA, FANA, CeNA, and XyNA as working Digital Polymerase candidate-generation families.

It is still a candidate generator, not a physical validation engine — but it is now robust enough to archive as a major development milestone.
