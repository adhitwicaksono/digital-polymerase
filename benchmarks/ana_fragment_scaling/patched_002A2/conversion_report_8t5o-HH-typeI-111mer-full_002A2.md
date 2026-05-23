# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A.1  
**Method:** Fragment-guided RNA → ANA candidate reconstruction with chain-preserving mode and chain-continuity validation  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- ANA fragment template PDB: `/mnt/data/1ho6_ANApart.pdb`
- Output PDB: `/mnt/data/ana_patch_002A2_outputs/converted_ana_8t5o-HH-typeI-111mer-full_002A2.pdb`

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
4. reconstruct the candidate residue according to the selected mode
5. preserve RNA nucleobase atoms in their original coordinates
6. export an ANA-like candidate residue
7. validate inter-residue chain continuity in the generated output

This is **not** a full-template reconstruction because the ANA template contains only 4 residues.

Patch 002A.2 adds `ana-chain-preserving` mode. In this mode, the source RNA chain atoms are preserved to maintain polymer continuity, while ANA-sensitive local atoms such as C2′/O2′ are taken from the aligned ANA template. This improves chain-continuity behavior but still does **not** create an experimentally validated ANA structure.

---

## Settings

- Conversion mode: `ana-chain-preserving`
- Anchor atoms: `C1', C3', C4', O4'`
- Pin C1' after alignment: `True`
- Residue naming policy: `template-observed`
- Skip residue-numbering gaps in inter-residue validation: `True`

---

## Alignment Summary

- Converted residues: `111`
- Mean anchor RMSD: `0.0489 Å`
- Maximum anchor RMSD: `0.1414 Å`

Important:

> Anchor RMSD measures local residue-frame alignment only. It does not prove polymer-chain continuity.

---

## Chain-Continuity Validation

The patch evaluates whether the generated output preserves basic covalent-distance plausibility.

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| O3'(i)→P(i+1) | source | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |

### Worst output O3′–P links

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A5 | G | GAO | GAO A9 | 0.0270 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 2 | A6 | G | GAO | GAO A9 | 0.0338 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 3 | A7 | U | UAR | UAR A10 | 0.0437 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 4 | A8 | G | GAO | GAO A9 | 0.0372 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 5 | A9 | C | CAR | CAR A11 | 0.0585 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 6 | A10 | A | AAR | GAO A9 | 0.0399 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 7 | A11 | G | GAO | GAO A9 | 0.0351 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 8 | A12 | G | GAO | GAO A9 | 0.0344 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 9 | A13 | U | UAR | UAR A10 | 0.0474 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 10 | A14 | A | AAR | GAO A9 | 0.0287 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 11 | A15 | C | CAR | CAR A11 | 0.1412 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 12 | A16 | A | AAR | GAO A9 | 0.0315 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 13 | A17 | U | UAR | UAR A10 | 0.0445 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 14 | A18 | C | CAR | CAR A11 | 0.0404 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 15 | A19 | C | CAR | CAR A11 | 0.0399 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 16 | A20 | A | AAR | GAO A9 | 0.0363 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 17 | A21 | G | GAO | GAO A9 | 0.0244 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 18 | A22 | C | CAR | CAR A11 | 0.1295 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 19 | A23 | U | UAR | UAR A10 | 0.0400 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 20 | A24 | G | GAO | GAO A9 | 0.0235 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 21 | A25 | A | AAR | GAO A9 | 0.0321 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 22 | A26 | U | UAR | UAR A10 | 0.1316 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 23 | A27 | G | GAO | GAO A9 | 0.0343 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 24 | A28 | A | AAR | GAO A9 | 0.0322 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 25 | A29 | G | GAO | GAO A9 | 0.0328 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 26 | A30 | U | UAR | UAR A10 | 0.0479 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 27 | A31 | C | CAR | CAR A11 | 0.0435 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 28 | A32 | C | CAR | CAR A11 | 0.0379 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 29 | A33 | C | CAR | CAR A11 | 0.0383 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 30 | A34 | A | AAR | GAO A9 | 0.0335 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 31 | A35 | A | AAR | GAO A9 | 0.1269 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 32 | A36 | A | AAR | GAO A9 | 0.1207 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 33 | A37 | U | UAR | UAR A10 | 0.0423 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 34 | A38 | A | AAR | GAO A9 | 0.1265 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 35 | A39 | G | GAO | GAO A9 | 0.0368 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 36 | A40 | G | GAO | GAO A9 | 0.0279 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 37 | A41 | A | AAR | GAO A9 | 0.0283 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 38 | A42 | C | CAR | CAR A11 | 0.0470 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 39 | A43 | A | AAR | GAO A9 | 0.0320 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 40 | A44 | A | AAR | GAO A9 | 0.0306 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 41 | A45 | A | AAR | GAO A9 | 0.0348 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 42 | A46 | A | AAR | GAO A9 | 0.0357 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 43 | A47 | A | AAR | GAO A9 | 0.0313 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 44 | A48 | G | GAO | GAO A9 | 0.0273 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 45 | A49 | G | GAO | GAO A9 | 0.0282 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 46 | A50 | G | GAO | GAO A9 | 0.0288 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 47 | A51 | A | AAR | GAO A9 | 0.0311 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 48 | A52 | G | GAO | GAO A9 | 0.0263 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 49 | A53 | A | AAR | GAO A9 | 0.0357 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 50 | A54 | G | GAO | GAO A9 | 0.0347 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 51 | A55 | G | GAO | GAO A9 | 0.0364 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 52 | A56 | U | UAR | UAR A10 | 0.0553 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 53 | A57 | G | GAO | GAO A9 | 0.0288 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 54 | A58 | A | AAR | GAO A9 | 0.0312 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 55 | A59 | A | AAR | GAO A9 | 0.0301 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 56 | A60 | G | GAO | GAO A9 | 0.0406 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 57 | A61 | A | AAR | GAO A9 | 0.0335 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 58 | A62 | A | AAR | GAO A9 | 0.1212 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 59 | A63 | U | UAR | UAR A10 | 0.1377 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 60 | A64 | A | AAR | GAO A9 | 0.0324 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 61 | A65 | C | CAR | CAR A11 | 0.1362 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 62 | A66 | G | GAO | GAO A9 | 0.1179 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 63 | A67 | A | AAR | GAO A9 | 0.0355 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 64 | A68 | C | CAR | CAR A11 | 0.0484 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 65 | A69 | C | CAR | CAR A11 | 0.0422 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 66 | A70 | A | AAR | GAO A9 | 0.0296 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 67 | A71 | C | CAR | CAR A11 | 0.0385 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 68 | A72 | C | CAR | CAR A11 | 0.0394 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 69 | A73 | U | UAR | UAR A10 | 0.0326 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 70 | A74 | A | AAR | GAO A9 | 0.0287 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 71 | A75 | G | GAO | GAO A9 | 0.0265 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 72 | A76 | G | GAO | GAO A9 | 0.0369 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 73 | A77 | C | CAR | CAR A11 | 0.0448 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 74 | A78 | U | UAR | UAR A10 | 0.0644 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 75 | A79 | C | CAR | CAR A11 | 0.0524 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 76 | A80 | G | GAO | GAO A9 | 0.0331 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 77 | A81 | A | AAR | GAO A9 | 0.0346 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 78 | A82 | A | AAR | GAO A9 | 0.0398 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 79 | A83 | A | AAR | GAO A9 | 0.0329 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 80 | A84 | G | GAO | GAO A9 | 0.0336 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 81 | A85 | A | AAR | GAO A9 | 0.0395 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 82 | A86 | G | GAO | GAO A9 | 0.0308 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 83 | A87 | C | CAR | CAR A11 | 0.0455 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 84 | A88 | C | CAR | CAR A11 | 0.0433 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 85 | A89 | U | UAR | UAR A10 | 0.0463 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 86 | A90 | A | AAR | GAO A9 | 0.0289 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 87 | A91 | A | AAR | GAO A9 | 0.0287 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 88 | A92 | A | AAR | GAO A9 | 0.1211 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 89 | A93 | A | AAR | GAO A9 | 0.0296 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 90 | A94 | C | CAR | CAR A11 | 0.0394 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 91 | A95 | A | AAR | GAO A9 | 0.0309 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 92 | A96 | U | UAR | UAR A10 | 0.0468 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 93 | A97 | A | AAR | GAO A9 | 0.0364 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 94 | A98 | C | CAR | CAR A11 | 0.0392 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 95 | A99 | C | CAR | CAR A11 | 0.0377 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 96 | A100 | U | UAR | UAR A10 | 0.0422 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 97 | A101 | U | UAR | UAR A10 | 0.0426 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 98 | A102 | U | UAR | UAR A10 | 0.0400 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 99 | A103 | C | CAR | CAR A11 | 0.1335 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 100 | A104 | C | CAR | CAR A11 | 0.0401 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 101 | A105 | U | UAR | UAR A10 | 0.0458 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 102 | A106 | G | GAO | GAO A9 | 0.0297 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 103 | A107 | G | GAO | GAO A9 | 0.0354 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 104 | A108 | A | AAR | GAO A9 | 0.0402 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 105 | A109 | U | UAR | UAR A10 | 0.0412 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 106 | A110 | U | UAR | UAR A10 | 0.1392 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 107 | A111 | C | CAR | CAR A11 | 0.0478 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 108 | A112 | C | CAR | CAR A11 | 0.0516 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 109 | A115 | U | UAR | UAR A10 | 0.0500 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 110 | A116 | G | GAO | GAO A9 | 0.0371 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 111 | A117 | C | CAR | CAR A11 | 0.1414 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |

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
- Patch 002A.2 reports chain-continuity problems but does not correct them.
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

The next Digital Polymerase requirement is chemically rigorous ANA stereochemistry validation, explicit connectivity/topology support, and eventually energy minimization.
