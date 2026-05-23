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

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008D_outputs/converted_pna_8t5o-HH-typeI-111mer-full_hybrid_guided_008D.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `111`
- Usable template residue count: `8`
- Converted residues: `111`

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
| PNA C'(i)→N1'(i+1) | 109 | 0 | 106 | 7.651 | 2.212 | 11.754 | 1.15–2.80 | FAIL |
| C8'→glycosidic N | 111 | 0 | 0 | 1.466 | 1.451 | 1.482 | 1.20–1.85 | PASS |
| C8'→C7' | 111 | 0 | 0 | 1.528 | 1.504 | 1.552 | 1.30–1.85 | PASS |
| C7'→O7' | 111 | 0 | 0 | 1.238 | 1.224 | 1.249 | 1.10–1.40 | PASS |
| C7'→N4' | 111 | 0 | 0 | 1.338 | 1.329 | 1.346 | 1.15–1.60 | PASS |
| N4'→C3' | 111 | 0 | 0 | 1.482 | 1.473 | 1.496 | 1.25–1.80 | PASS |
| C3'→C2' | 111 | 0 | 0 | 1.522 | 1.492 | 1.553 | 1.25–1.90 | PASS |
| C2'→N1' | 111 | 0 | 0 | 1.476 | 1.457 | 1.499 | 1.20–1.80 | PASS |
| N4'→C5' | 111 | 0 | 0 | 1.480 | 1.468 | 1.487 | 1.25–1.80 | PASS |
| C5'→C' | 111 | 0 | 0 | 1.510 | 1.467 | 1.538 | 1.25–1.90 | PASS |
| C'→O1' | 111 | 0 | 0 | 1.241 | 1.235 | 1.246 | 1.10–1.40 | PASS |
| required base oxygens present | 94 | 0 | 0 | 94.000 | 94.000 | 94.000 | 1.00–94.00 | PASS |

---

## Global Sanity Diagnostics

- Mean base-fit RMSD: `0.0463 Å`
- Maximum base-fit RMSD: `0.0516 Å`
- Mean total residue shift: `0.7866 Å`
- Maximum total residue shift: `2.4524 Å`
- Mean C8′→glycosidic N distance: `1.4661 Å`
- Mean C′(i)→N1′(i+1) distance: `7.6514 Å`
- Heavy-atom inter-residue clashes below 1.00 Å: `45`
- Minimum inter-residue heavy-atom distance: `0.3315 Å`

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Base-fit RMSD (Å) | Total shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Missing required base atoms | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|
| 1 | A5 | G | GPN | GPN A1001 | 0.0516 | 1.5658 | 1.46937537749889 | 5.894207877744213 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 2 | A6 | G | GPN | GPN A1001 | 0.0511 | 0.4464 | 1.4693753774988927 | 8.698422908566021 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 3 | A7 | U | UPN | TPN A1005 | 0.0437 | 0.1023 | 1.4818512071054961 | 8.09637327786686 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 4 | A8 | G | GPN | GPN A1001 | 0.0507 | 1.0614 | 1.469375377498893 | 8.126755725196613 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 5 | A9 | C | CPN | CPN A1003 | 0.0424 | 0.6571 | 1.4719079454911403 | 9.681355808428803 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 6 | A10 | A | APN | APN A1004 | 0.0458 | 1.0987 | 1.4510375598170986 | 5.744654960561882 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 7 | A11 | G | GPN | GPN A1001 | 0.0496 | 0.4535 | 1.4693753774988634 | 7.08708621742387 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 8 | A12 | G | GPN | GPN A1001 | 0.0508 | 0.4222 | 1.469375377498884 | 9.52393323153041 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 9 | A13 | U | UPN | TPN A1005 | 0.0449 | 0.6004 | 1.4818512071055139 | 7.786761825005342 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 10 | A14 | A | APN | APN A1004 | 0.0461 | 0.3844 | 1.4510375598170875 | 6.840308156749498 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 11 | A15 | C | CPN | CPN A1003 | 0.0448 | 2.4477 | 1.4719079454911699 | 4.829800484148415 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 12 | A16 | A | APN | APN A1004 | 0.0448 | 1.4666 | 1.4510375598171215 | 8.223166584728412 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 13 | A17 | U | UPN | TPN A1005 | 0.0443 | 0.5008 | 1.481851207105499 | 8.352013219876538 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 14 | A18 | C | CPN | CPN A1003 | 0.0440 | 0.4306 | 1.471907945491154 | 9.869627493208746 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 15 | A19 | C | CPN | CPN A1003 | 0.0442 | 0.6832 | 1.471907945491184 | 8.085048153874606 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 16 | A20 | A | APN | APN A1004 | 0.0467 | 0.4627 | 1.4510375598171112 | 6.693506095812863 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 17 | A21 | G | GPN | GPN A1001 | 0.0506 | 0.5346 | 1.4693753774988838 | 10.234959943368453 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 18 | A22 | C | CPN | CPN A1003 | 0.0458 | 1.0111 | 1.471907945491146 | 3.045795534069767 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 19 | A23 | U | UPN | TPN A1005 | 0.0441 | 0.1774 | 1.4818512071055114 | 10.092861542259683 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 20 | A24 | G | GPN | GPN A1001 | 0.0515 | 2.4516 | 1.4693753774988918 | 7.546576608843602 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 21 | A25 | A | APN | APN A1004 | 0.0451 | 0.4359 | 1.4510375598171188 | 7.520629652993543 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 22 | A26 | U | UPN | TPN A1005 | 0.0442 | 2.4443 | 1.4818512071054843 | 4.225498341108247 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 23 | A27 | G | GPN | GPN A1001 | 0.0508 | 1.1585 | 1.469375377498905 | 4.437179747094027 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 24 | A28 | A | APN | APN A1004 | 0.0462 | 0.4734 | 1.4510375598171203 | 7.135196294741981 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 25 | A29 | G | GPN | GPN A1001 | 0.0511 | 0.4113 | 1.469375377498896 | 8.83303006585957 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 26 | A30 | U | UPN | TPN A1005 | 0.0437 | 0.6309 | 1.4818512071054892 | 8.107758143292232 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 27 | A31 | C | CPN | CPN A1003 | 0.0437 | 0.5404 | 1.471907945491137 | 8.56860353228525 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 28 | A32 | C | CPN | CPN A1003 | 0.0441 | 0.6624 | 1.4719079454911521 | 8.441517649082003 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 29 | A33 | C | CPN | CPN A1003 | 0.0438 | 0.5016 | 1.4719079454911577 | 8.359730320115089 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 30 | A34 | A | APN | APN A1004 | 0.0471 | 0.5170 | 1.4510375598171188 | 10.639600029516723 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 31 | A35 | A | APN | APN A1004 | 0.0454 | 1.4749 | 1.4510375598171104 | 2.626430668421563 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 32 | A36 | A | APN | APN A1004 | 0.0449 | 1.8907 | 1.4510375598171046 | 2.9554873196604357 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 33 | A37 | U | UPN | TPN A1005 | 0.0459 | 1.8715 | 1.4818512071054653 | 10.08251774169398 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 34 | A38 | A | APN | APN A1004 | 0.0459 | 0.9383 | 1.451037559817114 | 2.568777495369462 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 35 | A39 | G | GPN | GPN A1001 | 0.0505 | 1.5129 | 1.46937537749888 | 5.748951391407597 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 36 | A40 | G | GPN | GPN A1001 | 0.0500 | 0.4326 | 1.469375377498898 | 8.88103625257672 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 37 | A41 | A | APN | APN A1004 | 0.0457 | 0.5645 | 1.4510375598171066 | 8.419453234339695 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 38 | A42 | C | CPN | CPN A1003 | 0.0433 | 0.7080 | 1.47190794549116 | 8.871677177669143 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 39 | A43 | A | APN | APN A1004 | 0.0451 | 0.2838 | 1.4510375598171152 | 8.142335700615513 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 40 | A44 | A | APN | APN A1004 | 0.0453 | 0.7300 | 1.4510375598171095 | 8.154570236863993 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 41 | A45 | A | APN | APN A1004 | 0.0464 | 0.5444 | 1.4510375598171192 | 8.505789652658336 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 42 | A46 | A | APN | APN A1004 | 0.0456 | 0.3725 | 1.4510375598171208 | 8.376212098446082 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 43 | A47 | A | APN | APN A1004 | 0.0448 | 0.3770 | 1.4510375598171195 | 7.146679811430424 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 44 | A48 | G | GPN | GPN A1001 | 0.0504 | 0.3897 | 1.4693753774988776 | 6.746427286170988 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 45 | A49 | G | GPN | GPN A1001 | 0.0500 | 0.2805 | 1.4693753774988818 | 6.900808134191252 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 46 | A50 | G | GPN | GPN A1001 | 0.0503 | 0.3524 | 1.4693753774988885 | 8.941334926371411 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 47 | A51 | A | APN | APN A1004 | 0.0451 | 0.3765 | 1.4510375598170828 | 7.888905044342387 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 48 | A52 | G | GPN | GPN A1001 | 0.0498 | 0.3310 | 1.4693753774988882 | 11.12630995627211 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 49 | A53 | A | APN | APN A1004 | 0.0459 | 0.9678 | 1.4510375598171081 | 10.524336179621432 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 50 | A54 | G | GPN | GPN A1001 | 0.0499 | 2.4464 | 1.4693753774988922 | 5.211527700660191 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 51 | A55 | G | GPN | GPN A1001 | 0.0503 | 0.5208 | 1.4693753774989053 | 8.4114580890862 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 52 | A56 | U | UPN | TPN A1005 | 0.0440 | 0.3694 | 1.4818512071055003 | 7.098688773548693 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 53 | A57 | G | GPN | GPN A1001 | 0.0507 | 0.5983 | 1.4693753774988807 | 8.33328512529019 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 54 | A58 | A | APN | APN A1004 | 0.0450 | 0.5346 | 1.4510375598171006 | 8.659846360885494 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 55 | A59 | A | APN | APN A1004 | 0.0454 | 0.6316 | 1.4510375598171081 | 7.140148338358503 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 56 | A60 | G | GPN | GPN A1001 | 0.0496 | 0.5356 | 1.4693753774988974 | 8.71471249071685 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 57 | A61 | A | APN | APN A1004 | 0.0446 | 0.1417 | 1.4510375598171181 | 4.187029803533726 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 58 | A62 | A | APN | APN A1004 | 0.0456 | 2.4367 | 1.4510375598171357 | 5.722366010898959 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 59 | A63 | U | UPN | TPN A1005 | 0.0442 | 2.0141 | 1.4818512071054994 | 5.66881268128502 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 60 | A64 | A | APN | APN A1004 | 0.0473 | 2.4524 | 1.451037559817101 | 8.48825462737109 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 61 | A65 | C | CPN | CPN A1003 | 0.0458 | 0.3867 | 1.4719079454911668 | 5.686052955665084 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 62 | A66 | G | GPN | GPN A1001 | 0.0497 | 0.4500 | 1.4693753774988993 | 8.276444098579288 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 63 | A67 | A | APN | APN A1004 | 0.0451 | 1.9042 | 1.4510375598170964 | 7.550085838409057 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 64 | A68 | C | CPN | CPN A1003 | 0.0437 | 0.6757 | 1.4719079454911488 | 8.755801332425825 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 65 | A69 | C | CPN | CPN A1003 | 0.0446 | 0.6399 | 1.4719079454911912 | 8.588454023535883 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 66 | A70 | A | APN | APN A1004 | 0.0439 | 0.5421 | 1.4510375598171306 | 7.7381638656348954 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 67 | A71 | C | CPN | CPN A1003 | 0.0452 | 0.4042 | 1.4719079454911619 | 8.1397113714741 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 68 | A72 | C | CPN | CPN A1003 | 0.0445 | 0.2810 | 1.4719079454911614 | 8.4603723094411 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 69 | A73 | U | UPN | TPN A1005 | 0.0448 | 0.2358 | 1.4818512071054704 | 7.953167462926235 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 70 | A74 | A | APN | APN A1004 | 0.0442 | 0.3393 | 1.4510375598170904 | 6.940038526505413 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 71 | A75 | G | GPN | GPN A1001 | 0.0503 | 0.4724 | 1.469375377498902 | 6.85248738332956 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 72 | A76 | G | GPN | GPN A1001 | 0.0497 | 0.4225 | 1.4693753774989107 | 9.008774460207517 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 73 | A77 | C | CPN | CPN A1003 | 0.0431 | 0.4599 | 1.4719079454911759 | 9.26804259585336 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 74 | A78 | U | UPN | TPN A1005 | 0.0465 | 0.5959 | 1.4818512071054941 | 8.844248789518947 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 75 | A79 | C | CPN | CPN A1003 | 0.0436 | 1.2321 | 1.4719079454911634 | 5.498755988313359 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 76 | A80 | G | GPN | GPN A1001 | 0.0512 | 0.7641 | 1.4693753774988667 | 9.661828582167107 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 77 | A81 | A | APN | APN A1004 | 0.0462 | 2.4371 | 1.4510375598171281 | 5.770797461499993 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 78 | A82 | A | APN | APN A1004 | 0.0464 | 0.7256 | 1.4510375598171095 | 7.867740483337398 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 79 | A83 | A | APN | APN A1004 | 0.0460 | 0.8659 | 1.4510375598171061 | 6.4563153093317025 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 80 | A84 | G | GPN | GPN A1001 | 0.0511 | 0.9831 | 1.469375377498886 | 7.905052642445921 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 81 | A85 | A | APN | APN A1004 | 0.0482 | 0.2772 | 1.4510375598171277 | 6.731336002988595 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 82 | A86 | G | GPN | GPN A1001 | 0.0504 | 0.4749 | 1.469375377498883 | 8.23944814406518 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 83 | A87 | C | CPN | CPN A1003 | 0.0441 | 0.4146 | 1.471907945491155 | 8.323024757793766 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 84 | A88 | C | CPN | CPN A1003 | 0.0441 | 0.3820 | 1.4719079454911574 | 9.009608145682057 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 85 | A89 | U | UPN | TPN A1005 | 0.0441 | 0.4437 | 1.4818512071054648 | 8.148559530517334 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 86 | A90 | A | APN | APN A1004 | 0.0459 | 1.0818 | 1.4510375598171035 | 11.753869386322794 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 87 | A91 | A | APN | APN A1004 | 0.0463 | 0.3809 | 1.4510375598171061 | 5.324108478457909 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 88 | A92 | A | APN | APN A1004 | 0.0448 | 0.7130 | 1.4510375598171155 | 5.331204393025748 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 89 | A93 | A | APN | APN A1004 | 0.0444 | 0.8100 | 1.4510375598171157 | 9.054732723673572 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 90 | A94 | C | CPN | CPN A1003 | 0.0448 | 0.5306 | 1.4719079454911896 | 9.025109193199684 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 91 | A95 | A | APN | APN A1004 | 0.0453 | 0.6004 | 1.4510375598171312 | 9.197485678728635 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 92 | A96 | U | UPN | TPN A1005 | 0.0446 | 0.6181 | 1.4818512071054926 | 8.591033899627933 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 93 | A97 | A | APN | APN A1004 | 0.0449 | 0.6869 | 1.4510375598171346 | 8.127700320510554 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 94 | A98 | C | CPN | CPN A1003 | 0.0445 | 0.4265 | 1.471907945491159 | 8.653897294612849 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 95 | A99 | C | CPN | CPN A1003 | 0.0448 | 0.4663 | 1.4719079454911623 | 8.69979711060132 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 96 | A100 | U | UPN | TPN A1005 | 0.0444 | 0.2402 | 1.4818512071054664 | 8.41249602787566 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 97 | A101 | U | UPN | TPN A1005 | 0.0445 | 0.4559 | 1.4818512071055048 | 8.703690859487448 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 98 | A102 | U | UPN | TPN A1005 | 0.0441 | 0.6504 | 1.4818512071054832 | 10.169130496315551 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 99 | A103 | C | CPN | CPN A1003 | 0.0452 | 0.8169 | 1.4719079454911406 | 4.017614086582096 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 100 | A104 | C | CPN | CPN A1003 | 0.0438 | 1.1639 | 1.4719079454911879 | 8.61379900065106 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 101 | A105 | U | UPN | TPN A1005 | 0.0451 | 0.3541 | 1.4818512071054706 | 6.348740761433492 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 102 | A106 | G | GPN | GPN A1001 | 0.0492 | 0.5023 | 1.4693753774988996 | 6.839864705790932 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 103 | A107 | G | GPN | GPN A1001 | 0.0499 | 0.4219 | 1.4693753774988993 | 9.810677609368414 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 104 | A108 | A | APN | APN A1004 | 0.0467 | 0.5032 | 1.451037559817122 | 8.297951297770858 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 105 | A109 | U | UPN | TPN A1005 | 0.0437 | 0.2720 | 1.4818512071054764 | 9.39672207264948 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 106 | A110 | U | UPN | TPN A1005 | 0.0453 | 1.2408 | 1.4818512071054917 | 2.211610334224769 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 107 | A111 | C | CPN | CPN A1003 | 0.0435 | 0.2762 | 1.471907945491153 | 7.6059248229181255 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 108 | A112 | C | CPN | CPN A1003 | 0.0431 | 1.5659 | 1.4719079454911599 | NA | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 109 | A115 | U | UPN | TPN A1005 | 0.0438 | 1.5652 | 1.4818512071055054 | 5.30937073467362 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 110 | A116 | G | GPN | GPN A1001 | 0.0509 | 0.7731 | 1.4693753774988831 | 7.870521617412554 | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |
| 111 | A117 | C | CPN | CPN A1003 | 0.0430 | 1.5656 | 1.4719079454911568 | NA | none | exact base-class donor; RNA base-frame placement; bounded hybrid smoothing applied |

---

## Interpretation

Correct description:

> a PNA-like computational candidate generated by RNA base-frame guidance plus bounded PNA linkage smoothing.

Incorrect description:

> a solved, physically validated, RNA-fold-preserving PNA analog.

The classification should be interpreted conservatively. If `C′(i)→N1′(i+1)` remains failed while the visual model is not tangled, that is still valuable: it indicates where PNA resists RNA-informed conversion.
