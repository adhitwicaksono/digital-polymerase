# Benchmark 004: RNA → FANA Chain-Preserving Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 004  
**Prototype tested:** Prototype 003A — RNA → FANA chain-preserving reconstruction  
**Status:** Successful candidate-generation benchmark; not physically validated  
**Recommended interpretation:** Chain-preserving FANA-like candidate structures for downstream inspection and validation

---

## Summary

Benchmark 004 evaluates **Prototype 003A**, the Digital Polymerase RNA → FANA converter.

This benchmark was created after the ANA development arc showed that residue-local XNA reconstruction can look locally plausible while breaking inter-residue polymer continuity. Prototype 003A therefore follows the improved principle:

```text
preserve chain continuity first
introduce XNA-local chemistry second
validate explicitly
```

For FANA, the converter preserves the RNA polymer-chain framework and introduces FANA-like 2′-fluoro sugar geometry from a FANA template. It then validates both inter-residue chain continuity and C2′–F2′ distances.

The benchmark shows successful candidate generation across inputs from **8 nt** to **111 nt**, with all tested outputs passing O3′→P chain-continuity validation and C2′–F2′ geometry validation.

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── fana_fragment_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 2KP4_FANA_10mer.pdb
    ├── outputs/
    │   ├── converted_fana_RNA-8mer_003A.pdb
    │   ├── converted_fana_RNA-12mer_003A.pdb
    │   ├── converted_fana_RNA-16mer_003A.pdb
    │   ├── converted_fana_RNA-22mer_003A.pdb
    │   ├── converted_fana_RNA-34mer_003A.pdb
    │   └── converted_fana_8t5o-HH-typeI-111mer-full_003A.pdb
    ├── reports/
    │   ├── conversion_report_RNA-8mer_003A.md
    │   ├── conversion_report_RNA-12mer_003A.md
    │   ├── conversion_report_RNA-16mer_003A.md
    │   ├── conversion_report_RNA-22mer_003A.md
    │   ├── conversion_report_RNA-34mer_003A.md
    │   └── conversion_report_8t5o-HH-typeI-111mer-full_003A.md
    └── benchmark_004_fana_chain_preserving_scaling_notes.md
```

---

## Files Included

This benchmark archives:

- **6 RNA input templates**
- **1 FANA template**
- **6 converted FANA-like candidate PDB outputs**
- **6 conversion reports**
- **1 benchmark evaluation note**
- optional screenshots from PyMOL / Discovery Studio visual inspection

---

## Input RNA Templates

All RNA templates are derived from the same HH-type I ribozyme source structure.

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

```text
2KP4_FANA_10mer.pdb
```

Template summary:

| Property | Value |
|---|---|
| Template length | 10 residues |
| Chain | A |
| Template sequence | `GCTATAATGG` |
| Observed residue names | `GFL`, `CFL`, `TAF`, `A5L` |
| Used as | FANA local sugar/substituent geometry donor |

The template contains FANA-like A, C, G, and T residue classes. RNA `U` residues are mapped to U/T-like FANA geometry while preserving RNA base identity by default.

---

## Method

Prototype 003A uses a **chain-preserving local reconstruction** strategy.

For each RNA residue:

1. determine the RNA base identity
2. select the best available FANA template residue
3. align FANA template anchor atoms to the RNA local frame using Kabsch alignment
4. preserve RNA chain-continuity atoms
5. preserve RNA nucleobase atoms
6. remove RNA O2′
7. introduce FANA-like C2′ and F2′ from the FANA template
8. export a FANA-like candidate residue
9. validate O3′→P, P→O5′, C1′→C2′, C2′→C3′, and C2′→F2′ geometry

Default anchor atoms:

```text
C1'
C3'
C4'
O4'
```

---

## Scaling Results

| Input | Converted residues | Chain status | C2′–F status | Mean anchor RMSD (Å) | Max anchor RMSD (Å) | Mean C2′–F (Å) | Max C2′–F (Å) |
|---|---:|---|---|---:|---:|---:|---:|
| `RNA-8mer` | 8 | `PASS` | `PASS` | 0.0477 | 0.0726 | 1.3822 | 1.3838 |
| `RNA-12mer` | 12 | `PASS` | `PASS` | 0.0508 | 0.0726 | 1.3822 | 1.3838 |
| `RNA-16mer` | 16 | `PASS` | `PASS` | 0.0514 | 0.0726 | 1.3819 | 1.3838 |
| `RNA-22mer` | 22 | `PASS` | `PASS` | 0.0551 | 0.0939 | 1.3819 | 1.3838 |
| `RNA-34mer` | 34 | `PASS` | `PASS` | 0.0535 | 0.0939 | 1.3822 | 1.3838 |
| `HH-111mer` | 111 | `PASS` | `PASS` | 0.0520 | 0.0955 | 1.3823 | 1.3838 |

Interpretation:

- All tested inputs ran successfully.
- Chain-continuity validation passed for all tested outputs.
- C2′–F2′ validation passed for all tested outputs.
- Mean C2′–F2′ distances were consistently near 1.382 Å.
- Visual inspection in PyMOL and Discovery Studio showed coherent chain-like structures without obvious residue explosion.

---

## Scientific Interpretation

This benchmark should be interpreted as:

> successful generation of FANA-like computational candidate structures using chain-preserving local reconstruction.

It should **not** be interpreted as:

> experimentally validated FANA structures or MD-ready FANA polymers.

The outputs are useful for:

- testing chain-preserving RNA → FANA reconstruction
- benchmarking short-to-long input scaling
- comparing visual coherence across PyMOL and Discovery Studio
- validating whether the converter avoids the ANA 002A.1 chain-continuity failure
- defining the next stage of Digital Polymerase converter development

The outputs are not yet suitable for:

- biological function claims
- force-field simulation without parameter/topology inspection
- publication-level structural claims without minimization and expert validation
- claims of FANA ribozyme activity, stability, or replication

---

## Relationship to Earlier Benchmarks

Benchmark 004 builds directly on earlier Digital Polymerase lessons:

```text
Prototype 001: RNA → HNA short-mer template-guided reconstruction
Benchmark 002: HH ribozyme RNA → HNA scaling failure
Prototype 002A: RNA → ANA residue-local fragment-guided reconstruction
Patch 002A.1: ANA chain-continuity validation
Patch 002A.2: ANA chain-preserving reconstruction
Prototype 003A: RNA → FANA chain-preserving reconstruction
Benchmark 004: FANA scaling benchmark
```

The key lesson carried into FANA was:

```text
Do not sacrifice chain continuity for local XNA geometry.
```

---

## Recommended Next Actions

1. Keep Benchmark 004 as a successful candidate-generation benchmark.
2. Add screenshots from PyMOL and Discovery Studio when available.
3. Preserve generated reports for all six RNA input sizes.
4. Add or refine topology/connectivity support in future versions.
5. Consider force-field and minimization workflow compatibility.
6. Proceed to the next XNA target only using the chain-preserving logic as default.

---

## Recommended Commit Message

```bash
git add src/digital_polymerase/prototypes/rna_to_fana_fragment_guided.py
git add benchmarks/fana_fragment_scaling/
git add docs/prototype_003A_rna_to_fana_fragment_guided.md
git commit -m "Add chain-preserving RNA-to-FANA prototype and benchmark"
```
