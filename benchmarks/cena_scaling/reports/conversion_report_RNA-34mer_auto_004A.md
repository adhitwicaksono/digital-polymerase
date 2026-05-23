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

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- CeNA template PDB: `/mnt/data/2H0N_CeNA_8mer_clean_ss.pdb`
- Output PDB: `/mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-34mer_auto_004A.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC`
- CeNA template base-class sequence: `GUGUACAC`
- Source residue count: `34`
- Template residue count: `8`
- Converted residues: `34`
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

- Mean template/local anchor RMSD: `0.8255 Å`
- Maximum template/local anchor RMSD: `0.9435 Å`
- Mean base-transplant anchor RMSD: `0.5651 Å`
- Maximum base-transplant anchor RMSD: `0.7666 Å`
- Mean C1′→glycosidic N distance: `1.4932 Å`
- Maximum C1′→glycosidic N distance: `1.4996 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 34 | 0 | 0 | 1.527 | 1.521 | 1.530 | 1.35–1.85 | PASS |
| C1'→C2' | CeNA template | 8 | 0 | 0 | 1.560 | 1.550 | 1.572 | 1.35–1.85 | PASS |
| C1'→C2' | output | 34 | 0 | 0 | 1.560 | 1.550 | 1.572 | 1.35–1.85 | PASS |
| C1'→glycosidic N | source RNA | 34 | 0 | 0 | 1.474 | 1.462 | 1.480 | 1.30–1.75 | PASS |
| C1'→glycosidic N | CeNA template | 8 | 0 | 0 | 1.493 | 1.484 | 1.500 | 1.30–1.75 | PASS |
| C1'→glycosidic N | output | 34 | 0 | 0 | 1.493 | 1.484 | 1.500 | 1.30–1.75 | PASS |
| C2'→C3' | source RNA | 34 | 0 | 0 | 1.522 | 1.519 | 1.525 | 1.35–1.85 | PASS |
| C2'→C3' | CeNA template | 8 | 0 | 0 | 1.533 | 1.522 | 1.545 | 1.35–1.85 | PASS |
| C2'→C3' | output | 34 | 0 | 26 | 2.280 | 1.565 | 2.580 | 1.35–1.85 | FAIL |
| C3'→C4' | source RNA | 34 | 0 | 0 | 1.520 | 1.516 | 1.529 | 1.35–1.85 | PASS |
| C3'→C4' | CeNA template | 8 | 0 | 0 | 1.540 | 1.523 | 1.565 | 1.35–1.85 | PASS |
| C3'→C4' | output | 34 | 0 | 0 | 1.520 | 1.516 | 1.529 | 1.35–1.85 | PASS |
| C3'→O3' | source RNA | 34 | 0 | 0 | 1.418 | 1.414 | 1.429 | 1.20–1.65 | PASS |
| C3'→O3' | CeNA template | 8 | 0 | 0 | 1.414 | 1.397 | 1.422 | 1.20–1.65 | PASS |
| C3'→O3' | output | 34 | 0 | 0 | 1.418 | 1.414 | 1.429 | 1.20–1.65 | PASS |
| C4'→C5' | source RNA | 34 | 0 | 0 | 1.507 | 1.504 | 1.510 | 1.30–1.80 | PASS |
| C4'→C5' | CeNA template | 8 | 0 | 0 | 1.505 | 1.494 | 1.521 | 1.30–1.80 | PASS |
| C4'→C5' | output | 34 | 0 | 0 | 1.507 | 1.504 | 1.510 | 1.30–1.80 | PASS |
| C4'→C6' | CeNA template | 8 | 0 | 0 | 1.458 | 1.451 | 1.467 | 1.20–1.70 | PASS |
| C4'→C6' | output | 34 | 0 | 28 | 1.835 | 1.335 | 2.268 | 1.20–1.70 | FAIL |
| C5'→O5' | source RNA | 34 | 0 | 0 | 1.419 | 1.418 | 1.423 | 1.20–1.75 | PASS |
| C5'→O5' | CeNA template | 7 | 1 | 0 | 1.444 | 1.425 | 1.481 | 1.20–1.75 | PASS |
| C5'→O5' | output | 34 | 0 | 0 | 1.419 | 1.418 | 1.423 | 1.20–1.75 | PASS |
| C6'→C7' | CeNA template | 8 | 0 | 0 | 1.322 | 1.310 | 1.332 | 1.15–1.50 | PASS |
| C6'→C7' | output | 34 | 0 | 0 | 1.321 | 1.310 | 1.332 | 1.15–1.50 | PASS |
| C7'→C1' | CeNA template | 8 | 0 | 0 | 1.559 | 1.547 | 1.568 | 1.30–1.85 | PASS |
| C7'→C1' | output | 34 | 0 | 0 | 1.560 | 1.547 | 1.568 | 1.30–1.85 | PASS |
| O3'(i)→P(i+1) | source RNA | 33 | 0 | 0 | 1.606 | 1.603 | 1.610 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | CeNA template | 7 | 0 | 0 | 1.603 | 1.593 | 1.624 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 33 | 0 | 0 | 1.606 | 1.603 | 1.610 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source RNA | 34 | 0 | 0 | 1.591 | 1.588 | 1.595 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | CeNA template | 7 | 1 | 0 | 1.642 | 1.624 | 1.658 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | output | 34 | 0 | 0 | 1.591 | 1.588 | 1.595 | 1.35–1.90 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output CeNA C4′–C6′ links

| Rank | Link | Distance (Å) | Expected range (Å) | Status |
|---:|---|---:|---|---|
| 1 | `A65:C4' → A65:C6'` | 2.268 | 1.20–1.70 | FAIL |
| 2 | `A82:C4' → A82:C6'` | 2.218 | 1.20–1.70 | FAIL |
| 3 | `A63:C4' → A63:C6'` | 2.212 | 1.20–1.70 | FAIL |
| 4 | `A67:C4' → A67:C6'` | 2.130 | 1.20–1.70 | FAIL |
| 5 | `A66:C4' → A66:C6'` | 2.091 | 1.20–1.70 | FAIL |
| 6 | `A59:C4' → A59:C6'` | 2.081 | 1.20–1.70 | FAIL |
| 7 | `A85:C4' → A85:C6'` | 2.062 | 1.20–1.70 | FAIL |
| 8 | `A81:C4' → A81:C6'` | 2.046 | 1.20–1.70 | FAIL |
| 9 | `A74:C4' → A74:C6'` | 2.010 | 1.20–1.70 | FAIL |
| 10 | `A78:C4' → A78:C6'` | 1.987 | 1.20–1.70 | FAIL |
| 11 | `A80:C4' → A80:C6'` | 1.930 | 1.20–1.70 | FAIL |
| 12 | `A56:C4' → A56:C6'` | 1.851 | 1.20–1.70 | FAIL |
| 13 | `A55:C4' → A55:C6'` | 1.845 | 1.20–1.70 | FAIL |
| 14 | `A77:C4' → A77:C6'` | 1.833 | 1.20–1.70 | FAIL |
| 15 | `A86:C4' → A86:C6'` | 1.830 | 1.20–1.70 | FAIL |
| 16 | `A87:C4' → A87:C6'` | 1.825 | 1.20–1.70 | FAIL |
| 17 | `A60:C4' → A60:C6'` | 1.825 | 1.20–1.70 | FAIL |
| 18 | `A64:C4' → A64:C6'` | 1.824 | 1.20–1.70 | FAIL |
| 19 | `A71:C4' → A71:C6'` | 1.815 | 1.20–1.70 | FAIL |
| 20 | `A75:C4' → A75:C6'` | 1.798 | 1.20–1.70 | FAIL |

### Worst output CeNA C6′–C7′ links

No failed links detected.

### Worst output CeNA C7′–C1′ links

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Template/local RMSD (Å) | Base RMSD (Å) | C1′–N (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 1 | A54 | G | XGL | XGL A1 | chain-preserving | 0.5447 | 0.2611 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 2 | A55 | G | XGL | XGL A3 | chain-preserving | 0.8996 | 0.6753 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 3 | A56 | U | XUL | XTL A2 | chain-preserving | 0.6880 | 0.1786 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 4 | A57 | G | XGL | XGL A1 | chain-preserving | 0.5452 | 0.2539 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 5 | A58 | A | XAL | XAL A5 | chain-preserving | 0.8703 | 0.6269 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 6 | A59 | A | XAL | XAL A7 | chain-preserving | 0.8953 | 0.7541 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 7 | A60 | G | XGL | XGL A3 | chain-preserving | 0.8987 | 0.6748 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 8 | A61 | A | XAL | XAL A5 | chain-preserving | 0.8766 | 0.6307 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 9 | A62 | A | XAL | XAL A7 | chain-preserving | 0.6826 | 0.5082 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 10 | A63 | U | XUL | XTL A4 | chain-preserving | 0.6957 | 0.5439 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 11 | A64 | A | XAL | XAL A5 | chain-preserving | 0.8862 | 0.6388 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 12 | A65 | C | XCL | XCL A6 | chain-preserving | 0.7069 | 0.5556 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 13 | A66 | G | XGL | XGL A1 | chain-preserving | 0.7750 | 0.4662 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 14 | A67 | A | XAL | XAL A7 | chain-preserving | 0.8958 | 0.7616 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 15 | A68 | C | XCL | XCL A8 | chain-preserving | 0.9115 | 0.6810 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 16 | A69 | C | XCL | XCL A6 | chain-preserving | 0.9072 | 0.6664 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 17 | A70 | A | XAL | XAL A5 | chain-preserving | 0.8710 | 0.6190 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 18 | A71 | C | XCL | XCL A8 | chain-preserving | 0.9435 | 0.6789 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 19 | A72 | C | XCL | XCL A6 | chain-preserving | 0.9161 | 0.6697 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 20 | A73 | U | XUL | XTL A2 | chain-preserving | 0.9190 | 0.6617 | 1.4844 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 21 | A74 | A | XAL | XAL A7 | chain-preserving | 0.9007 | 0.7522 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 22 | A75 | G | XGL | XGL A3 | chain-preserving | 0.9022 | 0.6597 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 23 | A76 | G | XGL | XGL A1 | chain-preserving | 0.5449 | 0.2625 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 24 | A77 | C | XCL | XCL A8 | chain-preserving | 0.9289 | 0.6828 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 25 | A78 | U | XUL | XTL A4 | chain-preserving | 0.8500 | 0.2085 | 1.4996 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 26 | A79 | C | XCL | XCL A6 | chain-preserving | 0.8053 | 0.4961 | 1.4947 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 27 | A80 | G | XGL | XGL A3 | chain-preserving | 0.9196 | 0.6804 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 28 | A81 | A | XAL | XAL A5 | chain-preserving | 0.8192 | 0.2009 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 29 | A82 | A | XAL | XAL A7 | chain-preserving | 0.9101 | 0.7666 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 30 | A83 | A | XAL | XAL A5 | chain-preserving | 0.8765 | 0.6272 | 1.4965 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 31 | A84 | G | XGL | XGL A1 | chain-preserving | 0.5463 | 0.2575 | 1.4993 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 32 | A85 | A | XAL | XAL A7 | chain-preserving | 0.8961 | 0.7604 | 1.4920 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 33 | A86 | G | XGL | XGL A3 | chain-preserving | 0.9044 | 0.6687 | 1.4891 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |
| 34 | A87 | C | XCL | XCL A8 | chain-preserving | 0.9320 | 0.6850 | 1.4876 | exact base-class CeNA template; RNA chain atoms preserved; CeNA local scaffold inserted; RNA base transformed |

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
