# Benchmark 003: RNA → ANA Fragment-Guided Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 003  
**Prototype tested:** Prototype 002A — RNA → ANA fragment-guided reconstruction  
**Status:** Archived scaling benchmark / partial success with major chain-continuity limitation

---

## Summary

This benchmark tests whether the **RNA → ANA fragment-guided converter** can scale from a short 8-mer RNA to longer RNA structures.

The converter uses a **4-mer ANA fragment template** as a local residue-level backbone geometry donor. For each RNA residue, the script selects a matching or fallback ANA template residue, aligns local anchor atoms, transforms the ANA backbone into the RNA local frame, preserves the RNA nucleobase atoms, and exports an ANA-like candidate structure.

The benchmark shows that the method scales computationally from **8 nt** to **111 nt**, with stable local anchor RMSD values. However, it also reveals a major limitation: **inter-residue O3′–P chain continuity is not yet enforced**. Therefore, the outputs should be interpreted as residue-local ANA-like candidate structures, not validated ANA polymers.

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── ana_fragment_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 1ho6_ANApart.pdb
    ├── outputs/
    │   ├── converted_ana_8mer.pdb
    │   ├── converted_ana_12mer.pdb
    │   ├── converted_ana_16mer.pdb
    │   ├── converted_ana_22mer.pdb
    │   ├── converted_ana_34mer.pdb
    │   └── converted_ana_HH_111mer.pdb
    ├── reports/
    │   ├── conversion_report_8mer.md
    │   ├── conversion_report_12mer.md
    │   ├── conversion_report_16mer.md
    │   ├── conversion_report_22mer.md
    │   ├── conversion_report_34mer.md
    │   └── conversion_report_HH_111mer.md
    └── benchmark_003_ana_fragment_scaling_notes.md
```

---

## Files Included

This benchmark archives:

- **6 RNA input templates**
- **1 ANA fragment template**
- **6 converted ANA-like PDB outputs**
- **6 conversion reports**
- **1 benchmark evaluation note**

In practical terms:

```text
7 template/input PDB files
12 result files: 6 converted PDBs + 6 reports
2 documentation files: README.md + benchmark notes
```

---

## Input RNA Templates

All RNA templates were extracted from the same HH-type I ribozyme structure, then reduced into smaller fragments for scaling tests.

| File | Length | Residue range | Source sequence |
|---|---:|---|---|
| `RNA-8mer.pdb` | 8 nt | A:72–79 | `CUAGGCUC` |
| `RNA-12mer.pdb` | 12 nt | A:72–83 | `CUAGGCUCGAAA` |
| `RNA-16mer.pdb` | 16 nt | A:67–82 | `ACCACCUAGGCUCGAA` |
| `RNA-22mer.pdb` | 22 nt | A:62–83 | `AUACGACCACCUAGGCUCGAAA` |
| `RNA-34mer.pdb` | 34 nt | A:54–87 | `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC` |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 nt | A:5–117, with a gap between A112 and A115 | `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC` |

---

## ANA Template

| File | Length | Residue names | Notes |
|---|---:|---|---|
| `1ho6_ANApart.pdb` | 4 residues | `GAO`, `UAR`, `CAR`, `CAR` | Used as local ANA residue/backbone geometry donor |

The ANA template is shorter than the RNA input structures. Therefore, this benchmark does **not** perform full-template reconstruction. It performs **fragment-guided local reconstruction**.

---

## Conversion Method

For each RNA residue, the converter:

1. determines the source RNA base identity
2. selects the best available ANA template residue
3. aligns ANA template anchor atoms onto RNA anchor atoms using Kabsch alignment
4. transforms the ANA backbone into the RNA local frame
5. preserves RNA nucleobase atoms in their original coordinates
6. combines transformed ANA backbone atoms with preserved RNA base atoms
7. exports an ANA-like candidate residue

Anchor atoms used:

```text
C1'
C2'
C3'
C4'
O4'
```

The converter pins `C1'` after alignment to preserve the base attachment point.

---

## Template Selection Policy

The current template index is:

| Source RNA base | Output residue | ANA template used | Notes |
|---|---|---|---|
| `C` | `CAR` | `CAR A11` | exact base-class template |
| `G` | `GAO` | `GAO A9` | exact base-class template |
| `U` | `UAR` | `UAR A10` | exact base-class template |
| `A` | `AAR` | `GAO A9` | purine fallback because A-like ANA template is absent |

The absence of an A-like ANA template is an important limitation. Adenine residues currently use a **G-like purine fallback**.

---

## Scaling Results

### Local anchor alignment

| Input | Converted residues | Mean anchor RMSD | Max anchor RMSD |
|---|---:|---:|---:|
| `RNA-8mer.pdb` | 8 | 0.2036 Å | 0.2161 Å |
| `RNA-12mer.pdb` | 12 | 0.2048 Å | 0.2161 Å |
| `RNA-16mer.pdb` | 16 | 0.2046 Å | 0.2161 Å |
| `RNA-22mer.pdb` | 22 | 0.1962 Å | 0.2161 Å |
| `RNA-34mer.pdb` | 34 | 0.1989 Å | 0.2161 Å |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 | 0.1961 Å | 0.2161 Å |

Interpretation:

- The local anchor alignment remains stable across fragment size.
- The converter does not computationally collapse when scaling from 8 nt to 111 nt.
- These RMSD values describe **intra-residue local alignment only**.

---

## Chain-Continuity Evaluation

A separate structural evaluation was performed on the converted PDB outputs by measuring inter-residue `O3′(i) → P(i+1)` distances.

For a normal phosphodiester-like RNA backbone, these distances are expected to be approximately:

```text
~1.6 Å
```

The source RNA templates had normal O3′–P connectivity, but the converted ANA-like outputs showed strong inter-residue distortion.

| Output | Mean O3′–P | Min O3′–P | Max O3′–P | Failed links |
|---|---:|---:|---:|---:|
| `converted_ana_8mer.pdb` | 3.203 Å | 0.935 Å | 5.303 Å | 7 / 7 |
| `converted_ana_12mer.pdb` | 2.793 Å | 0.847 Å | 5.303 Å | 11 / 11 |
| `converted_ana_16mer.pdb` | 2.965 Å | 0.847 Å | 5.303 Å | 15 / 15 |
| `converted_ana_22mer.pdb` | 2.635 Å | 0.847 Å | 5.303 Å | 19 / 21 |
| `converted_ana_34mer.pdb` | 2.968 Å | 0.847 Å | 6.350 Å | 31 / 33 |
| `converted_ana_HH_111mer.pdb` | 3.045 Å | 0.847 Å | 6.350 Å | 103 / 109 |

Interpretation:

- The residue-local reconstruction succeeds locally but fails to enforce polymer-chain continuity.
- The current outputs should not be treated as valid covalently continuous ANA polymers.
- A chain-aware reconstruction or validation module is required before physical modeling.

---

## Scientific Interpretation

This benchmark should be interpreted as:

> a residue-local RNA → ANA fragment-guided scaling test.

It should **not** be interpreted as:

> a validated RNA → ANA polymer conversion workflow.

The outputs are useful for:

- testing parser scalability
- testing residue-level Kabsch alignment
- testing report generation
- identifying failure modes
- defining the next algorithmic requirement

The outputs are **not** suitable for:

- claiming ANA structural validity
- molecular dynamics without correction
- force-field simulation as-is
- functional interpretation
- biological claims about ANA ribozymes or ANA stability

---

## Main Lesson

The benchmark reveals the next required Digital Polymerase module:

```text
chain-continuity validation
```

The next patch should add inter-residue O3′–P checks directly into the converter report.

After that, the next algorithmic step should move from:

```text
residue-local reconstruction
```

to:

```text
fragment-chain reconstruction
```

where connected ANA fragments are aligned and stitched with continuity constraints.

---

## Recommended Next Actions

1. Keep this benchmark in the repository as an archived partial-success/failure case.
2. Add chain-continuity metrics to the converter report.
3. Patch the ANA converter before progressing to FANA.
4. Avoid interpreting current ANA outputs as MD-ready structures.
5. Use this benchmark as a regression test for future chain-aware reconstruction.

---

## Related Files

Suggested related documentation:

```text
docs/prototype_002A_rna_to_ana_fragment_guided.md
benchmarks/ana_fragment_scaling/benchmark_003_ana_fragment_scaling_notes.md
```

Suggested related script:

```text
src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py
```

---

## Recommended Commit Message

```bash
git add benchmarks/ana_fragment_scaling/
git commit -m "Add ANA fragment-guided scaling benchmark"
```
