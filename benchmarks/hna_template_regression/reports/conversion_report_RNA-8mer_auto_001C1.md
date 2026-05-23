# RNA → HNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 001B/001C  
**Requested mode:** `auto`  
**Actual mode:** `full-template`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**Base-attachment status:** `PASS`  
**HNA local scaffold status:** `C1′→C6′ PASS`, `C6′→O4′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-8mer.pdb`
- HNA template PDB: `/mnt/data/481d-HNA8nt.pdb`
- Output PDB: `/mnt/data/hna_full_prototype_001C1_outputs/converted_hna_RNA-8mer_auto_001C1.pdb`

---

## Source and Template

- Source RNA sequence: `CUAGGCUC`
- HNA template base-class sequence: `GUGUACAC`
- Source residue count: `8`
- Template residue count: `8`
- Converted residues: `8`
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
- Actual mode: `full-template`
- Full-template anchors: `C1', C2', C4'`
- Chain-preserving HNA-template anchors: `C3', C4', C5', O5', O3'`
- Base-transplant anchors: `C1', C2', C4'`
- Base label policy: `preserve`

---

## Alignment Summary

- Mean template/local anchor RMSD: `0.2454 Å`
- Maximum template/local anchor RMSD: `0.2642 Å`
- Mean base-transplant anchor RMSD: `nan Å`
- Maximum base-transplant anchor RMSD: `nan Å`
- Mean C1′→glycosidic N distance: `1.4386 Å`
- Maximum C1′→glycosidic N distance: `1.4877 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 8 | 0 | 0 | 1.527 | 1.522 | 1.530 | 1.35–1.90 | PASS |
| C1'→C2' | HNA template | 8 | 0 | 0 | 1.667 | 1.642 | 1.685 | 1.35–1.90 | PASS |
| C1'→C2' | output | 8 | 0 | 0 | 1.667 | 1.642 | 1.685 | 1.35–1.90 | PASS |
| C1'→C6' | HNA template | 8 | 0 | 0 | 1.599 | 1.573 | 1.613 | 1.35–1.85 | PASS |
| C1'→C6' | output | 8 | 0 | 0 | 1.599 | 1.573 | 1.613 | 1.35–1.85 | PASS |
| C1'→glycosidic N | source RNA | 8 | 0 | 0 | 1.477 | 1.473 | 1.480 | 1.30–1.70 | PASS |
| C1'→glycosidic N | HNA template | 8 | 0 | 0 | 1.474 | 1.457 | 1.488 | 1.30–1.70 | PASS |
| C1'→glycosidic N | output | 8 | 0 | 0 | 1.439 | 1.380 | 1.488 | 1.30–1.70 | PASS |
| C2'→C3' | source RNA | 8 | 0 | 0 | 1.522 | 1.520 | 1.523 | 1.35–1.85 | PASS |
| C2'→C3' | HNA template | 8 | 0 | 0 | 1.581 | 1.559 | 1.595 | 1.35–1.85 | PASS |
| C2'→C3' | output | 8 | 0 | 0 | 1.581 | 1.559 | 1.595 | 1.35–1.85 | PASS |
| C4'→O4' | HNA template | 8 | 0 | 0 | 1.444 | 1.438 | 1.454 | 1.20–1.70 | PASS |
| C4'→O4' | output | 8 | 0 | 0 | 1.444 | 1.438 | 1.454 | 1.20–1.70 | PASS |
| C6'→O4' | HNA template | 8 | 0 | 0 | 1.391 | 1.379 | 1.410 | 1.20–1.60 | PASS |
| C6'→O4' | output | 8 | 0 | 0 | 1.391 | 1.379 | 1.410 | 1.20–1.60 | PASS |
| O3'(i)→P(i+1) | source RNA | 7 | 0 | 0 | 1.606 | 1.604 | 1.609 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | HNA template | 7 | 0 | 0 | 1.591 | 1.581 | 1.601 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 7 | 0 | 0 | 1.591 | 1.581 | 1.601 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source RNA | 8 | 0 | 0 | 1.591 | 1.590 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | HNA template | 7 | 1 | 0 | 1.564 | 1.557 | 1.574 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 7 | 1 | 0 | 1.564 | 1.557 | 1.574 | 1.40–1.80 | PASS |

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
| 1 | A72 | C | 6HC | 6HG A1 | full-template | 0.2308 | NA | 1.3800 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 2 | A73 | U | 6HU | 6HT A2 | full-template | 0.2316 | NA | 1.4570 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 3 | A74 | A | 6HA | 6HG A3 | full-template | 0.2539 | NA | 1.4877 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 4 | A75 | G | 6HG | 6HT A4 | full-template | 0.2502 | NA | 1.3800 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 5 | A76 | G | 6HG | 6HA A5 | full-template | 0.2441 | NA | 1.4767 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 6 | A77 | C | 6HC | 6HC A6 | full-template | 0.2324 | NA | 1.4782 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 7 | A78 | U | 6HU | 6HA A7 | full-template | 0.2642 | NA | 1.3800 | full HNA scaffold from corresponding template residue; transformed source RNA base |
| 8 | A79 | C | 6HC | 6HC A8 | full-template | 0.2562 | NA | 1.4695 | full HNA scaffold from corresponding template residue; transformed source RNA base |

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
