# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A  
**Method:** Fragment-guided RNA → ANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated

---

## Inputs

- Source RNA PDB: `RNA-8mer.pdb`
- ANA fragment template PDB: `1ho6_ANApart.pdb`
- Output PDB: `converted_ana_8mer.pdb`

---

## Source Sequence

```text
CUAGGCUC
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

This is **not** a full-template reconstruction because the ANA template contains only 4 residues.

---

## Settings

- Anchor atoms: `C1', C2', C3', C4', O4'`
- Pin C1' after alignment: `True`
- Residue naming policy: `template-observed`

---

## Alignment Summary

- Converted residues: `8`
- Mean anchor RMSD: `0.2036 Å`
- Maximum anchor RMSD: `0.2161 Å`

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A72 | C | CAR | CAR A11 | 0.2089 | exact base-class template |
| 2 | A73 | U | UAR | UAR A10 | 0.1897 | exact base-class template |
| 3 | A74 | A | AAR | GAO A9 | 0.2042 | purine fallback: A uses G-like ANA backbone template |
| 4 | A75 | G | GAO | GAO A9 | 0.1975 | exact base-class template |
| 5 | A76 | G | GAO | GAO A9 | 0.2089 | exact base-class template |
| 6 | A77 | C | CAR | CAR A11 | 0.1979 | exact base-class template |
| 7 | A78 | U | UAR | UAR A10 | 0.2161 | exact base-class template |
| 8 | A79 | C | CAR | CAR A11 | 0.2058 | exact base-class template |

---

## Scientific Interpretation

This output should be interpreted as:

> an ANA-like candidate structure generated using fragment-guided local backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed ANA structure.

---

## Important Limitations

- The ANA template contains only a 4-mer fragment.
- A-like ANA geometry is absent in the uploaded template; A residues may use a purine fallback template.
- RNA nucleobase atoms are preserved, but backbone geometry is template-derived.
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
5. Compare local ANA backbone geometry with the original 4-mer ANA template.
6. Add explicit connectivity records or topology files in future versions.
7. Perform energy minimization with appropriate force-field support.
8. Repeat the prototype when a full ANA 8-mer template becomes available.

---

## Development Note

This prototype introduces a second Digital Polymerase mode:

```text
Prototype 001: full-template reconstruction
Prototype 002A: fragment-guided local reconstruction
```

This is useful because many XNA systems may not have full-length templates matching the desired source molecule.
