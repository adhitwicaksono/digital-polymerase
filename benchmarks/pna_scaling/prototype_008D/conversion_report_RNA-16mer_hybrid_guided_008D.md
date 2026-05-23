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

- Source RNA PDB: `/mnt/data/RNA-16mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008D_outputs/converted_pna_RNA-16mer_hybrid_guided_008D.pdb`

---

## Source and Template

- Source RNA sequence: `ACCACCUAGGCUCGAA`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `16`
- Usable template residue count: `8`
- Converted residues: `16`

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
| PNA C'(i)→N1'(i+1) | 15 | 0 | 15 | 7.825 | 4.329 | 9.720 | 1.15–2.80 | FAIL |
| C8'→glycosidic N | 16 | 0 | 0 | 1.466 | 1.451 | 1.482 | 1.20–1.85 | PASS |
| C8'→C7' | 16 | 0 | 0 | 1.523 | 1.504 | 1.552 | 1.30–1.85 | PASS |
| C7'→O7' | 16 | 0 | 0 | 1.239 | 1.224 | 1.249 | 1.10–1.40 | PASS |
| C7'→N4' | 16 | 0 | 0 | 1.339 | 1.329 | 1.346 | 1.15–1.60 | PASS |
| N4'→C3' | 16 | 0 | 0 | 1.482 | 1.473 | 1.496 | 1.25–1.80 | PASS |
| C3'→C2' | 16 | 0 | 0 | 1.523 | 1.492 | 1.553 | 1.25–1.90 | PASS |
| C2'→N1' | 16 | 0 | 0 | 1.479 | 1.457 | 1.499 | 1.20–1.80 | PASS |
| N4'→C5' | 16 | 0 | 0 | 1.479 | 1.468 | 1.487 | 1.25–1.80 | PASS |
| C5'→C' | 16 | 0 | 0 | 1.513 | 1.467 | 1.538 | 1.25–1.90 | PASS |
| C'→O1' | 16 | 0 | 0 | 1.242 | 1.235 | 1.246 | 1.10–1.40 | PASS |
| required base oxygens present | 13 | 0 | 0 | 13.000 | 13.000 | 13.000 | 1.00–13.00 | PASS |

---

## Global Sanity Diagnostics

- Mean base-fit RMSD: `0.0458 Å`
- Maximum base-fit RMSD: `0.0512 Å`
- Mean total residue shift: `0.7809 Å`
- Maximum total residue shift: `2.4617 Å`
- Mean C8′→glycosidic N distance: `1.4662 Å`
- Mean C′(i)→N1′(i+1) distance: `7.8253 Å`
- Heavy-atom inter-residue clashes below 1.00 Å: `13`
- Minimum inter-residue heavy-atom distance: `0.2660 Å`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Base-fit RMSD (Å) | Total shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|
| 1 | A67 | A | APN | APN A1004 | 0.0451 | 1.5658 | 1.45103755981709 | 7.218446069658032 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 2 | A68 | C | CPN | CPN A1003 | 0.0437 | 0.5181 | 1.4719079454911699 | 8.819722304749561 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 3 | A69 | C | CPN | CPN A1003 | 0.0446 | 0.6329 | 1.4719079454911634 | 8.591384995785347 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 4 | A70 | A | APN | APN A1004 | 0.0439 | 0.5421 | 1.4510375598171306 | 7.738169888826925 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 5 | A71 | C | CPN | CPN A1003 | 0.0452 | 0.4042 | 1.4719079454911619 | 8.139718430328527 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 6 | A72 | C | CPN | CPN A1003 | 0.0445 | 0.2810 | 1.4719079454911832 | 8.460372252086907 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 7 | A73 | U | UPN | TPN A1005 | 0.0448 | 0.2358 | 1.4818512071054704 | 7.9531674499399045 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 8 | A74 | A | APN | APN A1004 | 0.0442 | 0.3393 | 1.4510375598171168 | 6.940038525760506 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 9 | A75 | G | GPN | GPN A1001 | 0.0503 | 0.4724 | 1.469375377498902 | 6.852487385110709 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 10 | A76 | G | GPN | GPN A1001 | 0.0497 | 0.4225 | 1.4693753774989378 | 9.008774463870218 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 11 | A77 | C | CPN | CPN A1003 | 0.0431 | 0.4599 | 1.4719079454911546 | 9.268043598609331 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 12 | A78 | U | UPN | TPN A1005 | 0.0465 | 0.5959 | 1.4818512071054941 | 8.844092815769338 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 13 | A79 | C | CPN | CPN A1003 | 0.0436 | 1.2323 | 1.4719079454911403 | 5.496824425547918 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 14 | A80 | G | GPN | GPN A1001 | 0.0512 | 0.7676 | 1.4693753774988931 | 9.720344799502568 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 15 | A81 | A | APN | APN A1004 | 0.0462 | 2.4617 | 1.4510375598171281 | 4.328519273037015 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 16 | A82 | A | APN | APN A1004 | 0.0464 | 1.5626 | 1.4510375598171095 | NA | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |

---

## Interpretation

Correct description:

> a PNA-like computational candidate generated by RNA base-frame guidance plus bounded PNA linkage smoothing.

Incorrect description:

> a solved, physically validated, RNA-fold-preserving PNA analog.

The classification should be interpreted conservatively. If `C′(i)→N1′(i+1)` remains failed while the visual model is not tangled, that is still valuable: it indicates where PNA resists RNA-informed conversion.
