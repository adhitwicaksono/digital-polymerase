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

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- GNA template PDB: `/mnt/data/2xc6-GNA-8nt.pdb`
- Output PDB: `/mnt/data/gna_prototype_007A_outputs/converted_gna_RNA-34mer_auto_007A.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC`
- GNA template base-class sequence: `CUCUAGAG`
- Source residue count: `34`
- Template residue count: `8`
- Converted residues: `34`

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

- Mean initial alignment RMSD: `0.9861 Å`
- Maximum initial alignment RMSD: `1.1970 Å`
- Mean base shift: `0.8505 Å`
- Maximum base shift: `1.3613 Å`
- Mean optimization cost: `0.0409`
- Mean C1G→glycosidic N distance: `1.4647 Å`
- Mean P(i)→O3G(i) distance: `1.5942 Å`
- Mean O2G(i)→P(i+1) distance: `1.5929 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| GNA O2G(i)→P(i+1) | 33 | 0 | 0 | 1.593 | 1.580 | 1.603 | 1.25–1.95 | PASS |
| GNA P(i)→O3G(i) | 34 | 0 | 0 | 1.594 | 1.587 | 1.606 | 1.25–1.95 | PASS |
| C1G→glycosidic N | 34 | 0 | 0 | 1.465 | 1.442 | 1.516 | 1.25–1.75 | PASS |
| C1G→C2G | 34 | 0 | 0 | 1.524 | 1.516 | 1.533 | 1.30–1.80 | PASS |
| C2G→C3G | 34 | 0 | 0 | 1.525 | 1.518 | 1.533 | 1.30–1.80 | PASS |
| C2G→O2G | 34 | 0 | 0 | 1.423 | 1.409 | 1.441 | 1.20–1.65 | PASS |
| C3G→O3G | 34 | 0 | 0 | 1.423 | 1.402 | 1.439 | 1.20–1.65 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base shift (Å) | Opt. cost | C1G–N (Å) | P–O3G (Å) | O2G–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A54 | G | ZGU | ZGU A6 | 1.0606 | 0.8280 | 0.0319 | 1.4498693044547035 | 1.6024668128851367 | 1.5840666515092923 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 2 | A55 | G | ZGU | ZGU A8 | 0.7476 | 0.7369 | 0.0281 | 1.4607077051894937 | 1.588941244369498 | 1.5903170103877189 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 3 | A56 | U | ZBU | ZTH A2 | 1.1705 | 1.0087 | 0.0488 | 1.4896006176153507 | 1.6056897007716546 | 1.5800721569540492 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 4 | A57 | G | ZGU | ZGU A6 | 1.0918 | 1.2988 | 0.0811 | 1.4498693044547122 | 1.6032717341315141 | 1.5846834855490568 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 5 | A58 | A | ZAD | ZAD A5 | 1.0846 | 0.8852 | 0.0364 | 1.4423723513711784 | 1.5897421242867822 | 1.598718465858484 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 6 | A59 | A | ZAD | ZAD A7 | 1.0832 | 0.9270 | 0.0403 | 1.4539859008945037 | 1.5922198373874887 | 1.5985060956749775 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 7 | A60 | G | ZGU | ZGU A8 | 0.7763 | 0.8309 | 0.0351 | 1.4607077051895003 | 1.5887465350993992 | 1.5903435958529741 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 8 | A61 | A | ZAD | ZAD A5 | 1.0584 | 0.8303 | 0.0326 | 1.4423723513711864 | 1.5898322841946244 | 1.5987043624958168 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 9 | A62 | A | ZAD | ZAD A7 | 0.8264 | 0.5144 | 0.0126 | 1.4539859008945057 | 1.592282210638121 | 1.5983199778324715 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 10 | A63 | U | ZBU | ZBU A4 | 0.8278 | 0.5507 | 0.0172 | 1.5163353850649173 | 1.5867223652737135 | 1.6022023798872398 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 11 | A64 | A | ZAD | ZAD A5 | 1.1252 | 0.9526 | 0.0419 | 1.4423723513711781 | 1.5897420296105835 | 1.5987437887341072 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 12 | A65 | C | ZCY | ZCY A1 | 0.8358 | 0.6660 | 0.0228 | 1.4831925026779111 | 1.5901515616246937 | 1.5963154729444171 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 13 | A66 | G | ZGU | ZGU A6 | 0.8583 | 0.7029 | 0.0233 | 1.4498693044547273 | 1.6027187081341243 | 1.5841172394053085 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 14 | A67 | A | ZAD | ZAD A7 | 1.0960 | 0.9258 | 0.0403 | 1.4539859008945086 | 1.5922134820561307 | 1.5985054924592144 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 15 | A68 | C | ZCY | ZCY A3 | 1.0664 | 0.9206 | 0.0402 | 1.48062453039248 | 1.6004996354942291 | 1.584934268043782 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 16 | A69 | C | ZCY | ZCY A1 | 0.9982 | 0.8462 | 0.0403 | 1.4831925026779207 | 1.590030620026728 | 1.596348503271062 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 17 | A70 | A | ZAD | ZAD A5 | 1.0657 | 0.8317 | 0.0325 | 1.4423723513711613 | 1.5898024199202674 | 1.598697347254911 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 18 | A71 | C | ZCY | ZCY A3 | 1.0712 | 0.9035 | 0.0393 | 1.4806245303924852 | 1.600637719974899 | 1.5849481094834783 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 19 | A72 | C | ZCY | ZCY A1 | 0.9020 | 0.8143 | 0.0384 | 1.4831925026779182 | 1.590189928934769 | 1.596358936793333 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 20 | A73 | U | ZBU | ZTH A2 | 1.0136 | 0.8210 | 0.0322 | 1.4896006176153394 | 1.6055905981523075 | 1.579962091321569 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 21 | A74 | A | ZAD | ZAD A7 | 1.0610 | 0.8455 | 0.0340 | 1.4539859008945137 | 1.5922928365042202 | 1.5984732301655844 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 22 | A75 | G | ZGU | ZGU A8 | 0.7888 | 0.8184 | 0.0342 | 1.4607077051895188 | 1.5889843109066997 | 1.5903678852987615 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 23 | A76 | G | ZGU | ZGU A6 | 1.1970 | 1.3196 | 0.0831 | 1.4498693044547002 | 1.6031078421624774 | 1.5844365759805084 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 24 | A77 | C | ZCY | ZCY A3 | 0.9268 | 0.9518 | 0.0448 | 1.4806245303924856 | 1.601106291183353 | 1.585188247122662 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 25 | A78 | U | ZBU | ZBU A4 | 1.0762 | 0.3917 | 0.0095 | 1.5163353850649215 | 1.5866115107389303 | 1.6021234915760125 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 26 | A79 | C | ZCY | ZCY A1 | 0.8296 | 0.6778 | 0.0257 | 1.483192502677916 | 1.590043526629084 | 1.5962694883722488 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 27 | A80 | G | ZGU | ZGU A8 | 0.8319 | 0.9228 | 0.0429 | 1.460707705189517 | 1.588750055207152 | 1.5903806458782888 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 28 | A81 | A | ZAD | ZAD A5 | 1.1756 | 1.0876 | 0.0561 | 1.442372351371181 | 1.59005809238755 | 1.5988769355222443 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 29 | A82 | A | ZAD | ZAD A7 | 0.9809 | 1.3613 | 0.1762 | 1.4539859008944969 | 1.5975177318529863 | 1.6033783079754658 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 30 | A83 | A | ZAD | ZAD A5 | 1.1799 | 0.9745 | 0.0440 | 1.4423723513711728 | 1.5897425978637454 | 1.5987529590755698 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 31 | A84 | G | ZGU | ZGU A6 | 0.9909 | 1.0518 | 0.0527 | 1.4498693044547017 | 1.6029128706742894 | 1.5844389133862233 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 32 | A85 | A | ZAD | ZAD A7 | 1.0825 | 0.8732 | 0.0361 | 1.45398590089451 | 1.5922364985733435 | 1.5984849095461666 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 33 | A86 | G | ZGU | ZGU A8 | 0.8003 | 0.8386 | 0.0358 | 1.460707705189501 | 1.5888323074566089 | 1.5903493787760852 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 34 | A87 | C | ZCY | ZCY A3 | 0.8472 | 0.0056 | 0.0002 | 1.48062453039249 | 1.6004998882236818 | NA | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |

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
