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

- Source RNA PDB: `/mnt/data/RNA-22mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008A1_outputs/converted_pna_RNA-22mer_auto_008A1.pdb`

---

## Source and Template

- Source RNA sequence: `AUACGACCACCUAGGCUCGAAA`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `22`
- Usable template residue count: `8`
- Converted residues: `22`

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

- Mean guide RMSD: `1.6500 Å`
- Maximum guide RMSD: `5.0505 Å`
- Mean suffix-linkage shift: `35.7494 Å`
- Maximum suffix-linkage shift: `67.0701 Å`
- Mean base shift: `10.3193 Å`
- Maximum base shift: `17.7763 Å`
- Mean C8′→glycosidic N distance: `1.4629 Å`
- Mean C′(i)→N1′(i+1) distance: `1.3400 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| PNA C'(i)→N1'(i+1) | 21 | 0 | 0 | 1.340 | 1.340 | 1.340 | 1.15–1.60 | PASS |
| C8'→glycosidic N | 22 | 0 | 0 | 1.463 | 1.444 | 1.482 | 1.25–1.75 | PASS |
| C8'→C7' | 22 | 0 | 0 | 1.528 | 1.504 | 1.552 | 1.30–1.80 | PASS |
| C7'→O7' | 22 | 0 | 0 | 1.238 | 1.212 | 1.258 | 1.10–1.40 | PASS |
| C7'→N4' | 22 | 0 | 0 | 1.335 | 1.317 | 1.346 | 1.15–1.55 | PASS |
| N4'→C3' | 22 | 0 | 0 | 1.484 | 1.457 | 1.496 | 1.25–1.75 | PASS |
| C3'→C2' | 22 | 0 | 0 | 1.525 | 1.484 | 1.553 | 1.25–1.85 | PASS |
| C2'→N1' | 22 | 0 | 0 | 1.474 | 1.457 | 1.499 | 1.20–1.75 | PASS |
| N4'→C5' | 22 | 0 | 0 | 1.479 | 1.468 | 1.487 | 1.25–1.75 | PASS |
| C5'→C' | 22 | 0 | 0 | 1.505 | 1.467 | 1.538 | 1.25–1.85 | PASS |
| C'→O1' | 22 | 0 | 0 | 1.244 | 1.231 | 1.254 | 1.10–1.40 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Guide RMSD (Å) | Suffix shift (Å) | Base shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | A62 | A | APN | APN A1004 | 0.8936 | 0.0000 | 0.3282 | 1.4510375598171084 | 1.3400000000000045 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 2 | A63 | U | UPN | TPN A1005 | 1.9256 | 4.6486 | 5.5506 | 1.4818512071055066 | 1.3400000000000087 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 3 | A64 | A | APN | APN A1004 | 2.8788 | 7.4625 | 4.5834 | 1.4510375598171075 | 1.3399999999999879 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 4 | A65 | C | CPN | CPN A1003 | 1.1171 | 12.0819 | 5.0978 | 1.4719079454911488 | 1.3400000000000123 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 5 | A66 | G | GPN | GPN A1001 | 4.9441 | 20.1465 | 9.2227 | 1.469375377498876 | 1.339999999999988 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 6 | A67 | A | APN | APN A1004 | 1.3674 | 22.8764 | 11.2570 | 1.4510375598171237 | 1.33999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 7 | A68 | C | CPN | CPN A1007 | 0.7585 | 24.6211 | 10.6242 | 1.4654695493254137 | 1.339999999999993 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 8 | A69 | C | CPN | CPN A1008 | 4.6238 | 26.5288 | 8.6486 | 1.4691477121106797 | 1.3400000000000138 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 9 | A70 | A | APN | APN A1004 | 0.4322 | 32.7139 | 11.4157 | 1.4510375598171115 | 1.3400000000000116 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 10 | A71 | C | CPN | CPN A1003 | 0.3030 | 34.4282 | 10.6428 | 1.4719079454911554 | 1.3400000000000094 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 11 | A72 | C | CPN | CPN A1007 | 0.4999 | 34.8522 | 11.0709 | 1.465469549325408 | 1.3400000000000047 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 12 | A73 | U | UPN | TPN A1005 | 0.4219 | 38.4742 | 10.7598 | 1.4818512071055023 | 1.3399999999999952 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 13 | A74 | A | APN | APN A1004 | 0.3941 | 40.7827 | 11.8607 | 1.4510375598171197 | 1.3399999999999905 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 14 | A75 | G | GPN | GPN A1002 | 0.5953 | 42.0515 | 12.1707 | 1.4440252767870778 | 1.3399999999999976 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 15 | A76 | G | GPN | GPN A1006 | 0.5702 | 43.1287 | 12.2607 | 1.4620075239204393 | 1.3400000000000023 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 16 | A77 | C | CPN | CPN A1008 | 4.8154 | 48.1322 | 11.7292 | 1.4691477121106642 | 1.3399999999999854 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 17 | A78 | U | UPN | TPN A1005 | 0.6792 | 52.5673 | 11.4999 | 1.481851207105499 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 18 | A79 | C | CPN | CPN A1003 | 0.9292 | 53.2785 | 12.3765 | 1.471907945491156 | 1.3400000000000063 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 19 | A80 | G | GPN | GPN A1001 | 5.0505 | 55.4706 | 11.4326 | 1.4693753774988998 | 1.339999999999989 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 20 | A81 | A | APN | APN A1004 | 2.1218 | 61.0935 | 17.7763 | 1.4510375598171148 | 1.3400000000000043 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 21 | A82 | A | APN | APN A1004 | 0.6368 | 64.0784 | 12.3827 | 1.4510375598171055 | 1.3400000000000116 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 22 | A83 | A | APN | APN A1004 | 0.3414 | 67.0701 | 14.3335 | 1.4510375598171164 | NA | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |

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
