# RNA → FANA Chain-Preserving Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 003A  
**Method:** Chain-preserving RNA → FANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**C2′–F status:** `PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-8mer.pdb`
- FANA template PDB: `/mnt/data/2KP4_FANA_10mer.pdb`
- Output PDB: `/mnt/data/fana_patch_003A_outputs/converted_fana_RNA-8mer_003A.pdb`

---

## Source Sequence

```text
CUAGGCUC
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

- Converted residues: `8`
- Mean anchor RMSD: `0.0477 Å`
- Maximum anchor RMSD: `0.0726 Å`
- Mean C2′–F distance: `1.3822 Å`
- Maximum C2′–F distance: `1.3838 Å`

Important:

> Chain continuity is preserved by keeping the RNA polymer-chain atoms. FANA-like local 2′ geometry is introduced from the FANA template.

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source | 8 | 0 | 0 | 1.527 | 1.522 | 1.530 | 1.35–1.75 | PASS |
| C1'→C2' | output | 8 | 0 | 0 | 1.548 | 1.526 | 1.561 | 1.35–1.75 | PASS |
| C2'→C3' | source | 8 | 0 | 0 | 1.522 | 1.520 | 1.523 | 1.35–1.75 | PASS |
| C2'→C3' | output | 8 | 0 | 0 | 1.509 | 1.500 | 1.516 | 1.35–1.75 | PASS |
| C2'→F2' | output | 8 | 0 | 0 | 1.382 | 1.381 | 1.384 | 1.25–1.50 | PASS |
| O3'(i)→P(i+1) | source | 7 | 0 | 0 | 1.606 | 1.604 | 1.609 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 7 | 0 | 0 | 1.606 | 1.604 | 1.609 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source | 8 | 0 | 0 | 1.591 | 1.590 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 8 | 0 | 0 | 1.591 | 1.590 | 1.595 | 1.40–1.80 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output C2′–F2′ distances

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | C2′–F (Å) | Note |
|---:|---|---|---|---|---:|---:|---|
| 1 | A72 | C | CFL | CFL A2 | 0.0550 | 1.3806 | exact base-class template |
| 2 | A73 | U | UFL | TAF A3 | 0.0380 | 1.3835 | exact base-class template |
| 3 | A74 | A | A5L | A5L A4 | 0.0726 | 1.3816 | exact base-class template |
| 4 | A75 | G | GFL | GFL A1 | 0.0594 | 1.3838 | exact base-class template |
| 5 | A76 | G | GFL | GFL A1 | 0.0438 | 1.3838 | exact base-class template |
| 6 | A77 | C | CFL | CFL A2 | 0.0431 | 1.3806 | exact base-class template |
| 7 | A78 | U | UFL | TAF A3 | 0.0310 | 1.3835 | exact base-class template |
| 8 | A79 | C | CFL | CFL A2 | 0.0391 | 1.3806 | exact base-class template |

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
