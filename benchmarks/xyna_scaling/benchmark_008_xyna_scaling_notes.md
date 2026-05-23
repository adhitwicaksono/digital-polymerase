# Benchmark 008: XyNA Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 008  
**Prototype tested:** Prototype 005A — RNA → XyNA chain-preserving local sugar reconstruction  
**Status:** Successful candidate-generation benchmark; not physically validated  
**Primary result:** XyNA-like candidate generation scales from 8 nt to 111 nt.

---

## Summary

Benchmark 008 documents the first RNA → XyNA scaling benchmark in Digital Polymerase.

XyNA, or xylose-based nucleic acid, is a pentose-based nucleic acid analog. Because its scaffold remains relatively close to RNA-like nucleic acid geometry, Prototype 005A uses a conservative **chain-preserving local sugar reconstruction** strategy.

The benchmark tested six RNA inputs:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer HH ribozyme-derived RNA
```

The XyNA template used was:

```text
2n4j_XyNA-8nt.pdb
```

All tested outputs passed the current core validation checks, including polymer-chain continuity, base attachment, and local XyNA sugar geometry.

Visual inspection in PyMOL and Discovery Studio showed coherent continuous structures for the 8-mer, 34-mer, and 111-mer outputs.

---

## Why XyNA Was Expected to Be Easier

Before XyNA, Digital Polymerase had working candidate-generation families for:

```text
HNA   → structurally more divergent hexitol scaffold
ANA   → pentose-like arabino chemistry
FANA  → fluorinated arabino chemistry
CeNA  → cyclohexenyl scaffold
```

Compared with HNA and CeNA, XyNA is less disruptive to the overall RNA-like polymer framework because it remains pentose-based.

However, XyNA is not just RNA with a renamed residue. Local sugar stereochemistry still matters, especially around the `C2′` and `O2′` geometry. Prototype 005A therefore preserves the RNA chain path but replaces the local `C2′/O2′` geometry using template-derived XyNA coordinates.

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── xyna_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 2n4j_XyNA-8nt.pdb
    ├── outputs/
    │   ├── converted_xyna_RNA-8mer_auto_005A.pdb
    │   ├── converted_xyna_RNA-12mer_auto_005A.pdb
    │   ├── converted_xyna_RNA-16mer_auto_005A.pdb
    │   ├── converted_xyna_RNA-22mer_auto_005A.pdb
    │   ├── converted_xyna_RNA-34mer_auto_005A.pdb
    │   └── converted_xyna_8t5o-HH-typeI-111mer-full_auto_005A.pdb
    ├── reports/
    │   ├── conversion_report_RNA-8mer_auto_005A.md
    │   ├── conversion_report_RNA-12mer_auto_005A.md
    │   ├── conversion_report_RNA-16mer_auto_005A.md
    │   ├── conversion_report_RNA-22mer_auto_005A.md
    │   ├── conversion_report_RNA-34mer_auto_005A.md
    │   └── conversion_report_8t5o-HH-typeI-111mer-full_auto_005A.md
    ├── visual_inspection/
    │   ├── pymol/
    │   └── discovery_studio/
    └── benchmark_008_xyna_scaling_notes.md
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

## XyNA Template

Primary template:

```text
2n4j_XyNA-8nt.pdb
```

Template properties observed during inspection:

```text
Length: 8 residues
Base-class sequence: GUGUACAC
Observed XyNA residue names: 8XG, 8XU, 8XA, 8XC
```

Important XyNA/RNA-like scaffold atoms observed:

```text
P
O5'
C5'
C4'
O4'
C1'
C2'
O2'
C3'
O3'
```

The template is used primarily as a local sugar-geometry donor.

---

## Prototype 005A Method

Prototype 005A uses **chain-preserving local sugar reconstruction** in `auto` mode.

For each source RNA residue, the converter:

1. infers RNA base identity
2. selects an appropriate XyNA template residue by base class
3. preserves RNA chain-continuity atoms
4. preserves RNA base atoms
5. replaces local `C2′/O2′` geometry using the XyNA template
6. exports a XyNA-like candidate residue
7. validates polymer-chain continuity and local sugar geometry

This is intentionally conservative because XyNA is pentose-based.

---

## Optional Full-Template Mode

Prototype 005A also includes an optional full-template mode for short inputs when a full-length XyNA template is available.

An optional 8-mer full-template output was generated for comparison:

```text
converted_xyna_RNA-8mer_full_template_005A.pdb
```

However, the main benchmark uses chain-preserving mode because it is more consistent for scaling to longer RNA inputs.

---

## Scaling Results

| Input | Residues | Mode | Chain | Base attach | XyNA sugar | Local/template RMSD mean/max (Å) | C1′→N mean/max (Å) | C2′→O2′ mean/max (Å) |
|---|---:|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0923 / 0.1275 | 1.4768 / 1.4799 | 1.4332 / 1.4343 |
| `RNA-12mer` | 12 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0830 / 0.1275 | 1.4760 / 1.4799 | 1.4330 / 1.4343 |
| `RNA-16mer` | 16 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0864 / 0.1285 | 1.4762 / 1.4799 | 1.4331 / 1.4343 |
| `RNA-22mer` | 22 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0766 / 0.1275 | 1.4742 / 1.4799 | 1.4331 / 1.4343 |
| `RNA-34mer` | 34 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0760 / 0.1275 | 1.4744 / 1.4804 | 1.4330 / 1.4343 |
| `HH-111mer` | 111 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0781 / 0.1285 | 1.4745 / 1.4804 | 1.4330 / 1.4343 |

Interpretation:

- All benchmarked inputs used chain-preserving mode in `auto`.
- All tested outputs passed O3′→P chain-continuity validation.
- All tested outputs passed C1′→glycosidic-N validation.
- All tested outputs passed XyNA local sugar checks involving C2′→O2′, C1′→O4′, and C4′→O4′.
- Visual inspection showed coherent continuous structures.

---

## Visual Inspection

Visual inspection was performed in PyMOL and Discovery Studio.

### 8-mer

- clean curved short-mer candidate
- coherent atom/stick view
- no obvious residue fragmentation

### 34-mer

- continuous longer chain
- sane base placement
- no obvious local sugar explosion
- atom/stick view remains connected and interpretable

### 111-mer HH ribozyme-derived RNA

- dense but coherent macromolecular candidate
- continuous folded chain architecture
- no obvious catastrophic chain breakage
- stick view reads as one connected nucleic-acid-like object

Visual inspection supports the benchmark conclusion:

```text
Prototype 005A produces visually coherent XyNA-like candidate structures up to 111 nt.
```

---

## Scientific Interpretation

Correct description:

```text
XyNA-like computational candidate structures generated by chain-preserving local sugar reconstruction.
```

Incorrect descriptions:

```text
validated XyNA molecules
experimentally confirmed XyNA ribozymes
MD-ready XyNA structures
proof of XyNA biological function
```

These outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No molecular dynamics validation.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- XyNA stereochemistry requires expert inspection.
- Chain-preserving mode preserves the RNA chain path and replaces local `C2′/O2′` geometry; it is not de novo XyNA folding.
- Large 111-mer output should be treated as a geometry candidate, not a validated XyNA ribozyme.
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

Prototype 005A reaches:

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
```

Development pattern reinforced by XyNA:

```text
pentose-based does not mean trivial
template-derived local geometry still matters
chain continuity must be preserved
visual inspection remains essential
```

---

## Recommended Repository Status

Keep the current script under:

```text
src/digital_polymerase/prototypes/rna_to_xyna_fragment_guided.py
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
git add src/digital_polymerase/prototypes/rna_to_xyna_fragment_guided.py
git add benchmarks/xyna_scaling/
git add docs/prototype_005A_rna_to_xyna_fragment_guided.md
git commit -m "Add RNA-to-XyNA prototype and scaling benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as XyNA scaling benchmark:** yes  
**Proceed to next XNA target:** yes, after documentation and repo cleanup

Benchmark 008 marks the point where XyNA joins HNA, ANA, FANA, and CeNA as a working Digital Polymerase candidate-generation family.
