# RNA → PNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 008A.1  
**Method:** PNA chimaera-guided pseudopeptide-backbone reconstruction  
**Status:** Experimental candidate, not physically validated  
**PNA chain-continuity status:** `C′(i)→N1′(i+1) PASS`  
**Base-attachment status:** `PASS`  
**PNA backbone status:** `C7′→N4′ PASS`, `C′→O1′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008A1_outputs/converted_pna_RNA-34mer_auto_008A1.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `34`
- Usable template residue count: `8`
- Converted residues: `34`

---

## Why PNA Is the Chimaera

PNA is not a sugar-modified nucleic acid. It abandons the sugar-phosphate backbone and uses a pseudopeptide backbone.

The uploaded template uses PNA-like residues:

```text
APN
TPN
GPN
CPN
```

Important PNA scaffold atoms include:

```text
C8'
C7'
O7'
N4'
C3'
C2'
N1'
C5'
C'
O1'
```

Observed linkage:

```text
C′(i) → N1′(i+1)
```

Observed base attachment:

```text
C8′ → glycosidic N
```

---

## Method Summary

Prototype 008A.1 performs PNA chimaera-guided pseudopeptide-backbone reconstruction:

1. infer source RNA base identity
2. select a PNA template residue by base class
3. place the PNA pseudopeptide scaffold using neighboring RNA `C1′` positions as a guide
4. enforce PNA `C′(i)→N1′(i+1)` continuity using suffix linkage correction
5. attach the source RNA base to PNA `C8′`
6. export a PNA-like candidate PDB
7. validate PNA-specific backbone and base-attachment geometry

---

## Alignment / Correction Summary

- Mean guide RMSD: `1.4845 Å`
- Maximum guide RMSD: `4.8716 Å`
- Mean suffix-linkage shift: `48.2311 Å`
- Maximum suffix-linkage shift: `102.3010 Å`
- Mean base shift: `5.1579 Å`
- Maximum base shift: `13.1182 Å`
- Mean C8′→glycosidic N distance: `1.4613 Å`
- Mean C′(i)→N1′(i+1) distance: `1.3400 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| PNA C'(i)→N1'(i+1) | 33 | 0 | 0 | 1.340 | 1.340 | 1.340 | 1.15–1.60 | PASS |
| C8'→glycosidic N | 34 | 0 | 0 | 1.461 | 1.444 | 1.482 | 1.25–1.75 | PASS |
| C8'→C7' | 34 | 0 | 0 | 1.532 | 1.504 | 1.552 | 1.30–1.80 | PASS |
| C7'→O7' | 34 | 0 | 0 | 1.237 | 1.212 | 1.258 | 1.10–1.40 | PASS |
| C7'→N4' | 34 | 0 | 0 | 1.334 | 1.317 | 1.346 | 1.15–1.55 | PASS |
| N4'→C3' | 34 | 0 | 0 | 1.483 | 1.457 | 1.496 | 1.25–1.75 | PASS |
| C3'→C2' | 34 | 0 | 0 | 1.526 | 1.484 | 1.553 | 1.25–1.85 | PASS |
| C2'→N1' | 34 | 0 | 0 | 1.474 | 1.457 | 1.499 | 1.20–1.75 | PASS |
| N4'→C5' | 34 | 0 | 0 | 1.480 | 1.468 | 1.487 | 1.25–1.75 | PASS |
| C5'→C' | 34 | 0 | 0 | 1.504 | 1.467 | 1.538 | 1.25–1.85 | PASS |
| C'→O1' | 34 | 0 | 0 | 1.243 | 1.231 | 1.254 | 1.10–1.40 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Guide RMSD (Å) | Suffix shift (Å) | Base shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | A54 | G | GPN | GPN A1001 | 0.4530 | 0.0000 | 0.2964 | 1.4693753774988951 | 1.3399999999999954 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 2 | A55 | G | GPN | GPN A1002 | 0.5878 | 0.5087 | 0.7991 | 1.4440252767870827 | 1.339999999999988 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 3 | A56 | U | UPN | TPN A1005 | 0.2722 | 2.9768 | 2.6923 | 1.4818512071054897 | 1.3400000000000116 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 4 | A57 | G | GPN | GPN A1006 | 0.3047 | 5.6419 | 2.6743 | 1.462007523920443 | 1.3400000000000025 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 5 | A58 | A | APN | APN A1004 | 0.6528 | 8.1797 | 4.2481 | 1.4510375598171044 | 1.3400000000000098 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 6 | A59 | A | APN | APN A1004 | 0.6444 | 9.3855 | 4.5201 | 1.4510375598171135 | 1.3399999999999963 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 7 | A60 | G | GPN | GPN A1001 | 4.2303 | 11.2965 | 2.4257 | 1.469375377498886 | 1.3399999999999888 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 8 | A61 | A | APN | APN A1004 | 1.2743 | 17.8327 | 5.1449 | 1.4510375598171081 | 1.340000000000008 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 9 | A62 | A | APN | APN A1004 | 3.2588 | 20.9022 | 11.3396 | 1.4510375598171084 | 1.3399999999999868 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 10 | A63 | U | UPN | TPN A1005 | 1.9256 | 26.2157 | 4.4273 | 1.4818512071055066 | 1.3400000000000087 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 11 | A64 | A | APN | APN A1004 | 2.8788 | 29.0297 | 5.4312 | 1.4510375598171075 | 1.3399999999999879 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 12 | A65 | C | CPN | CPN A1003 | 1.1171 | 33.6491 | 7.3421 | 1.4719079454911488 | 1.3399999999999916 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 13 | A66 | G | GPN | GPN A1002 | 1.6177 | 38.0529 | 4.2588 | 1.444025276787084 | 1.3400000000000074 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 14 | A67 | A | APN | APN A1004 | 1.3674 | 40.1002 | 7.3524 | 1.4510375598171237 | 1.33999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 15 | A68 | C | CPN | CPN A1007 | 0.7585 | 41.8449 | 7.0263 | 1.4654695493254137 | 1.339999999999993 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 16 | A69 | C | CPN | CPN A1008 | 4.6238 | 43.7527 | 3.9640 | 1.4691477121106797 | 1.3400000000000138 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 17 | A70 | A | APN | APN A1004 | 0.4322 | 49.9377 | 2.0933 | 1.4510375598171115 | 1.3400000000000116 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 18 | A71 | C | CPN | CPN A1003 | 0.3030 | 51.6521 | 2.2633 | 1.4719079454911554 | 1.3400000000000094 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 19 | A72 | C | CPN | CPN A1007 | 0.4999 | 52.0760 | 2.6141 | 1.465469549325408 | 1.3400000000000047 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 20 | A73 | U | UPN | TPN A1005 | 0.4219 | 55.6980 | 2.9459 | 1.4818512071055023 | 1.3399999999999952 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 21 | A74 | A | APN | APN A1004 | 0.3941 | 58.0065 | 3.4361 | 1.4510375598171197 | 1.3400000000000003 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 22 | A75 | G | GPN | GPN A1006 | 0.2907 | 59.2583 | 3.6723 | 1.462007523920453 | 1.3399999999999845 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 23 | A76 | G | GPN | GPN A1001 | 4.8716 | 64.5295 | 5.1938 | 1.4693753774988976 | 1.339999999999996 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 24 | A77 | C | CPN | CPN A1008 | 4.8154 | 67.7352 | 5.5035 | 1.4691477121106642 | 1.3399999999999854 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 25 | A78 | U | UPN | TPN A1005 | 0.6792 | 72.1703 | 5.7408 | 1.481851207105499 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 26 | A79 | C | CPN | CPN A1003 | 0.9292 | 72.8814 | 6.3605 | 1.471907945491156 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 27 | A80 | G | GPN | GPN A1002 | 0.8172 | 74.1674 | 4.2968 | 1.4440252767870647 | 1.3400000000000083 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 28 | A81 | A | APN | APN A1004 | 2.1218 | 78.9005 | 8.5857 | 1.4510375598171148 | 1.3400000000000043 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 29 | A82 | A | APN | APN A1004 | 0.6368 | 81.8854 | 4.3184 | 1.4510375598171055 | 1.3399999999999908 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 30 | A83 | A | APN | APN A1004 | 1.4303 | 85.3669 | 7.3498 | 1.4510375598171164 | 1.3399999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 31 | A84 | G | GPN | GPN A1006 | 0.5789 | 89.6998 | 4.8643 | 1.4620075239204389 | 1.3399999999999996 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 32 | A85 | A | APN | APN A1004 | 0.5541 | 94.7378 | 8.9680 | 1.451037559817105 | 1.3400000000000034 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 33 | A86 | G | GPN | GPN A1001 | 4.4934 | 99.4829 | 10.1002 | 1.469375377498881 | 1.339999999999988 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 34 | A87 | C | CPN | CPN A1007 | 0.2363 | 102.3010 | 13.1182 | 1.4654695493254055 | NA | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |

---

## Scientific Interpretation

This output should be interpreted as:

> a PNA-like computational candidate generated by chimaera-guided pseudopeptide-backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready PNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- PNA stereochemistry and peptide-like backbone geometry require expert inspection.
- The suffix-linkage correction prioritizes PNA chain continuity and may increase base shifts.
- Molecular viewers may not render standard nucleic-acid cartoon paths for PNA.
- The output is a candidate geometry only; biological function, stability, binding, or catalytic activity is not implied.
