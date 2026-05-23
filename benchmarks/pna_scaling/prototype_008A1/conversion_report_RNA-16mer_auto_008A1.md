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

- Source RNA PDB: `/mnt/data/RNA-16mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008A1_outputs/converted_pna_RNA-16mer_auto_008A1.pdb`

---

## Source and Template

- Source RNA sequence: `ACCACCUAGGCUCGAA`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `16`
- Usable template residue count: `8`
- Converted residues: `16`

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

- Mean guide RMSD: `1.3463 Å`
- Maximum guide RMSD: `4.5478 Å`
- Mean suffix-linkage shift: `20.5892 Å`
- Maximum suffix-linkage shift: `43.1728 Å`
- Mean base shift: `9.1560 Å`
- Maximum base shift: `16.6051 Å`
- Mean C8′→glycosidic N distance: `1.4630 Å`
- Mean C′(i)→N1′(i+1) distance: `1.3400 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| PNA C'(i)→N1'(i+1) | 15 | 0 | 0 | 1.340 | 1.340 | 1.340 | 1.15–1.60 | PASS |
| C8'→glycosidic N | 16 | 0 | 0 | 1.463 | 1.444 | 1.482 | 1.25–1.75 | PASS |
| C8'→C7' | 16 | 0 | 0 | 1.528 | 1.504 | 1.552 | 1.30–1.80 | PASS |
| C7'→O7' | 16 | 0 | 0 | 1.238 | 1.212 | 1.258 | 1.10–1.40 | PASS |
| C7'→N4' | 16 | 0 | 0 | 1.334 | 1.317 | 1.346 | 1.15–1.55 | PASS |
| N4'→C3' | 16 | 0 | 0 | 1.483 | 1.457 | 1.496 | 1.25–1.75 | PASS |
| C3'→C2' | 16 | 0 | 0 | 1.524 | 1.484 | 1.553 | 1.25–1.85 | PASS |
| C2'→N1' | 16 | 0 | 0 | 1.474 | 1.457 | 1.499 | 1.20–1.75 | PASS |
| N4'→C5' | 16 | 0 | 0 | 1.479 | 1.468 | 1.487 | 1.25–1.75 | PASS |
| C5'→C' | 16 | 0 | 0 | 1.507 | 1.467 | 1.538 | 1.25–1.85 | PASS |
| C'→O1' | 16 | 0 | 0 | 1.244 | 1.231 | 1.254 | 1.10–1.40 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Guide RMSD (Å) | Suffix shift (Å) | Base shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | A67 | A | APN | APN A1004 | 0.1714 | 0.0000 | 0.2306 | 1.4510375598171237 | 1.3399999999999992 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 2 | A68 | C | CPN | CPN A1003 | 0.6424 | 3.0411 | 2.8467 | 1.471907945491152 | 1.339999999999994 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 3 | A69 | C | CPN | CPN A1007 | 0.6292 | 3.4293 | 3.4404 | 1.4654695493253969 | 1.340000000000006 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 4 | A70 | A | APN | APN A1004 | 0.4322 | 4.0983 | 3.2872 | 1.4510375598171115 | 1.3400000000000039 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 5 | A71 | C | CPN | CPN A1008 | 4.5478 | 7.0447 | 2.4955 | 1.4691477121106629 | 1.3399999999999963 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 6 | A72 | C | CPN | CPN A1003 | 0.5669 | 15.3522 | 8.7189 | 1.4719079454911503 | 1.3399999999999979 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 7 | A73 | U | UPN | TPN A1005 | 0.4219 | 17.4535 | 9.3016 | 1.4818512071055023 | 1.3399999999999952 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 8 | A74 | A | APN | APN A1004 | 0.3941 | 19.7620 | 10.3642 | 1.4510375598171197 | 1.3399999999999828 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 9 | A75 | G | GPN | GPN A1001 | 4.4159 | 25.3567 | 11.3259 | 1.4693753774988918 | 1.3399999999999976 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 10 | A76 | G | GPN | GPN A1002 | 0.6006 | 25.8087 | 13.7824 | 1.4440252767870727 | 1.339999999999991 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 11 | A77 | C | CPN | CPN A1007 | 0.5440 | 25.9602 | 13.5807 | 1.4654695493254102 | 1.3399999999999952 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 12 | A78 | U | UPN | TPN A1005 | 0.6792 | 28.1752 | 11.6156 | 1.481851207105499 | 1.3399999999999845 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 13 | A79 | C | CPN | CPN A1008 | 4.2298 | 32.3931 | 10.9482 | 1.4691477121106782 | 1.3399999999999987 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 14 | A80 | G | GPN | GPN A1006 | 0.9621 | 36.9299 | 12.7644 | 1.4620075239204307 | 1.3400000000000096 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 15 | A81 | A | APN | APN A1004 | 2.1218 | 41.4493 | 16.6051 | 1.4510375598171148 | 1.3400000000000123 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 16 | A82 | A | APN | APN A1004 | 0.1807 | 43.1728 | 15.1893 | 1.4510375598171055 | NA | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |

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
