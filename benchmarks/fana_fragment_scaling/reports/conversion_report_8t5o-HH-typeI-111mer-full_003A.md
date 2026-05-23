# RNA → FANA Chain-Preserving Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 003A  
**Method:** Chain-preserving RNA → FANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**C2′–F status:** `PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- FANA template PDB: `/mnt/data/2KP4_FANA_10mer.pdb`
- Output PDB: `/mnt/data/fana_patch_003A_outputs/converted_fana_8t5o-HH-typeI-111mer-full_003A.pdb`

---

## Source Sequence

```text
GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
```

---

## Template Index

The FANA template provides local sugar/substituent geometry donors.

- `A` → `A5L` at chain `A`, residue `4`
- `C` → `CFL` at chain `A`, residue `2`
- `G` → `GFL` at chain `A`, residue `1`
- `U` → `TAF` at chain `A`, residue `3`

Notes:

- RNA `U` is mapped to a U/T-like FANA geometry donor when the template uses thymine-like FANA residues.
- RNA bases are preserved by default; residue labels are provisional.

---

## Method Summary

This prototype uses a **chain-preserving** strategy.

For each RNA residue:

1. determine source RNA base identity
2. select the best available FANA template residue
3. align FANA template anchor atoms onto RNA anchor atoms using Kabsch alignment
4. preserve RNA chain-continuity atoms and RNA nucleobase atoms
5. replace RNA 2′ chemistry by introducing FANA-like `C2′` and `F2′`
6. remove RNA `O2′`
7. export a FANA-like candidate residue
8. validate inter-residue chain continuity and C2′–F geometry

This is **not** a full-template reconstruction.

---

## Settings

- Anchor atoms: `C1', C3', C4', O4'`
- Residue naming policy: `template-observed`
- Skip residue-numbering gaps in inter-residue validation: `True`

---

## Alignment Summary

- Converted residues: `111`
- Mean anchor RMSD: `0.0520 Å`
- Maximum anchor RMSD: `0.0955 Å`
- Mean C2′–F distance: `1.3823 Å`
- Maximum C2′–F distance: `1.3838 Å`

Important:

> Chain continuity is preserved by keeping the RNA polymer-chain atoms. FANA-like local 2′ geometry is introduced from the FANA template.

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source | 111 | 0 | 0 | 1.527 | 1.521 | 1.530 | 1.35–1.75 | PASS |
| C1'→C2' | output | 111 | 0 | 0 | 1.546 | 1.508 | 1.566 | 1.35–1.75 | PASS |
| C2'→C3' | source | 111 | 0 | 0 | 1.522 | 1.519 | 1.526 | 1.35–1.75 | PASS |
| C2'→C3' | output | 111 | 0 | 0 | 1.513 | 1.500 | 1.537 | 1.35–1.75 | PASS |
| C2'→F2' | output | 111 | 0 | 0 | 1.382 | 1.381 | 1.384 | 1.25–1.50 | PASS |
| O3'(i)→P(i+1) | source | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output C2′–F2′ distances

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | C2′–F (Å) | Note |
|---:|---|---|---|---|---:|---:|---|
| 1 | A5 | G | GFL | GFL A1 | 0.0550 | 1.3838 | exact base-class template |
| 2 | A6 | G | GFL | GFL A1 | 0.0475 | 1.3838 | exact base-class template |
| 3 | A7 | U | UFL | TAF A3 | 0.0274 | 1.3835 | exact base-class template |
| 4 | A8 | G | GFL | GFL A1 | 0.0430 | 1.3838 | exact base-class template |
| 5 | A9 | C | CFL | CFL A2 | 0.0359 | 1.3806 | exact base-class template |
| 6 | A10 | A | A5L | A5L A4 | 0.0534 | 1.3816 | exact base-class template |
| 7 | A11 | G | GFL | GFL A1 | 0.0433 | 1.3838 | exact base-class template |
| 8 | A12 | G | GFL | GFL A1 | 0.0442 | 1.3838 | exact base-class template |
| 9 | A13 | U | UFL | TAF A3 | 0.0269 | 1.3835 | exact base-class template |
| 10 | A14 | A | A5L | A5L A4 | 0.0666 | 1.3816 | exact base-class template |
| 11 | A15 | C | CFL | CFL A2 | 0.0714 | 1.3806 | exact base-class template |
| 12 | A16 | A | A5L | A5L A4 | 0.0647 | 1.3816 | exact base-class template |
| 13 | A17 | U | UFL | TAF A3 | 0.0273 | 1.3835 | exact base-class template |
| 14 | A18 | C | CFL | CFL A2 | 0.0504 | 1.3806 | exact base-class template |
| 15 | A19 | C | CFL | CFL A2 | 0.0502 | 1.3806 | exact base-class template |
| 16 | A20 | A | A5L | A5L A4 | 0.0590 | 1.3816 | exact base-class template |
| 17 | A21 | G | GFL | GFL A1 | 0.0590 | 1.3838 | exact base-class template |
| 18 | A22 | C | CFL | CFL A2 | 0.0600 | 1.3806 | exact base-class template |
| 19 | A23 | U | UFL | TAF A3 | 0.0297 | 1.3835 | exact base-class template |
| 20 | A24 | G | GFL | GFL A1 | 0.0580 | 1.3838 | exact base-class template |
| 21 | A25 | A | A5L | A5L A4 | 0.0625 | 1.3816 | exact base-class template |
| 22 | A26 | U | UFL | TAF A3 | 0.0879 | 1.3835 | exact base-class template |
| 23 | A27 | G | GFL | GFL A1 | 0.0446 | 1.3838 | exact base-class template |
| 24 | A28 | A | A5L | A5L A4 | 0.0620 | 1.3816 | exact base-class template |
| 25 | A29 | G | GFL | GFL A1 | 0.0465 | 1.3838 | exact base-class template |
| 26 | A30 | U | UFL | TAF A3 | 0.0261 | 1.3835 | exact base-class template |
| 27 | A31 | C | CFL | CFL A2 | 0.0486 | 1.3806 | exact base-class template |
| 28 | A32 | C | CFL | CFL A2 | 0.0528 | 1.3806 | exact base-class template |
| 29 | A33 | C | CFL | CFL A2 | 0.0527 | 1.3806 | exact base-class template |
| 30 | A34 | A | A5L | A5L A4 | 0.0632 | 1.3816 | exact base-class template |
| 31 | A35 | A | A5L | A5L A4 | 0.0495 | 1.3816 | exact base-class template |
| 32 | A36 | A | A5L | A5L A4 | 0.0435 | 1.3816 | exact base-class template |
| 33 | A37 | U | UFL | TAF A3 | 0.0282 | 1.3835 | exact base-class template |
| 34 | A38 | A | A5L | A5L A4 | 0.0492 | 1.3816 | exact base-class template |
| 35 | A39 | G | GFL | GFL A1 | 0.0469 | 1.3838 | exact base-class template |
| 36 | A40 | G | GFL | GFL A1 | 0.0579 | 1.3838 | exact base-class template |
| 37 | A41 | A | A5L | A5L A4 | 0.0675 | 1.3816 | exact base-class template |
| 38 | A42 | C | CFL | CFL A2 | 0.0435 | 1.3806 | exact base-class template |
| 39 | A43 | A | A5L | A5L A4 | 0.0648 | 1.3816 | exact base-class template |
| 40 | A44 | A | A5L | A5L A4 | 0.0646 | 1.3816 | exact base-class template |
| 41 | A45 | A | A5L | A5L A4 | 0.0594 | 1.3816 | exact base-class template |
| 42 | A46 | A | A5L | A5L A4 | 0.0590 | 1.3816 | exact base-class template |
| 43 | A47 | A | A5L | A5L A4 | 0.0682 | 1.3816 | exact base-class template |
| 44 | A48 | G | GFL | GFL A1 | 0.0624 | 1.3838 | exact base-class template |
| 45 | A49 | G | GFL | GFL A1 | 0.0587 | 1.3838 | exact base-class template |
| 46 | A50 | G | GFL | GFL A1 | 0.0548 | 1.3838 | exact base-class template |
| 47 | A51 | A | A5L | A5L A4 | 0.0701 | 1.3816 | exact base-class template |
| 48 | A52 | G | GFL | GFL A1 | 0.0642 | 1.3838 | exact base-class template |
| 49 | A53 | A | A5L | A5L A4 | 0.0577 | 1.3816 | exact base-class template |
| 50 | A54 | G | GFL | GFL A1 | 0.0473 | 1.3838 | exact base-class template |
| 51 | A55 | G | GFL | GFL A1 | 0.0446 | 1.3838 | exact base-class template |
| 52 | A56 | U | UFL | TAF A3 | 0.0258 | 1.3835 | exact base-class template |
| 53 | A57 | G | GFL | GFL A1 | 0.0514 | 1.3838 | exact base-class template |
| 54 | A58 | A | A5L | A5L A4 | 0.0644 | 1.3816 | exact base-class template |
| 55 | A59 | A | A5L | A5L A4 | 0.0649 | 1.3816 | exact base-class template |
| 56 | A60 | G | GFL | GFL A1 | 0.0414 | 1.3838 | exact base-class template |
| 57 | A61 | A | A5L | A5L A4 | 0.0637 | 1.3816 | exact base-class template |
| 58 | A62 | A | A5L | A5L A4 | 0.0438 | 1.3816 | exact base-class template |
| 59 | A63 | U | UFL | TAF A3 | 0.0939 | 1.3835 | exact base-class template |
| 60 | A64 | A | A5L | A5L A4 | 0.0614 | 1.3816 | exact base-class template |
| 61 | A65 | C | CFL | CFL A2 | 0.0666 | 1.3806 | exact base-class template |
| 62 | A66 | G | GFL | GFL A1 | 0.0594 | 1.3838 | exact base-class template |
| 63 | A67 | A | A5L | A5L A4 | 0.0596 | 1.3816 | exact base-class template |
| 64 | A68 | C | CFL | CFL A2 | 0.0419 | 1.3806 | exact base-class template |
| 65 | A69 | C | CFL | CFL A2 | 0.0496 | 1.3806 | exact base-class template |
| 66 | A70 | A | A5L | A5L A4 | 0.0711 | 1.3816 | exact base-class template |
| 67 | A71 | C | CFL | CFL A2 | 0.0559 | 1.3806 | exact base-class template |
| 68 | A72 | C | CFL | CFL A2 | 0.0550 | 1.3806 | exact base-class template |
| 69 | A73 | U | UFL | TAF A3 | 0.0380 | 1.3835 | exact base-class template |
| 70 | A74 | A | A5L | A5L A4 | 0.0726 | 1.3816 | exact base-class template |
| 71 | A75 | G | GFL | GFL A1 | 0.0594 | 1.3838 | exact base-class template |
| 72 | A76 | G | GFL | GFL A1 | 0.0438 | 1.3838 | exact base-class template |
| 73 | A77 | C | CFL | CFL A2 | 0.0431 | 1.3806 | exact base-class template |
| 74 | A78 | U | UFL | TAF A3 | 0.0310 | 1.3835 | exact base-class template |
| 75 | A79 | C | CFL | CFL A2 | 0.0391 | 1.3806 | exact base-class template |
| 76 | A80 | G | GFL | GFL A1 | 0.0477 | 1.3838 | exact base-class template |
| 77 | A81 | A | A5L | A5L A4 | 0.0589 | 1.3816 | exact base-class template |
| 78 | A82 | A | A5L | A5L A4 | 0.0564 | 1.3816 | exact base-class template |
| 79 | A83 | A | A5L | A5L A4 | 0.0650 | 1.3816 | exact base-class template |
| 80 | A84 | G | GFL | GFL A1 | 0.0471 | 1.3838 | exact base-class template |
| 81 | A85 | A | A5L | A5L A4 | 0.0566 | 1.3816 | exact base-class template |
| 82 | A86 | G | GFL | GFL A1 | 0.0523 | 1.3838 | exact base-class template |
| 83 | A87 | C | CFL | CFL A2 | 0.0470 | 1.3806 | exact base-class template |
| 84 | A88 | C | CFL | CFL A2 | 0.0477 | 1.3806 | exact base-class template |
| 85 | A89 | U | UFL | TAF A3 | 0.0273 | 1.3835 | exact base-class template |
| 86 | A90 | A | A5L | A5L A4 | 0.0697 | 1.3816 | exact base-class template |
| 87 | A91 | A | A5L | A5L A4 | 0.0692 | 1.3816 | exact base-class template |
| 88 | A92 | A | A5L | A5L A4 | 0.0439 | 1.3816 | exact base-class template |
| 89 | A93 | A | A5L | A5L A4 | 0.0684 | 1.3816 | exact base-class template |
| 90 | A94 | C | CFL | CFL A2 | 0.0531 | 1.3806 | exact base-class template |
| 91 | A95 | A | A5L | A5L A4 | 0.0666 | 1.3816 | exact base-class template |
| 92 | A96 | U | UFL | TAF A3 | 0.0262 | 1.3835 | exact base-class template |
| 93 | A97 | A | A5L | A5L A4 | 0.0594 | 1.3816 | exact base-class template |
| 94 | A98 | C | CFL | CFL A2 | 0.0526 | 1.3806 | exact base-class template |
| 95 | A99 | C | CFL | CFL A2 | 0.0541 | 1.3806 | exact base-class template |
| 96 | A100 | U | UFL | TAF A3 | 0.0296 | 1.3835 | exact base-class template |
| 97 | A101 | U | UFL | TAF A3 | 0.0291 | 1.3835 | exact base-class template |
| 98 | A102 | U | UFL | TAF A3 | 0.0292 | 1.3835 | exact base-class template |
| 99 | A103 | C | CFL | CFL A2 | 0.0639 | 1.3806 | exact base-class template |
| 100 | A104 | C | CFL | CFL A2 | 0.0503 | 1.3806 | exact base-class template |
| 101 | A105 | U | UFL | TAF A3 | 0.0275 | 1.3835 | exact base-class template |
| 102 | A106 | G | GFL | GFL A1 | 0.0529 | 1.3838 | exact base-class template |
| 103 | A107 | G | GFL | GFL A1 | 0.0444 | 1.3838 | exact base-class template |
| 104 | A108 | A | A5L | A5L A4 | 0.0534 | 1.3816 | exact base-class template |
| 105 | A109 | U | UFL | TAF A3 | 0.0281 | 1.3835 | exact base-class template |
| 106 | A110 | U | UFL | TAF A3 | 0.0955 | 1.3835 | exact base-class template |
| 107 | A111 | C | CFL | CFL A2 | 0.0415 | 1.3806 | exact base-class template |
| 108 | A112 | C | CFL | CFL A2 | 0.0393 | 1.3806 | exact base-class template |
| 109 | A115 | U | UFL | TAF A3 | 0.0262 | 1.3835 | exact base-class template |
| 110 | A116 | G | GFL | GFL A1 | 0.0426 | 1.3838 | exact base-class template |
| 111 | A117 | C | CFL | CFL A2 | 0.0717 | 1.3806 | exact base-class template |

---

## Scientific Interpretation

This output should be interpreted as:

> a FANA-like candidate structure generated using chain-preserving local reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed FANA structure.

---

## Important Limitations

- This is not energy-minimized.
- No force-field parameters are generated.
- RNA bases are preserved.
- RNA chain atoms are preserved to maintain polymer continuity.
- FANA-like C2′ and F2′ geometry is introduced from a template, but stereochemistry still needs expert review.
- Connectivity is not explicitly written with `CONECT` records.
- Residue names are provisional and may need adjustment for downstream tools.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect the output in PyMOL, ChimeraX, VMD, or Mol*.
2. Check residue completeness and atom naming.
3. Inspect base-backbone attachment geometry.
4. Review O3′–P and C2′–F validation tables.
5. Compare local C2′/F geometry with the FANA template.
6. Add explicit topology/connectivity in future versions.
7. Perform energy minimization with appropriate force-field support.
8. Run short MD only after force-field/topology validation.

---

## Development Note

Prototype 003A applies the successful ANA 002A.2 lesson:

```text
Do not sacrifice chain continuity for local XNA geometry.
```

The strategy is therefore:

```text
preserve chain first
introduce XNA-local chemistry second
validate explicitly
```
