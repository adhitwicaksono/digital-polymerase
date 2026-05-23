# RNA → PNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 008A.1  
**Method:** PNA chimaera-guided pseudopeptide-backbone reconstruction  
**Status:** Experimental candidate, not physically validated  
**PNA chain-continuity status:** `C′(i)→N1′(i+1) PASS`  
**Base-attachment status:** `PASS`  
**PNA backbone status:** `C7′→N4′ PASS`, `C′→O1′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- PNA template PDB: `/mnt/data/3mbs_PNA-1mer-8.pdb`
- Output PDB: `/mnt/data/pna_prototype_008A1_outputs/converted_pna_8t5o-HH-typeI-111mer-full_auto_008A1.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- PNA template base-class sequence: `GGCAUGCC`
- Source residue count: `111`
- Usable template residue count: `8`
- Converted residues: `111`

---

## Why PNA Is the Chimaera

PNA is not a sugar-modified nucleic acid. It abandons the sugar-phosphate backbone and uses a pseudopeptide backbone.

The uploaded template uses PNA-like residues:

```text
APN
TPN
GPN
CPN
```

Important PNA scaffold atoms include:

```text
C8'
C7'
O7'
N4'
C3'
C2'
N1'
C5'
C'
O1'
```

Observed linkage:

```text
C′(i) → N1′(i+1)
```

Observed base attachment:

```text
C8′ → glycosidic N
```

---

## Method Summary

Prototype 008A.1 performs PNA chimaera-guided pseudopeptide-backbone reconstruction:

1. infer source RNA base identity
2. select a PNA template residue by base class
3. place the PNA pseudopeptide scaffold using neighboring RNA `C1′` positions as a guide
4. enforce PNA `C′(i)→N1′(i+1)` continuity using suffix linkage correction
5. attach the source RNA base to PNA `C8′`
6. export a PNA-like candidate PDB
7. validate PNA-specific backbone and base-attachment geometry

---

## Alignment / Correction Summary

- Mean guide RMSD: `1.5039 Å`
- Maximum guide RMSD: `5.2815 Å`
- Mean suffix-linkage shift: `173.2061 Å`
- Maximum suffix-linkage shift: `345.4594 Å`
- Mean base shift: `15.9654 Å`
- Maximum base shift: `29.4084 Å`
- Mean C8′→glycosidic N distance: `1.4627 Å`
- Mean C′(i)→N1′(i+1) distance: `1.3400 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| PNA C'(i)→N1'(i+1) | 109 | 0 | 0 | 1.340 | 1.340 | 1.340 | 1.15–1.60 | PASS |
| C8'→glycosidic N | 111 | 0 | 0 | 1.463 | 1.444 | 1.482 | 1.25–1.75 | PASS |
| C8'→C7' | 111 | 0 | 0 | 1.530 | 1.504 | 1.552 | 1.30–1.80 | PASS |
| C7'→O7' | 111 | 0 | 0 | 1.236 | 1.212 | 1.258 | 1.10–1.40 | PASS |
| C7'→N4' | 111 | 0 | 0 | 1.334 | 1.317 | 1.346 | 1.15–1.55 | PASS |
| N4'→C3' | 111 | 0 | 0 | 1.482 | 1.457 | 1.496 | 1.25–1.75 | PASS |
| C3'→C2' | 111 | 0 | 0 | 1.525 | 1.484 | 1.553 | 1.25–1.85 | PASS |
| C2'→N1' | 111 | 0 | 0 | 1.475 | 1.457 | 1.499 | 1.20–1.75 | PASS |
| N4'→C5' | 111 | 0 | 0 | 1.479 | 1.468 | 1.487 | 1.25–1.75 | PASS |
| C5'→C' | 111 | 0 | 0 | 1.506 | 1.467 | 1.538 | 1.25–1.85 | PASS |
| C'→O1' | 111 | 0 | 0 | 1.243 | 1.231 | 1.254 | 1.10–1.40 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Guide RMSD (Å) | Suffix shift (Å) | Base shift (Å) | C8′–N (Å) | C′–next N1′ (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | A5 | G | GPN | GPN A1001 | 0.0683 | 0.0000 | 0.0635 | 1.4693753774988956 | 1.3399999999999856 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 2 | A6 | G | GPN | GPN A1002 | 0.5648 | 0.0151 | 0.7381 | 1.44402527678709 | 1.3400000000000045 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 3 | A7 | U | UPN | TPN A1005 | 0.3196 | 4.0619 | 4.1414 | 1.4818512071054921 | 1.3400000000000012 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 4 | A8 | G | GPN | GPN A1006 | 0.7510 | 7.5985 | 2.0104 | 1.4620075239204526 | 1.3400000000000047 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 5 | A9 | C | CPN | CPN A1003 | 0.8733 | 11.8863 | 4.1079 | 1.4719079454911628 | 1.339999999999998 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 6 | A10 | A | APN | APN A1004 | 0.9839 | 12.4107 | 5.4124 | 1.4510375598171206 | 1.340000000000001 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 7 | A11 | G | GPN | GPN A1001 | 4.6526 | 12.8101 | 2.9733 | 1.469375377498879 | 1.3399999999999992 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 8 | A12 | G | GPN | GPN A1002 | 0.6901 | 17.2552 | 5.9486 | 1.4440252767870791 | 1.3399999999999885 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 9 | A13 | U | UPN | TPN A1005 | 0.4195 | 18.3042 | 4.9287 | 1.4818512071055 | 1.3400000000000047 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 10 | A14 | A | APN | APN A1004 | 1.0554 | 18.6054 | 4.6200 | 1.4510375598171041 | 1.3399999999999925 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 11 | A15 | C | CPN | CPN A1007 | 3.1184 | 23.0814 | 8.2533 | 1.4654695493254004 | 1.340000000000001 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 12 | A16 | A | APN | APN A1004 | 0.8736 | 27.5589 | 8.5447 | 1.451037559817114 | 1.3399999999999985 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 13 | A17 | U | UPN | TPN A1005 | 0.3197 | 30.5118 | 6.0541 | 1.4818512071054921 | 1.3400000000000025 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 14 | A18 | C | CPN | CPN A1008 | 4.7980 | 31.1373 | 5.8985 | 1.4691477121106602 | 1.340000000000007 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 15 | A19 | C | CPN | CPN A1003 | 0.5952 | 38.0450 | 4.5204 | 1.4719079454911526 | 1.3400000000000045 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 16 | A20 | A | APN | APN A1004 | 0.4439 | 39.7161 | 5.8912 | 1.4510375598171061 | 1.3399999999999932 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 17 | A21 | G | GPN | GPN A1006 | 0.6539 | 43.1306 | 7.7838 | 1.4620075239204615 | 1.3399999999999959 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 18 | A22 | C | CPN | CPN A1007 | 1.1738 | 47.3812 | 9.0906 | 1.465469549325398 | 1.3400000000000036 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 19 | A23 | U | UPN | TPN A1005 | 1.0240 | 52.6274 | 6.2544 | 1.4818512071054983 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 20 | A24 | G | GPN | GPN A1001 | 2.8390 | 57.2998 | 9.9488 | 1.469375377498882 | 1.3400000000000094 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 21 | A25 | A | APN | APN A1004 | 1.6555 | 61.4259 | 13.0275 | 1.4510375598171092 | 1.3399999999999939 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 22 | A26 | U | UPN | TPN A1005 | 3.0273 | 63.8954 | 11.4128 | 1.481851207105487 | 1.3400000000000025 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 23 | A27 | G | GPN | GPN A1002 | 2.0334 | 66.5030 | 9.7994 | 1.4440252767870632 | 1.339999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 24 | A28 | A | APN | APN A1004 | 1.7628 | 71.3682 | 16.6841 | 1.451037559817113 | 1.3399999999999952 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 25 | A29 | G | GPN | GPN A1006 | 0.2556 | 74.2000 | 15.3134 | 1.4620075239204462 | 1.3400000000000147 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 26 | A30 | U | UPN | TPN A1005 | 0.4676 | 77.1645 | 16.2099 | 1.4818512071054897 | 1.3400000000000096 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 27 | A31 | C | CPN | CPN A1008 | 4.6492 | 77.3973 | 14.2364 | 1.4691477121106593 | 1.340000000000004 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 28 | A32 | C | CPN | CPN A1003 | 0.4808 | 83.1086 | 11.7338 | 1.4719079454911608 | 1.34 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 29 | A33 | C | CPN | CPN A1007 | 0.6756 | 83.6292 | 10.7981 | 1.465469549325401 | 1.3399999999999976 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 30 | A34 | A | APN | APN A1004 | 1.2665 | 86.4144 | 10.3332 | 1.4510375598171064 | 1.340000000000006 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 31 | A35 | A | APN | APN A1004 | 2.0434 | 90.4984 | 10.6523 | 1.4510375598171084 | 1.34 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 32 | A36 | A | APN | APN A1004 | 2.8880 | 92.7512 | 5.9717 | 1.4510375598171095 | 1.3400000000000032 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 33 | A37 | U | UPN | TPN A1005 | 1.2717 | 97.5946 | 13.7661 | 1.4818512071054863 | 1.3400000000000039 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 34 | A38 | A | APN | APN A1004 | 2.2027 | 100.0096 | 9.7856 | 1.4510375598171195 | 1.3399999999999987 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 35 | A39 | G | GPN | GPN A1001 | 5.1794 | 108.9191 | 15.6561 | 1.4693753774988825 | 1.3399999999999996 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 36 | A40 | G | GPN | GPN A1002 | 0.5586 | 113.3508 | 18.2994 | 1.4440252767870623 | 1.3399999999999899 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 37 | A41 | A | APN | APN A1004 | 0.5979 | 113.9856 | 19.0773 | 1.4510375598171183 | 1.3400000000000047 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 38 | A42 | C | CPN | CPN A1008 | 4.1569 | 115.5961 | 15.4307 | 1.4691477121106664 | 1.3400000000000052 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 39 | A43 | A | APN | APN A1004 | 0.4944 | 124.4505 | 12.0678 | 1.451037559817104 | 1.3399999999999972 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 40 | A44 | A | APN | APN A1004 | 0.8159 | 129.5024 | 13.9693 | 1.4510375598171048 | 1.3399999999999994 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 41 | A45 | A | APN | APN A1004 | 0.5321 | 130.6618 | 12.6622 | 1.4510375598170995 | 1.3399999999999899 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 42 | A46 | A | APN | APN A1004 | 0.3350 | 131.3109 | 11.9498 | 1.4510375598171001 | 1.3399999999999899 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 43 | A47 | A | APN | APN A1004 | 0.4423 | 131.7857 | 11.7055 | 1.4510375598171106 | 1.3399999999999903 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 44 | A48 | G | GPN | GPN A1006 | 0.2293 | 133.4764 | 12.0379 | 1.46200752392046 | 1.3400000000000005 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 45 | A49 | G | GPN | GPN A1001 | 4.6190 | 133.6899 | 13.5775 | 1.4693753774988805 | 1.3400000000000034 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 46 | A50 | G | GPN | GPN A1002 | 0.4632 | 140.7114 | 18.1394 | 1.4440252767870811 | 1.3400000000000085 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 47 | A51 | A | APN | APN A1004 | 0.4211 | 141.9896 | 18.7974 | 1.4510375598170993 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 48 | A52 | G | GPN | GPN A1006 | 1.1412 | 146.0404 | 17.7948 | 1.462007523920458 | 1.3400000000000032 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 49 | A53 | A | APN | APN A1004 | 2.3096 | 149.4364 | 16.0938 | 1.4510375598171106 | 1.3399999999999912 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 50 | A54 | G | GPN | GPN A1001 | 4.1873 | 157.4516 | 24.2458 | 1.4693753774988951 | 1.3400000000000085 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 51 | A55 | G | GPN | GPN A1002 | 0.5878 | 159.1461 | 25.5366 | 1.4440252767870827 | 1.339999999999988 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 52 | A56 | U | UPN | TPN A1005 | 0.2722 | 161.6142 | 26.2069 | 1.4818512071054897 | 1.3400000000000116 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 53 | A57 | G | GPN | GPN A1006 | 0.3047 | 164.2793 | 25.1943 | 1.462007523920443 | 1.3400000000000025 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 54 | A58 | A | APN | APN A1004 | 0.6528 | 166.8171 | 26.3694 | 1.4510375598171044 | 1.3400000000000098 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 55 | A59 | A | APN | APN A1004 | 0.6444 | 168.0229 | 24.7555 | 1.4510375598171135 | 1.3399999999999963 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 56 | A60 | G | GPN | GPN A1001 | 4.2303 | 169.9339 | 24.6051 | 1.469375377498886 | 1.3399999999999888 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 57 | A61 | A | APN | APN A1004 | 1.2743 | 176.4701 | 21.5598 | 1.4510375598171081 | 1.340000000000008 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 58 | A62 | A | APN | APN A1004 | 3.2588 | 179.5396 | 15.6373 | 1.4510375598171084 | 1.3399999999999868 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 59 | A63 | U | UPN | TPN A1005 | 1.9256 | 184.8531 | 23.9393 | 1.4818512071055066 | 1.3400000000000087 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 60 | A64 | A | APN | APN A1004 | 2.8788 | 187.6671 | 24.1612 | 1.4510375598171075 | 1.3399999999999879 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 61 | A65 | C | CPN | CPN A1003 | 1.1171 | 192.2865 | 21.3170 | 1.4719079454911488 | 1.3399999999999916 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 62 | A66 | G | GPN | GPN A1002 | 1.6177 | 196.6903 | 21.4674 | 1.444025276787084 | 1.3400000000000074 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 63 | A67 | A | APN | APN A1004 | 1.3674 | 198.7376 | 20.5419 | 1.4510375598171237 | 1.33999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 64 | A68 | C | CPN | CPN A1007 | 0.7585 | 200.4823 | 22.1255 | 1.4654695493254137 | 1.339999999999993 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 65 | A69 | C | CPN | CPN A1008 | 4.6238 | 202.3901 | 21.4649 | 1.4691477121106797 | 1.3400000000000138 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 66 | A70 | A | APN | APN A1004 | 0.4322 | 208.5751 | 26.8391 | 1.4510375598171115 | 1.3400000000000116 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 67 | A71 | C | CPN | CPN A1003 | 0.3030 | 210.2895 | 25.8581 | 1.4719079454911554 | 1.3400000000000094 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 68 | A72 | C | CPN | CPN A1007 | 0.4999 | 210.7134 | 26.3065 | 1.465469549325408 | 1.3400000000000047 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 69 | A73 | U | UPN | TPN A1005 | 0.4219 | 214.3354 | 22.7232 | 1.4818512071055023 | 1.3399999999999952 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 70 | A74 | A | APN | APN A1004 | 0.3941 | 216.6439 | 24.7401 | 1.4510375598171197 | 1.3400000000000003 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 71 | A75 | G | GPN | GPN A1006 | 0.2907 | 217.8957 | 24.2058 | 1.462007523920453 | 1.3399999999999845 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 72 | A76 | G | GPN | GPN A1001 | 4.8716 | 223.1669 | 23.1191 | 1.4693753774988976 | 1.339999999999996 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 73 | A77 | C | CPN | CPN A1008 | 4.8154 | 226.3726 | 23.3985 | 1.4691477121106642 | 1.3399999999999854 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 74 | A78 | U | UPN | TPN A1005 | 0.6792 | 230.8077 | 23.5620 | 1.481851207105499 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 75 | A79 | C | CPN | CPN A1003 | 0.9292 | 231.5188 | 24.8476 | 1.471907945491156 | 1.3400000000000065 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 76 | A80 | G | GPN | GPN A1002 | 0.8172 | 232.8048 | 24.2675 | 1.4440252767870647 | 1.3400000000000083 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 77 | A81 | A | APN | APN A1004 | 2.1218 | 237.5379 | 29.4084 | 1.4510375598171148 | 1.3400000000000043 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 78 | A82 | A | APN | APN A1004 | 0.6368 | 240.5228 | 24.6914 | 1.4510375598171055 | 1.3399999999999908 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 79 | A83 | A | APN | APN A1004 | 1.4303 | 244.0043 | 26.5685 | 1.4510375598171164 | 1.3399999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 80 | A84 | G | GPN | GPN A1006 | 0.5789 | 248.3372 | 23.8495 | 1.4620075239204389 | 1.3399999999999996 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 81 | A85 | A | APN | APN A1004 | 0.5541 | 253.3752 | 26.7743 | 1.451037559817105 | 1.3400000000000034 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 82 | A86 | G | GPN | GPN A1001 | 4.4934 | 258.1203 | 25.7575 | 1.469375377498881 | 1.3399999999999925 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 83 | A87 | C | CPN | CPN A1007 | 0.4664 | 261.7446 | 23.0738 | 1.4654695493254055 | 1.3399999999999934 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 84 | A88 | C | CPN | CPN A1008 | 4.7837 | 263.1994 | 22.0471 | 1.4691477121106569 | 1.3400000000000019 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 85 | A89 | U | UPN | TPN A1005 | 0.4519 | 271.5004 | 21.5537 | 1.4818512071054948 | 1.3399999999999983 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 86 | A90 | A | APN | APN A1004 | 2.2868 | 274.3688 | 23.3289 | 1.4510375598171124 | 1.3400000000000092 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 87 | A91 | A | APN | APN A1004 | 2.4583 | 277.5989 | 17.7607 | 1.4510375598171157 | 1.3399999999999932 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 88 | A92 | A | APN | APN A1004 | 1.0595 | 282.1722 | 20.0910 | 1.4510375598171188 | 1.3399999999999948 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 89 | A93 | A | APN | APN A1004 | 1.0044 | 286.8020 | 16.9986 | 1.4510375598171097 | 1.340000000000012 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 90 | A94 | C | CPN | CPN A1003 | 0.4350 | 289.0838 | 18.2357 | 1.4719079454911568 | 1.3400000000000032 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 91 | A95 | A | APN | APN A1004 | 0.5495 | 290.4088 | 17.3076 | 1.451037559817111 | 1.339999999999998 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 92 | A96 | U | UPN | TPN A1005 | 0.4367 | 293.7584 | 20.8103 | 1.4818512071055037 | 1.340000000000004 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 93 | A97 | A | APN | APN A1004 | 0.6185 | 294.6601 | 21.0719 | 1.451037559817116 | 1.3399999999999996 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 94 | A98 | C | CPN | CPN A1007 | 0.5667 | 296.5734 | 21.8781 | 1.4654695493254055 | 1.33999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 95 | A99 | C | CPN | CPN A1008 | 4.5443 | 299.6984 | 17.2050 | 1.4691477121106697 | 1.3399999999999823 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 96 | A100 | U | UPN | TPN A1005 | 0.3319 | 306.8684 | 13.9103 | 1.481851207105505 | 1.3400000000000056 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 97 | A101 | U | UPN | TPN A1005 | 0.4137 | 308.5905 | 13.0154 | 1.481851207105488 | 1.3400000000000063 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 98 | A102 | U | UPN | TPN A1005 | 0.8052 | 309.6976 | 12.2885 | 1.4818512071054915 | 1.340000000000005 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 99 | A103 | C | CPN | CPN A1003 | 1.8507 | 313.8916 | 14.8902 | 1.4719079454911475 | 1.3400000000000005 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 100 | A104 | C | CPN | CPN A1007 | 1.6706 | 317.1979 | 10.1358 | 1.4654695493253957 | 1.3400000000000147 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 101 | A105 | U | UPN | TPN A1005 | 0.3927 | 320.8113 | 13.0139 | 1.4818512071054952 | 1.34 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 102 | A106 | G | GPN | GPN A1002 | 0.7164 | 321.2284 | 12.9921 | 1.4440252767870743 | 1.3399999999999992 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 103 | A107 | G | GPN | GPN A1006 | 0.4344 | 322.4668 | 11.8853 | 1.462007523920459 | 1.3399999999999954 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 104 | A108 | A | APN | APN A1004 | 0.5781 | 323.3835 | 11.2359 | 1.4510375598171161 | 1.3399999999999999 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 105 | A109 | U | UPN | TPN A1005 | 0.5177 | 328.2389 | 14.0196 | 1.4818512071054912 | 1.3400000000000014 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 106 | A110 | U | UPN | TPN A1005 | 1.2502 | 332.4292 | 12.9274 | 1.4818512071054954 | 1.3400000000000136 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 107 | A111 | C | CPN | CPN A1008 | 5.2815 | 337.5334 | 12.8030 | 1.469147712110658 | 1.340000000000002 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 108 | A112 | C | CPN | CPN A1003 | 0.2104 | 338.4271 | 13.2091 | 1.471907945491152 | NA | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 109 | A115 | U | UPN | TPN A1005 | 0.7727 | 338.4271 | 13.1400 | 1.4818512071055012 | 1.3399999999999923 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 110 | A116 | G | GPN | GPN A1001 | 4.5352 | 343.9492 | 14.6416 | 1.4693753774988882 | 1.3399999999999876 | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |
| 111 | A117 | C | CPN | CPN A1007 | 0.3482 | 345.4594 | 16.4793 | 1.4654695493254106 | NA | exact base-class PNA template; PNA chimaera-guided scaffold with suffix linkage correction |

---

## Scientific Interpretation

This output should be interpreted as:

> a PNA-like computational candidate generated by chimaera-guided pseudopeptide-backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready PNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- PNA stereochemistry and peptide-like backbone geometry require expert inspection.
- The suffix-linkage correction prioritizes PNA chain continuity and may increase base shifts.
- Molecular viewers may not render standard nucleic-acid cartoon paths for PNA.
- The output is a candidate geometry only; biological function, stability, binding, or catalytic activity is not implied.
