# RNA → GNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 007A  
**Method:** Linkage-optimized GNA reconstruction  
**Status:** Experimental candidate, not physically validated  
**GNA chain-continuity status:** `O2G(i)→P(i+1) PASS`, `P(i)→O3G(i) PASS`  
**Base-attachment status:** `PASS`  
**Local GNA scaffold status:** `C1G→C2G PASS`, `C2G→C3G PASS`, `C2G→O2G PASS`, `C3G→O3G PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-12mer.pdb`
- GNA template PDB: `/mnt/data/2xc6-GNA-8nt.pdb`
- Output PDB: `/mnt/data/gna_prototype_007A_outputs/converted_gna_RNA-12mer_auto_007A.pdb`

---

## Source and Template

- Source RNA sequence: `CUAGGCUCGAAA`
- GNA template base-class sequence: `CUCUAGAG`
- Source residue count: `12`
- Template residue count: `8`
- Converted residues: `12`

---

## Why GNA Is Difficult

GNA is not a pentose-like local edit. It uses a much smaller glycerol-like scaffold.

The uploaded GNA template uses atoms such as:

```text
C1G
C2G
C3G
O2G
O3G
```

The observed GNA-like linkage pattern is:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

Therefore, this prototype treats GNA as a linkage-remapped and scaffold-optimized reconstruction problem, not as a simple RNA sugar modification.

---

## Method Summary

Prototype 007A performs linkage-optimized GNA reconstruction:

1. parse source RNA and GNA template PDB files
2. infer source base identity
3. select a GNA template residue by base class
4. use source RNA phosphate positions as the global chain guide
5. generate an initial GNA glycerol scaffold from the template
6. locally optimize GNA scaffold distances
7. attach source RNA bases to `C1G`
8. export a GNA-like candidate PDB
9. validate GNA-specific linkages and scaffold geometry

---

## Alignment / Optimization Summary

- Mean initial alignment RMSD: `0.9965 Å`
- Maximum initial alignment RMSD: `1.1972 Å`
- Mean base shift: `0.8467 Å`
- Maximum base shift: `1.3338 Å`
- Mean optimization cost: `0.0452`
- Mean C1G→glycosidic N distance: `1.4672 Å`
- Mean P(i)→O3G(i) distance: `1.5947 Å`
- Mean O2G(i)→P(i+1) distance: `1.5926 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| GNA O2G(i)→P(i+1) | 11 | 0 | 0 | 1.593 | 1.580 | 1.602 | 1.25–1.95 | PASS |
| GNA P(i)→O3G(i) | 12 | 0 | 0 | 1.595 | 1.587 | 1.606 | 1.25–1.95 | PASS |
| C1G→glycosidic N | 12 | 0 | 0 | 1.467 | 1.442 | 1.516 | 1.25–1.75 | PASS |
| C1G→C2G | 12 | 0 | 0 | 1.524 | 1.516 | 1.533 | 1.30–1.80 | PASS |
| C2G→C3G | 12 | 0 | 0 | 1.526 | 1.518 | 1.533 | 1.30–1.80 | PASS |
| C2G→O2G | 12 | 0 | 0 | 1.425 | 1.409 | 1.441 | 1.20–1.65 | PASS |
| C3G→O3G | 12 | 0 | 0 | 1.424 | 1.402 | 1.439 | 1.20–1.65 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base shift (Å) | Opt. cost | C1G–N (Å) | P–O3G (Å) | O2G–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A72 | C | ZCY | ZCY A1 | 0.9020 | 0.8143 | 0.0384 | 1.4831925026779182 | 1.590189928934769 | 1.596358936793333 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 2 | A73 | U | ZBU | ZTH A2 | 1.0136 | 0.8210 | 0.0322 | 1.4896006176153394 | 1.6055905981523075 | 1.579962091321569 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 3 | A74 | A | ZAD | ZAD A5 | 1.0545 | 0.8130 | 0.0311 | 1.442372351371165 | 1.5898129462674806 | 1.5986890879132931 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 4 | A75 | G | ZGU | ZGU A6 | 0.9418 | 0.8355 | 0.0333 | 1.4498693044547166 | 1.602685730840654 | 1.584099275977451 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 5 | A76 | G | ZGU | ZGU A8 | 1.0619 | 1.3338 | 0.0888 | 1.4607077051895012 | 1.5894486987228467 | 1.5907449543103045 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 6 | A77 | C | ZCY | ZCY A3 | 0.9268 | 0.9518 | 0.0448 | 1.4806245303924856 | 1.601106291183353 | 1.585188247122662 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 7 | A78 | U | ZBU | ZBU A4 | 1.0762 | 0.3917 | 0.0095 | 1.5163353850649215 | 1.5866115107389303 | 1.6021234915760125 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 8 | A79 | C | ZCY | ZCY A1 | 0.8296 | 0.6778 | 0.0257 | 1.483192502677916 | 1.590043526629084 | 1.5962694883722488 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 9 | A80 | G | ZGU | ZGU A6 | 1.1972 | 0.9850 | 0.0451 | 1.4498693044547086 | 1.6024719482651968 | 1.5841314146136571 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 10 | A81 | A | ZAD | ZAD A7 | 1.1756 | 1.1305 | 0.0611 | 1.4539859008945155 | 1.5925572765361968 | 1.5986778029253643 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 11 | A82 | A | ZAD | ZAD A5 | 0.9694 | 1.3092 | 0.1315 | 1.4423723513711562 | 1.593739224173542 | 1.6022961152551836 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 12 | A83 | A | ZAD | ZAD A7 | 0.8091 | 0.0964 | 0.0008 | 1.4539859008944986 | 1.59224712629792 | NA | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |

---

## Scientific Interpretation

This output should be interpreted as:

> a GNA-like computational candidate generated by linkage-optimized glycerol-scaffold reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready GNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- GNA stereochemistry requires expert inspection.
- Molecular viewers may not render standard nucleic-acid cartoon paths reliably for GNA-like structures.
- The output is a candidate geometry only; biological function, stability, replication, or catalytic activity is not implied.
