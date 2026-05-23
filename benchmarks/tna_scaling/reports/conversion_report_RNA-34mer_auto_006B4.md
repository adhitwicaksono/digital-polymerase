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

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- TNA template PDB: `/mnt/data/6MU5_TNA_13mer.pdb`
- Output PDB: `/mnt/data/tna_prototype_006B4_outputs/converted_tna_RNA-34mer_auto_006B4.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC`
- TNA template base-class sequence: `GUACGUGAUCGCA`
- Source residue count: `34`
- Template residue count: `13`
- Converted residues: `34`

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

- Mean initial segment RMSD: `0.9575 Å`
- Maximum initial segment RMSD: `1.5504 Å`
- Mean base-transplant RMSD: `0.0995 Å`
- Maximum base-transplant RMSD: `0.3348 Å`
- Mean optimization cost: `0.0054`
- Mean C1′→glycosidic N distance: `1.4475 Å`
- Mean P(i)→O3′(i) distance: `1.6026 Å`
- Mean O2′(i)→P(i+1) distance: `1.5722 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| TNA O2'(i)→P(i+1) | 33 | 0 | 0 | 1.572 | 1.333 | 1.620 | 1.25–1.90 | PASS |
| TNA P(i)→O3'(i) | 34 | 0 | 0 | 1.603 | 1.589 | 1.617 | 1.35–1.90 | PASS |
| C1'→glycosidic N | 34 | 0 | 0 | 1.448 | 1.415 | 1.473 | 1.30–1.75 | PASS |
| C1'→C2' | 34 | 0 | 0 | 1.473 | 1.446 | 1.491 | 1.25–1.90 | PASS |
| C2'→C3' | 34 | 0 | 0 | 1.432 | 1.380 | 1.453 | 1.20–1.90 | PASS |
| C3'→C4' | 34 | 0 | 0 | 1.530 | 1.496 | 1.578 | 1.25–2.00 | PASS |
| C2'→O2' | 34 | 0 | 0 | 1.200 | 1.184 | 1.225 | 1.05–1.65 | PASS |
| C3'→O3' | 34 | 0 | 0 | 1.431 | 1.423 | 1.437 | 1.10–1.75 | PASS |
| C1'→O4' | 34 | 0 | 0 | 1.490 | 1.462 | 1.540 | 1.20–1.85 | PASS |
| C4'→O4' | 34 | 0 | 0 | 1.523 | 1.505 | 1.583 | 1.20–1.95 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base RMSD (Å) | Opt. cost | C1′–N (Å) | P–O3′ (Å) | O2′–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A54 | G | TG | TG T4 | 0.7786 | 0.0557 | 0.0021 | 1.4515805179183119 | 1.599179292980538 | 1.599442571349117 | exact base-class TNA template; linkage-optimized |
| 2 | A55 | G | TG | TG T8 | 0.7970 | 0.0388 | 0.0023 | 1.4601102698084145 | 1.5924097404346116 | 1.6197153497298225 | exact base-class TNA template; linkage-optimized |
| 3 | A56 | U | TU | TFT T5 | 1.1368 | 0.0671 | 0.0064 | 1.4586521175386604 | 1.603717998305074 | 1.6098100092316348 | exact base-class TNA template; linkage-optimized |
| 4 | A57 | G | TG | TG T10 | 1.0194 | 0.0546 | 0.0069 | 1.4664422934435608 | 1.6100677994673358 | 1.612183648836333 | exact base-class TNA template; linkage-optimized |
| 5 | A58 | A | FA2 | FA2 T6 | 0.9776 | 0.0807 | 0.0021 | 1.473466999969791 | 1.6167545253018971 | 1.613089320223588 | exact base-class TNA template; linkage-optimized |
| 6 | A59 | A | FA2 | FA2 T11 | 0.9532 | 0.0743 | 0.0029 | 1.4461666570627363 | 1.6003189313297224 | 1.3333923114253285 | exact base-class TNA template; linkage-optimized |
| 7 | A60 | G | TG | TG T14 | 0.9698 | 0.0984 | 0.0029 | 1.4545246646241459 | 1.6010864279868493 | 1.6145306363019691 | exact base-class TNA template; linkage-optimized |
| 8 | A61 | A | FA2 | FA2 T16 | 0.8231 | 0.0686 | 0.0184 | 1.4475648517423874 | 1.600195979764589 | 1.5802286845663527 | exact base-class TNA template; linkage-optimized |
| 9 | A62 | A | FA2 | FA2 T6 | 0.7602 | 0.2782 | 0.0012 | 1.473466999969808 | 1.616728134796664 | 1.6130812915056876 | exact base-class TNA template; linkage-optimized |
| 10 | A63 | U | TU | TFT T9 | 0.7150 | 0.3316 | 0.0019 | 1.4534142561568688 | 1.6069803748838842 | 1.6164447151308827 | exact base-class TNA template; linkage-optimized |
| 11 | A64 | A | FA2 | FA2 T11 | 1.0485 | 0.0774 | 0.0024 | 1.4461666570627414 | 1.6002930367975245 | 1.3333775919479292 | exact base-class TNA template; linkage-optimized |
| 12 | A65 | C | TC | TC T7 | 0.7306 | 0.3174 | 0.0022 | 1.4220780569293687 | 1.6101705062239406 | 1.6148776702571488 | exact base-class TNA template; linkage-optimized |
| 13 | A66 | G | TG | TG T4 | 0.9801 | 0.3348 | 0.0041 | 1.451580517918322 | 1.5992449115417242 | 1.5994676492378015 | exact base-class TNA template; linkage-optimized |
| 14 | A67 | A | FA2 | FA2 T16 | 0.8078 | 0.0675 | 0.0168 | 1.4475648517424073 | 1.6001660277560912 | 1.580213906554939 | exact base-class TNA template; linkage-optimized |
| 15 | A68 | C | TC | TC T13 | 1.0465 | 0.1214 | 0.0021 | 1.4149621903075762 | 1.5889689306711718 | 1.6008347007093662 | exact base-class TNA template; linkage-optimized |
| 16 | A69 | C | TC | TC T15 | 1.0959 | 0.0649 | 0.0027 | 1.4149943462784573 | 1.6025211605578036 | 1.5889856038173396 | exact base-class TNA template; linkage-optimized |
| 17 | A70 | A | FA2 | FA2 T6 | 0.9417 | 0.0832 | 0.0022 | 1.4734669999697945 | 1.6167698669150323 | 1.613093562678464 | exact base-class TNA template; linkage-optimized |
| 18 | A71 | C | TC | TC T7 | 0.8192 | 0.0483 | 0.0026 | 1.4220780569293467 | 1.6101780625264914 | 1.6148798519175258 | exact base-class TNA template; linkage-optimized |
| 19 | A72 | C | TC | TC T13 | 0.9605 | 0.1037 | 0.0028 | 1.4149621903075698 | 1.5890236226632262 | 1.600866653937341 | exact base-class TNA template; linkage-optimized |
| 20 | A73 | U | TU | TFT T12 | 0.9726 | 0.0966 | 0.0020 | 1.4586068695848184 | 1.6039309315789 | 1.6038221768760028 | exact base-class TNA template; linkage-optimized |
| 21 | A74 | A | FA2 | FA2 T11 | 0.8936 | 0.0812 | 0.0031 | 1.4461666570627418 | 1.6003351141774187 | 1.3333944120400847 | exact base-class TNA template; linkage-optimized |
| 22 | A75 | G | TG | TG T8 | 0.8249 | 0.0410 | 0.0027 | 1.4601102698084174 | 1.5924194734380297 | 1.6197182413373405 | exact base-class TNA template; linkage-optimized |
| 23 | A76 | G | TG | TG T10 | 1.0343 | 0.0620 | 0.0077 | 1.4664422934435553 | 1.6100707595554211 | 1.6121350918773187 | exact base-class TNA template; linkage-optimized |
| 24 | A77 | C | TC | TC T15 | 0.9687 | 0.0490 | 0.0086 | 1.4149943462784447 | 1.6026909049770706 | 1.5891151564038968 | exact base-class TNA template; linkage-optimized |
| 25 | A78 | U | TU | TFT T5 | 1.5504 | 0.0638 | 0.0029 | 1.4586521175386546 | 1.6036144516475193 | 1.609759296904496 | exact base-class TNA template; linkage-optimized |
| 26 | A79 | C | TC | TC T7 | 0.8645 | 0.0480 | 0.0012 | 1.422078056929353 | 1.610115397382598 | 1.6148553859949322 | exact base-class TNA template; linkage-optimized |
| 27 | A80 | G | TG | TG T14 | 1.0585 | 0.0926 | 0.0034 | 1.4545246646241532 | 1.6010959207240738 | 1.6145329736697798 | exact base-class TNA template; linkage-optimized |
| 28 | A81 | A | FA2 | FA2 T16 | 1.0007 | 0.0590 | 0.0324 | 1.4475648517423862 | 1.6003002296291464 | 1.5803087455423455 | exact base-class TNA template; linkage-optimized |
| 29 | A82 | A | FA2 | FA2 T6 | 1.1644 | 0.0653 | 0.0085 | 1.4734669999697974 | 1.6170939699628266 | 1.6133907289790583 | exact base-class TNA template; linkage-optimized |
| 30 | A83 | A | FA2 | FA2 T11 | 1.1351 | 0.0919 | 0.0022 | 1.4461666570627252 | 1.6002799123030573 | 1.333369792003152 | exact base-class TNA template; linkage-optimized |
| 31 | A84 | G | TG | TG T4 | 1.2154 | 0.0502 | 0.0052 | 1.4515805179183214 | 1.5992711168435216 | 1.5995496745689493 | exact base-class TNA template; linkage-optimized |
| 32 | A85 | A | FA2 | FA2 T16 | 0.8056 | 0.0726 | 0.0162 | 1.4475648517423885 | 1.6001735702932987 | 1.5802111247886899 | exact base-class TNA template; linkage-optimized |
| 33 | A86 | G | TG | TG T8 | 0.9380 | 0.0415 | 0.0022 | 1.4601102698084227 | 1.592396611270453 | 1.6197154968885945 | exact base-class TNA template; linkage-optimized |
| 34 | A87 | C | TC | TC T13 | 0.7653 | 0.1026 | 0.0000 | 1.414962190307561 | 1.588947190765263 | NA | exact base-class TNA template; linkage-optimized |

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
