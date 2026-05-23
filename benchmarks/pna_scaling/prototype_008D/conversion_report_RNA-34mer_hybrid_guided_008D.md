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

- Source RNA PDB: `/mnt/data/RNA-34mer.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008D_outputs/converted_pna_RNA-34mer_hybrid_guided_008D.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `34`
- Usable template residue count: `8`
- Converted residues: `34`

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
| PNA C'(i)→N1'(i+1) | 33 | 0 | 33 | 7.482 | 4.187 | 9.662 | 1.15–2.80 | FAIL |
| C8'→glycosidic N | 34 | 0 | 0 | 1.465 | 1.451 | 1.482 | 1.20–1.85 | PASS |
| C8'→C7' | 34 | 0 | 0 | 1.530 | 1.504 | 1.552 | 1.30–1.85 | PASS |
| C7'→O7' | 34 | 0 | 0 | 1.240 | 1.224 | 1.249 | 1.10–1.40 | PASS |
| C7'→N4' | 34 | 0 | 0 | 1.339 | 1.329 | 1.346 | 1.15–1.60 | PASS |
| N4'→C3' | 34 | 0 | 0 | 1.482 | 1.473 | 1.496 | 1.25–1.80 | PASS |
| C3'→C2' | 34 | 0 | 0 | 1.522 | 1.492 | 1.553 | 1.25–1.90 | PASS |
| C2'→N1' | 34 | 0 | 0 | 1.474 | 1.457 | 1.499 | 1.20–1.80 | PASS |
| N4'→C5' | 34 | 0 | 0 | 1.481 | 1.468 | 1.487 | 1.25–1.80 | PASS |
| C5'→C' | 34 | 0 | 0 | 1.509 | 1.467 | 1.538 | 1.25–1.90 | PASS |
| C'→O1' | 34 | 0 | 0 | 1.241 | 1.235 | 1.246 | 1.10–1.40 | PASS |
| required base oxygens present | 26 | 0 | 0 | 26.000 | 26.000 | 26.000 | 1.00–26.00 | PASS |

---

## Global Sanity Diagnostics

- Mean base-fit RMSD: `0.0466 Å`
- Maximum base-fit RMSD: `0.0512 Å`
- Mean total residue shift: `0.8440 Å`
- Maximum total residue shift: `2.4524 Å`
- Mean C8′→glycosidic N distance: `1.4650 Å`
- Mean C′(i)→N1′(i+1) distance: `7.4818 Å`
- Heavy-atom inter-residue clashes below 1.00 Å: `12`
- Minimum inter-residue heavy-atom distance: `0.5715 Å`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Base-fit RMSD (Å) | Total shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|
| 1 | A54 | G | GPN | GPN A1001 | 0.0499 | 1.5658 | 1.4693753774988922 | 5.711637517105404 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 2 | A55 | G | GPN | GPN A1001 | 0.0503 | 0.3437 | 1.4693753774989053 | 8.464844958281741 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 3 | A56 | U | UPN | TPN A1005 | 0.0440 | 0.3560 | 1.4818512071055003 | 7.102174506145322 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 4 | A57 | G | GPN | GPN A1001 | 0.0507 | 0.5973 | 1.4693753774988807 | 8.3336557093291 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 5 | A58 | A | APN | APN A1004 | 0.0450 | 0.5346 | 1.4510375598171037 | 8.659843423230223 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 6 | A59 | A | APN | APN A1004 | 0.0454 | 0.6316 | 1.4510375598171175 | 7.1401475410746125 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 7 | A60 | G | GPN | GPN A1001 | 0.0496 | 0.5357 | 1.4693753774989204 | 8.714712453416597 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 8 | A61 | A | APN | APN A1004 | 0.0446 | 0.1417 | 1.4510375598171181 | 4.187029803687161 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 9 | A62 | A | APN | APN A1004 | 0.0456 | 2.4367 | 1.4510375598171357 | 5.722366010773142 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 10 | A63 | U | UPN | TPN A1005 | 0.0442 | 2.0141 | 1.4818512071054994 | 5.668812681275488 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 11 | A64 | A | APN | APN A1004 | 0.0473 | 2.4524 | 1.451037559817101 | 8.488254627371136 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 12 | A65 | C | CPN | CPN A1003 | 0.0458 | 0.3867 | 1.4719079454911668 | 5.686052955665084 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 13 | A66 | G | GPN | GPN A1001 | 0.0497 | 0.4500 | 1.4693753774988993 | 8.276444098579288 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 14 | A67 | A | APN | APN A1004 | 0.0451 | 1.9042 | 1.4510375598170964 | 7.550085838409057 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 15 | A68 | C | CPN | CPN A1003 | 0.0437 | 0.6757 | 1.4719079454911488 | 8.755801332425825 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 16 | A69 | C | CPN | CPN A1003 | 0.0446 | 0.6399 | 1.4719079454911912 | 8.588454023535883 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 17 | A70 | A | APN | APN A1004 | 0.0439 | 0.5421 | 1.4510375598171306 | 7.7381638656348954 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 18 | A71 | C | CPN | CPN A1003 | 0.0452 | 0.4042 | 1.4719079454911619 | 8.1397113714741 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 19 | A72 | C | CPN | CPN A1003 | 0.0445 | 0.2810 | 1.4719079454911614 | 8.4603723094411 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 20 | A73 | U | UPN | TPN A1005 | 0.0448 | 0.2358 | 1.4818512071054704 | 7.953167462926235 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 21 | A74 | A | APN | APN A1004 | 0.0442 | 0.3393 | 1.4510375598170904 | 6.940038526505413 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 22 | A75 | G | GPN | GPN A1001 | 0.0503 | 0.4724 | 1.469375377498902 | 6.85248738332956 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 23 | A76 | G | GPN | GPN A1001 | 0.0497 | 0.4225 | 1.4693753774989107 | 9.008774460207517 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 24 | A77 | C | CPN | CPN A1003 | 0.0431 | 0.4599 | 1.4719079454911759 | 9.268042595853405 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 25 | A78 | U | UPN | TPN A1005 | 0.0465 | 0.5959 | 1.4818512071054941 | 8.84424878952241 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 26 | A79 | C | CPN | CPN A1003 | 0.0436 | 1.2321 | 1.4719079454911403 | 5.498755988380519 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 27 | A80 | G | GPN | GPN A1001 | 0.0512 | 0.7641 | 1.4693753774988667 | 9.66182857131836 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 28 | A81 | A | APN | APN A1004 | 0.0462 | 2.4371 | 1.4510375598171281 | 5.770797201830203 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 29 | A82 | A | APN | APN A1004 | 0.0464 | 0.7256 | 1.4510375598171095 | 7.867744142602351 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 30 | A83 | A | APN | APN A1004 | 0.0460 | 0.8659 | 1.4510375598171272 | 6.456172955452413 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 31 | A84 | G | GPN | GPN A1001 | 0.0511 | 0.9833 | 1.469375377498886 | 7.905661205894777 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 32 | A85 | A | APN | APN A1004 | 0.0482 | 0.2732 | 1.4510375598171277 | 6.744729481743499 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 33 | A86 | G | GPN | GPN A1001 | 0.0504 | 0.4304 | 1.469375377498883 | 6.736903212465482 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 34 | A87 | C | CPN | CPN A1003 | 0.0441 | 1.5658 | 1.4719079454911355 | NA | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |

---

## Interpretation

Correct description:

> a PNA-like computational candidate generated by RNA base-frame guidance plus bounded PNA linkage smoothing.

Incorrect description:

> a solved, physically validated, RNA-fold-preserving PNA analog.

The classification should be interpreted conservatively. If `C′(i)→N1′(i+1)` remains failed while the visual model is not tangled, that is still valuable: it indicates where PNA resists RNA-informed conversion.
