# Prototype 007A: RNA → GNA Linkage-Optimized Glycerol-Scaffold Reconstruction

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype:** 007A  
**Conversion:** RNA → GNA  
**Method:** Linkage-optimized glycerol-scaffold reconstruction  
**Status:** Successful first-pass scalable candidate generator; not physically validated

---

## Summary

Prototype 007A is the Digital Polymerase prototype for generating GNA-like candidate structures from RNA PDB inputs.

GNA, or glycerol nucleic acid, is one of the most divergent XNA targets currently explored in Digital Polymerase. It uses a compact glycerol-like scaffold rather than a ribose, arabinose, cyclohexenyl, hexitol, or threose-like scaffold.

The uploaded GNA template uses atoms such as:

```text
C1G
C2G
C3G
O2G
O3G
```

Prototype 007A therefore performs **linkage-optimized glycerol-scaffold reconstruction**, not simple RNA chain preservation.

---

## Current Script

Recommended path:

```text
src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py
```

Example command:

```bash
python src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py \
  --rna benchmarks/gna_scaling/inputs/RNA-34mer.pdb \
  --template benchmarks/gna_scaling/templates/2xc6-GNA-8nt.pdb \
  --output benchmarks/gna_scaling/outputs/converted_gna_RNA-34mer_auto_007A.pdb \
  --report benchmarks/gna_scaling/reports/conversion_report_RNA-34mer_auto_007A.md
```

---

## Template Used

Primary template:

```text
2xc6-GNA-8nt.pdb
```

Important observed atoms:

```text
P
OP1
OP2
C1G
C2G
C3G
O2G
O3G
```

GNA-specific base-bearing atom:

```text
C1G
```

GNA-specific linkage atoms:

```text
O3G
O2G
```

---

## Why GNA Needed a Dedicated Algorithm

Earlier XNA prototypes used one of these broad strategies:

```text
full-template reconstruction
chain-preserving local scaffold reconstruction
linkage-optimized TNA reconstruction
```

GNA is closer to the TNA problem than the XyNA problem, but even more compressed.

The observed GNA-like linkage pattern is:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

This makes canonical RNA O3′→P chain preservation inappropriate.

GNA also lacks the larger sugar scaffold of RNA-like polymers, meaning base placement and crowding become more difficult.

---

## Method

For each source RNA residue, Prototype 007A:

1. parses the source RNA and GNA template
2. infers the source RNA base identity
3. selects a GNA template residue by base class or fallback logic
4. uses source RNA phosphate positions as a global chain guide
5. generates an initial GNA glycerol scaffold from the template
6. locally optimizes GNA scaffold geometry
7. attaches source RNA bases to `C1G`
8. exports a GNA-like candidate PDB
9. validates GNA-specific linkages and local scaffold geometry

---

## Optimization Targets

Prototype 007A optimizes or validates:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
C1G    → C2G
C2G    → C3G
C2G    → O2G
C3G    → O3G
C1G    → glycosidic N
```

This explicitly treats GNA as a small-backbone linkage-remapping problem.

---

## Base Attachment

Source RNA bases are reattached to the GNA `C1G` atom.

The converter preserves the approximate source base orientation and translates the base to satisfy the target `C1G→glycosidic N` distance. This is sufficient for first-pass candidate generation, but it is not yet a full base-orientation refinement algorithm.

Future GNA development should improve:

```text
base-plane orientation
base-carbonyl visibility/audit
clash reduction
base-backbone steric scoring
```

---

## Example Usage

### 8-mer test

```bash
python src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py \
  --rna benchmarks/gna_scaling/inputs/RNA-8mer.pdb \
  --template benchmarks/gna_scaling/templates/2xc6-GNA-8nt.pdb \
  --output benchmarks/gna_scaling/outputs/converted_gna_RNA-8mer_auto_007A.pdb \
  --report benchmarks/gna_scaling/reports/conversion_report_RNA-8mer_auto_007A.md
```

### 111-mer HH ribozyme-derived test

```bash
python src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py \
  --rna benchmarks/gna_scaling/inputs/8t5o-HH-typeI-111mer-full.pdb \
  --template benchmarks/gna_scaling/templates/2xc6-GNA-8nt.pdb \
  --output benchmarks/gna_scaling/outputs/converted_gna_8t5o-HH-typeI-111mer-full_auto_007A.pdb \
  --report benchmarks/gna_scaling/reports/conversion_report_8t5o-HH-typeI-111mer-full_auto_007A.md
```

---

## Benchmark Results

Prototype 007A was tested on six RNA inputs.

| Input | Residues | O2G→P(next) | P→O3G | Base attach | C1G→C2G | C2G→C3G | C2G→O2G | C3G→O3G | Initial RMSD mean/max (Å) | Base shift mean/max (Å) | Mean P→O3G / O2G→P(next) (Å) |
|---|---:|---|---|---|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.8819 / 1.0762 | 0.7804 / 1.3338 | 1.5944 / 1.5910 |
| `RNA-12mer` | 12 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9965 / 1.1972 | 0.8467 / 1.3338 | 1.5947 / 1.5926 |
| `RNA-16mer` | 16 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 1.0182 / 1.1972 | 0.8267 / 1.3338 | 1.5946 / 1.5920 |
| `RNA-22mer` | 22 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9687 / 1.1970 | 0.8156 / 1.3196 | 1.5944 / 1.5926 |
| `RNA-34mer` | 34 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9861 / 1.1970 | 0.8505 / 1.3613 | 1.5942 / 1.5929 |
| `HH-111mer` | 111 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9987 / 1.4842 | 0.8870 / 1.6972 | 1.5944 / 1.5928 |

All tested outputs passed the main report-level validation checks.

---

## Validation Metrics

Prototype 007A reports:

- converted residue count
- source sequence
- template sequence
- initial alignment RMSD
- base shift
- local optimization cost
- GNA O2G(i)→P(i+1) linkage
- GNA P(i)→O3G(i) linkage
- C1G→glycosidic-N base attachment
- C1G→C2G local scaffold distance
- C2G→C3G local scaffold distance
- C2G→O2G local scaffold distance
- C3G→O3G local scaffold distance
- per-residue template usage

---

## Visual Inspection

The following outputs were inspected visually:

```text
converted_gna_RNA-8mer_auto_007A.pdb
converted_gna_RNA-34mer_auto_007A.pdb
converted_gna_8t5o-HH-typeI-111mer-full_auto_007A.pdb
```

Observed:

- coherent atom/stick structures
- bases remain attached
- no obvious molecular confetti
- larger structures are compact and crowded
- PyMOL cartoon/ribbon rendering is not reliable for GNA-like structures
- Discovery Studio made the 8-mer base oxygens easier to inspect than PyMOL

Current visual status:

```text
8-mer  → good first candidate
34-mer → coherent but crowded
111-mer → globally coherent but locally rough
```

---

## Carbonyl / Base-Oxygen Audit Note

During visual inspection, base carbonyl/ketone-like groups were not consistently obvious in PyMOL. Discovery Studio showed them more clearly in the 8-mer.

For future development, Prototype 007B should include an explicit base-atom audit.

Expected base oxygen logic:

```text
A: no canonical carbonyl oxygen
G: O6
C: O2
U: O2 and O4
```

This would distinguish between:

```text
atoms missing from the output
```

and:

```text
atoms present but visually hidden or poorly rendered
```

---

## Scientific Interpretation

Correct description:

```text
GNA-like candidate structures generated through linkage-optimized glycerol-scaffold reconstruction.
```

Incorrect descriptions:

```text
validated GNA structures
experimentally confirmed GNA ribozymes
MD-ready GNA polymers
proof of GNA biological function
```

The outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- GNA stereochemistry requires expert inspection.
- Base orientation is rough.
- Larger outputs are compact and crowded.
- PyMOL cartoon/ribbon rendering may fail or be uninformative.
- The 111-mer output is a geometry candidate, not proof that GNA can adopt or maintain that fold experimentally.
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
GNA   → Prototype 007A
```

Development pattern learned from GNA:

```text
small-backbone XNAs need explicit scaffold compression
base placement becomes a major challenge
viewer behavior is not enough for validation
report-level validation must be paired with visual and chemical audits
```

---

## Recommended Repository Placement

```text
src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py
docs/prototype_007A_rna_to_gna_linkage_optimized.md
benchmarks/gna_scaling/
```

---

## Recommended Future Patch: Prototype 007B

A future GNA patch should focus on:

```text
base-orientation audit
expected base atom / carbonyl audit
base-plane preservation score
clash or crowding heuristic
optional local base rotation refinement
explicit warning when base shift is large
```

This would make GNA outputs easier to interpret and safer to document.

---

## Current Status

Prototype 007A is a successful first-pass scalable GNA-like candidate generator.

It should remain under:

```text
src/digital_polymerase/prototypes/
```

until the project adds:

- shared core parser/alignment/validation modules
- explicit topology/connectivity support
- stronger stereochemical validation
- force-field or minimization workflows
- explicit base-atom and carbonyl audit

---

## Final Note

Prototype 007A marks the point where GNA joined HNA, ANA, FANA, CeNA, XyNA, and TNA as a working Digital Polymerase candidate-generation family.

It is still a rough beast, but it is no longer outside the cage.
