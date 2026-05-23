# RNA → HNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 001B/001C  
**Requested mode:** `auto`  
**Actual mode:** `chain-preserving`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**Base-attachment status:** `PASS`  
**HNA local scaffold status:** `C1′→C6′ PASS`, `C6′→O4′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- HNA template PDB: `/mnt/data/481d-HNA8nt.pdb`
- Output PDB: `/mnt/data/hna_full_prototype_001C1_outputs/converted_hna_8t5o-HH-typeI-111mer-full_auto_001C1.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- HNA template base-class sequence: `GUGUACAC`
- Source residue count: `111`
- Template residue count: `8`
- Converted residues: `111`
- Base label policy: `preserve`

---

## Method Summary

This converter supports two RNA → HNA modes.

### Full-template mode / Prototype 001B

Used when the HNA template is at least as long as the source RNA.

```text
HNA full scaffold donor + transformed RNA bases
```

### Chain-preserving mode / Prototype 001C

Used when the source RNA is longer than the HNA template.

```text
RNA chain atoms preserved
+
HNA local scaffold atoms inserted from template
+
RNA bases transformed onto the new HNA-like local scaffold
```

In `auto` mode, the script chooses full-template mode when possible and chain-preserving mode when the source RNA is longer than the template.

---

## Settings

- Requested mode: `auto`
- Actual mode: `chain-preserving`
- Full-template anchors: `C1', C2', C4'`
- Chain-preserving HNA-template anchors: `C3', C4', C5', O5', O3'`
- Base-transplant anchors: `C1', C2', C4'`
- Base label policy: `preserve`

---

## Alignment Summary

- Mean template/local anchor RMSD: `0.4094 Å`
- Maximum template/local anchor RMSD: `0.9276 Å`
- Mean base-transplant anchor RMSD: `0.2667 Å`
- Maximum base-transplant anchor RMSD: `0.5470 Å`
- Mean C1′→glycosidic N distance: `1.4751 Å`
- Maximum C1′→glycosidic N distance: `1.4877 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 111 | 0 | 0 | 1.527 | 1.521 | 1.530 | 1.35–1.90 | PASS |
| C1'→C2' | HNA template | 8 | 0 | 0 | 1.667 | 1.642 | 1.685 | 1.35–1.90 | PASS |
| C1'→C2' | output | 111 | 0 | 0 | 1.667 | 1.642 | 1.685 | 1.35–1.90 | PASS |
| C1'→C6' | HNA template | 8 | 0 | 0 | 1.599 | 1.573 | 1.613 | 1.35–1.85 | PASS |
| C1'→C6' | output | 111 | 0 | 0 | 1.600 | 1.573 | 1.613 | 1.35–1.85 | PASS |
| C1'→glycosidic N | source RNA | 111 | 0 | 0 | 1.474 | 1.462 | 1.480 | 1.30–1.70 | PASS |
| C1'→glycosidic N | HNA template | 8 | 0 | 0 | 1.474 | 1.457 | 1.488 | 1.30–1.70 | PASS |
| C1'→glycosidic N | output | 111 | 0 | 0 | 1.475 | 1.457 | 1.488 | 1.30–1.70 | PASS |
| C2'→C3' | source RNA | 111 | 0 | 0 | 1.522 | 1.519 | 1.526 | 1.35–1.85 | PASS |
| C2'→C3' | HNA template | 8 | 0 | 0 | 1.581 | 1.559 | 1.595 | 1.35–1.85 | PASS |
| C2'→C3' | output | 111 | 0 | 39 | 1.703 | 1.330 | 2.119 | 1.35–1.85 | FAIL |
| C4'→O4' | HNA template | 8 | 0 | 0 | 1.444 | 1.438 | 1.454 | 1.20–1.70 | PASS |
| C4'→O4' | output | 111 | 0 | 15 | 1.514 | 1.133 | 2.256 | 1.20–1.70 | FAIL |
| C6'→O4' | HNA template | 8 | 0 | 0 | 1.391 | 1.379 | 1.410 | 1.20–1.60 | PASS |
| C6'→O4' | output | 111 | 0 | 0 | 1.392 | 1.379 | 1.410 | 1.20–1.60 | PASS |
| O3'(i)→P(i+1) | source RNA | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | HNA template | 7 | 0 | 0 | 1.591 | 1.581 | 1.601 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source RNA | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | HNA template | 7 | 1 | 0 | 1.564 | 1.557 | 1.574 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.40–1.80 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output HNA C1′–C6′ links

No failed links detected.

### Worst output HNA C6′–O4′ links

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Template/local RMSD (Å) | Base RMSD (Å) | C1′–N (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 1 | A5 | G | 6HG | 6HG A1 | chain-preserving | 0.5855 | 0.1331 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 2 | A6 | G | 6HG | 6HG A3 | chain-preserving | 0.1370 | 0.2596 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 3 | A7 | U | 6HU | 6HT A2 | chain-preserving | 0.1773 | 0.2433 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 4 | A8 | G | 6HG | 6HG A1 | chain-preserving | 0.6498 | 0.2257 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 5 | A9 | C | 6HC | 6HC A6 | chain-preserving | 0.6871 | 0.2631 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 6 | A10 | A | 6HA | 6HA A5 | chain-preserving | 0.6606 | 0.1348 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 7 | A11 | G | 6HG | 6HG A3 | chain-preserving | 0.6645 | 0.2678 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 8 | A12 | G | 6HG | 6HG A1 | chain-preserving | 0.3023 | 0.3002 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 9 | A13 | U | 6HU | 6HT A4 | chain-preserving | 0.1007 | 0.2625 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 10 | A14 | A | 6HA | 6HA A7 | chain-preserving | 0.1715 | 0.2742 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 11 | A15 | C | 6HC | 6HC A8 | chain-preserving | 0.5018 | 0.4615 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 12 | A16 | A | 6HA | 6HA A5 | chain-preserving | 0.6890 | 0.1948 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 13 | A17 | U | 6HU | 6HT A2 | chain-preserving | 0.1099 | 0.2445 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 14 | A18 | C | 6HC | 6HC A6 | chain-preserving | 0.1140 | 0.2467 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 15 | A19 | C | 6HC | 6HC A8 | chain-preserving | 0.0948 | 0.2740 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 16 | A20 | A | 6HA | 6HA A7 | chain-preserving | 0.7706 | 0.2902 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 17 | A21 | G | 6HG | 6HG A3 | chain-preserving | 0.0829 | 0.2653 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 18 | A22 | C | 6HC | 6HC A6 | chain-preserving | 0.5236 | 0.3271 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 19 | A23 | U | 6HU | 6HT A4 | chain-preserving | 0.1014 | 0.2632 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 20 | A24 | G | 6HG | 6HG A1 | chain-preserving | 0.6906 | 0.2056 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 21 | A25 | A | 6HA | 6HA A5 | chain-preserving | 0.6687 | 0.2108 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 22 | A26 | U | 6HU | 6HT A2 | chain-preserving | 0.5375 | 0.3217 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 23 | A27 | G | 6HG | 6HG A3 | chain-preserving | 0.3907 | 0.2616 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 24 | A28 | A | 6HA | 6HA A7 | chain-preserving | 0.6054 | 0.3641 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 25 | A29 | G | 6HG | 6HG A1 | chain-preserving | 0.7114 | 0.1912 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 26 | A30 | U | 6HU | 6HT A4 | chain-preserving | 0.6503 | 0.2634 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 27 | A31 | C | 6HC | 6HC A8 | chain-preserving | 0.0891 | 0.2736 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 28 | A32 | C | 6HC | 6HC A6 | chain-preserving | 0.4570 | 0.2504 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 29 | A33 | C | 6HC | 6HC A8 | chain-preserving | 0.0879 | 0.2746 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 30 | A34 | A | 6HA | 6HA A5 | chain-preserving | 0.6932 | 0.1918 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 31 | A35 | A | 6HA | 6HA A7 | chain-preserving | 0.4505 | 0.3526 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 32 | A36 | A | 6HA | 6HA A5 | chain-preserving | 0.6306 | 0.5470 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 33 | A37 | U | 6HU | 6HT A2 | chain-preserving | 0.2610 | 0.2446 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 34 | A38 | A | 6HA | 6HA A7 | chain-preserving | 0.4242 | 0.4264 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 35 | A39 | G | 6HG | 6HG A3 | chain-preserving | 0.7019 | 0.2668 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 36 | A40 | G | 6HG | 6HG A1 | chain-preserving | 0.6932 | 0.1920 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 37 | A41 | A | 6HA | 6HA A5 | chain-preserving | 0.7053 | 0.1854 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 38 | A42 | C | 6HC | 6HC A6 | chain-preserving | 0.7170 | 0.2676 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 39 | A43 | A | 6HA | 6HA A7 | chain-preserving | 0.1322 | 0.2734 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 40 | A44 | A | 6HA | 6HA A5 | chain-preserving | 0.6768 | 0.2050 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 41 | A45 | A | 6HA | 6HA A7 | chain-preserving | 0.1442 | 0.2749 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 42 | A46 | A | 6HA | 6HA A5 | chain-preserving | 0.6821 | 0.2023 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 43 | A47 | A | 6HA | 6HA A7 | chain-preserving | 0.1539 | 0.2719 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 44 | A48 | G | 6HG | 6HG A3 | chain-preserving | 0.0822 | 0.2595 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 45 | A49 | G | 6HG | 6HG A1 | chain-preserving | 0.6828 | 0.1983 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 46 | A50 | G | 6HG | 6HG A3 | chain-preserving | 0.0779 | 0.2614 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 47 | A51 | A | 6HA | 6HA A5 | chain-preserving | 0.6870 | 0.1909 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 48 | A52 | G | 6HG | 6HG A1 | chain-preserving | 0.7250 | 0.1755 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 49 | A53 | A | 6HA | 6HA A7 | chain-preserving | 0.1712 | 0.2772 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 50 | A54 | G | 6HG | 6HG A3 | chain-preserving | 0.1222 | 0.2608 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 51 | A55 | G | 6HG | 6HG A1 | chain-preserving | 0.7052 | 0.1948 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 52 | A56 | U | 6HU | 6HT A4 | chain-preserving | 0.6486 | 0.2643 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 53 | A57 | G | 6HG | 6HG A3 | chain-preserving | 0.5488 | 0.2611 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 54 | A58 | A | 6HA | 6HA A5 | chain-preserving | 0.6951 | 0.1936 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 55 | A59 | A | 6HA | 6HA A7 | chain-preserving | 0.1211 | 0.2767 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 56 | A60 | G | 6HG | 6HG A1 | chain-preserving | 0.7066 | 0.1906 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 57 | A61 | A | 6HA | 6HA A5 | chain-preserving | 0.6776 | 0.2009 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 58 | A62 | A | 6HA | 6HA A7 | chain-preserving | 0.4857 | 0.4504 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 59 | A63 | U | 6HU | 6HT A2 | chain-preserving | 0.4734 | 0.3324 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 60 | A64 | A | 6HA | 6HA A5 | chain-preserving | 0.6594 | 0.2180 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 61 | A65 | C | 6HC | 6HC A8 | chain-preserving | 0.4703 | 0.3507 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 62 | A66 | G | 6HG | 6HG A3 | chain-preserving | 0.4210 | 0.3584 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 63 | A67 | A | 6HA | 6HA A7 | chain-preserving | 0.1388 | 0.2751 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 64 | A68 | C | 6HC | 6HC A6 | chain-preserving | 0.1051 | 0.2505 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 65 | A69 | C | 6HC | 6HC A8 | chain-preserving | 0.0875 | 0.2736 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 66 | A70 | A | 6HA | 6HA A5 | chain-preserving | 0.6917 | 0.1890 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 67 | A71 | C | 6HC | 6HC A6 | chain-preserving | 0.1502 | 0.2435 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 68 | A72 | C | 6HC | 6HC A8 | chain-preserving | 0.1509 | 0.2696 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 69 | A73 | U | 6HU | 6HT A4 | chain-preserving | 0.1001 | 0.2603 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 70 | A74 | A | 6HA | 6HA A7 | chain-preserving | 0.1094 | 0.2731 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 71 | A75 | G | 6HG | 6HG A1 | chain-preserving | 0.7004 | 0.1900 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 72 | A76 | G | 6HG | 6HG A3 | chain-preserving | 0.7019 | 0.2700 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 73 | A77 | C | 6HC | 6HC A6 | chain-preserving | 0.1149 | 0.2492 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 74 | A78 | U | 6HU | 6HT A2 | chain-preserving | 0.5855 | 0.2455 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 75 | A79 | C | 6HC | 6HC A8 | chain-preserving | 0.4243 | 0.3256 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 76 | A80 | G | 6HG | 6HG A1 | chain-preserving | 0.6335 | 0.2285 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 77 | A81 | A | 6HA | 6HA A5 | chain-preserving | 0.3039 | 0.3160 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 78 | A82 | A | 6HA | 6HA A7 | chain-preserving | 0.2125 | 0.2679 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 79 | A83 | A | 6HA | 6HA A5 | chain-preserving | 0.6772 | 0.1968 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 80 | A84 | G | 6HG | 6HG A3 | chain-preserving | 0.7390 | 0.2966 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 81 | A85 | A | 6HA | 6HA A7 | chain-preserving | 0.1213 | 0.2738 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 82 | A86 | G | 6HG | 6HG A1 | chain-preserving | 0.6867 | 0.1975 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 83 | A87 | C | 6HC | 6HC A6 | chain-preserving | 0.1284 | 0.2455 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 84 | A88 | C | 6HC | 6HC A8 | chain-preserving | 0.1159 | 0.2736 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 85 | A89 | U | 6HU | 6HT A4 | chain-preserving | 0.1062 | 0.2623 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 86 | A90 | A | 6HA | 6HA A5 | chain-preserving | 0.6888 | 0.1933 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 87 | A91 | A | 6HA | 6HA A7 | chain-preserving | 0.5126 | 0.3405 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 88 | A92 | A | 6HA | 6HA A5 | chain-preserving | 0.7945 | 0.4683 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 89 | A93 | A | 6HA | 6HA A7 | chain-preserving | 0.1107 | 0.2769 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 90 | A94 | C | 6HC | 6HC A6 | chain-preserving | 0.1028 | 0.2468 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 91 | A95 | A | 6HA | 6HA A5 | chain-preserving | 0.6859 | 0.1960 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 92 | A96 | U | 6HU | 6HT A2 | chain-preserving | 0.7211 | 0.2620 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 93 | A97 | A | 6HA | 6HA A7 | chain-preserving | 0.1131 | 0.2756 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 94 | A98 | C | 6HC | 6HC A8 | chain-preserving | 0.1056 | 0.2731 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 95 | A99 | C | 6HC | 6HC A6 | chain-preserving | 0.1035 | 0.2472 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 96 | A100 | U | 6HU | 6HT A4 | chain-preserving | 0.1116 | 0.2601 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 97 | A101 | U | 6HU | 6HT A2 | chain-preserving | 0.1013 | 0.2433 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 98 | A102 | U | 6HU | 6HT A4 | chain-preserving | 0.1009 | 0.2632 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 99 | A103 | C | 6HC | 6HC A8 | chain-preserving | 0.5737 | 0.3473 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 100 | A104 | C | 6HC | 6HC A6 | chain-preserving | 0.7384 | 0.2744 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 101 | A105 | U | 6HU | 6HT A2 | chain-preserving | 0.1030 | 0.2447 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 102 | A106 | G | 6HG | 6HG A3 | chain-preserving | 0.0877 | 0.2611 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 103 | A107 | G | 6HG | 6HG A1 | chain-preserving | 0.1493 | 0.2743 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 104 | A108 | A | 6HA | 6HA A5 | chain-preserving | 0.3130 | 0.3196 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 105 | A109 | U | 6HU | 6HT A4 | chain-preserving | 0.1171 | 0.2626 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 106 | A110 | U | 6HU | 6HT A2 | chain-preserving | 0.5137 | 0.3249 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 107 | A111 | C | 6HC | 6HC A8 | chain-preserving | 0.1131 | 0.2757 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 108 | A112 | C | 6HC | 6HC A6 | chain-preserving | 0.6849 | 0.2642 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 109 | A115 | U | 6HU | 6HT A4 | chain-preserving | 0.1070 | 0.2605 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 110 | A116 | G | 6HG | 6HG A3 | chain-preserving | 0.7354 | 0.2888 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 111 | A117 | C | 6HC | 6HC A8 | chain-preserving | 0.9276 | 0.4240 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |

---

## Scientific Interpretation

This output should be interpreted as:

> an HNA-like computational candidate generated by template-guided or chain-preserving reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed HNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- `6HU` residue labels are provisional when RNA `U` is preserved.
- Chain-preserving mode preserves the RNA chain path and inserts local HNA scaffold atoms; it is not a fully de novo HNA fold prediction.
- HNA stereochemistry requires expert review.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect in PyMOL, ChimeraX, Discovery Studio, VMD, or Mol*.
2. Inspect the HNA ring/scaffold geometry.
3. Compare against the 481D HNA template.
4. Check C1′→glycosidic N and HNA local scaffold distances.
5. Add topology/connectivity support in future versions.
6. Perform energy minimization only with appropriate HNA parameters.
7. Treat large RNA outputs as candidate geometry, not validated HNA folds.
