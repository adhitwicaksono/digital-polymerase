# RNA → XyNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 005A  
**Requested mode:** `auto`  
**Actual mode:** `chain-preserving`  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`  
**Base-attachment status:** `PASS`  
**XyNA local sugar status:** `C2′→O2′ PASS`, `C1′→O4′ PASS`, `C4′→O4′ PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- XyNA template PDB: `/mnt/data/2n4j_XyNA-8nt.pdb`
- Output PDB: `/mnt/data/xyna_prototype_005A_outputs/converted_xyna_8t5o-HH-typeI-111mer-full_auto_005A.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- XyNA template base-class sequence: `GUGUACAC`
- Source residue count: `111`
- Template residue count: `8`
- Converted residues: `111`
- Base label policy: `preserve`

---

## Method Summary

Prototype 005A supports two RNA → XyNA modes.

### Chain-preserving mode

This is the default in `auto` mode because XyNA is pentose-based and close enough to RNA-like chain geometry for a conservative local sugar replacement strategy.

```text
RNA chain/base framework preserved
+
XyNA-like C2′/O2′ geometry inserted from template
```

### Full-template mode

This mode uses the full XyNA scaffold as donor and transforms RNA bases onto the XyNA template. It is available for short RNA inputs when a full-length XyNA template exists.

---

## Alignment Summary

- Mean local/template anchor RMSD: `0.0781 Å`
- Maximum local/template anchor RMSD: `0.1285 Å`
- Mean C1′→glycosidic N distance: `1.4745 Å`
- Maximum C1′→glycosidic N distance: `1.4804 Å`
- Mean C2′→O2′ distance: `1.4330 Å`
- Maximum C2′→O2′ distance: `1.4343 Å`

---

## Structural Validation

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| C1'→C2' | source RNA | 111 | 0 | 0 | 1.527 | 1.521 | 1.530 | 1.35–1.75 | PASS |
| C1'→C2' | XyNA template | 8 | 0 | 0 | 1.525 | 1.519 | 1.532 | 1.35–1.75 | PASS |
| C1'→C2' | output | 111 | 0 | 0 | 1.511 | 1.494 | 1.543 | 1.35–1.75 | PASS |
| C1'→O4' | source RNA | 111 | 0 | 0 | 1.412 | 1.409 | 1.416 | 1.20–1.60 | PASS |
| C1'→O4' | XyNA template | 8 | 0 | 0 | 1.422 | 1.414 | 1.427 | 1.20–1.60 | PASS |
| C1'→O4' | output | 111 | 0 | 0 | 1.412 | 1.409 | 1.416 | 1.20–1.60 | PASS |
| C1'→glycosidic N | source RNA | 111 | 0 | 0 | 1.474 | 1.462 | 1.480 | 1.30–1.75 | PASS |
| C1'→glycosidic N | XyNA template | 8 | 0 | 0 | 1.476 | 1.473 | 1.481 | 1.30–1.75 | PASS |
| C1'→glycosidic N | output | 111 | 0 | 0 | 1.474 | 1.462 | 1.480 | 1.30–1.75 | PASS |
| C2'→C3' | source RNA | 111 | 0 | 0 | 1.522 | 1.519 | 1.526 | 1.35–1.75 | PASS |
| C2'→C3' | XyNA template | 8 | 0 | 0 | 1.529 | 1.524 | 1.532 | 1.35–1.75 | PASS |
| C2'→C3' | output | 111 | 0 | 0 | 1.521 | 1.496 | 1.539 | 1.35–1.75 | PASS |
| C2'→O2' | source RNA | 111 | 0 | 0 | 1.419 | 1.410 | 1.421 | 1.25–1.60 | PASS |
| C2'→O2' | XyNA template | 8 | 0 | 0 | 1.433 | 1.432 | 1.434 | 1.25–1.60 | PASS |
| C2'→O2' | output | 111 | 0 | 0 | 1.433 | 1.432 | 1.434 | 1.25–1.60 | PASS |
| C3'→C4' | source RNA | 111 | 0 | 0 | 1.520 | 1.515 | 1.529 | 1.35–1.75 | PASS |
| C3'→C4' | XyNA template | 8 | 0 | 0 | 1.528 | 1.526 | 1.530 | 1.35–1.75 | PASS |
| C3'→C4' | output | 111 | 0 | 0 | 1.520 | 1.515 | 1.529 | 1.35–1.75 | PASS |
| C4'→O4' | source RNA | 111 | 0 | 0 | 1.451 | 1.448 | 1.456 | 1.20–1.60 | PASS |
| C4'→O4' | XyNA template | 8 | 0 | 0 | 1.424 | 1.420 | 1.429 | 1.20–1.60 | PASS |
| C4'→O4' | output | 111 | 0 | 0 | 1.451 | 1.448 | 1.456 | 1.20–1.60 | PASS |
| O3'(i)→P(i+1) | source RNA | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.85 | PASS |
| O3'(i)→P(i+1) | XyNA template | 7 | 0 | 0 | 1.615 | 1.611 | 1.619 | 1.40–1.85 | PASS |
| O3'(i)→P(i+1) | output | 109 | 0 | 0 | 1.606 | 1.603 | 1.613 | 1.40–1.85 | PASS |
| P(i)→O5'(i) | source RNA | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | XyNA template | 7 | 1 | 0 | 1.612 | 1.607 | 1.615 | 1.35–1.90 | PASS |
| P(i)→O5'(i) | output | 111 | 0 | 0 | 1.591 | 1.587 | 1.595 | 1.35–1.90 | PASS |

### Worst output O3′–P links

No failed links detected.

### Worst output C2′–O2′ distances

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Mode | Anchor RMSD (Å) | C1′–N (Å) | C2′–O2′ (Å) | Note |
|---:|---|---|---|---|---|---:|---:|---:|---|
| 1 | A5 | G | 8XG | 8XG A1 | chain-preserving | 0.0573 | 1.474960677441961 | 1.4322827933058428 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 2 | A6 | G | 8XG | 8XG A3 | chain-preserving | 0.0833 | 1.4745019498122056 | 1.4331182784404157 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 3 | A7 | U | 8XU | 8XU A2 | chain-preserving | 0.0699 | 1.4804016346924234 | 1.4331437471517183 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 4 | A8 | G | 8XG | 8XG A1 | chain-preserving | 0.0445 | 1.4735979777401813 | 1.432282793305846 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 5 | A9 | C | 8XC | 8XC A6 | chain-preserving | 0.1036 | 1.4791818684664937 | 1.434169097421919 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 6 | A10 | A | 8XA | 8XA A5 | chain-preserving | 0.0904 | 1.4739107842742738 | 1.4316441596989005 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 7 | A11 | G | 8XG | 8XG A3 | chain-preserving | 0.0785 | 1.474010515566282 | 1.4331182784403955 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 8 | A12 | G | 8XG | 8XG A1 | chain-preserving | 0.0458 | 1.4722897133377097 | 1.432282793305863 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 9 | A13 | U | 8XU | 8XU A4 | chain-preserving | 0.1022 | 1.4782127722354255 | 1.4324709421136805 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 10 | A14 | A | 8XA | 8XA A7 | chain-preserving | 0.0614 | 1.474998644067181 | 1.4333059687310359 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 11 | A15 | C | 8XC | 8XC A8 | chain-preserving | 0.0355 | 1.4670013633258676 | 1.4343493298356427 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 12 | A16 | A | 8XA | 8XA A5 | chain-preserving | 0.1018 | 1.4732504878668884 | 1.4316441596989102 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 13 | A17 | U | 8XU | 8XU A2 | chain-preserving | 0.0698 | 1.478048375392349 | 1.4331437471516917 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 14 | A18 | C | 8XC | 8XC A6 | chain-preserving | 0.1228 | 1.4778914033175892 | 1.4341690974219072 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 15 | A19 | C | 8XC | 8XC A8 | chain-preserving | 0.0835 | 1.4788272380504754 | 1.4343493298356735 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 16 | A20 | A | 8XA | 8XA A7 | chain-preserving | 0.0547 | 1.4732606693996906 | 1.4333059687310157 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 17 | A21 | G | 8XG | 8XG A3 | chain-preserving | 0.0956 | 1.4734809126690307 | 1.4331182784403862 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 18 | A22 | C | 8XC | 8XC A6 | chain-preserving | 0.0353 | 1.471298066334618 | 1.4341690974219128 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 19 | A23 | U | 8XU | 8XU A4 | chain-preserving | 0.1099 | 1.4791974175207445 | 1.432470942113676 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 20 | A24 | G | 8XG | 8XG A1 | chain-preserving | 0.0604 | 1.475248453651105 | 1.4322827933058422 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 21 | A25 | A | 8XA | 8XA A5 | chain-preserving | 0.0995 | 1.473989823574107 | 1.4316441596989324 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 22 | A26 | U | 8XU | 8XU A2 | chain-preserving | 0.0370 | 1.4693199107069963 | 1.4331437471516972 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 23 | A27 | G | 8XG | 8XG A3 | chain-preserving | 0.0798 | 1.4747287886252205 | 1.433118278440413 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 24 | A28 | A | 8XA | 8XA A7 | chain-preserving | 0.0572 | 1.474529416458003 | 1.4333059687310377 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 25 | A29 | G | 8XG | 8XG A1 | chain-preserving | 0.0482 | 1.473592209534238 | 1.4322827933058637 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 26 | A30 | U | 8XU | 8XU A4 | chain-preserving | 0.1004 | 1.4790953316132063 | 1.4324709421136665 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 27 | A31 | C | 8XC | 8XC A8 | chain-preserving | 0.0810 | 1.4786165831614457 | 1.4343493298356393 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 28 | A32 | C | 8XC | 8XC A6 | chain-preserving | 0.1255 | 1.4799081052552032 | 1.4341690974219352 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 29 | A33 | C | 8XC | 8XC A8 | chain-preserving | 0.0861 | 1.4775997428261824 | 1.4343493298356422 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 30 | A34 | A | 8XA | 8XA A5 | chain-preserving | 0.1002 | 1.4720441569463842 | 1.43164415969893 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 31 | A35 | A | 8XA | 8XA A7 | chain-preserving | 0.0572 | 1.4641656327069008 | 1.4333059687310314 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 32 | A36 | A | 8XA | 8XA A5 | chain-preserving | 0.0273 | 1.4648713254071135 | 1.4316441596989091 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 33 | A37 | U | 8XU | 8XU A2 | chain-preserving | 0.0717 | 1.4767850215925127 | 1.4331437471516724 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 34 | A38 | A | 8XA | 8XA A7 | chain-preserving | 0.0574 | 1.4630632248812747 | 1.4333059687310377 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 35 | A39 | G | 8XG | 8XG A3 | chain-preserving | 0.0827 | 1.4728020912532696 | 1.4331182784403957 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 36 | A40 | G | 8XG | 8XG A1 | chain-preserving | 0.0603 | 1.4725664670907201 | 1.4322827933058466 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 37 | A41 | A | 8XA | 8XA A5 | chain-preserving | 0.1045 | 1.4734724293314914 | 1.431644159698914 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 38 | A42 | C | 8XC | 8XC A6 | chain-preserving | 0.1148 | 1.4795685181835783 | 1.434169097421916 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 39 | A43 | A | 8XA | 8XA A7 | chain-preserving | 0.0601 | 1.473419492201724 | 1.4333059687310086 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 40 | A44 | A | 8XA | 8XA A5 | chain-preserving | 0.1017 | 1.4739626860948816 | 1.4316441596989142 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 41 | A45 | A | 8XA | 8XA A7 | chain-preserving | 0.0548 | 1.4734955038954325 | 1.4333059687310379 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 42 | A46 | A | 8XA | 8XA A5 | chain-preserving | 0.0961 | 1.4736298721185166 | 1.4316441596988967 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 43 | A47 | A | 8XA | 8XA A7 | chain-preserving | 0.0634 | 1.4728845847519878 | 1.4333059687310423 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 44 | A48 | G | 8XG | 8XG A3 | chain-preserving | 0.0996 | 1.4722747705506811 | 1.4331182784404097 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 45 | A49 | G | 8XG | 8XG A1 | chain-preserving | 0.0613 | 1.4728051466504362 | 1.4322827933058504 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 46 | A50 | G | 8XG | 8XG A3 | chain-preserving | 0.0913 | 1.473873128868293 | 1.4331182784403929 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 47 | A51 | A | 8XA | 8XA A5 | chain-preserving | 0.1073 | 1.4732766203262666 | 1.4316441596989047 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 48 | A52 | G | 8XG | 8XG A1 | chain-preserving | 0.0669 | 1.470948333558994 | 1.4322827933058573 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 49 | A53 | A | 8XA | 8XA A7 | chain-preserving | 0.0531 | 1.4724744479956422 | 1.4333059687310417 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 50 | A54 | G | 8XG | 8XG A3 | chain-preserving | 0.0831 | 1.4732077246607205 | 1.433118278440399 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 51 | A55 | G | 8XG | 8XG A1 | chain-preserving | 0.0463 | 1.4731391651843333 | 1.4322827933058386 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 52 | A56 | U | 8XU | 8XU A4 | chain-preserving | 0.0928 | 1.4786223317669647 | 1.4324709421136625 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 53 | A57 | G | 8XG | 8XG A3 | chain-preserving | 0.0875 | 1.4747399770806997 | 1.433118278440413 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 54 | A58 | A | 8XA | 8XA A5 | chain-preserving | 0.1014 | 1.4735508135113553 | 1.431644159698908 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 55 | A59 | A | 8XA | 8XA A7 | chain-preserving | 0.0599 | 1.4729826882893193 | 1.4333059687310694 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 56 | A60 | G | 8XG | 8XG A1 | chain-preserving | 0.0429 | 1.4718542726778407 | 1.4322827933058397 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 57 | A61 | A | 8XA | 8XA A5 | chain-preserving | 0.1008 | 1.4733122547511617 | 1.4316441596989198 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 58 | A62 | A | 8XA | 8XA A7 | chain-preserving | 0.0521 | 1.4629535194256884 | 1.4333059687310301 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 59 | A63 | U | 8XU | 8XU A2 | chain-preserving | 0.0427 | 1.4691810644028889 | 1.4331437471516832 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 60 | A64 | A | 8XA | 8XA A5 | chain-preserving | 0.0984 | 1.4748996576038642 | 1.4316441596989125 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 61 | A65 | C | 8XC | 8XC A8 | chain-preserving | 0.0315 | 1.4712470900566057 | 1.4343493298356473 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 62 | A66 | G | 8XG | 8XG A3 | chain-preserving | 0.0257 | 1.4621901381147462 | 1.433118278440439 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 63 | A67 | A | 8XA | 8XA A7 | chain-preserving | 0.0551 | 1.473087573771492 | 1.4333059687310503 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 64 | A68 | C | 8XC | 8XC A6 | chain-preserving | 0.1128 | 1.4775364631710464 | 1.4341690974219197 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 65 | A69 | C | 8XC | 8XC A8 | chain-preserving | 0.0823 | 1.4782594494878025 | 1.4343493298356516 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 66 | A70 | A | 8XA | 8XA A5 | chain-preserving | 0.1083 | 1.473578976505849 | 1.4316441596989058 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 67 | A71 | C | 8XC | 8XC A6 | chain-preserving | 0.1285 | 1.47844851110886 | 1.434169097421907 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 68 | A72 | C | 8XC | 8XC A8 | chain-preserving | 0.0880 | 1.4775550751156712 | 1.434349329835652 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 69 | A73 | U | 8XU | 8XU A4 | chain-preserving | 0.1222 | 1.4797469378241543 | 1.4324709421136472 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 70 | A74 | A | 8XA | 8XA A7 | chain-preserving | 0.0675 | 1.4730495578900287 | 1.4333059687310148 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 71 | A75 | G | 8XG | 8XG A1 | chain-preserving | 0.0618 | 1.47440733856016 | 1.432282793305842 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 72 | A76 | G | 8XG | 8XG A3 | chain-preserving | 0.0794 | 1.4732338578786295 | 1.4331182784404097 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 73 | A77 | C | 8XC | 8XC A6 | chain-preserving | 0.1149 | 1.4799070916783905 | 1.4341690974219095 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 74 | A78 | U | 8XU | 8XU A2 | chain-preserving | 0.0551 | 1.477041299354893 | 1.4331437471516724 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 75 | A79 | C | 8XC | 8XC A8 | chain-preserving | 0.0697 | 1.4796144768148174 | 1.4343493298356493 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 76 | A80 | G | 8XG | 8XG A1 | chain-preserving | 0.0496 | 1.4746257152240514 | 1.4322827933058646 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 77 | A81 | A | 8XA | 8XA A5 | chain-preserving | 0.0960 | 1.4747176000848614 | 1.431644159698929 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 78 | A82 | A | 8XA | 8XA A7 | chain-preserving | 0.0526 | 1.474905081691689 | 1.4333059687310448 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 79 | A83 | A | 8XA | 8XA A5 | chain-preserving | 0.1021 | 1.473169711879811 | 1.4316441596989073 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 80 | A84 | G | 8XG | 8XG A3 | chain-preserving | 0.0828 | 1.4742852505536252 | 1.4331182784403915 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 81 | A85 | A | 8XA | 8XA A7 | chain-preserving | 0.0528 | 1.4745070362667112 | 1.4333059687310297 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 82 | A86 | G | 8XG | 8XG A1 | chain-preserving | 0.0545 | 1.4745985894473148 | 1.4322827933058608 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 83 | A87 | C | 8XC | 8XC A6 | chain-preserving | 0.1184 | 1.480354011714775 | 1.4341690974219232 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 84 | A88 | C | 8XC | 8XC A8 | chain-preserving | 0.0803 | 1.479503295028454 | 1.4343493298356524 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 85 | A89 | U | 8XU | 8XU A4 | chain-preserving | 0.1035 | 1.4775066835720192 | 1.4324709421136588 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 86 | A90 | A | 8XA | 8XA A5 | chain-preserving | 0.1067 | 1.4723426910879003 | 1.4316441596988856 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 87 | A91 | A | 8XA | 8XA A7 | chain-preserving | 0.0642 | 1.4755504057808235 | 1.4333059687310261 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 88 | A92 | A | 8XA | 8XA A5 | chain-preserving | 0.0266 | 1.4639170058442368 | 1.4316441596989362 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 89 | A93 | A | 8XA | 8XA A7 | chain-preserving | 0.0633 | 1.4743208605998694 | 1.4333059687310248 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 90 | A94 | C | 8XC | 8XC A6 | chain-preserving | 0.1257 | 1.4789773493870624 | 1.4341690974218957 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 91 | A95 | A | 8XA | 8XA A5 | chain-preserving | 0.1037 | 1.4727572780332832 | 1.4316441596989093 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 92 | A96 | U | 8XU | 8XU A2 | chain-preserving | 0.0667 | 1.4787515004219074 | 1.4331437471517052 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 93 | A97 | A | 8XA | 8XA A7 | chain-preserving | 0.0552 | 1.4730444664028264 | 1.4333059687310223 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 94 | A98 | C | 8XC | 8XC A8 | chain-preserving | 0.0859 | 1.478245243523545 | 1.4343493298356575 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 95 | A99 | C | 8XC | 8XC A6 | chain-preserving | 0.1270 | 1.4793224800563112 | 1.4341690974219155 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 96 | A100 | U | 8XU | 8XU A4 | chain-preserving | 0.1088 | 1.4785049881552503 | 1.4324709421136488 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 97 | A101 | U | 8XU | 8XU A2 | chain-preserving | 0.0730 | 1.478487064535925 | 1.4331437471517081 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 98 | A102 | U | 8XU | 8XU A4 | chain-preserving | 0.1092 | 1.478525278782891 | 1.4324709421136514 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 99 | A103 | C | 8XC | 8XC A8 | chain-preserving | 0.0290 | 1.4706056575438637 | 1.4343493298356584 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 100 | A104 | C | 8XC | 8XC A6 | chain-preserving | 0.1227 | 1.4785269696559493 | 1.4341690974219192 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 101 | A105 | U | 8XU | 8XU A2 | chain-preserving | 0.0696 | 1.4768835431407568 | 1.4331437471517028 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 102 | A106 | G | 8XG | 8XG A3 | chain-preserving | 0.0892 | 1.4728930714753312 | 1.433118278440407 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 103 | A107 | G | 8XG | 8XG A1 | chain-preserving | 0.0460 | 1.472696166899336 | 1.4322827933058595 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 104 | A108 | A | 8XA | 8XA A5 | chain-preserving | 0.0904 | 1.4729334676080972 | 1.431644159698907 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 105 | A109 | U | 8XU | 8XU A4 | chain-preserving | 0.1072 | 1.4789175095318858 | 1.4324709421136372 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 106 | A110 | U | 8XU | 8XU A2 | chain-preserving | 0.0437 | 1.4688978861718056 | 1.4331437471516795 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 107 | A111 | C | 8XC | 8XC A8 | chain-preserving | 0.0735 | 1.4792247969798165 | 1.4343493298356755 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 108 | A112 | C | 8XC | 8XC A6 | chain-preserving | 0.1095 | 1.4788079658968654 | 1.434169097421937 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 109 | A115 | U | 8XU | 8XU A4 | chain-preserving | 0.0986 | 1.4782601259588852 | 1.432470942113665 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 110 | A116 | G | 8XG | 8XG A3 | chain-preserving | 0.0777 | 1.4737496395249927 | 1.4331182784403869 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |
| 111 | A117 | C | 8XC | 8XC A8 | chain-preserving | 0.0358 | 1.4693457727846218 | 1.4343493298356593 | exact base-class XyNA template; RNA chain/base preserved; XyNA C2'/O2' inserted |

---

## Scientific Interpretation

This output should be interpreted as:

> a XyNA-like computational candidate generated by template-guided or chain-preserving local sugar reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed XyNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- XyNA stereochemistry requires expert inspection.
- Chain-preserving mode preserves the RNA chain path and replaces local C2′/O2′ geometry; it is not de novo XyNA folding.
- Biological function, stability, replication, or catalytic activity is not implied.
