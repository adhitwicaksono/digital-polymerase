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

- Source RNA PDB: `/mnt/data/RNA-12mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008D_outputs/converted_pna_RNA-12mer_hybrid_guided_008D.pdb`

---

## Source and Template

- Source RNA sequence: `CUAGGCUCGAAA`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `12`
- Usable template residue count: `8`
- Converted residues: `12`

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
| PNA C'(i)→N1'(i+1) | 11 | 0 | 11 | 7.566 | 5.499 | 9.658 | 1.15–2.80 | FAIL |
| C8'→glycosidic N | 12 | 0 | 0 | 1.466 | 1.451 | 1.482 | 1.20–1.85 | PASS |
| C8'→C7' | 12 | 0 | 0 | 1.527 | 1.504 | 1.552 | 1.30–1.85 | PASS |
| C7'→O7' | 12 | 0 | 0 | 1.239 | 1.224 | 1.249 | 1.10–1.40 | PASS |
| C7'→N4' | 12 | 0 | 0 | 1.339 | 1.329 | 1.346 | 1.15–1.60 | PASS |
| N4'→C3' | 12 | 0 | 0 | 1.482 | 1.473 | 1.496 | 1.25–1.80 | PASS |
| C3'→C2' | 12 | 0 | 0 | 1.522 | 1.492 | 1.553 | 1.25–1.90 | PASS |
| C2'→N1' | 12 | 0 | 0 | 1.476 | 1.457 | 1.499 | 1.20–1.80 | PASS |
| N4'→C5' | 12 | 0 | 0 | 1.480 | 1.468 | 1.487 | 1.25–1.80 | PASS |
| C5'→C' | 12 | 0 | 0 | 1.510 | 1.467 | 1.538 | 1.25–1.90 | PASS |
| C'→O1' | 12 | 0 | 0 | 1.241 | 1.235 | 1.246 | 1.10–1.40 | PASS |
| required base oxygens present | 10 | 0 | 0 | 10.000 | 10.000 | 10.000 | 1.00–10.00 | PASS |

---

## Global Sanity Diagnostics

- Mean base-fit RMSD: `0.0464 Å`
- Maximum base-fit RMSD: `0.0512 Å`
- Mean total residue shift: `0.9058 Å`
- Maximum total residue shift: `2.4399 Å`
- Mean C8′→glycosidic N distance: `1.4660 Å`
- Mean C′(i)→N1′(i+1) distance: `7.5662 Å`
- Heavy-atom inter-residue clashes below 1.00 Å: `6`
- Minimum inter-residue heavy-atom distance: `0.5370 Å`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Base-fit RMSD (Å) | Total shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|
| 1 | A72 | C | CPN | CPN A1003 | 0.0445 | 1.5660 | 1.4719079454911614 | 6.922279426448315 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 2 | A73 | U | UPN | TPN A1005 | 0.0448 | 0.2185 | 1.4818512071054704 | 7.9558513334876295 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 3 | A74 | A | APN | APN A1004 | 0.0442 | 0.3387 | 1.4510375598170904 | 6.940186260384921 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 4 | A75 | G | GPN | GPN A1001 | 0.0503 | 0.4723 | 1.469375377498902 | 6.852506107786641 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 5 | A76 | G | GPN | GPN A1001 | 0.0497 | 0.4225 | 1.4693753774988805 | 9.008773296989816 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 6 | A77 | C | CPN | CPN A1003 | 0.0431 | 0.4599 | 1.4719079454911332 | 9.26804213185901 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 7 | A78 | U | UPN | TPN A1005 | 0.0465 | 0.5959 | 1.4818512071054941 | 8.844261849166339 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 8 | A79 | C | CPN | CPN A1003 | 0.0436 | 1.2321 | 1.4719079454911403 | 5.4988999822878855 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 9 | A80 | G | GPN | GPN A1001 | 0.0512 | 0.7638 | 1.4693753774988931 | 9.657598609504191 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 10 | A81 | A | APN | APN A1004 | 0.0462 | 2.4399 | 1.4510375598171281 | 5.733177848702396 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 11 | A82 | A | APN | APN A1004 | 0.0464 | 0.7951 | 1.4510375598171095 | 6.546212042472561 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 12 | A83 | A | APN | APN A1004 | 0.0460 | 1.5654 | 1.4510375598171272 | NA | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |

---

## Interpretation

Correct description:

> a PNA-like computational candidate generated by RNA base-frame guidance plus bounded PNA linkage smoothing.

Incorrect description:

> a solved, physically validated, RNA-fold-preserving PNA analog.

The classification should be interpreted conservatively. If `C′(i)→N1′(i+1)` remains failed while the visual model is not tangled, that is still valuable: it indicates where PNA resists RNA-informed conversion.
