# RNA → PNA Hybrid-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 008D  
**Method:** RNA-informed PNA hybrid-guided reconstruction  
**Status:** Experimental boundary-test candidate; not physically validated  
**Classification:** `PARTIAL_PASS_LINKAGE_NOT_FULLY_SOLVED`  
**PNA chain-continuity status:** `C′(i)→N1′(i+1) FAIL`  
**Base-attachment status:** `PASS`  
**Base-oxygen audit:** `PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-22mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008D_outputs/converted_pna_RNA-22mer_hybrid_guided_008D.pdb`

---

## Source and Template

- Source RNA sequence: `AUACGACCACCUAGGCUCGAAA`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `22`
- Usable template residue count: `8`
- Converted residues: `22`

---

## 008D Strategy

Prototype 008D is a hybrid boundary-test.

It uses:

```text
RNA base-frame alignment
+
PNA local pseudopeptide scaffold
+
bounded C′(i)→N1′(i+1) smoothing
+
movement caps to prevent collapse
```

This is intentionally different from:

```text
008A.1 → aggressive RNA-fold forcing
008B   → template-primary scaffold-first generation
008C   → sequence-primary generation
```

008D asks:

```text
Can PNA be nudged toward RNA-informed geometry without collapsing?
```

---

## Parameters

```text
iterations       = 60
step_cap         = 0.08
max_total_shift  = 2.5
spring           = 0.015
```

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean | Min | Max | Expected | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| PNA C'(i)→N1'(i+1) | 21 | 0 | 21 | 7.611 | 5.499 | 9.658 | 1.15–2.80 | FAIL |
| C8'→glycosidic N | 22 | 0 | 0 | 1.465 | 1.451 | 1.482 | 1.20–1.85 | PASS |
| C8'→C7' | 22 | 0 | 0 | 1.525 | 1.504 | 1.552 | 1.30–1.85 | PASS |
| C7'→O7' | 22 | 0 | 0 | 1.239 | 1.224 | 1.249 | 1.10–1.40 | PASS |
| C7'→N4' | 22 | 0 | 0 | 1.338 | 1.329 | 1.346 | 1.15–1.60 | PASS |
| N4'→C3' | 22 | 0 | 0 | 1.483 | 1.473 | 1.496 | 1.25–1.80 | PASS |
| C3'→C2' | 22 | 0 | 0 | 1.525 | 1.492 | 1.553 | 1.25–1.90 | PASS |
| C2'→N1' | 22 | 0 | 0 | 1.477 | 1.457 | 1.499 | 1.20–1.80 | PASS |
| N4'→C5' | 22 | 0 | 0 | 1.480 | 1.468 | 1.487 | 1.25–1.80 | PASS |
| C5'→C' | 22 | 0 | 0 | 1.509 | 1.467 | 1.538 | 1.25–1.90 | PASS |
| C'→O1' | 22 | 0 | 0 | 1.242 | 1.235 | 1.246 | 1.10–1.40 | PASS |
| required base oxygens present | 17 | 0 | 0 | 17.000 | 17.000 | 17.000 | 1.00–17.00 | PASS |

---

## Global Sanity Diagnostics

- Mean base-fit RMSD: `0.0460 Å`
- Maximum base-fit RMSD: `0.0512 Å`
- Mean total residue shift: `0.9377 Å`
- Maximum total residue shift: `2.4468 Å`
- Mean C8′→glycosidic N distance: `1.4652 Å`
- Mean C′(i)→N1′(i+1) distance: `7.6110 Å`
- Heavy-atom inter-residue clashes below 1.00 Å: `8`
- Minimum inter-residue heavy-atom distance: `0.5370 Å`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Base-fit RMSD (Å) | Total shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|
| 1 | A62 | A | APN | APN A1004 | 0.0456 | 1.5637 | 1.4510375598171357 | 6.157272566288415 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 2 | A63 | U | UPN | TPN A1005 | 0.0442 | 2.0129 | 1.4818512071054843 | 5.673983459982915 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 3 | A64 | A | APN | APN A1004 | 0.0473 | 2.4468 | 1.451037559817101 | 8.501340276378986 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 4 | A65 | C | CPN | CPN A1003 | 0.0458 | 0.3862 | 1.4719079454911532 | 5.686131692435145 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 5 | A66 | G | GPN | GPN A1001 | 0.0497 | 0.4501 | 1.4693753774988814 | 8.276431816085394 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 6 | A67 | A | APN | APN A1004 | 0.0451 | 1.9042 | 1.4510375598170964 | 7.550088255070503 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 7 | A68 | C | CPN | CPN A1003 | 0.0437 | 0.6757 | 1.4719079454911488 | 8.75580135068659 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 8 | A69 | C | CPN | CPN A1003 | 0.0446 | 0.6399 | 1.4719079454911912 | 8.588454024187683 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 9 | A70 | A | APN | APN A1004 | 0.0439 | 0.5421 | 1.4510375598171306 | 7.738163865648076 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 10 | A71 | C | CPN | CPN A1003 | 0.0452 | 0.4042 | 1.4719079454911619 | 8.139711371474448 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 11 | A72 | C | CPN | CPN A1003 | 0.0445 | 0.2810 | 1.4719079454911614 | 8.460372309441105 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 12 | A73 | U | UPN | TPN A1005 | 0.0448 | 0.2358 | 1.4818512071054704 | 7.95316746292617 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 13 | A74 | A | APN | APN A1004 | 0.0442 | 0.3393 | 1.4510375598170904 | 6.9400385265021365 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 14 | A75 | G | GPN | GPN A1001 | 0.0503 | 0.4724 | 1.469375377498902 | 6.852487383171998 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 15 | A76 | G | GPN | GPN A1001 | 0.0497 | 0.4225 | 1.4693753774989107 | 9.008774454180712 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 16 | A77 | C | CPN | CPN A1003 | 0.0431 | 0.4599 | 1.4719079454911546 | 9.26804231125533 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 17 | A78 | U | UPN | TPN A1005 | 0.0465 | 0.5959 | 1.4818512071054941 | 8.84426185557907 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 18 | A79 | C | CPN | CPN A1003 | 0.0436 | 1.2321 | 1.4719079454911403 | 5.498899982436662 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 19 | A80 | G | GPN | GPN A1001 | 0.0512 | 0.7638 | 1.4693753774988931 | 9.65759860950863 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 20 | A81 | A | APN | APN A1004 | 0.0462 | 2.4399 | 1.4510375598171281 | 5.733177848703146 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 21 | A82 | A | APN | APN A1004 | 0.0464 | 0.7951 | 1.4510375598171095 | 6.546212042472562 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 22 | A83 | A | APN | APN A1004 | 0.0460 | 1.5654 | 1.4510375598171272 | NA | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |

---

## Interpretation

Correct description:

> a PNA-like computational candidate generated by RNA base-frame guidance plus bounded PNA linkage smoothing.

Incorrect description:

> a solved, physically validated, RNA-fold-preserving PNA analog.

The classification should be interpreted conservatively. If `C′(i)→N1′(i+1)` remains failed while the visual model is not tangled, that is still valuable: it indicates where PNA resists RNA-informed conversion.
