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

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- HNA template PDB: `/mnt/data/481d-HNA8nt.pdb`
- Output PDB: `/mnt/data/hna_full_prototype_001C1_outputs/converted_hna_RNA-34mer_auto_001C1.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC`
- HNA template base-class sequence: `GUGUACAC`
- Source residue count: `34`
- Template residue count: `8`
- Converted residues: `34`
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

- Mean template/local anchor RMSD: `0.3216 Å`
- Maximum template/local anchor RMSD: `0.8427 Å`
- Mean base-transplant anchor RMSD: `0.2675 Å`
- Maximum base-transplant anchor RMSD: `0.4504 Å`
- Mean C1′→glycosidic N distance: `1.4756 Å`
- Maximum C1′→glycosidic N distance: `1.4877 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 34 | 0 | 0 | 1.527 | 1.521 | 1.530 | 1.35–1.90 | PASS |
| C1'→C2' | HNA template | 8 | 0 | 0 | 1.667 | 1.642 | 1.685 | 1.35–1.90 | PASS |
| C1'→C2' | output | 34 | 0 | 0 | 1.667 | 1.642 | 1.685 | 1.35–1.90 | PASS |
| C1'→C6' | HNA template | 8 | 0 | 0 | 1.599 | 1.573 | 1.613 | 1.35–1.85 | PASS |
| C1'→C6' | output | 34 | 0 | 0 | 1.601 | 1.573 | 1.613 | 1.35–1.85 | PASS |
| C1'→glycosidic N | source RNA | 34 | 0 | 0 | 1.474 | 1.462 | 1.480 | 1.30–1.70 | PASS |
| C1'→glycosidic N | HNA template | 8 | 0 | 0 | 1.474 | 1.457 | 1.488 | 1.30–1.70 | PASS |
| C1'→glycosidic N | output | 34 | 0 | 0 | 1.476 | 1.457 | 1.488 | 1.30–1.70 | PASS |
| C2'→C3' | source RNA | 34 | 0 | 0 | 1.522 | 1.519 | 1.525 | 1.35–1.85 | PASS |
| C2'→C3' | HNA template | 8 | 0 | 0 | 1.581 | 1.559 | 1.595 | 1.35–1.85 | PASS |
| C2'→C3' | output | 34 | 0 | 9 | 1.707 | 1.424 | 2.364 | 1.35–1.85 | FAIL |
| C4'→O4' | HNA template | 8 | 0 | 0 | 1.444 | 1.438 | 1.454 | 1.20–1.70 | PASS |
| C4'→O4' | output | 34 | 0 | 4 | 1.505 | 1.342 | 1.920 | 1.20–1.70 | FAIL |
| C6'→O4' | HNA template | 8 | 0 | 0 | 1.391 | 1.379 | 1.410 | 1.20–1.60 | PASS |
| C6'→O4' | output | 34 | 0 | 0 | 1.392 | 1.379 | 1.410 | 1.20–1.60 | PASS |
| O3'(i)→P(i+1) | source RNA | 33 | 0 | 0 | 1.606 | 1.603 | 1.610 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | HNA template | 7 | 0 | 0 | 1.591 | 1.581 | 1.601 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 33 | 0 | 0 | 1.606 | 1.603 | 1.610 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source RNA | 34 | 0 | 0 | 1.591 | 1.588 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | HNA template | 7 | 1 | 0 | 1.564 | 1.557 | 1.574 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 34 | 0 | 0 | 1.591 | 1.588 | 1.595 | 1.40–1.80 | PASS |

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
| 1 | A54 | G | 6HG | 6HG A1 | chain-preserving | 0.6560 | 0.2192 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 2 | A55 | G | 6HG | 6HG A3 | chain-preserving | 0.0834 | 0.2632 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 3 | A56 | U | 6HU | 6HT A2 | chain-preserving | 0.6844 | 0.2568 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 4 | A57 | G | 6HG | 6HG A1 | chain-preserving | 0.3152 | 0.2976 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 5 | A58 | A | 6HA | 6HA A5 | chain-preserving | 0.6951 | 0.1936 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 6 | A59 | A | 6HA | 6HA A7 | chain-preserving | 0.1211 | 0.2767 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 7 | A60 | G | 6HG | 6HG A3 | chain-preserving | 0.0837 | 0.2625 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 8 | A61 | A | 6HA | 6HA A5 | chain-preserving | 0.6776 | 0.2009 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 9 | A62 | A | 6HA | 6HA A7 | chain-preserving | 0.4857 | 0.4504 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 10 | A63 | U | 6HU | 6HT A4 | chain-preserving | 0.4530 | 0.3552 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 11 | A64 | A | 6HA | 6HA A5 | chain-preserving | 0.6594 | 0.2180 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 12 | A65 | C | 6HC | 6HC A6 | chain-preserving | 0.4616 | 0.3267 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 13 | A66 | G | 6HG | 6HG A1 | chain-preserving | 0.8427 | 0.3137 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 14 | A67 | A | 6HA | 6HA A7 | chain-preserving | 0.1388 | 0.2751 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 15 | A68 | C | 6HC | 6HC A8 | chain-preserving | 0.0958 | 0.2762 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 16 | A69 | C | 6HC | 6HC A6 | chain-preserving | 0.1047 | 0.2480 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 17 | A70 | A | 6HA | 6HA A5 | chain-preserving | 0.6917 | 0.1890 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 18 | A71 | C | 6HC | 6HC A8 | chain-preserving | 0.1644 | 0.2696 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 19 | A72 | C | 6HC | 6HC A6 | chain-preserving | 0.1388 | 0.2436 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 20 | A73 | U | 6HU | 6HT A2 | chain-preserving | 0.0964 | 0.2414 | 1.4570 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 21 | A74 | A | 6HA | 6HA A7 | chain-preserving | 0.1094 | 0.2731 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 22 | A75 | G | 6HG | 6HG A3 | chain-preserving | 0.0799 | 0.2614 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 23 | A76 | G | 6HG | 6HG A1 | chain-preserving | 0.1405 | 0.2710 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 24 | A77 | C | 6HC | 6HC A8 | chain-preserving | 0.1212 | 0.2752 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 25 | A78 | U | 6HU | 6HT A4 | chain-preserving | 0.5464 | 0.2556 | 1.4804 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 26 | A79 | C | 6HC | 6HC A6 | chain-preserving | 0.4479 | 0.2992 | 1.4782 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 27 | A80 | G | 6HG | 6HG A3 | chain-preserving | 0.1524 | 0.2590 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 28 | A81 | A | 6HA | 6HA A5 | chain-preserving | 0.3039 | 0.3160 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 29 | A82 | A | 6HA | 6HA A7 | chain-preserving | 0.2125 | 0.2679 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 30 | A83 | A | 6HA | 6HA A5 | chain-preserving | 0.6772 | 0.1968 | 1.4767 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 31 | A84 | G | 6HG | 6HG A1 | chain-preserving | 0.1496 | 0.2357 | 1.4647 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 32 | A85 | A | 6HA | 6HA A7 | chain-preserving | 0.1213 | 0.2738 | 1.4807 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 33 | A86 | G | 6HG | 6HG A3 | chain-preserving | 0.0860 | 0.2603 | 1.4877 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |
| 34 | A87 | C | 6HC | 6HC A8 | chain-preserving | 0.1377 | 0.2715 | 1.4695 | exact base-class HNA template; RNA chain atoms preserved; HNA local scaffold inserted; RNA base transformed |

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
