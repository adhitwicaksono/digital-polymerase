# Benchmark 004: FANA Chain-Preserving Scaling Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 004  
**Prototype tested:** Prototype 003A — RNA → FANA chain-preserving reconstruction  
**Status:** Successful candidate-generation benchmark  
**Core finding:** Chain-preserving RNA → FANA reconstruction scales from 8 nt to 111 nt while preserving O3′→P continuity and C2′–F geometry.

---

## Executive Summary

Benchmark 004 evaluates the first RNA → FANA converter in Digital Polymerase.

The converter was developed after the RNA → ANA prototype revealed a critical lesson: residue-local reconstruction can produce plausible local geometry while breaking polymer-chain continuity. Prototype 003A therefore adopts a chain-preserving strategy from the beginning.

Instead of replacing the entire backbone residue-by-residue, Prototype 003A preserves the RNA chain framework and introduces FANA-like 2′-fluoro local geometry from a FANA template.

The benchmark tested six RNA inputs extracted from an HH-type I ribozyme source:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer full structure
```

All outputs passed the key validation checks:

```text
O3′(i) → P(i+1)
P(i) → O5′(i)
C2′ → F2′
```

Visual inspection in PyMOL and Discovery Studio showed coherent continuous structures.

---

## Why This Benchmark Matters

Benchmark 004 is important because it shows that the Digital Polymerase workflow can now incorporate lessons from earlier failure modes.

The ANA 002A.1 benchmark showed:

```text
low local RMSD does not guarantee a valid polymer chain
```

The ANA 002A.2 patch showed:

```text
preserving chain continuity first gives visually coherent ANA-like candidates
```

Prototype 003A applies that logic to FANA:

```text
preserve chain first
introduce XNA-local chemistry second
validate explicitly
```

This makes FANA the first converter family developed directly from the improved chain-preserving design philosophy.

---

## Input Dataset

The RNA input dataset was designed to test scaling from short oligomers to ribozyme-scale structures.

| File | Length | Residue range | Sequence |
|---|---:|---|---|
| `RNA-8mer.pdb` | 8 nt | A:72–79 | `CUAGGCUC` |
| `RNA-12mer.pdb` | 12 nt | A:72–83 | `CUAGGCUCGAAA` |
| `RNA-16mer.pdb` | 16 nt | A:67–82 | `ACCACCUAGGCUCGAA` |
| `RNA-22mer.pdb` | 22 nt | A:62–83 | `AUACGACCACCUAGGCUCGAAA` |
| `RNA-34mer.pdb` | 34 nt | A:54–87 | `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC` |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 nt | A:5–117, with source numbering gap | `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC` |

---

## FANA Template

The FANA template used was:

```text
2KP4_FANA_10mer.pdb
```

Observed template properties:

```text
Length: 10 residues
Sequence: GCTATAATGG
Residue names: GFL, CFL, TAF, A5L
```

Important atom-name observation:

```text
FANA fluorine atom names may appear as F or F2′ depending on residue/template convention.
```

Prototype 003A standardizes the output fluorine atom as:

```text
F2′
```

---

## Method Tested

Prototype 003A performs **chain-preserving local FANA reconstruction**.

For each source RNA residue:

1. infer RNA base identity
2. select a FANA template residue by base class
3. align FANA local template geometry onto the RNA residue frame
4. preserve RNA chain atoms
5. preserve RNA nucleobase atoms
6. remove RNA `O2′`
7. introduce FANA-like `C2′` and `F2′`
8. export a FANA-like residue
9. validate chain and local FANA geometry

The conversion is not full-template reconstruction. It is a local chemistry substitution constrained by the original RNA chain framework.

---

## Validation Results

| Input | Converted residues | Chain status | C2′–F status | Mean anchor RMSD (Å) | Max anchor RMSD (Å) | Mean C2′–F (Å) | Max C2′–F (Å) |
|---|---:|---|---|---:|---:|---:|---:|
| `RNA-8mer` | 8 | `PASS` | `PASS` | 0.0477 | 0.0726 | 1.3822 | 1.3838 |
| `RNA-12mer` | 12 | `PASS` | `PASS` | 0.0508 | 0.0726 | 1.3822 | 1.3838 |
| `RNA-16mer` | 16 | `PASS` | `PASS` | 0.0514 | 0.0726 | 1.3819 | 1.3838 |
| `RNA-22mer` | 22 | `PASS` | `PASS` | 0.0551 | 0.0939 | 1.3819 | 1.3838 |
| `RNA-34mer` | 34 | `PASS` | `PASS` | 0.0535 | 0.0939 | 1.3822 | 1.3838 |
| `HH-111mer` | 111 | `PASS` | `PASS` | 0.0520 | 0.0955 | 1.3823 | 1.3838 |

The validation results show:

- O3′→P chain-continuity validation passed for all tested outputs.
- C2′→F2′ geometry validation passed for all tested outputs.
- Mean C2′→F2′ distance remained approximately 1.382 Å.
- Local alignment RMSD remained low across all input sizes.
- No chain-continuity collapse was observed in the benchmark reports.

---

## Visual Inspection

The outputs were visually inspected in PyMOL and Discovery Studio.

### PyMOL cartoon-style impression

The 8-mer, 34-mer, and 111-mer outputs showed continuous orange backbone paths and coherent nucleobase placement.

### Discovery Studio line/stick impression

The same outputs showed dense but coherent atomic structures, without obvious residue scattering or backbone fragmentation.

Visual inspection supports the report-level conclusion:

```text
Prototype 003A produces visually coherent FANA-like candidate structures.
```

However, visual coherence does not replace physical validation.

---

## Scientific Interpretation

The correct interpretation is:

```text
FANA-like computational candidate structures generated by chain-preserving local reconstruction
```

The incorrect interpretation is:

```text
validated FANA molecules
```

or:

```text
experimentally confirmed FANA ribozymes
```

The generated structures preserve polymer continuity and local C2′–F geometry at the coordinate-candidate level, but they are not yet energy-minimized, force-field parameterized, or experimentally validated.

---

## What Worked

### 1. Chain continuity was preserved

Unlike ANA 002A.1, the FANA converter does not break O3′→P continuity.

### 2. C2′–F geometry was introduced consistently

The C2′–F2′ distance remained close to the expected template-derived value.

### 3. Scaling was successful

The converter worked across:

```text
8 nt
12 nt
16 nt
22 nt
34 nt
111 nt
```

### 4. Visual inspection was coherent

The structures looked continuous in PyMOL and Discovery Studio.

### 5. The method follows the improved Digital Polymerase design rule

```text
chain continuity first, local XNA chemistry second
```

---

## Known Limitations

### 1. Not physically refined

The structures are not energy-minimized or MD-relaxed.

### 2. No force-field/topology generation

The converter writes PDB candidates only. It does not generate AMBER, CHARMM, GROMACS, or other topology/parameter files.

### 3. Residue names are provisional

Output residue names such as `UFL` are practical placeholders and may require adjustment for downstream tools.

### 4. RNA bases are preserved

The converter preserves RNA nucleobase atoms. For RNA `U`, the local sugar/substituent geometry may use a T-like FANA donor, but the base is not chemically converted to thymine.

### 5. Stereochemistry requires expert review

The FANA-like C2′/F geometry is template-derived, but stereochemical correctness should still be checked by a structural chemist or through appropriate validation workflows.

### 6. No explicit CONECT/topology records

Some viewers and downstream tools may infer bonds differently.

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

Prototype 003A reaches:

```text
Level 3: geometric candidate reconstruction
```

It does not reach:

```text
Level 4: physically refined modeling
```

---

## Relationship to Future Work

Prototype 003A provides a cleaner template for future RNA → XNA converters than the early ANA residue-local approach.

Future XNA targets should start from the chain-preserving logic unless there is a strong reason not to.

Possible next targets:

```text
CeNA
TNA
GNA
HNA refactor
```

For each new target, the key question should be:

```text
Can we preserve polymer continuity while introducing target-specific local chemistry?
```

---

## Recommended Repository Status

Keep Prototype 003A under:

```text
src/digital_polymerase/prototypes/rna_to_fana_fragment_guided.py
```

Do not yet promote it to:

```text
src/digital_polymerase/converters/
```

until additional validation, refactoring, and topology compatibility are implemented.

Recommended benchmark location:

```text
benchmarks/fana_fragment_scaling/
```

Recommended documentation:

```text
docs/prototype_003A_rna_to_fana_fragment_guided.md
```

---

## Recommended README Addition

Add this to the main project README or roadmap:

```text
Prototype 003A introduced chain-preserving RNA → FANA reconstruction. Unlike earlier residue-local approaches, this converter preserves RNA polymer-chain continuity while introducing FANA-like C2′/F2′ local geometry from a FANA template. Benchmark 004 showed successful candidate generation from 8 nt to 111 nt, with O3′→P and C2′→F2′ validation passing across all tested inputs.
```

---

## Recommended Commit Message

```bash
git add src/digital_polymerase/prototypes/rna_to_fana_fragment_guided.py
git add benchmarks/fana_fragment_scaling/
git add docs/prototype_003A_rna_to_fana_fragment_guided.md
git commit -m "Add chain-preserving RNA-to-FANA prototype and benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as software-development benchmark:** yes  
**Proceed to next XNA target:** yes, using the chain-preserving strategy as default

Benchmark 004 is a strong milestone because it shows that Digital Polymerase can learn from earlier failure modes and generate more structurally coherent XNA-like candidates.
