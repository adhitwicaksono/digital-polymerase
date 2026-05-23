# RNA → TNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 006B  
**Method:** Linkage-optimized TNA reconstruction  
**Status:** Experimental candidate, not physically validated  
**TNA chain-continuity status:** `O2′(i)→P(i+1) PASS`, `P(i)→O3′(i) PASS`  
**Base-attachment status:** `PASS`  
**Local TNA sugar status:** `C2′→O2′ PASS`, `C3′→O3′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-16mer.pdb`
- TNA template PDB: `/mnt/data/6MU5_TNA_13mer.pdb`
- Output PDB: `/mnt/data/tna_prototype_006B4_outputs/converted_tna_RNA-16mer_auto_006B4.pdb`

---

## Source and Template

- Source RNA sequence: `ACCACCUAGGCUCGAA`
- TNA template base-class sequence: `GUACGUGAUCGCA`
- Source residue count: `16`
- Template residue count: `13`
- Converted residues: `16`

---

## Why TNA Needed Prototype 006B.4

Prototype 006A showed the correct conceptual issue: TNA does not use RNA-like O3′→P chain logic.  
Prototype 006A.1 added direct O2′/O3′ linkage correction, but some residues still could not satisfy both sugar and phosphate distances while keeping the initial sugar fixed.

Prototype 006B.4 therefore locally optimizes each TNA-like sugar scaffold so that:

```text
P(i)    → O3′(i)
O2′(i) → P(i+1)
C2′    → O2′
C3′    → O3′
internal threose-like sugar distances
```

are improved simultaneously.

---

## Alignment / Optimization Summary

- Mean initial segment RMSD: `0.9598 Å`
- Maximum initial segment RMSD: `1.2477 Å`
- Mean base-transplant RMSD: `0.0724 Å`
- Maximum base-transplant RMSD: `0.1307 Å`
- Mean optimization cost: `0.0040`
- Mean C1′→glycosidic N distance: `1.4426 Å`
- Mean P(i)→O3′(i) distance: `1.6031 Å`
- Mean O2′(i)→P(i+1) distance: `1.5871 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| TNA O2'(i)→P(i+1) | 15 | 0 | 0 | 1.587 | 1.333 | 1.620 | 1.25–1.90 | PASS |
| TNA P(i)→O3'(i) | 16 | 0 | 0 | 1.603 | 1.589 | 1.617 | 1.35–1.90 | PASS |
| C1'→glycosidic N | 16 | 0 | 0 | 1.443 | 1.415 | 1.473 | 1.30–1.75 | PASS |
| C1'→C2' | 16 | 0 | 0 | 1.475 | 1.453 | 1.491 | 1.25–1.90 | PASS |
| C2'→C3' | 16 | 0 | 0 | 1.428 | 1.381 | 1.453 | 1.20–1.90 | PASS |
| C3'→C4' | 16 | 0 | 0 | 1.525 | 1.496 | 1.577 | 1.25–2.00 | PASS |
| C2'→O2' | 16 | 0 | 0 | 1.201 | 1.184 | 1.225 | 1.05–1.65 | PASS |
| C3'→O3' | 16 | 0 | 0 | 1.431 | 1.423 | 1.437 | 1.10–1.75 | PASS |
| C1'→O4' | 16 | 0 | 0 | 1.499 | 1.462 | 1.540 | 1.20–1.85 | PASS |
| C4'→O4' | 16 | 0 | 0 | 1.524 | 1.510 | 1.583 | 1.20–1.95 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base RMSD (Å) | Opt. cost | C1′–N (Å) | P–O3′ (Å) | O2′–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A67 | A | FA2 | FA2 T6 | 0.9973 | 0.0818 | 0.0021 | 1.4734669999698011 | 1.6167531221382605 | 1.6130890681986882 | exact base-class TNA template; linkage-optimized |
| 2 | A68 | C | TC | TC T7 | 0.8782 | 0.0451 | 0.0016 | 1.4220780569293576 | 1.610133129430179 | 1.6148605404774186 | exact base-class TNA template; linkage-optimized |
| 3 | A69 | C | TC | TC T13 | 1.0661 | 0.1307 | 0.0021 | 1.4149621903075513 | 1.5889684344770922 | 1.6008328060682726 | exact base-class TNA template; linkage-optimized |
| 4 | A70 | A | FA2 | FA2 T11 | 0.9071 | 0.0807 | 0.0032 | 1.4461666570627312 | 1.6003345270399956 | 1.3333956383178929 | exact base-class TNA template; linkage-optimized |
| 5 | A71 | C | TC | TC T15 | 1.0546 | 0.0561 | 0.0048 | 1.4149943462784544 | 1.6025829542491192 | 1.5890355294826461 | exact base-class TNA template; linkage-optimized |
| 6 | A72 | C | TC | TC T7 | 0.7883 | 0.0488 | 0.0027 | 1.4220780569293623 | 1.6101841226905356 | 1.6148812466761553 | exact base-class TNA template; linkage-optimized |
| 7 | A73 | U | TU | TFT T5 | 0.8525 | 0.0674 | 0.0030 | 1.458652117538659 | 1.603649518040659 | 1.6097480080001547 | exact base-class TNA template; linkage-optimized |
| 8 | A74 | A | FA2 | FA2 T16 | 0.8125 | 0.0721 | 0.0162 | 1.447564851742401 | 1.600183364935014 | 1.580210736947958 | exact base-class TNA template; linkage-optimized |
| 9 | A75 | G | TG | TG T4 | 0.8056 | 0.0541 | 0.0043 | 1.4515805179183179 | 1.5992464417048033 | 1.5994588558631155 | exact base-class TNA template; linkage-optimized |
| 10 | A76 | G | TG | TG T8 | 1.0895 | 0.0392 | 0.0072 | 1.4601102698084218 | 1.592513480488541 | 1.6197582944640097 | exact base-class TNA template; linkage-optimized |
| 11 | A77 | C | TC | TC T13 | 0.8606 | 0.0762 | 0.0046 | 1.4149621903075735 | 1.5891177324809438 | 1.6009354069908188 | exact base-class TNA template; linkage-optimized |
| 12 | A78 | U | TU | TFT T9 | 1.2477 | 0.0761 | 0.0024 | 1.4534142561568517 | 1.6069726738510735 | 1.6164494820626976 | exact base-class TNA template; linkage-optimized |
| 13 | A79 | C | TC | TC T15 | 1.0754 | 0.0922 | 0.0022 | 1.4149943462784533 | 1.602501133612669 | 1.5889655210568743 | exact base-class TNA template; linkage-optimized |
| 14 | A80 | G | TG | TG T10 | 0.9967 | 0.0664 | 0.0021 | 1.4664422934435655 | 1.60992523809357 | 1.612062050585148 | exact base-class TNA template; linkage-optimized |
| 15 | A81 | A | FA2 | FA2 T6 | 1.1620 | 0.0663 | 0.0053 | 1.4734669999698016 | 1.6168623385513397 | 1.6131523167298796 | exact base-class TNA template; linkage-optimized |
| 16 | A82 | A | FA2 | FA2 T11 | 0.7622 | 0.1046 | 0.0000 | 1.4461666570627183 | 1.6002594508881742 | NA | exact base-class TNA template; linkage-optimized |

---

## Scientific Interpretation

This output should be interpreted as:

> a TNA-like computational candidate generated by linkage-optimized reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready TNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- TNA stereochemistry requires expert inspection.
- The output lacks RNA-like O5′/C5′ sugar-extension atoms because TNA is shorter.
- Molecular viewers may not render standard nucleic-acid cartoon paths reliably for TNA-like structures.
- Biological function, stability, replication, or catalytic activity is not implied.
