# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A  
**Method:** Fragment-guided RNA → ANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated

---

## Inputs

- Source RNA PDB: `RNA-34mer.pdb`
- ANA fragment template PDB: `1ho6_ANApart.pdb`
- Output PDB: `converted_ana_34mer.pdb`

---

## Source Sequence

```text
GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC
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

- Converted residues: `34`
- Mean anchor RMSD: `0.1989 Å`
- Maximum anchor RMSD: `0.2161 Å`

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A54 | G | GAO | GAO A9 | 0.2048 | exact base-class template |
| 2 | A55 | G | GAO | GAO A9 | 0.2040 | exact base-class template |
| 3 | A56 | U | UAR | UAR A10 | 0.1996 | exact base-class template |
| 4 | A57 | G | GAO | GAO A9 | 0.1947 | exact base-class template |
| 5 | A58 | A | AAR | GAO A9 | 0.2001 | purine fallback: A uses G-like ANA backbone template |
| 6 | A59 | A | AAR | GAO A9 | 0.1966 | purine fallback: A uses G-like ANA backbone template |
| 7 | A60 | G | GAO | GAO A9 | 0.2114 | exact base-class template |
| 8 | A61 | A | AAR | GAO A9 | 0.2064 | purine fallback: A uses G-like ANA backbone template |
| 9 | A62 | A | AAR | GAO A9 | 0.1518 | purine fallback: A uses G-like ANA backbone template |
| 10 | A63 | U | UAR | UAR A10 | 0.1757 | exact base-class template |
| 11 | A64 | A | AAR | GAO A9 | 0.1970 | purine fallback: A uses G-like ANA backbone template |
| 12 | A65 | C | CAR | CAR A11 | 0.1543 | exact base-class template |
| 13 | A66 | G | GAO | GAO A9 | 0.1550 | exact base-class template |
| 14 | A67 | A | AAR | GAO A9 | 0.2033 | purine fallback: A uses G-like ANA backbone template |
| 15 | A68 | C | CAR | CAR A11 | 0.2026 | exact base-class template |
| 16 | A69 | C | CAR | CAR A11 | 0.2066 | exact base-class template |
| 17 | A70 | A | AAR | GAO A9 | 0.2044 | purine fallback: A uses G-like ANA backbone template |
| 18 | A71 | C | CAR | CAR A11 | 0.2077 | exact base-class template |
| 19 | A72 | C | CAR | CAR A11 | 0.2089 | exact base-class template |
| 20 | A73 | U | UAR | UAR A10 | 0.1897 | exact base-class template |
| 21 | A74 | A | AAR | GAO A9 | 0.2042 | purine fallback: A uses G-like ANA backbone template |
| 22 | A75 | G | GAO | GAO A9 | 0.1975 | exact base-class template |
| 23 | A76 | G | GAO | GAO A9 | 0.2089 | exact base-class template |
| 24 | A77 | C | CAR | CAR A11 | 0.1979 | exact base-class template |
| 25 | A78 | U | UAR | UAR A10 | 0.2161 | exact base-class template |
| 26 | A79 | C | CAR | CAR A11 | 0.2058 | exact base-class template |
| 27 | A80 | G | GAO | GAO A9 | 0.2030 | exact base-class template |
| 28 | A81 | A | AAR | GAO A9 | 0.2017 | purine fallback: A uses G-like ANA backbone template |
| 29 | A82 | A | AAR | GAO A9 | 0.2149 | purine fallback: A uses G-like ANA backbone template |
| 30 | A83 | A | AAR | GAO A9 | 0.2093 | purine fallback: A uses G-like ANA backbone template |
| 31 | A84 | G | GAO | GAO A9 | 0.2019 | exact base-class template |
| 32 | A85 | A | AAR | GAO A9 | 0.2123 | purine fallback: A uses G-like ANA backbone template |
| 33 | A86 | G | GAO | GAO A9 | 0.2045 | exact base-class template |
| 34 | A87 | C | CAR | CAR A11 | 0.2089 | exact base-class template |

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
