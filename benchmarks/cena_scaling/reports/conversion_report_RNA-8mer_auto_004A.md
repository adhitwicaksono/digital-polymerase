# RNA → CeNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 004A  
**Requested mode:** `auto`  
**Actual mode:** `full-template`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**Base-attachment status:** `PASS`  
**CeNA local scaffold status:** `C4′→C6′ PASS`, `C6′→C7′ PASS`, `C7′→C1′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-8mer.pdb`
- CeNA template PDB: `/mnt/data/2H0N_CeNA_8mer_clean_ss.pdb`
- Output PDB: `/mnt/data/cena_prototype_004A_outputs/converted_cena_RNA-8mer_auto_004A.pdb`

---

## Source and Template

- Source RNA sequence: `CUAGGCUC`
- CeNA template base-class sequence: `GUGUACAC`
- Source residue count: `8`
- Template residue count: `8`
- Converted residues: `8`
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
- Actual mode: `full-template`
- Full-template anchors: `C1', C2', C3', C4'`
- Chain-preserving CeNA-template anchors: `O5', C5', C4', C3', O3'`
- Base-transplant anchors: `C1', C2', C3', C4'`
- Base label policy: `preserve`

---

## Alignment Summary

- Mean template/local anchor RMSD: `0.5160 Å`
- Maximum template/local anchor RMSD: `0.5421 Å`
- Mean base-transplant anchor RMSD: `nan Å`
- Maximum base-transplant anchor RMSD: `nan Å`
- Mean C1′→glycosidic N distance: `1.4865 Å`
- Maximum C1′→glycosidic N distance: `1.4965 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 8 | 0 | 0 | 1.527 | 1.522 | 1.530 | 1.35–1.85 | PASS |
| C1'→C2' | CeNA template | 8 | 0 | 0 | 1.560 | 1.550 | 1.572 | 1.35–1.85 | PASS |
| C1'→C2' | output | 8 | 0 | 0 | 1.560 | 1.550 | 1.572 | 1.35–1.85 | PASS |
| C1'→glycosidic N | source RNA | 8 | 0 | 0 | 1.477 | 1.473 | 1.480 | 1.30–1.75 | PASS |
| C1'→glycosidic N | CeNA template | 8 | 0 | 0 | 1.493 | 1.484 | 1.500 | 1.30–1.75 | PASS |
| C1'→glycosidic N | output | 8 | 0 | 0 | 1.487 | 1.480 | 1.497 | 1.30–1.75 | PASS |
| C2'→C3' | source RNA | 8 | 0 | 0 | 1.522 | 1.520 | 1.523 | 1.35–1.85 | PASS |
| C2'→C3' | CeNA template | 8 | 0 | 0 | 1.533 | 1.522 | 1.545 | 1.35–1.85 | PASS |
| C2'→C3' | output | 8 | 0 | 0 | 1.533 | 1.522 | 1.545 | 1.35–1.85 | PASS |
| C3'→C4' | source RNA | 8 | 0 | 0 | 1.519 | 1.516 | 1.523 | 1.35–1.85 | PASS |
| C3'→C4' | CeNA template | 8 | 0 | 0 | 1.540 | 1.523 | 1.565 | 1.35–1.85 | PASS |
| C3'→C4' | output | 8 | 0 | 0 | 1.540 | 1.523 | 1.565 | 1.35–1.85 | PASS |
| C3'→O3' | source RNA | 8 | 0 | 0 | 1.417 | 1.415 | 1.425 | 1.20–1.65 | PASS |
| C3'→O3' | CeNA template | 8 | 0 | 0 | 1.414 | 1.397 | 1.422 | 1.20–1.65 | PASS |
| C3'→O3' | output | 8 | 0 | 0 | 1.414 | 1.397 | 1.422 | 1.20–1.65 | PASS |
| C4'→C5' | source RNA | 8 | 0 | 0 | 1.507 | 1.506 | 1.509 | 1.30–1.80 | PASS |
| C4'→C5' | CeNA template | 8 | 0 | 0 | 1.505 | 1.494 | 1.521 | 1.30–1.80 | PASS |
| C4'→C5' | output | 8 | 0 | 0 | 1.505 | 1.494 | 1.521 | 1.30–1.80 | PASS |
| C4'→C6' | CeNA template | 8 | 0 | 0 | 1.458 | 1.451 | 1.467 | 1.20–1.70 | PASS |
| C4'→C6' | output | 8 | 0 | 0 | 1.458 | 1.451 | 1.467 | 1.20–1.70 | PASS |
| C5'→O5' | source RNA | 8 | 0 | 0 | 1.419 | 1.418 | 1.421 | 1.20–1.75 | PASS |
| C5'→O5' | CeNA template | 7 | 1 | 0 | 1.444 | 1.425 | 1.481 | 1.20–1.75 | PASS |
| C5'→O5' | output | 7 | 1 | 0 | 1.444 | 1.425 | 1.481 | 1.20–1.75 | PASS |
| C6'→C7' | CeNA template | 8 | 0 | 0 | 1.322 | 1.310 | 1.332 | 1.15–1.50 | PASS |
| C6'→C7' | output | 8 | 0 | 0 | 1.322 | 1.310 | 1.332 | 1.15–1.50 | PASS |
| C7'→C1' | CeNA template | 8 | 0 | 0 | 1.559 | 1.547 | 1.568 | 1.30–1.85 | PASS |
| C7'→C1' | output | 8 | 0 | 0 | 1.559 | 1.547 | 1.568 | 1.30–1.85 | PASS |
| O3'(i)→P(i+1) | source RNA | 7 | 0 | 0 | 1.606 | 1.604 | 1.609 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | CeNA template | 7 | 0 | 0 | 1.603 | 1.593 | 1.624 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 7 | 0 | 0 | 1.603 | 1.593 | 1.624 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source RNA | 8 | 0 | 0 | 1.591 | 1.590 | 1.595 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | CeNA template | 7 | 1 | 0 | 1.642 | 1.624 | 1.658 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | output | 7 | 1 | 0 | 1.642 | 1.624 | 1.658 | 1.35–1.90 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output CeNA C4′–C6′ links

No failed links detected.

### Worst output CeNA C6′–C7′ links

No failed links detected.

### Worst output CeNA C7′–C1′ links

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Template/local RMSD (Å) | Base RMSD (Å) | C1′–N (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 1 | A72 | C | XCL | XGL A1 | full-template | 0.5377 | NA | 1.4800 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 2 | A73 | U | XUL | XTL A2 | full-template | 0.5126 | NA | 1.4844 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 3 | A74 | A | XAL | XGL A3 | full-template | 0.5002 | NA | 1.4891 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 4 | A75 | G | XGL | XTL A4 | full-template | 0.5091 | NA | 1.4800 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 5 | A76 | G | XGL | XAL A5 | full-template | 0.4886 | NA | 1.4965 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 6 | A77 | C | XCL | XCL A6 | full-template | 0.5045 | NA | 1.4947 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 7 | A78 | U | XUL | XAL A7 | full-template | 0.5336 | NA | 1.4800 | full CeNA scaffold from corresponding template residue; transformed source RNA base |
| 8 | A79 | C | XCL | XCL A8 | full-template | 0.5421 | NA | 1.4876 | full CeNA scaffold from corresponding template residue; transformed source RNA base |

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
