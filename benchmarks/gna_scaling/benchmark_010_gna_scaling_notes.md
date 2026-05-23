# Benchmark 010: GNA Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 010  
**Prototype tested:** Prototype 007A — RNA → GNA linkage-optimized glycerol-scaffold reconstruction  
**Status:** Successful first-pass candidate-generation benchmark; not physically validated  
**Primary result:** GNA-like candidate generation scales from 8 nt to 111 nt, with coherent visual outputs but notable roughness and crowding.

---

## Summary

Benchmark 010 documents the first RNA → GNA scaling benchmark in Digital Polymerase.

GNA, or glycerol nucleic acid, is one of the most structurally divergent XNA targets tested so far in this project. Unlike pentose-like analogs such as XyNA or arabino/fluoro-arabino analogs such as ANA/FANA, GNA uses a compact glycerol-like scaffold.

The uploaded GNA template uses atoms such as:

```text
C1G
C2G
C3G
O2G
O3G
```

The observed GNA-like linkage pattern is:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

Therefore, Prototype 007A treats GNA as a **linkage-optimized glycerol-scaffold reconstruction** problem rather than a chain-preserving RNA sugar-edit problem.

The benchmark tested six RNA inputs:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer HH ribozyme-derived RNA
```

All tested outputs passed the current report-level validation checks, including GNA-specific linkage and local scaffold checks. Visual inspection showed coherent structures for the 8-mer, 34-mer, and 111-mer, although the 34-mer and 111-mer outputs are compact/crowded and should be treated as rough first-pass candidates.

---

## Why GNA Is a Wild Beast

Earlier Digital Polymerase prototype families include:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
XyNA  → Prototype 005A
TNA   → Prototype 006B.4
```

GNA is challenging because:

```text
RNA uses a ribose scaffold.
TNA uses a shorter threose-like scaffold.
GNA uses an even smaller glycerol-like scaffold.
```

This makes GNA more compressed than RNA-like systems. When large RNA structures are converted into GNA-like candidates, steric crowding and visual tangling are expected.

The key lesson is:

```text
GNA is not a local sugar edit.
GNA requires scaffold compression and linkage remapping.
```

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── gna_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 2xc6-GNA-8nt.pdb
    ├── outputs/
    │   ├── converted_gna_RNA-8mer_auto_007A.pdb
    │   ├── converted_gna_RNA-12mer_auto_007A.pdb
    │   ├── converted_gna_RNA-16mer_auto_007A.pdb
    │   ├── converted_gna_RNA-22mer_auto_007A.pdb
    │   ├── converted_gna_RNA-34mer_auto_007A.pdb
    │   └── converted_gna_8t5o-HH-typeI-111mer-full_auto_007A.pdb
    ├── reports/
    │   ├── conversion_report_RNA-8mer_auto_007A.md
    │   ├── conversion_report_RNA-12mer_auto_007A.md
    │   ├── conversion_report_RNA-16mer_auto_007A.md
    │   ├── conversion_report_RNA-22mer_auto_007A.md
    │   ├── conversion_report_RNA-34mer_auto_007A.md
    │   └── conversion_report_8t5o-HH-typeI-111mer-full_auto_007A.md
    ├── visual_inspection/
    │   ├── pymol/
    │   └── discovery_studio/
    └── benchmark_010_gna_scaling_notes.md
```

---

## Input RNA Dataset

| File | Length | Residue range | Sequence |
|---|---:|---|---|
| `RNA-8mer.pdb` | 8 nt | A:72–79 | `CUAGGCUC` |
| `RNA-12mer.pdb` | 12 nt | A:72–83 | `CUAGGCUCGAAA` |
| `RNA-16mer.pdb` | 16 nt | A:67–82 | `ACCACCUAGGCUCGAA` |
| `RNA-22mer.pdb` | 22 nt | A:62–83 | `AUACGACCACCUAGGCUCGAAA` |
| `RNA-34mer.pdb` | 34 nt | A:54–87 | `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC` |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 nt | A:5–117, with source numbering gap | `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC` |

---

## GNA Template

Primary template:

```text
2xc6-GNA-8nt.pdb
```

Template characteristics observed during development:

```text
Length: 8 residues
GNA-like residue names include ZAD, ZGU, ZCY, and ZBU/ZTH-like residues
GNA scaffold atoms include C1G, C2G, C3G, O2G, and O3G
```

Important GNA scaffold atoms:

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

GNA-specific linkages validated in this benchmark:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

---

## Prototype 007A Method

Prototype 007A performs **linkage-optimized GNA glycerol-scaffold reconstruction**.

For each source RNA residue, the converter:

1. infers RNA base identity
2. selects a GNA template residue by base class or fallback logic
3. uses source RNA phosphate positions as a global chain guide
4. generates an initial GNA glycerol scaffold from the template
5. locally optimizes GNA scaffold distances
6. attaches source RNA bases to `C1G`
7. exports a GNA-like candidate PDB
8. validates GNA-specific linkages and local scaffold geometry

---

## GNA-Specific Linkage Checks

Prototype 007A validates:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

These checks are more appropriate for GNA than canonical RNA O3′(i)→P(i+1) validation.

The converter also validates local scaffold geometry:

```text
C1G → C2G
C2G → C3G
C2G → O2G
C3G → O3G
C1G → glycosidic N
```

---

## Scaling Results

| Input | Residues | O2G→P(next) | P→O3G | Base attach | C1G→C2G | C2G→C3G | C2G→O2G | C3G→O3G | Initial RMSD mean/max (Å) | Base shift mean/max (Å) | Mean P→O3G / O2G→P(next) (Å) |
|---|---:|---|---|---|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.8819 / 1.0762 | 0.7804 / 1.3338 | 1.5944 / 1.5910 |
| `RNA-12mer` | 12 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9965 / 1.1972 | 0.8467 / 1.3338 | 1.5947 / 1.5926 |
| `RNA-16mer` | 16 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 1.0182 / 1.1972 | 0.8267 / 1.3338 | 1.5946 / 1.5920 |
| `RNA-22mer` | 22 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9687 / 1.1970 | 0.8156 / 1.3196 | 1.5944 / 1.5926 |
| `RNA-34mer` | 34 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9861 / 1.1970 | 0.8505 / 1.3613 | 1.5942 / 1.5929 |
| `HH-111mer` | 111 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9987 / 1.4842 | 0.8870 / 1.6972 | 1.5944 / 1.5928 |

Interpretation:

- All benchmarked inputs used linkage-optimized GNA reconstruction.
- All tested outputs passed GNA O2G(i)→P(i+1) validation.
- All tested outputs passed GNA P(i)→O3G(i) validation.
- All tested outputs passed base-attachment validation.
- All tested outputs passed key local GNA scaffold checks.
- Visual inspection showed coherent atom/stick structures, but larger outputs are compact and crowded.

---

## Visual Inspection

Visual inspection was performed in PyMOL and Discovery Studio.

### 8-mer

- coherent curved oligomer
- bases appear attached
- carbonyl/base oxygens are visible in Discovery Studio
- PyMOL visualization was more ambiguous for some oxygen groups

### 34-mer

- connected overall
- not fragmented into molecular confetti
- bases remain attached
- visibly compact and crowded

### 111-mer HH ribozyme-derived RNA

- dense macromolecular candidate
- global architecture remains recognizable
- no obvious catastrophic fragmentation
- highly crowded, as expected for a compressed glycerol-like scaffold

Important visualization note:

```text
For GNA, stick representation is more reliable than PyMOL nucleic-acid cartoon rendering.
```

GNA does not follow canonical DNA/RNA atom and linkage grammar, so standard ribbon/cartoon rendering should not be used as the main success criterion.

---

## Carbonyl / Base-Oxygen Audit Note

During visual inspection, PyMOL initially made some carbonyl/ketone-like base oxygens difficult to see consistently. Discovery Studio showed these atoms more clearly in the 8-mer output.

The current interpretation is:

```text
base oxygens are likely present,
but GNA compactness and viewer rendering can make them visually ambiguous.
```

Future GNA patches should include an explicit base-atom audit, checking expected base atoms such as:

```text
G: O6
C: O2
U: O2 and O4
A: no canonical carbonyl oxygen
```

This is recommended for Prototype 007B.

---

## Scientific Interpretation

Correct description:

```text
GNA-like computational candidate structures generated by linkage-optimized glycerol-scaffold reconstruction.
```

Incorrect descriptions:

```text
validated GNA molecules
experimentally confirmed GNA ribozymes
MD-ready GNA structures
proof of GNA biological function
```

These outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No molecular dynamics validation.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- GNA stereochemistry requires expert inspection.
- Base orientation is rough and should be audited in future versions.
- Larger outputs are compact and crowded.
- Molecular viewers may not recognize the output as a canonical nucleic-acid polymer.
- PyMOL cartoon/ribbon behavior should not be used as a success criterion.
- Large 111-mer output should be treated as a geometry candidate, not a validated GNA ribozyme.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Development Classification

Digital Polymerase conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Local atom/residue identity transformation.

3. **Geometric candidate reconstruction**  
   Coordinate-level candidate generation using templates, coordinate transformations, and local optimization.

4. **Physically refined modeling**  
   Energy minimization, MD, force-field validation, and expert inspection.

Prototype 007A reaches:

```text
Level 3: geometric candidate reconstruction
```

It does not reach:

```text
Level 4: physically refined modeling
```

---

## Relationship to Other XNA Families

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

Development pattern reinforced by GNA:

```text
small-backbone XNAs require explicit scaffold compression
viewer visualization is not enough
base placement needs separate auditing
target-specific linkage validation matters more than pretty ribbons
```

---

## Recommended Repository Status

Keep the current script under:

```text
src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py
```

Do not yet promote it into:

```text
src/digital_polymerase/converters/
```

until the project adds:

- shared core modules
- explicit topology/connectivity support
- stronger stereochemistry validation
- force-field/minimization compatibility
- cross-XNA shared conversion framework
- explicit base-atom and carbonyl audit

---

## Recommended Commit Message

```bash
git add src/digital_polymerase/prototypes/rna_to_gna_linkage_optimized.py
git add benchmarks/gna_scaling/
git add docs/prototype_007A_rna_to_gna_linkage_optimized.md
git commit -m "Add linkage-optimized RNA-to-GNA prototype and scaling benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as GNA scaling benchmark:** yes  
**Proceed to next XNA target:** yes, after documentation and repo cleanup

Benchmark 010 marks the point where GNA joins HNA, ANA, FANA, CeNA, XyNA, and TNA as a working Digital Polymerase candidate-generation family.
