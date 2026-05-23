# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A.1  
**Method:** Fragment-guided RNA → ANA candidate reconstruction with chain-continuity validation  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `FAIL`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- ANA fragment template PDB: `/mnt/data/1ho6_ANApart.pdb`
- Output PDB: `/mnt/data/ana_patch_002A1_test_outputs/converted_ana_34mer_patched.pdb`

---

## Source Sequence

```text
GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC
```

---

## Template Index

The ANA template is shorter than the RNA input, so template residues are used as local geometry donors.

- `C` → `CAR` at chain `A`, residue `11`
- `G` → `GAO` at chain `A`, residue `9`
- `U` → `UAR` at chain `A`, residue `10`

---

## Method Summary

This prototype uses a local ANA fragment as a residue-level backbone geometry donor.

For each RNA residue:

1. determine source RNA base identity
2. select the best available ANA template residue
3. align ANA template anchor atoms onto RNA anchor atoms using Kabsch alignment
4. transform the ANA backbone into the RNA local frame
5. preserve RNA nucleobase atoms in their original coordinates
6. combine transformed ANA backbone + preserved RNA base atoms
7. export an ANA-like candidate residue
8. validate inter-residue chain continuity in the generated output

This is **not** a full-template reconstruction because the ANA template contains only 4 residues.

Patch 002A.1 adds chain-continuity validation, but it does **not** yet fix broken chain geometry.

---

## Settings

- Anchor atoms: `C1', C2', C3', C4', O4'`
- Pin C1' after alignment: `True`
- Residue naming policy: `template-observed`
- Skip residue-numbering gaps in inter-residue validation: `True`

---

## Alignment Summary

- Converted residues: `34`
- Mean anchor RMSD: `0.3047 Å`
- Maximum anchor RMSD: `0.3562 Å`

Important:

> Anchor RMSD measures local residue-frame alignment only. It does not prove polymer-chain continuity.

---

## Chain-Continuity Validation

The patch evaluates whether the generated output preserves basic covalent-distance plausibility.

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| O3'(i)→P(i+1) | source | 33 | 0 | 0 | 1.606 | 1.603 | 1.610 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 33 | 0 | 31 | 2.968 | 0.847 | 6.349 | 1.40–1.80 | FAIL |
| P(i)→O5'(i) | source | 34 | 0 | 0 | 1.591 | 1.588 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 34 | 0 | 0 | 1.611 | 1.611 | 1.612 | 1.40–1.80 | PASS |

### Worst output O3′–P links

| Rank | Link | Distance (Å) | Expected range (Å) | Status | Note |
|---:|---|---:|---|---|---|
| 1 | `A83:O3' → A84:P` | 6.349 | 1.40–1.80 | FAIL |  |
| 2 | `A56:O3' → A57:P` | 5.615 | 1.40–1.80 | FAIL |  |
| 3 | `A77:O3' → A78:P` | 5.302 | 1.40–1.80 | FAIL |  |
| 4 | `A75:O3' → A76:P` | 4.984 | 1.40–1.80 | FAIL |  |
| 5 | `A55:O3' → A56:P` | 4.753 | 1.40–1.80 | FAIL |  |
| 6 | `A61:O3' → A62:P` | 4.073 | 1.40–1.80 | FAIL |  |
| 7 | `A81:O3' → A82:P` | 3.585 | 1.40–1.80 | FAIL |  |
| 8 | `A70:O3' → A71:P` | 3.514 | 1.40–1.80 | FAIL |  |
| 9 | `A71:O3' → A72:P` | 3.330 | 1.40–1.80 | FAIL |  |
| 10 | `A86:O3' → A87:P` | 3.260 | 1.40–1.80 | FAIL |  |
| 11 | `A76:O3' → A77:P` | 2.951 | 1.40–1.80 | FAIL |  |
| 12 | `A85:O3' → A86:P` | 2.872 | 1.40–1.80 | FAIL |  |
| 13 | `A74:O3' → A75:P` | 2.850 | 1.40–1.80 | FAIL |  |
| 14 | `A60:O3' → A61:P` | 2.844 | 1.40–1.80 | FAIL |  |
| 15 | `A79:O3' → A80:P` | 2.836 | 1.40–1.80 | FAIL |  |
| 16 | `A72:O3' → A73:P` | 2.808 | 1.40–1.80 | FAIL |  |
| 17 | `A59:O3' → A60:P` | 2.696 | 1.40–1.80 | FAIL |  |
| 18 | `A69:O3' → A70:P` | 2.673 | 1.40–1.80 | FAIL |  |
| 19 | `A67:O3' → A68:P` | 2.655 | 1.40–1.80 | FAIL |  |
| 20 | `A68:O3' → A69:P` | 2.616 | 1.40–1.80 | FAIL |  |

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A54 | G | GAO | GAO A9 | 0.3227 | exact base-class template |
| 2 | A55 | G | GAO | GAO A9 | 0.3231 | exact base-class template |
| 3 | A56 | U | UAR | UAR A10 | 0.3274 | exact base-class template |
| 4 | A57 | G | GAO | GAO A9 | 0.3045 | exact base-class template |
| 5 | A58 | A | AAR | GAO A9 | 0.3137 | purine fallback: A uses G-like ANA backbone template |
| 6 | A59 | A | AAR | GAO A9 | 0.3080 | purine fallback: A uses G-like ANA backbone template |
| 7 | A60 | G | GAO | GAO A9 | 0.3366 | exact base-class template |
| 8 | A61 | A | AAR | GAO A9 | 0.3240 | purine fallback: A uses G-like ANA backbone template |
| 9 | A62 | A | AAR | GAO A9 | 0.1559 | purine fallback: A uses G-like ANA backbone template |
| 10 | A63 | U | UAR | UAR A10 | 0.1821 | exact base-class template |
| 11 | A64 | A | AAR | GAO A9 | 0.3106 | purine fallback: A uses G-like ANA backbone template |
| 12 | A65 | C | CAR | CAR A11 | 0.1552 | exact base-class template |
| 13 | A66 | G | GAO | GAO A9 | 0.1621 | exact base-class template |
| 14 | A67 | A | AAR | GAO A9 | 0.3215 | purine fallback: A uses G-like ANA backbone template |
| 15 | A68 | C | CAR | CAR A11 | 0.3288 | exact base-class template |
| 16 | A69 | C | CAR | CAR A11 | 0.3306 | exact base-class template |
| 17 | A70 | A | AAR | GAO A9 | 0.3166 | purine fallback: A uses G-like ANA backbone template |
| 18 | A71 | C | CAR | CAR A11 | 0.3287 | exact base-class template |
| 19 | A72 | C | CAR | CAR A11 | 0.3313 | exact base-class template |
| 20 | A73 | U | UAR | UAR A10 | 0.2972 | exact base-class template |
| 21 | A74 | A | AAR | GAO A9 | 0.3154 | purine fallback: A uses G-like ANA backbone template |
| 22 | A75 | G | GAO | GAO A9 | 0.3038 | exact base-class template |
| 23 | A76 | G | GAO | GAO A9 | 0.3309 | exact base-class template |
| 24 | A77 | C | CAR | CAR A11 | 0.3203 | exact base-class template |
| 25 | A78 | U | UAR | UAR A10 | 0.3562 | exact base-class template |
| 26 | A79 | C | CAR | CAR A11 | 0.3358 | exact base-class template |
| 27 | A80 | G | GAO | GAO A9 | 0.3195 | exact base-class template |
| 28 | A81 | A | AAR | GAO A9 | 0.3193 | purine fallback: A uses G-like ANA backbone template |
| 29 | A82 | A | AAR | GAO A9 | 0.3413 | purine fallback: A uses G-like ANA backbone template |
| 30 | A83 | A | AAR | GAO A9 | 0.3277 | purine fallback: A uses G-like ANA backbone template |
| 31 | A84 | G | GAO | GAO A9 | 0.3182 | exact base-class template |
| 32 | A85 | A | AAR | GAO A9 | 0.3372 | purine fallback: A uses G-like ANA backbone template |
| 33 | A86 | G | GAO | GAO A9 | 0.3190 | exact base-class template |
| 34 | A87 | C | CAR | CAR A11 | 0.3359 | exact base-class template |

---

## Scientific Interpretation

This output should be interpreted as:

> an ANA-like candidate structure generated using fragment-guided local backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed ANA structure.

If chain-continuity status is `FAIL`, the structure should also **not** be interpreted as a continuous ANA polymer.

---

## Important Limitations

- The ANA template contains only a 4-mer fragment.
- A-like ANA geometry is absent in the uploaded template; A residues may use a purine fallback template.
- RNA nucleobase atoms are preserved, but backbone geometry is template-derived.
- Patch 002A.1 reports chain-continuity problems but does not correct them.
- The output is not energy-minimized.
- No force-field parameters are generated.
- Connectivity is not explicitly written with `CONECT` records.
- Molecular viewers may infer nonstandard residue bonds differently.
- Residue names are provisional and may need adjustment for downstream tools.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect the output in PyMOL, ChimeraX, VMD, or Mol*.
2. Check residue completeness and atom naming.
3. Inspect base-backbone attachment geometry.
4. Check bond lengths, angles, torsions, and clashes.
5. Review the O3′–P chain-continuity table.
6. Compare local ANA backbone geometry with the original 4-mer ANA template.
7. Add explicit connectivity records or topology files in future versions.
8. Implement fragment-chain reconstruction or chain-aware coordinate correction.
9. Perform energy minimization with appropriate force-field support.

---

## Development Note

This patch marks a transition from:

```text
low local RMSD = looks promising
```

to:

```text
low local RMSD + chain-continuity validation = more honest structural assessment
```

The next Digital Polymerase requirement is chain-aware reconstruction.
