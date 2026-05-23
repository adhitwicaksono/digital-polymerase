# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A  
**Method:** Fragment-guided RNA → ANA candidate reconstruction  
**Status:** Experimental candidate, not physically validated

---

## Inputs

- Source RNA PDB: `8t5o-HH-typeI-111mer-full.pdb`
- ANA fragment template PDB: `1ho6_ANApart.pdb`
- Output PDB: `converted_ana_HH_111mer.pdb`

---

## Source Sequence

```text
GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC
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

- Converted residues: `111`
- Mean anchor RMSD: `0.1961 Å`
- Maximum anchor RMSD: `0.2161 Å`

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A5 | G | GAO | GAO A9 | 0.1954 | exact base-class template |
| 2 | A6 | G | GAO | GAO A9 | 0.2042 | exact base-class template |
| 3 | A7 | U | UAR | UAR A10 | 0.1911 | exact base-class template |
| 4 | A8 | G | GAO | GAO A9 | 0.2032 | exact base-class template |
| 5 | A9 | C | CAR | CAR A11 | 0.2146 | exact base-class template |
| 6 | A10 | A | AAR | GAO A9 | 0.2062 | purine fallback: A uses G-like ANA backbone template |
| 7 | A11 | G | GAO | GAO A9 | 0.1971 | exact base-class template |
| 8 | A12 | G | GAO | GAO A9 | 0.1985 | exact base-class template |
| 9 | A13 | U | UAR | UAR A10 | 0.1971 | exact base-class template |
| 10 | A14 | A | AAR | GAO A9 | 0.1961 | purine fallback: A uses G-like ANA backbone template |
| 11 | A15 | C | CAR | CAR A11 | 0.1685 | exact base-class template |
| 12 | A16 | A | AAR | GAO A9 | 0.2019 | purine fallback: A uses G-like ANA backbone template |
| 13 | A17 | U | UAR | UAR A10 | 0.1927 | exact base-class template |
| 14 | A18 | C | CAR | CAR A11 | 0.2016 | exact base-class template |
| 15 | A19 | C | CAR | CAR A11 | 0.1991 | exact base-class template |
| 16 | A20 | A | AAR | GAO A9 | 0.2075 | purine fallback: A uses G-like ANA backbone template |
| 17 | A21 | G | GAO | GAO A9 | 0.1884 | exact base-class template |
| 18 | A22 | C | CAR | CAR A11 | 0.1625 | exact base-class template |
| 19 | A23 | U | UAR | UAR A10 | 0.1890 | exact base-class template |
| 20 | A24 | G | GAO | GAO A9 | 0.1820 | exact base-class template |
| 21 | A25 | A | AAR | GAO A9 | 0.1999 | purine fallback: A uses G-like ANA backbone template |
| 22 | A26 | U | UAR | UAR A10 | 0.1688 | exact base-class template |
| 23 | A27 | G | GAO | GAO A9 | 0.1968 | exact base-class template |
| 24 | A28 | A | AAR | GAO A9 | 0.1999 | purine fallback: A uses G-like ANA backbone template |
| 25 | A29 | G | GAO | GAO A9 | 0.1974 | exact base-class template |
| 26 | A30 | U | UAR | UAR A10 | 0.1932 | exact base-class template |
| 27 | A31 | C | CAR | CAR A11 | 0.2070 | exact base-class template |
| 28 | A32 | C | CAR | CAR A11 | 0.1981 | exact base-class template |
| 29 | A33 | C | CAR | CAR A11 | 0.2011 | exact base-class template |
| 30 | A34 | A | AAR | GAO A9 | 0.2054 | purine fallback: A uses G-like ANA backbone template |
| 31 | A35 | A | AAR | GAO A9 | 0.1510 | purine fallback: A uses G-like ANA backbone template |
| 32 | A36 | A | AAR | GAO A9 | 0.1577 | purine fallback: A uses G-like ANA backbone template |
| 33 | A37 | U | UAR | UAR A10 | 0.1885 | exact base-class template |
| 34 | A38 | A | AAR | GAO A9 | 0.1603 | purine fallback: A uses G-like ANA backbone template |
| 35 | A39 | G | GAO | GAO A9 | 0.2133 | exact base-class template |
| 36 | A40 | G | GAO | GAO A9 | 0.2022 | exact base-class template |
| 37 | A41 | A | AAR | GAO A9 | 0.1962 | purine fallback: A uses G-like ANA backbone template |
| 38 | A42 | C | CAR | CAR A11 | 0.2049 | exact base-class template |
| 39 | A43 | A | AAR | GAO A9 | 0.2033 | purine fallback: A uses G-like ANA backbone template |
| 40 | A44 | A | AAR | GAO A9 | 0.1975 | purine fallback: A uses G-like ANA backbone template |
| 41 | A45 | A | AAR | GAO A9 | 0.2018 | purine fallback: A uses G-like ANA backbone template |
| 42 | A46 | A | AAR | GAO A9 | 0.2042 | purine fallback: A uses G-like ANA backbone template |
| 43 | A47 | A | AAR | GAO A9 | 0.2059 | purine fallback: A uses G-like ANA backbone template |
| 44 | A48 | G | GAO | GAO A9 | 0.2014 | exact base-class template |
| 45 | A49 | G | GAO | GAO A9 | 0.2021 | exact base-class template |
| 46 | A50 | G | GAO | GAO A9 | 0.1984 | exact base-class template |
| 47 | A51 | A | AAR | GAO A9 | 0.2086 | purine fallback: A uses G-like ANA backbone template |
| 48 | A52 | G | GAO | GAO A9 | 0.1977 | exact base-class template |
| 49 | A53 | A | AAR | GAO A9 | 0.1985 | purine fallback: A uses G-like ANA backbone template |
| 50 | A54 | G | GAO | GAO A9 | 0.2048 | exact base-class template |
| 51 | A55 | G | GAO | GAO A9 | 0.2040 | exact base-class template |
| 52 | A56 | U | UAR | UAR A10 | 0.1996 | exact base-class template |
| 53 | A57 | G | GAO | GAO A9 | 0.1947 | exact base-class template |
| 54 | A58 | A | AAR | GAO A9 | 0.2001 | purine fallback: A uses G-like ANA backbone template |
| 55 | A59 | A | AAR | GAO A9 | 0.1966 | purine fallback: A uses G-like ANA backbone template |
| 56 | A60 | G | GAO | GAO A9 | 0.2114 | exact base-class template |
| 57 | A61 | A | AAR | GAO A9 | 0.2064 | purine fallback: A uses G-like ANA backbone template |
| 58 | A62 | A | AAR | GAO A9 | 0.1518 | purine fallback: A uses G-like ANA backbone template |
| 59 | A63 | U | UAR | UAR A10 | 0.1757 | exact base-class template |
| 60 | A64 | A | AAR | GAO A9 | 0.1970 | purine fallback: A uses G-like ANA backbone template |
| 61 | A65 | C | CAR | CAR A11 | 0.1543 | exact base-class template |
| 62 | A66 | G | GAO | GAO A9 | 0.1550 | exact base-class template |
| 63 | A67 | A | AAR | GAO A9 | 0.2033 | purine fallback: A uses G-like ANA backbone template |
| 64 | A68 | C | CAR | CAR A11 | 0.2026 | exact base-class template |
| 65 | A69 | C | CAR | CAR A11 | 0.2066 | exact base-class template |
| 66 | A70 | A | AAR | GAO A9 | 0.2044 | purine fallback: A uses G-like ANA backbone template |
| 67 | A71 | C | CAR | CAR A11 | 0.2077 | exact base-class template |
| 68 | A72 | C | CAR | CAR A11 | 0.2089 | exact base-class template |
| 69 | A73 | U | UAR | UAR A10 | 0.1897 | exact base-class template |
| 70 | A74 | A | AAR | GAO A9 | 0.2042 | purine fallback: A uses G-like ANA backbone template |
| 71 | A75 | G | GAO | GAO A9 | 0.1975 | exact base-class template |
| 72 | A76 | G | GAO | GAO A9 | 0.2089 | exact base-class template |
| 73 | A77 | C | CAR | CAR A11 | 0.1979 | exact base-class template |
| 74 | A78 | U | UAR | UAR A10 | 0.2161 | exact base-class template |
| 75 | A79 | C | CAR | CAR A11 | 0.2058 | exact base-class template |
| 76 | A80 | G | GAO | GAO A9 | 0.2030 | exact base-class template |
| 77 | A81 | A | AAR | GAO A9 | 0.2017 | purine fallback: A uses G-like ANA backbone template |
| 78 | A82 | A | AAR | GAO A9 | 0.2149 | purine fallback: A uses G-like ANA backbone template |
| 79 | A83 | A | AAR | GAO A9 | 0.2093 | purine fallback: A uses G-like ANA backbone template |
| 80 | A84 | G | GAO | GAO A9 | 0.2019 | exact base-class template |
| 81 | A85 | A | AAR | GAO A9 | 0.2123 | purine fallback: A uses G-like ANA backbone template |
| 82 | A86 | G | GAO | GAO A9 | 0.2045 | exact base-class template |
| 83 | A87 | C | CAR | CAR A11 | 0.2089 | exact base-class template |
| 84 | A88 | C | CAR | CAR A11 | 0.2045 | exact base-class template |
| 85 | A89 | U | UAR | UAR A10 | 0.1950 | exact base-class template |
| 86 | A90 | A | AAR | GAO A9 | 0.1998 | purine fallback: A uses G-like ANA backbone template |
| 87 | A91 | A | AAR | GAO A9 | 0.2006 | purine fallback: A uses G-like ANA backbone template |
| 88 | A92 | A | AAR | GAO A9 | 0.1555 | purine fallback: A uses G-like ANA backbone template |
| 89 | A93 | A | AAR | GAO A9 | 0.2013 | purine fallback: A uses G-like ANA backbone template |
| 90 | A94 | C | CAR | CAR A11 | 0.2061 | exact base-class template |
| 91 | A95 | A | AAR | GAO A9 | 0.2023 | purine fallback: A uses G-like ANA backbone template |
| 92 | A96 | U | UAR | UAR A10 | 0.1917 | exact base-class template |
| 93 | A97 | A | AAR | GAO A9 | 0.2071 | purine fallback: A uses G-like ANA backbone template |
| 94 | A98 | C | CAR | CAR A11 | 0.2020 | exact base-class template |
| 95 | A99 | C | CAR | CAR A11 | 0.2016 | exact base-class template |
| 96 | A100 | U | UAR | UAR A10 | 0.1948 | exact base-class template |
| 97 | A101 | U | UAR | UAR A10 | 0.1948 | exact base-class template |
| 98 | A102 | U | UAR | UAR A10 | 0.1878 | exact base-class template |
| 99 | A103 | C | CAR | CAR A11 | 0.1629 | exact base-class template |
| 100 | A104 | C | CAR | CAR A11 | 0.1991 | exact base-class template |
| 101 | A105 | U | UAR | UAR A10 | 0.1964 | exact base-class template |
| 102 | A106 | G | GAO | GAO A9 | 0.1990 | exact base-class template |
| 103 | A107 | G | GAO | GAO A9 | 0.2026 | exact base-class template |
| 104 | A108 | A | AAR | GAO A9 | 0.2087 | purine fallback: A uses G-like ANA backbone template |
| 105 | A109 | U | UAR | UAR A10 | 0.1876 | exact base-class template |
| 106 | A110 | U | UAR | UAR A10 | 0.1728 | exact base-class template |
| 107 | A111 | C | CAR | CAR A11 | 0.1995 | exact base-class template |
| 108 | A112 | C | CAR | CAR A11 | 0.2063 | exact base-class template |
| 109 | A115 | U | UAR | UAR A10 | 0.1949 | exact base-class template |
| 110 | A116 | G | GAO | GAO A9 | 0.2033 | exact base-class template |
| 111 | A117 | C | CAR | CAR A11 | 0.1677 | exact base-class template |

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
