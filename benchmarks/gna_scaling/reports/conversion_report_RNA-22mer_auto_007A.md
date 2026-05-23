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

- Source RNA PDB: `/mnt/data/RNA-22mer.pdb`
- GNA template PDB: `/mnt/data/2xc6-GNA-8nt.pdb`
- Output PDB: `/mnt/data/gna_prototype_007A_outputs/converted_gna_RNA-22mer_auto_007A.pdb`

---

## Source and Template

- Source RNA sequence: `AUACGACCACCUAGGCUCGAAA`
- GNA template base-class sequence: `CUCUAGAG`
- Source residue count: `22`
- Template residue count: `8`
- Converted residues: `22`

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

- Mean initial alignment RMSD: `0.9687 Å`
- Maximum initial alignment RMSD: `1.1970 Å`
- Mean base shift: `0.8156 Å`
- Maximum base shift: `1.3196 Å`
- Mean optimization cost: `0.0385`
- Mean C1G→glycosidic N distance: `1.4671 Å`
- Mean P(i)→O3G(i) distance: `1.5944 Å`
- Mean O2G(i)→P(i+1) distance: `1.5926 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| GNA O2G(i)→P(i+1) | 21 | 0 | 0 | 1.593 | 1.580 | 1.602 | 1.25–1.95 | PASS |
| GNA P(i)→O3G(i) | 22 | 0 | 0 | 1.594 | 1.587 | 1.606 | 1.25–1.95 | PASS |
| C1G→glycosidic N | 22 | 0 | 0 | 1.467 | 1.442 | 1.516 | 1.25–1.75 | PASS |
| C1G→C2G | 22 | 0 | 0 | 1.523 | 1.516 | 1.533 | 1.30–1.80 | PASS |
| C2G→C3G | 22 | 0 | 0 | 1.525 | 1.518 | 1.533 | 1.30–1.80 | PASS |
| C2G→O2G | 22 | 0 | 0 | 1.426 | 1.409 | 1.441 | 1.20–1.65 | PASS |
| C3G→O3G | 22 | 0 | 0 | 1.426 | 1.402 | 1.439 | 1.20–1.65 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base shift (Å) | Opt. cost | C1G–N (Å) | P–O3G (Å) | O2G–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A62 | A | ZAD | ZAD A5 | 0.8055 | 0.4900 | 0.0108 | 1.4423723513711681 | 1.58980613440018 | 1.598537306494176 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 2 | A63 | U | ZBU | ZTH A2 | 0.8221 | 0.5681 | 0.0167 | 1.4896006176153405 | 1.605622736780404 | 1.5798862656711345 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 3 | A64 | A | ZAD | ZAD A7 | 1.1184 | 0.9815 | 0.0449 | 1.4539859008945135 | 1.5922124286799109 | 1.5985256815874185 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 4 | A65 | C | ZCY | ZCY A1 | 0.8358 | 0.6660 | 0.0228 | 1.4831925026779111 | 1.5901515616246937 | 1.5963154729444171 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 5 | A66 | G | ZGU | ZGU A6 | 0.8583 | 0.7029 | 0.0233 | 1.4498693044547273 | 1.6027187081341243 | 1.5841172394053085 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 6 | A67 | A | ZAD | ZAD A5 | 1.0978 | 0.8964 | 0.0374 | 1.4423723513711744 | 1.5897398570869863 | 1.5987234293537158 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 7 | A68 | C | ZCY | ZCY A3 | 1.0664 | 0.9206 | 0.0402 | 1.48062453039248 | 1.6004996354942291 | 1.584934268043782 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 8 | A69 | C | ZCY | ZCY A1 | 0.9982 | 0.8462 | 0.0403 | 1.4831925026779207 | 1.590030620026728 | 1.596348503271062 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 9 | A70 | A | ZAD | ZAD A7 | 1.0708 | 0.8638 | 0.0354 | 1.4539859008944997 | 1.5922822704114112 | 1.5984812800456498 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 10 | A71 | C | ZCY | ZCY A3 | 1.0712 | 0.9035 | 0.0393 | 1.4806245303924852 | 1.600637719974899 | 1.5849481094834783 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 11 | A72 | C | ZCY | ZCY A1 | 0.9020 | 0.8143 | 0.0384 | 1.4831925026779182 | 1.590189928934769 | 1.596358936793333 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 12 | A73 | U | ZBU | ZBU A4 | 1.0054 | 0.7949 | 0.0310 | 1.5163353850649235 | 1.5866969210942907 | 1.6022507261063943 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 13 | A74 | A | ZAD | ZAD A5 | 1.0545 | 0.8130 | 0.0311 | 1.442372351371165 | 1.5898129462674806 | 1.5986890879132931 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 14 | A75 | G | ZGU | ZGU A8 | 0.7888 | 0.8184 | 0.0342 | 1.4607077051895188 | 1.5889843109066997 | 1.5903678852987615 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 15 | A76 | G | ZGU | ZGU A6 | 1.1970 | 1.3196 | 0.0831 | 1.4498693044547002 | 1.6031078421624774 | 1.5844365759805084 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 16 | A77 | C | ZCY | ZCY A3 | 0.9268 | 0.9518 | 0.0448 | 1.4806245303924856 | 1.601106291183353 | 1.585188247122662 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 17 | A78 | U | ZBU | ZTH A2 | 1.0766 | 0.4553 | 0.0110 | 1.4896006176153438 | 1.6055506965144022 | 1.5798264636750385 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 18 | A79 | C | ZCY | ZCY A1 | 0.8296 | 0.6778 | 0.0257 | 1.483192502677916 | 1.590043526629084 | 1.5962694883722488 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 19 | A80 | G | ZGU | ZGU A8 | 0.8319 | 0.9228 | 0.0429 | 1.460707705189517 | 1.588750055207152 | 1.5903806458782888 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 20 | A81 | A | ZAD | ZAD A7 | 1.1756 | 1.1305 | 0.0611 | 1.4539859008945155 | 1.5925572765361968 | 1.5986778029253643 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 21 | A82 | A | ZAD | ZAD A5 | 0.9694 | 1.3092 | 0.1315 | 1.4423723513711562 | 1.593739224173542 | 1.6022961152551836 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 22 | A83 | A | ZAD | ZAD A7 | 0.8091 | 0.0964 | 0.0008 | 1.4539859008944986 | 1.59224712629792 | NA | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |

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
