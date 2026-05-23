# RNA → CeNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 004A  
**Requested mode:** `auto`  
**Actual mode:** `chain-preserving`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**Base-attachment status:** `PASS`  
**CeNA local scaffold status:** `C4′→C6′ FAIL`, `C6′→C7′ PASS`, `C7′→C1′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- CeNA template PDB: `/mnt/data/2H0N_CeNA_8mer_clean_ss.pdb`
- Output PDB: `/mnt/data/cena_prototype_004A_outputs/converted_cena_8t5o-HH-typeI-111mer-full_auto_004A.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- CeNA template base-class sequence: `GUGUACAC`
- Source residue count: `111`
- Template residue count: `8`
- Converted residues: `111`
- Base label policy: `preserve`

---

## Method Summary

This converter supports two RNA → CeNA modes.

### Full-template mode

Used when the CeNA template is at least as long as the source RNA.

```text
CeNA full scaffold donor + transformed RNA bases
```

### Chain-preserving mode

Used when the source RNA is longer than the CeNA template.

```text
RNA chain atoms preserved
+
CeNA local cyclohexenyl scaffold atoms inserted from template
+
RNA bases transformed onto the new CeNA-like local scaffold
```

In `auto` mode, the script chooses full-template mode when possible and chain-preserving mode when the source RNA is longer than the template.

---

## Settings

- Requested mode: `auto`
- Actual mode: `chain-preserving`
- Full-template anchors: `C1', C2', C3', C4'`
- Chain-preserving CeNA-template anchors: `O5', C5', C4', C3', O3'`
- Base-transplant anchors: `C1', C2', C3', C4'`
- Base label policy: `preserve`

---

## Alignment Summary

- Mean template/local anchor RMSD: `0.7988 Å`
- Maximum template/local anchor RMSD: `0.9389 Å`
- Mean base-transplant anchor RMSD: `0.5186 Å`
- Maximum base-transplant anchor RMSD: `0.7666 Å`
- Mean C1′→glycosidic N distance: `1.4931 Å`
- Maximum C1′→glycosidic N distance: `1.4996 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 111 | 0 | 0 | 1.527 | 1.521 | 1.530 | 1.35–1.85 | PASS |
| C1'→C2' | CeNA template | 8 | 0 | 0 | 1.560 | 1.550 | 1.572 | 1.35–1.85 | PASS |
| C1'→C2' | output | 111 | 0 | 0 | 1.560 | 1.550 | 1.572 | 1.35–1.85 | PASS |
| C1'→glycosidic N | source RNA | 111 | 0 | 0 | 1.474 | 1.462 | 1.480 | 1.30–1.75 | PASS |
| C1'→glycosidic N | CeNA template | 8 | 0 | 0 | 1.493 | 1.484 | 1.500 | 1.30–1.75 | PASS |
| C1'→glycosidic N | output | 111 | 0 | 0 | 1.493 | 1.484 | 1.500 | 1.30–1.75 | PASS |
| C2'→C3' | source RNA | 111 | 0 | 0 | 1.522 | 1.519 | 1.526 | 1.35–1.85 | PASS |
| C2'→C3' | CeNA template | 8 | 0 | 0 | 1.533 | 1.522 | 1.545 | 1.35–1.85 | PASS |
| C2'→C3' | output | 111 | 0 | 76 | 2.186 | 1.518 | 2.584 | 1.35–1.85 | FAIL |
| C3'→C4' | source RNA | 111 | 0 | 0 | 1.520 | 1.515 | 1.529 | 1.35–1.85 | PASS |
| C3'→C4' | CeNA template | 8 | 0 | 0 | 1.540 | 1.523 | 1.565 | 1.35–1.85 | PASS |
| C3'→C4' | output | 111 | 0 | 0 | 1.520 | 1.515 | 1.529 | 1.35–1.85 | PASS |
| C3'→O3' | source RNA | 111 | 0 | 0 | 1.418 | 1.414 | 1.437 | 1.20–1.65 | PASS |
| C3'→O3' | CeNA template | 8 | 0 | 0 | 1.414 | 1.397 | 1.422 | 1.20–1.65 | PASS |
| C3'→O3' | output | 111 | 0 | 0 | 1.418 | 1.414 | 1.437 | 1.20–1.65 | PASS |
| C4'→C5' | source RNA | 111 | 0 | 0 | 1.507 | 1.504 | 1.510 | 1.30–1.80 | PASS |
| C4'→C5' | CeNA template | 8 | 0 | 0 | 1.505 | 1.494 | 1.521 | 1.30–1.80 | PASS |
| C4'→C5' | output | 111 | 0 | 0 | 1.507 | 1.504 | 1.510 | 1.30–1.80 | PASS |
| C4'→C6' | CeNA template | 8 | 0 | 0 | 1.458 | 1.451 | 1.467 | 1.20–1.70 | PASS |
| C4'→C6' | output | 111 | 0 | 87 | 1.835 | 1.262 | 2.580 | 1.20–1.70 | FAIL |
| C5'→O5' | source RNA | 111 | 0 | 0 | 1.419 | 1.417 | 1.424 | 1.20–1.75 | PASS |
| C5'→O5' | CeNA template | 7 | 1 | 0 | 1.444 | 1.425 | 1.481 | 1.20–1.75 | PASS |
| C5'→O5' | output | 111 | 0 | 0 | 1.419 | 1.417 | 1.424 | 1.20–1.75 | PASS |
| C6'→C7' | CeNA template | 8 | 0 | 0 | 1.322 | 1.310 | 1.332 | 1.15–1.50 | PASS |
| C6'→C7' | output | 111 | 0 | 0 | 1.321 | 1.310 | 1.332 | 1.15–1.50 | PASS |
| C7'→C1' | CeNA template | 8 | 0 | 0 | 1.559 | 1.547 | 1.568 | 1.30–1.85 | PASS |
| C7'→C1' | output | 111 | 0 | 0 | 1.559 | 1.547 | 1.568 | 1.30–1.85 | PASS |
| O3'(i)→P(i+1) | source RNA | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | CeNA template | 7 | 0 | 0 | 1.603 | 1.593 | 1.624 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source RNA | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | CeNA template | 7 | 1 | 0 | 1.642 | 1.624 | 1.658 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | output | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.35–1.90 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output CeNA C4′–C6′ links

| Rank | Link | Distance (Å) | Expected range (Å) | Status |
|---:|---|---:|---|---|
| 1 | `A36:C4' → A36:C6'` | 2.580 | 1.20–1.70 | FAIL |
| 2 | `A117:C4' → A117:C6'` | 2.411 | 1.20–1.70 | FAIL |
| 3 | `A103:C4' → A103:C6'` | 2.373 | 1.20–1.70 | FAIL |
| 4 | `A26:C4' → A26:C6'` | 2.367 | 1.20–1.70 | FAIL |
| 5 | `A22:C4' → A22:C6'` | 2.341 | 1.20–1.70 | FAIL |
| 6 | `A92:C4' → A92:C6'` | 2.333 | 1.20–1.70 | FAIL |
| 7 | `A27:C4' → A27:C6'` | 2.322 | 1.20–1.70 | FAIL |
| 8 | `A110:C4' → A110:C6'` | 2.315 | 1.20–1.70 | FAIL |
| 9 | `A65:C4' → A65:C6'` | 2.248 | 1.20–1.70 | FAIL |
| 10 | `A63:C4' → A63:C6'` | 2.246 | 1.20–1.70 | FAIL |
| 11 | `A35:C4' → A35:C6'` | 2.232 | 1.20–1.70 | FAIL |
| 12 | `A82:C4' → A82:C6'` | 2.218 | 1.20–1.70 | FAIL |
| 13 | `A53:C4' → A53:C6'` | 2.208 | 1.20–1.70 | FAIL |
| 14 | `A14:C4' → A14:C6'` | 2.183 | 1.20–1.70 | FAIL |
| 15 | `A66:C4' → A66:C6'` | 2.180 | 1.20–1.70 | FAIL |
| 16 | `A45:C4' → A45:C6'` | 2.136 | 1.20–1.70 | FAIL |
| 17 | `A67:C4' → A67:C6'` | 2.130 | 1.20–1.70 | FAIL |
| 18 | `A47:C4' → A47:C6'` | 2.119 | 1.20–1.70 | FAIL |
| 19 | `A32:C4' → A32:C6'` | 2.104 | 1.20–1.70 | FAIL |
| 20 | `A43:C4' → A43:C6'` | 2.092 | 1.20–1.70 | FAIL |

### Worst output CeNA C6′–C7′ links

No failed links detected.

### Worst output CeNA C7′–C1′ links

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Template/local RMSD (Å) | Base RMSD (Å) | C1′–N (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 1 | A5 | G | XGL | XGL A1 | chain-preserving | 0.5419 | 0.2560 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 2 | A6 | G | XGL | XGL A3 | chain-preserving | 0.9149 | 0.6811 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 3 | A7 | U | XUL | XTL A2 | chain-preserving | 0.9223 | 0.6983 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 4 | A8 | G | XGL | XGL A1 | chain-preserving | 0.5496 | 0.2585 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 5 | A9 | C | XCL | XCL A6 | chain-preserving | 0.6960 | 0.1783 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 6 | A10 | A | XAL | XAL A5 | chain-preserving | 0.6837 | 0.3796 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 7 | A11 | G | XGL | XGL A3 | chain-preserving | 0.7359 | 0.1799 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 8 | A12 | G | XGL | XGL A1 | chain-preserving | 0.5495 | 0.2549 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 9 | A13 | U | XUL | XTL A4 | chain-preserving | 0.8972 | 0.6807 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 10 | A14 | A | XAL | XAL A7 | chain-preserving | 0.8985 | 0.7584 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 11 | A15 | C | XCL | XCL A8 | chain-preserving | 0.7584 | 0.5123 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 12 | A16 | A | XAL | XAL A5 | chain-preserving | 0.8723 | 0.6260 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 13 | A17 | U | XUL | XTL A2 | chain-preserving | 0.9161 | 0.6843 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 14 | A18 | C | XCL | XCL A6 | chain-preserving | 0.9118 | 0.6757 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 15 | A19 | C | XCL | XCL A8 | chain-preserving | 0.9154 | 0.6741 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 16 | A20 | A | XAL | XAL A7 | chain-preserving | 0.6738 | 0.2453 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 17 | A21 | G | XGL | XGL A3 | chain-preserving | 0.8992 | 0.6593 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 18 | A22 | C | XCL | XCL A6 | chain-preserving | 0.6974 | 0.5497 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 19 | A23 | U | XUL | XTL A4 | chain-preserving | 0.8979 | 0.6748 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 20 | A24 | G | XGL | XGL A1 | chain-preserving | 0.5485 | 0.2484 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 21 | A25 | A | XAL | XAL A5 | chain-preserving | 0.8818 | 0.6361 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 22 | A26 | U | XUL | XTL A2 | chain-preserving | 0.6967 | 0.5563 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 23 | A27 | G | XGL | XGL A3 | chain-preserving | 0.9354 | 0.2409 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 24 | A28 | A | XAL | XAL A7 | chain-preserving | 0.6985 | 0.4576 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 25 | A29 | G | XGL | XGL A1 | chain-preserving | 0.5481 | 0.2539 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 26 | A30 | U | XUL | XTL A4 | chain-preserving | 0.7652 | 0.2085 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 27 | A31 | C | XCL | XCL A8 | chain-preserving | 0.9083 | 0.6727 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 28 | A32 | C | XCL | XCL A6 | chain-preserving | 0.8582 | 0.1806 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 29 | A33 | C | XCL | XCL A8 | chain-preserving | 0.9117 | 0.6719 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 30 | A34 | A | XAL | XAL A5 | chain-preserving | 0.8714 | 0.6269 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 31 | A35 | A | XAL | XAL A7 | chain-preserving | 0.6697 | 0.5309 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 32 | A36 | A | XAL | XAL A5 | chain-preserving | 0.7837 | 0.5577 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 33 | A37 | U | XUL | XTL A2 | chain-preserving | 0.9335 | 0.7088 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 34 | A38 | A | XAL | XAL A7 | chain-preserving | 0.6654 | 0.5142 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 35 | A39 | G | XGL | XGL A3 | chain-preserving | 0.6874 | 0.1813 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 36 | A40 | G | XGL | XGL A1 | chain-preserving | 0.5358 | 0.2613 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 37 | A41 | A | XAL | XAL A5 | chain-preserving | 0.8669 | 0.6169 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 38 | A42 | C | XCL | XCL A6 | chain-preserving | 0.6552 | 0.1797 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 39 | A43 | A | XAL | XAL A7 | chain-preserving | 0.8976 | 0.7574 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 40 | A44 | A | XAL | XAL A5 | chain-preserving | 0.8785 | 0.6313 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 41 | A45 | A | XAL | XAL A7 | chain-preserving | 0.8949 | 0.7594 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 42 | A46 | A | XAL | XAL A5 | chain-preserving | 0.8758 | 0.6348 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 43 | A47 | A | XAL | XAL A7 | chain-preserving | 0.9008 | 0.7606 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 44 | A48 | G | XGL | XGL A3 | chain-preserving | 0.9049 | 0.6584 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 45 | A49 | G | XGL | XGL A1 | chain-preserving | 0.5367 | 0.2621 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 46 | A50 | G | XGL | XGL A3 | chain-preserving | 0.9033 | 0.6657 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 47 | A51 | A | XAL | XAL A5 | chain-preserving | 0.8742 | 0.6229 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 48 | A52 | G | XGL | XGL A1 | chain-preserving | 0.5343 | 0.2601 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 49 | A53 | A | XAL | XAL A7 | chain-preserving | 0.8922 | 0.7612 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 50 | A54 | G | XGL | XGL A3 | chain-preserving | 0.9116 | 0.6816 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 51 | A55 | G | XGL | XGL A1 | chain-preserving | 0.5473 | 0.2588 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 52 | A56 | U | XUL | XTL A4 | chain-preserving | 0.7694 | 0.2104 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 53 | A57 | G | XGL | XGL A3 | chain-preserving | 0.8241 | 0.1864 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 54 | A58 | A | XAL | XAL A5 | chain-preserving | 0.8703 | 0.6269 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 55 | A59 | A | XAL | XAL A7 | chain-preserving | 0.8953 | 0.7541 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 56 | A60 | G | XGL | XGL A1 | chain-preserving | 0.5453 | 0.2631 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 57 | A61 | A | XAL | XAL A5 | chain-preserving | 0.8766 | 0.6307 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 58 | A62 | A | XAL | XAL A7 | chain-preserving | 0.6826 | 0.5082 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 59 | A63 | U | XUL | XTL A2 | chain-preserving | 0.6905 | 0.5490 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 60 | A64 | A | XAL | XAL A5 | chain-preserving | 0.8862 | 0.6388 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 61 | A65 | C | XCL | XCL A8 | chain-preserving | 0.7652 | 0.5521 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 62 | A66 | G | XGL | XGL A3 | chain-preserving | 0.6902 | 0.5273 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 63 | A67 | A | XAL | XAL A7 | chain-preserving | 0.8958 | 0.7616 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 64 | A68 | C | XCL | XCL A6 | chain-preserving | 0.9062 | 0.6783 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 65 | A69 | C | XCL | XCL A8 | chain-preserving | 0.9083 | 0.6720 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 66 | A70 | A | XAL | XAL A5 | chain-preserving | 0.8710 | 0.6190 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 67 | A71 | C | XCL | XCL A6 | chain-preserving | 0.9179 | 0.6704 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 68 | A72 | C | XCL | XCL A8 | chain-preserving | 0.9389 | 0.6781 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 69 | A73 | U | XUL | XTL A4 | chain-preserving | 0.8950 | 0.6600 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 70 | A74 | A | XAL | XAL A7 | chain-preserving | 0.9007 | 0.7522 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 71 | A75 | G | XGL | XGL A1 | chain-preserving | 0.5378 | 0.2584 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 72 | A76 | G | XGL | XGL A3 | chain-preserving | 0.6910 | 0.1814 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 73 | A77 | C | XCL | XCL A6 | chain-preserving | 0.9132 | 0.6806 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 74 | A78 | U | XUL | XTL A2 | chain-preserving | 0.7622 | 0.1804 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 75 | A79 | C | XCL | XCL A8 | chain-preserving | 0.7622 | 0.5087 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 76 | A80 | G | XGL | XGL A1 | chain-preserving | 0.5451 | 0.2588 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 77 | A81 | A | XAL | XAL A5 | chain-preserving | 0.8192 | 0.2009 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 78 | A82 | A | XAL | XAL A7 | chain-preserving | 0.9101 | 0.7666 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 79 | A83 | A | XAL | XAL A5 | chain-preserving | 0.8765 | 0.6272 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 80 | A84 | G | XGL | XGL A3 | chain-preserving | 0.6221 | 0.2006 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 81 | A85 | A | XAL | XAL A7 | chain-preserving | 0.8961 | 0.7604 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 82 | A86 | G | XGL | XGL A1 | chain-preserving | 0.5403 | 0.2617 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 83 | A87 | C | XCL | XCL A6 | chain-preserving | 0.9125 | 0.6809 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 84 | A88 | C | XCL | XCL A8 | chain-preserving | 0.9241 | 0.6824 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 85 | A89 | U | XUL | XTL A4 | chain-preserving | 0.9008 | 0.6833 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 86 | A90 | A | XAL | XAL A5 | chain-preserving | 0.8717 | 0.6218 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 87 | A91 | A | XAL | XAL A7 | chain-preserving | 0.7896 | 0.5341 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 88 | A92 | A | XAL | XAL A5 | chain-preserving | 0.7023 | 0.5231 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 89 | A93 | A | XAL | XAL A7 | chain-preserving | 0.8973 | 0.7442 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 90 | A94 | C | XCL | XCL A6 | chain-preserving | 0.9091 | 0.6689 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 91 | A95 | A | XAL | XAL A5 | chain-preserving | 0.8740 | 0.6264 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 92 | A96 | U | XUL | XTL A2 | chain-preserving | 0.6521 | 0.1793 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 93 | A97 | A | XAL | XAL A7 | chain-preserving | 0.8950 | 0.7564 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 94 | A98 | C | XCL | XCL A8 | chain-preserving | 0.9219 | 0.6769 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 95 | A99 | C | XCL | XCL A6 | chain-preserving | 0.9099 | 0.6684 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 96 | A100 | U | XUL | XTL A4 | chain-preserving | 0.9064 | 0.6806 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 97 | A101 | U | XUL | XTL A2 | chain-preserving | 0.9166 | 0.6756 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 98 | A102 | U | XUL | XTL A4 | chain-preserving | 0.8993 | 0.6774 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 99 | A103 | C | XCL | XCL A8 | chain-preserving | 0.7830 | 0.5457 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 100 | A104 | C | XCL | XCL A6 | chain-preserving | 0.6242 | 0.1858 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 101 | A105 | U | XUL | XTL A2 | chain-preserving | 0.9150 | 0.6768 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 102 | A106 | G | XGL | XGL A3 | chain-preserving | 0.9048 | 0.6703 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 103 | A107 | G | XGL | XGL A1 | chain-preserving | 0.5478 | 0.2574 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 104 | A108 | A | XAL | XAL A5 | chain-preserving | 0.8230 | 0.2044 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 105 | A109 | U | XUL | XTL A4 | chain-preserving | 0.9067 | 0.6831 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 106 | A110 | U | XUL | XTL A2 | chain-preserving | 0.6890 | 0.5517 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 107 | A111 | C | XCL | XCL A8 | chain-preserving | 0.9219 | 0.6868 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 108 | A112 | C | XCL | XCL A6 | chain-preserving | 0.6944 | 0.1770 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 109 | A115 | U | XUL | XTL A4 | chain-preserving | 0.8988 | 0.6755 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 110 | A116 | G | XGL | XGL A3 | chain-preserving | 0.6443 | 0.1952 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 111 | A117 | C | XCL | XCL A8 | chain-preserving | 0.9202 | 0.5012 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |

---

## Scientific Interpretation

This output should be interpreted as:

> a CeNA-like computational candidate generated by template-guided or chain-preserving reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed CeNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- `XUL` residue labels are provisional when RNA `U` is preserved.
- Chain-preserving mode preserves the RNA chain path and inserts local CeNA-like scaffold atoms; it is not a fully de novo CeNA fold prediction.
- CeNA stereochemistry requires expert review.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect in PyMOL, ChimeraX, Discovery Studio, VMD, or Mol*.
2. Inspect CeNA cyclohexenyl scaffold geometry.
3. Compare local scaffold geometry against the 2H0N CeNA template.
4. Check C1′→glycosidic N and CeNA local scaffold distances.
5. Add topology/connectivity support in future versions.
6. Perform energy minimization only with appropriate CeNA parameters.
7. Treat large RNA outputs as candidate geometry, not validated CeNA folds.
