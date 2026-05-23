# Benchmark 009: TNA Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 009  
**Prototype tested:** Prototype 006B.4 — RNA → TNA linkage-optimized reconstruction  
**Status:** Successful candidate-generation benchmark; not physically validated  
**Primary result:** TNA-like candidate generation scales from 8 nt to 111 nt after linkage remapping and local optimization.

---

## Summary

Benchmark 009 documents the first RNA → TNA scaling benchmark in Digital Polymerase.

TNA, or threose nucleic acid, is substantially trickier than the earlier pentose-like targets. It is not simply RNA with a shorter sugar. The key complication is that TNA uses a different linkage logic from canonical RNA.

Canonical RNA-style chain logic is commonly represented as:

```text
O3′(i) → P(i+1)
```

The uploaded TNA template instead indicated a TNA-like linkage pattern:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
```

For this reason, Prototype 006B.4 uses **linkage-optimized reconstruction** rather than simple chain-preserving local replacement.

The benchmark tested six RNA inputs:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer HH ribozyme-derived RNA
```

All tested outputs passed the current core validation checks, including TNA-specific linkage checks and local sugar geometry checks.

Visual inspection in PyMOL showed coherent atom/stick structures for the 8-mer, 34-mer, and 111-mer outputs. Unlike RNA-like XNAs, PyMOL did not reliably render standard ribbon/cartoon visuals for TNA, which is expected because TNA is not recognized as a canonical nucleic acid polymer.

---

## Why TNA Was Difficult

Earlier successful Digital Polymerase prototypes included:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
XyNA  → Prototype 005A
```

For ANA, FANA, and XyNA, chain-preserving strategies worked well because the RNA-like polymer path could be largely retained while modifying local sugar/scaffold geometry.

TNA required a different approach because its linkage pattern shifts the polymer logic. Preserving RNA O3′→P geometry directly would produce a misleading model.

The key lesson from this benchmark is:

```text
TNA is not a local sugar edit.
TNA requires linkage remapping.
```

---

## Prototype Development Path

The TNA prototype passed through several stages:

```text
Prototype 006A   → first linkage-remapped TNA attempt
Prototype 006A.1 → added O2′/O3′ bond correction
Prototype 006B   → introduced local sugar optimization
Prototype 006B.1 → strengthened internal sugar constraints
Prototype 006B.2 → improved terminal/gap-adjacent behavior
Prototype 006B.3 → added terminal rescue behavior
Prototype 006B.4 → final tested version with numbering-gap-aware next-residue handling
```

Prototype 006B.4 is the version archived for Benchmark 009.

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── tna_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 6MU5_TNA_13mer.pdb
    ├── outputs/
    │   ├── converted_tna_RNA-8mer_auto_006B4.pdb
    │   ├── converted_tna_RNA-12mer_auto_006B4.pdb
    │   ├── converted_tna_RNA-16mer_auto_006B4.pdb
    │   ├── converted_tna_RNA-22mer_auto_006B4.pdb
    │   ├── converted_tna_RNA-34mer_auto_006B4.pdb
    │   └── converted_tna_8t5o-HH-typeI-111mer-full_auto_006B4.pdb
    ├── reports/
    │   ├── conversion_report_RNA-8mer_auto_006B4.md
    │   ├── conversion_report_RNA-12mer_auto_006B4.md
    │   ├── conversion_report_RNA-16mer_auto_006B4.md
    │   ├── conversion_report_RNA-22mer_auto_006B4.md
    │   ├── conversion_report_RNA-34mer_auto_006B4.md
    │   └── conversion_report_8t5o-HH-typeI-111mer-full_auto_006B4.md
    ├── visual_inspection/
    │   ├── pymol/
    │   └── discovery_studio/
    └── benchmark_009_tna_scaling_notes.md
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

## TNA Template

Primary template:

```text
6MU5_TNA_13mer.pdb
```

Template properties observed during development:

```text
Length: 13 residues
TNA-like residue names include FA2 and related TNA residues
TNA-specific atom names required normalization, including C1T/O2T-style names
```

Important normalized TNA scaffold atoms include:

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

The converter normalizes template atom names internally, for example:

```text
C1T → C1′
C2T → C2′
C3T → C3′
C4T → C4′
O2T → O2′
O3T → O3′
O4T → O4′
```

---

## Prototype 006B.4 Method

Prototype 006B.4 performs **linkage-optimized TNA reconstruction**.

For each source RNA residue, the converter:

1. infers RNA base identity
2. selects a TNA template residue by base class or fallback logic
3. uses source RNA phosphate positions as the global chain path
4. places an initial TNA-like sugar scaffold from the template
5. locally optimizes the TNA sugar to satisfy TNA-specific distances
6. transforms source RNA bases onto the optimized TNA-like sugar frame
7. corrects C1′→glycosidic-N distance
8. exports a TNA-like candidate PDB
9. validates TNA-specific linkages and local sugar geometry

---

## TNA-Specific Linkage Checks

Prototype 006B.4 validates:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
```

These checks replace the canonical RNA-like O3′(i)→P(i+1) assumption.

This is why TNA needed a separate prototype rather than reusing ANA/FANA/XyNA chain-preserving logic.

---

## Scaling Results

| Input | Residues | O2′→P(next) | P→O3′ | Base attach | C2′→O2′ | C3′→O3′ | Segment RMSD mean/max (Å) | Base RMSD mean/max (Å) | Mean P→O3′ / O2′→P(next) (Å) |
|---|---:|---|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9191 / 1.2477 | 0.0674 / 0.0936 | 1.6026 / 1.6106 |
| `RNA-12mer` | 12 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9397 / 1.2477 | 0.0682 / 0.0922 | 1.6041 / 1.5809 |
| `RNA-16mer` | 16 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9598 / 1.2477 | 0.0724 / 0.1307 | 1.6031 / 1.5871 |
| `RNA-22mer` | 22 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9425 / 1.2907 | 0.1199 / 0.3648 | 1.6038 / 1.5794 |
| `RNA-34mer` | 34 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9575 / 1.5504 | 0.0995 / 0.3348 | 1.6026 / 1.5722 |
| `HH-111mer` | 111 | `PASS` | `PASS` | `PASS` | `PASS` | `PASS` | 0.9595 / 1.3923 | 0.0987 / 0.3689 | 1.6032 / 1.5752 |

Interpretation:

- All benchmarked inputs used linkage-optimized TNA reconstruction.
- All tested outputs passed TNA O2′(i)→P(i+1) validation.
- All tested outputs passed TNA P(i)→O3′(i) validation.
- All tested outputs passed base-attachment validation.
- All tested outputs passed key local sugar checks, including C2′→O2′ and C3′→O3′.
- Visual inspection showed coherent atom/stick structures.

---

## Visual Inspection

Visual inspection was performed in PyMOL.

### 8-mer

- compact but coherent TNA-like candidate
- atom/stick representation appears connected
- no obvious residue explosion

### 34-mer

- coherent longer candidate
- global folded shape preserved in stick representation
- dense but interpretable structure

### 111-mer HH ribozyme-derived RNA

- dense macromolecular candidate
- global architecture remains recognizable
- no obvious catastrophic fragmentation
- PyMOL ribbon/cartoon rendering is not reliable for this output

Important note:

```text
Failure to display a canonical nucleic-acid ribbon in PyMOL is not treated as failure for TNA.
```

TNA does not follow the standard RNA/DNA atom/linkage grammar that PyMOL expects for cartoon nucleic acid rendering. For TNA, atom/stick visualization and linkage-specific validation are more informative.

---

## Scientific Interpretation

Correct description:

```text
TNA-like computational candidate structures generated by linkage-optimized reconstruction.
```

Incorrect descriptions:

```text
validated TNA molecules
experimentally confirmed TNA ribozymes
MD-ready TNA structures
proof of TNA biological function
```

These outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No molecular dynamics validation.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- TNA stereochemistry requires expert inspection.
- Molecular viewers may not recognize the output as a canonical nucleic-acid polymer.
- PyMOL cartoon/ribbon failure is expected and should not be interpreted as structural failure.
- Large 111-mer output should be treated as a geometry candidate, not a validated TNA ribozyme.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Development Classification

Digital Polymerase conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Local atom/residue identity transformation.

3. **Geometric candidate reconstruction**  
   Coordinate-level candidate generation using templates and coordinate transformations.

4. **Physically refined modeling**  
   Energy minimization, MD, force-field validation, and expert inspection.

Prototype 006B.4 reaches:

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
```

Development pattern reinforced by TNA:

```text
not all XNAs can be handled by chain preservation
some XNAs require explicit linkage remapping
viewer cartoon support is not a reliable success criterion
target-specific validation matters more than pretty ribbons
```

---

## Recommended Repository Status

Keep the current script under:

```text
src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py
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

---

## Recommended Commit Message

```bash
git add src/digital_polymerase/prototypes/rna_to_tna_linkage_optimized.py
git add benchmarks/tna_scaling/
git add docs/prototype_006B_rna_to_tna_linkage_optimized.md
git commit -m "Add linkage-optimized RNA-to-TNA prototype and scaling benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as TNA scaling benchmark:** yes  
**Proceed to next XNA target:** yes, after documentation and repo cleanup

Benchmark 009 marks the point where TNA joins HNA, ANA, FANA, CeNA, and XyNA as a working Digital Polymerase candidate-generation family.
