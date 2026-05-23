# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A.1  
**Method:** Fragment-guided RNA → ANA candidate reconstruction with chain-continuity validation  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `FAIL`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- ANA fragment template PDB: `/mnt/data/1ho6_ANApart.pdb`
- Output PDB: `/mnt/data/ana_patch_002A1_test_outputs/converted_ana_HH_111mer_patched.pdb`

---

## Source Sequence

```text
GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
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

- Converted residues: `111`
- Mean anchor RMSD: `0.2994 Å`
- Maximum anchor RMSD: `0.3562 Å`

Important:

> Anchor RMSD measures local residue-frame alignment only. It does not prove polymer-chain continuity.

---

## Chain-Continuity Validation

The patch evaluates whether the generated output preserves basic covalent-distance plausibility.

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| O3'(i)→P(i+1) | source | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 109 | 0 | 103 | 3.045 | 0.847 | 6.349 | 1.40–1.80 | FAIL |
| P(i)→O5'(i) | source | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 111 | 0 | 0 | 1.611 | 1.611 | 1.612 | 1.40–1.80 | PASS |

### Worst output O3′–P links

| Rank | Link | Distance (Å) | Expected range (Å) | Status | Note |
|---:|---|---:|---|---|---|
| 1 | `A83:O3' → A84:P` | 6.349 | 1.40–1.80 | FAIL |  |
| 2 | `A106:O3' → A107:P` | 6.104 | 1.40–1.80 | FAIL |  |
| 3 | `A103:O3' → A104:P` | 5.663 | 1.40–1.80 | FAIL |  |
| 4 | `A56:O3' → A57:P` | 5.615 | 1.40–1.80 | FAIL |  |
| 5 | `A10:O3' → A11:P` | 5.591 | 1.40–1.80 | FAIL |  |
| 6 | `A107:O3' → A108:P` | 5.461 | 1.40–1.80 | FAIL |  |
| 7 | `A77:O3' → A78:P` | 5.302 | 1.40–1.80 | FAIL |  |
| 8 | `A31:O3' → A32:P` | 5.302 | 1.40–1.80 | FAIL |  |
| 9 | `A95:O3' → A96:P` | 5.167 | 1.40–1.80 | FAIL |  |
| 10 | `A41:O3' → A42:P` | 5.062 | 1.40–1.80 | FAIL |  |
| 11 | `A75:O3' → A76:P` | 4.984 | 1.40–1.80 | FAIL |  |
| 12 | `A19:O3' → A20:P` | 4.834 | 1.40–1.80 | FAIL |  |
| 13 | `A111:O3' → A112:P` | 4.771 | 1.40–1.80 | FAIL |  |
| 14 | `A29:O3' → A30:P` | 4.769 | 1.40–1.80 | FAIL |  |
| 15 | `A55:O3' → A56:P` | 4.753 | 1.40–1.80 | FAIL |  |
| 16 | `A8:O3' → A9:P` | 4.705 | 1.40–1.80 | FAIL |  |
| 17 | `A38:O3' → A39:P` | 4.562 | 1.40–1.80 | FAIL |  |
| 18 | `A11:O3' → A12:P` | 4.201 | 1.40–1.80 | FAIL |  |
| 19 | `A61:O3' → A62:P` | 4.073 | 1.40–1.80 | FAIL |  |
| 20 | `A14:O3' → A15:P` | 3.704 | 1.40–1.80 | FAIL |  |

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A5 | G | GAO | GAO A9 | 0.3032 | exact base-class template |
| 2 | A6 | G | GAO | GAO A9 | 0.3215 | exact base-class template |
| 3 | A7 | U | UAR | UAR A10 | 0.3084 | exact base-class template |
| 4 | A8 | G | GAO | GAO A9 | 0.3229 | exact base-class template |
| 5 | A9 | C | CAR | CAR A11 | 0.3522 | exact base-class template |
| 6 | A10 | A | AAR | GAO A9 | 0.3293 | purine fallback: A uses G-like ANA backbone template |
| 7 | A11 | G | GAO | GAO A9 | 0.3131 | exact base-class template |
| 8 | A12 | G | GAO | GAO A9 | 0.3147 | exact base-class template |
| 9 | A13 | U | UAR | UAR A10 | 0.3191 | exact base-class template |
| 10 | A14 | A | AAR | GAO A9 | 0.3062 | purine fallback: A uses G-like ANA backbone template |
| 11 | A15 | C | CAR | CAR A11 | 0.1713 | exact base-class template |
| 12 | A16 | A | AAR | GAO A9 | 0.3164 | purine fallback: A uses G-like ANA backbone template |
| 13 | A17 | U | UAR | UAR A10 | 0.3109 | exact base-class template |
| 14 | A18 | C | CAR | CAR A11 | 0.3222 | exact base-class template |
| 15 | A19 | C | CAR | CAR A11 | 0.3185 | exact base-class template |
| 16 | A20 | A | AAR | GAO A9 | 0.3283 | purine fallback: A uses G-like ANA backbone template |
| 17 | A21 | G | GAO | GAO A9 | 0.2903 | exact base-class template |
| 18 | A22 | C | CAR | CAR A11 | 0.1675 | exact base-class template |
| 19 | A23 | U | UAR | UAR A10 | 0.3026 | exact base-class template |
| 20 | A24 | G | GAO | GAO A9 | 0.2811 | exact base-class template |
| 21 | A25 | A | AAR | GAO A9 | 0.3144 | purine fallback: A uses G-like ANA backbone template |
| 22 | A26 | U | UAR | UAR A10 | 0.1750 | exact base-class template |
| 23 | A27 | G | GAO | GAO A9 | 0.3120 | exact base-class template |
| 24 | A28 | A | AAR | GAO A9 | 0.3147 | purine fallback: A uses G-like ANA backbone template |
| 25 | A29 | G | GAO | GAO A9 | 0.3118 | exact base-class template |
| 26 | A30 | U | UAR | UAR A10 | 0.3139 | exact base-class template |
| 27 | A31 | C | CAR | CAR A11 | 0.3319 | exact base-class template |
| 28 | A32 | C | CAR | CAR A11 | 0.3154 | exact base-class template |
| 29 | A33 | C | CAR | CAR A11 | 0.3200 | exact base-class template |
| 30 | A34 | A | AAR | GAO A9 | 0.3227 | purine fallback: A uses G-like ANA backbone template |
| 31 | A35 | A | AAR | GAO A9 | 0.1529 | purine fallback: A uses G-like ANA backbone template |
| 32 | A36 | A | AAR | GAO A9 | 0.1645 | purine fallback: A uses G-like ANA backbone template |
| 33 | A37 | U | UAR | UAR A10 | 0.3035 | exact base-class template |
| 34 | A38 | A | AAR | GAO A9 | 0.1653 | purine fallback: A uses G-like ANA backbone template |
| 35 | A39 | G | GAO | GAO A9 | 0.3360 | exact base-class template |
| 36 | A40 | G | GAO | GAO A9 | 0.3119 | exact base-class template |
| 37 | A41 | A | AAR | GAO A9 | 0.3059 | purine fallback: A uses G-like ANA backbone template |
| 38 | A42 | C | CAR | CAR A11 | 0.3315 | exact base-class template |
| 39 | A43 | A | AAR | GAO A9 | 0.3185 | purine fallback: A uses G-like ANA backbone template |
| 40 | A44 | A | AAR | GAO A9 | 0.3097 | purine fallback: A uses G-like ANA backbone template |
| 41 | A45 | A | AAR | GAO A9 | 0.3192 | purine fallback: A uses G-like ANA backbone template |
| 42 | A46 | A | AAR | GAO A9 | 0.3232 | purine fallback: A uses G-like ANA backbone template |
| 43 | A47 | A | AAR | GAO A9 | 0.3206 | purine fallback: A uses G-like ANA backbone template |
| 44 | A48 | G | GAO | GAO A9 | 0.3079 | exact base-class template |
| 45 | A49 | G | GAO | GAO A9 | 0.3113 | exact base-class template |
| 46 | A50 | G | GAO | GAO A9 | 0.3082 | exact base-class template |
| 47 | A51 | A | AAR | GAO A9 | 0.3238 | purine fallback: A uses G-like ANA backbone template |
| 48 | A52 | G | GAO | GAO A9 | 0.3011 | exact base-class template |
| 49 | A53 | A | AAR | GAO A9 | 0.3152 | purine fallback: A uses G-like ANA backbone template |
| 50 | A54 | G | GAO | GAO A9 | 0.3227 | exact base-class template |
| 51 | A55 | G | GAO | GAO A9 | 0.3231 | exact base-class template |
| 52 | A56 | U | UAR | UAR A10 | 0.3274 | exact base-class template |
| 53 | A57 | G | GAO | GAO A9 | 0.3045 | exact base-class template |
| 54 | A58 | A | AAR | GAO A9 | 0.3137 | purine fallback: A uses G-like ANA backbone template |
| 55 | A59 | A | AAR | GAO A9 | 0.3080 | purine fallback: A uses G-like ANA backbone template |
| 56 | A60 | G | GAO | GAO A9 | 0.3366 | exact base-class template |
| 57 | A61 | A | AAR | GAO A9 | 0.3240 | purine fallback: A uses G-like ANA backbone template |
| 58 | A62 | A | AAR | GAO A9 | 0.1559 | purine fallback: A uses G-like ANA backbone template |
| 59 | A63 | U | UAR | UAR A10 | 0.1821 | exact base-class template |
| 60 | A64 | A | AAR | GAO A9 | 0.3106 | purine fallback: A uses G-like ANA backbone template |
| 61 | A65 | C | CAR | CAR A11 | 0.1552 | exact base-class template |
| 62 | A66 | G | GAO | GAO A9 | 0.1621 | exact base-class template |
| 63 | A67 | A | AAR | GAO A9 | 0.3215 | purine fallback: A uses G-like ANA backbone template |
| 64 | A68 | C | CAR | CAR A11 | 0.3288 | exact base-class template |
| 65 | A69 | C | CAR | CAR A11 | 0.3306 | exact base-class template |
| 66 | A70 | A | AAR | GAO A9 | 0.3166 | purine fallback: A uses G-like ANA backbone template |
| 67 | A71 | C | CAR | CAR A11 | 0.3287 | exact base-class template |
| 68 | A72 | C | CAR | CAR A11 | 0.3313 | exact base-class template |
| 69 | A73 | U | UAR | UAR A10 | 0.2972 | exact base-class template |
| 70 | A74 | A | AAR | GAO A9 | 0.3154 | purine fallback: A uses G-like ANA backbone template |
| 71 | A75 | G | GAO | GAO A9 | 0.3038 | exact base-class template |
| 72 | A76 | G | GAO | GAO A9 | 0.3309 | exact base-class template |
| 73 | A77 | C | CAR | CAR A11 | 0.3203 | exact base-class template |
| 74 | A78 | U | UAR | UAR A10 | 0.3562 | exact base-class template |
| 75 | A79 | C | CAR | CAR A11 | 0.3358 | exact base-class template |
| 76 | A80 | G | GAO | GAO A9 | 0.3195 | exact base-class template |
| 77 | A81 | A | AAR | GAO A9 | 0.3193 | purine fallback: A uses G-like ANA backbone template |
| 78 | A82 | A | AAR | GAO A9 | 0.3413 | purine fallback: A uses G-like ANA backbone template |
| 79 | A83 | A | AAR | GAO A9 | 0.3277 | purine fallback: A uses G-like ANA backbone template |
| 80 | A84 | G | GAO | GAO A9 | 0.3182 | exact base-class template |
| 81 | A85 | A | AAR | GAO A9 | 0.3372 | purine fallback: A uses G-like ANA backbone template |
| 82 | A86 | G | GAO | GAO A9 | 0.3190 | exact base-class template |
| 83 | A87 | C | CAR | CAR A11 | 0.3359 | exact base-class template |
| 84 | A88 | C | CAR | CAR A11 | 0.3285 | exact base-class template |
| 85 | A89 | U | UAR | UAR A10 | 0.3152 | exact base-class template |
| 86 | A90 | A | AAR | GAO A9 | 0.3103 | purine fallback: A uses G-like ANA backbone template |
| 87 | A91 | A | AAR | GAO A9 | 0.3117 | purine fallback: A uses G-like ANA backbone template |
| 88 | A92 | A | AAR | GAO A9 | 0.1611 | purine fallback: A uses G-like ANA backbone template |
| 89 | A93 | A | AAR | GAO A9 | 0.3134 | purine fallback: A uses G-like ANA backbone template |
| 90 | A94 | C | CAR | CAR A11 | 0.3277 | exact base-class template |
| 91 | A95 | A | AAR | GAO A9 | 0.3160 | purine fallback: A uses G-like ANA backbone template |
| 92 | A96 | U | UAR | UAR A10 | 0.3110 | exact base-class template |
| 93 | A97 | A | AAR | GAO A9 | 0.3274 | purine fallback: A uses G-like ANA backbone template |
| 94 | A98 | C | CAR | CAR A11 | 0.3216 | exact base-class template |
| 95 | A99 | C | CAR | CAR A11 | 0.3202 | exact base-class template |
| 96 | A100 | U | UAR | UAR A10 | 0.3121 | exact base-class template |
| 97 | A101 | U | UAR | UAR A10 | 0.3127 | exact base-class template |
| 98 | A102 | U | UAR | UAR A10 | 0.3010 | exact base-class template |
| 99 | A103 | C | CAR | CAR A11 | 0.1665 | exact base-class template |
| 100 | A104 | C | CAR | CAR A11 | 0.3184 | exact base-class template |
| 101 | A105 | U | UAR | UAR A10 | 0.3170 | exact base-class template |
| 102 | A106 | G | GAO | GAO A9 | 0.3103 | exact base-class template |
| 103 | A107 | G | GAO | GAO A9 | 0.3209 | exact base-class template |
| 104 | A108 | A | AAR | GAO A9 | 0.3331 | purine fallback: A uses G-like ANA backbone template |
| 105 | A109 | U | UAR | UAR A10 | 0.3018 | exact base-class template |
| 106 | A110 | U | UAR | UAR A10 | 0.1775 | exact base-class template |
| 107 | A111 | C | CAR | CAR A11 | 0.3240 | exact base-class template |
| 108 | A112 | C | CAR | CAR A11 | 0.3362 | exact base-class template |
| 109 | A115 | U | UAR | UAR A10 | 0.3175 | exact base-class template |
| 110 | A116 | G | GAO | GAO A9 | 0.3232 | exact base-class template |
| 111 | A117 | C | CAR | CAR A11 | 0.1703 | exact base-class template |

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
