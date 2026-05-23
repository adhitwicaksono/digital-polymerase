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

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- TNA template PDB: `/mnt/data/6MU5_TNA_13mer.pdb`
- Output PDB: `/mnt/data/tna_prototype_006B4_outputs/converted_tna_8t5o-HH-typeI-111mer-full_auto_006B4.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- TNA template base-class sequence: `GUACGUGAUCGCA`
- Source residue count: `111`
- Template residue count: `13`
- Converted residues: `111`

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

- Mean initial segment RMSD: `0.9595 Å`
- Maximum initial segment RMSD: `1.3923 Å`
- Mean base-transplant RMSD: `0.0987 Å`
- Maximum base-transplant RMSD: `0.3689 Å`
- Mean optimization cost: `0.0058`
- Mean C1′→glycosidic N distance: `1.4477 Å`
- Mean P(i)→O3′(i) distance: `1.6032 Å`
- Mean O2′(i)→P(i+1) distance: `1.5752 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| TNA O2'(i)→P(i+1) | 109 | 0 | 0 | 1.575 | 1.333 | 1.620 | 1.25–1.90 | PASS |
| TNA P(i)→O3'(i) | 111 | 0 | 0 | 1.603 | 1.589 | 1.617 | 1.35–1.90 | PASS |
| C1'→glycosidic N | 111 | 0 | 0 | 1.448 | 1.415 | 1.473 | 1.30–1.75 | PASS |
| C1'→C2' | 111 | 0 | 0 | 1.472 | 1.446 | 1.491 | 1.25–1.90 | PASS |
| C2'→C3' | 111 | 0 | 0 | 1.428 | 1.380 | 1.453 | 1.20–1.90 | PASS |
| C3'→C4' | 111 | 0 | 0 | 1.533 | 1.496 | 1.578 | 1.25–2.00 | PASS |
| C2'→O2' | 111 | 0 | 0 | 1.201 | 1.184 | 1.225 | 1.05–1.65 | PASS |
| C3'→O3' | 111 | 0 | 0 | 1.431 | 1.423 | 1.437 | 1.10–1.75 | PASS |
| C1'→O4' | 111 | 0 | 0 | 1.492 | 1.462 | 1.540 | 1.20–1.85 | PASS |
| C4'→O4' | 111 | 0 | 0 | 1.527 | 1.505 | 1.583 | 1.20–1.95 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base RMSD (Å) | Opt. cost | C1′–N (Å) | P–O3′ (Å) | O2′–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A5 | G | TG | TG T4 | 1.0829 | 0.0575 | 0.0022 | 1.4515805179183228 | 1.5991376764583682 | 1.5994416255464796 | exact base-class TNA template; linkage-optimized |
| 2 | A6 | G | TG | TG T8 | 0.8735 | 0.0394 | 0.0029 | 1.4601102698084198 | 1.5924209696567693 | 1.619726891920255 | exact base-class TNA template; linkage-optimized |
| 3 | A7 | U | TU | TFT T5 | 0.9616 | 0.0685 | 0.0036 | 1.4586521175386655 | 1.603654283659745 | 1.6097709437629797 | exact base-class TNA template; linkage-optimized |
| 4 | A8 | G | TG | TG T10 | 0.7554 | 0.0553 | 0.0041 | 1.4664422934435641 | 1.6100167005033512 | 1.6121570125122784 | exact base-class TNA template; linkage-optimized |
| 5 | A9 | C | TC | TC T7 | 0.9613 | 0.0436 | 0.0057 | 1.4220780569293605 | 1.6102534565261188 | 1.6149406848973233 | exact base-class TNA template; linkage-optimized |
| 6 | A10 | A | FA2 | FA2 T6 | 0.8871 | 0.0790 | 0.0032 | 1.4734669999697907 | 1.616812199542664 | 1.6130841676000156 | exact base-class TNA template; linkage-optimized |
| 7 | A11 | G | TG | TG T14 | 1.3923 | 0.0647 | 0.0158 | 1.4545246646241583 | 1.6014778920996429 | 1.6148579060846349 | exact base-class TNA template; linkage-optimized |
| 8 | A12 | G | TG | TG T4 | 1.1382 | 0.0496 | 0.0075 | 1.4515805179182963 | 1.5993044042269526 | 1.599498926994667 | exact base-class TNA template; linkage-optimized |
| 9 | A13 | U | TU | TFT T9 | 0.8225 | 0.0690 | 0.0022 | 1.453414256156873 | 1.6069804760002697 | 1.6164550246201284 | exact base-class TNA template; linkage-optimized |
| 10 | A14 | A | FA2 | FA2 T11 | 1.0049 | 0.0736 | 0.0034 | 1.446166657062746 | 1.6003231670896274 | 1.3333997191315101 | exact base-class TNA template; linkage-optimized |
| 11 | A15 | C | TC | TC T13 | 1.1090 | 0.2551 | 0.0038 | 1.41496219030758 | 1.5890444060316018 | 1.6008315533722886 | exact base-class TNA template; linkage-optimized |
| 12 | A16 | A | FA2 | FA2 T16 | 0.8105 | 0.0658 | 0.0189 | 1.4475648517423967 | 1.6001948103486001 | 1.580235569050679 | exact base-class TNA template; linkage-optimized |
| 13 | A17 | U | TU | TFT T12 | 0.9382 | 0.0918 | 0.0020 | 1.4586068695848065 | 1.6039344462093996 | 1.6038242726916492 | exact base-class TNA template; linkage-optimized |
| 14 | A18 | C | TC | TC T15 | 1.0741 | 0.0562 | 0.0033 | 1.4149943462784644 | 1.602544435469102 | 1.5890050662509452 | exact base-class TNA template; linkage-optimized |
| 15 | A19 | C | TC | TC T7 | 0.7419 | 0.0450 | 0.0022 | 1.4220780569293736 | 1.610170251899425 | 1.6148673720348015 | exact base-class TNA template; linkage-optimized |
| 16 | A20 | A | FA2 | FA2 T6 | 1.1909 | 0.0685 | 0.0084 | 1.4734669999697991 | 1.6169440639677375 | 1.6131948199246458 | exact base-class TNA template; linkage-optimized |
| 17 | A21 | G | TG | TG T8 | 1.0120 | 0.0408 | 0.0020 | 1.460110269808424 | 1.5923803563785042 | 1.6197141662698906 | exact base-class TNA template; linkage-optimized |
| 18 | A22 | C | TC | TC T13 | 1.0433 | 0.2887 | 0.0045 | 1.4149621903075644 | 1.5891000669598945 | 1.6009328199865929 | exact base-class TNA template; linkage-optimized |
| 19 | A23 | U | TU | TFT T5 | 0.9045 | 0.0700 | 0.0031 | 1.4586521175386586 | 1.603644317378209 | 1.6097943162281891 | exact base-class TNA template; linkage-optimized |
| 20 | A24 | G | TG | TG T10 | 0.9829 | 0.0580 | 0.0019 | 1.4664422934435613 | 1.6099169961284183 | 1.612060484356751 | exact base-class TNA template; linkage-optimized |
| 21 | A25 | A | FA2 | FA2 T11 | 1.0334 | 0.0768 | 0.0030 | 1.4461666570627203 | 1.6003068598889143 | 1.3333923724269452 | exact base-class TNA template; linkage-optimized |
| 22 | A26 | U | TU | TFT T9 | 0.6998 | 0.3245 | 0.0012 | 1.4534142561568522 | 1.606949094719701 | 1.6164387186056826 | exact base-class TNA template; linkage-optimized |
| 23 | A27 | G | TG | TG T14 | 1.0710 | 0.0949 | 0.0026 | 1.4545246646241483 | 1.6010425588481145 | 1.6145240968966006 | exact base-class TNA template; linkage-optimized |
| 24 | A28 | A | FA2 | FA2 T16 | 1.0894 | 0.0744 | 0.0128 | 1.4475648517424116 | 1.6002044164856408 | 1.5801469437039 | exact base-class TNA template; linkage-optimized |
| 25 | A29 | G | TG | TG T4 | 0.7892 | 0.0512 | 0.0038 | 1.4515805179183288 | 1.5992338591913706 | 1.5994535636720686 | exact base-class TNA template; linkage-optimized |
| 26 | A30 | U | TU | TFT T12 | 1.0039 | 0.0819 | 0.0066 | 1.4586068695848056 | 1.6040678399367496 | 1.6039317510245175 | exact base-class TNA template; linkage-optimized |
| 27 | A31 | C | TC | TC T15 | 1.1331 | 0.0696 | 0.0025 | 1.4149943462784706 | 1.6025108413976754 | 1.588977709562894 | exact base-class TNA template; linkage-optimized |
| 28 | A32 | C | TC | TC T7 | 0.9607 | 0.0421 | 0.0064 | 1.4220780569293514 | 1.6102764698619685 | 1.6149744426168267 | exact base-class TNA template; linkage-optimized |
| 29 | A33 | C | TC | TC T13 | 1.0205 | 0.1193 | 0.0021 | 1.4149621903075666 | 1.588976554699322 | 1.6008369281472143 | exact base-class TNA template; linkage-optimized |
| 30 | A34 | A | FA2 | FA2 T6 | 0.9088 | 0.0787 | 0.0023 | 1.4734669999697874 | 1.6167798038220507 | 1.613100299502718 | exact base-class TNA template; linkage-optimized |
| 31 | A35 | A | FA2 | FA2 T11 | 0.5888 | 0.2789 | 0.0014 | 1.4461666570627407 | 1.600324100564028 | 1.3333373879631225 | exact base-class TNA template; linkage-optimized |
| 32 | A36 | A | FA2 | FA2 T16 | 1.0312 | 0.3192 | 0.0456 | 1.4475648517424107 | 1.6002502826369782 | 1.580295564932543 | exact base-class TNA template; linkage-optimized |
| 33 | A37 | U | TU | TFT T5 | 1.0512 | 0.0720 | 0.0074 | 1.4586521175386635 | 1.6037500563673672 | 1.6098791870382847 | exact base-class TNA template; linkage-optimized |
| 34 | A38 | A | FA2 | FA2 T6 | 0.9208 | 0.2829 | 0.0013 | 1.4734669999698071 | 1.6167269853124204 | 1.6130802217680102 | exact base-class TNA template; linkage-optimized |
| 35 | A39 | G | TG | TG T8 | 1.0333 | 0.0389 | 0.0102 | 1.460110269808414 | 1.592609797606733 | 1.6198498166286894 | exact base-class TNA template; linkage-optimized |
| 36 | A40 | G | TG | TG T10 | 0.8690 | 0.0696 | 0.0020 | 1.4664422934435586 | 1.6099334860236842 | 1.612060893683765 | exact base-class TNA template; linkage-optimized |
| 37 | A41 | A | FA2 | FA2 T11 | 0.8553 | 0.0739 | 0.0030 | 1.4461666570627385 | 1.6003382402963144 | 1.3333915603544795 | exact base-class TNA template; linkage-optimized |
| 38 | A42 | C | TC | TC T15 | 1.2235 | 0.0489 | 0.0099 | 1.4149943462784573 | 1.6026812079146198 | 1.5891080430375377 | exact base-class TNA template; linkage-optimized |
| 39 | A43 | A | FA2 | FA2 T16 | 0.8206 | 0.0656 | 0.0196 | 1.4475648517424076 | 1.6002172297665662 | 1.5802428606632901 | exact base-class TNA template; linkage-optimized |
| 40 | A44 | A | FA2 | FA2 T6 | 0.9971 | 0.0761 | 0.0023 | 1.4734669999698058 | 1.6167617485795136 | 1.6130959315459694 | exact base-class TNA template; linkage-optimized |
| 41 | A45 | A | FA2 | FA2 T11 | 0.9202 | 0.0735 | 0.0035 | 1.4461666570627478 | 1.6003345224197896 | 1.3334080164059192 | exact base-class TNA template; linkage-optimized |
| 42 | A46 | A | FA2 | FA2 T16 | 0.8130 | 0.0663 | 0.0182 | 1.4475648517424067 | 1.6001858377323332 | 1.5802268454571158 | exact base-class TNA template; linkage-optimized |
| 43 | A47 | A | FA2 | FA2 T6 | 0.9552 | 0.0789 | 0.0025 | 1.4734669999698038 | 1.6167861479014205 | 1.6131079707643876 | exact base-class TNA template; linkage-optimized |
| 44 | A48 | G | TG | TG T14 | 0.9381 | 0.0927 | 0.0038 | 1.4545246646241543 | 1.6011207598947776 | 1.6145465056028343 | exact base-class TNA template; linkage-optimized |
| 45 | A49 | G | TG | TG T4 | 0.8247 | 0.0560 | 0.0039 | 1.4515805179183032 | 1.5992325410611574 | 1.5994514434416875 | exact base-class TNA template; linkage-optimized |
| 46 | A50 | G | TG | TG T8 | 0.9826 | 0.0405 | 0.0020 | 1.4601102698084303 | 1.5923845771923533 | 1.6197141867914375 | exact base-class TNA template; linkage-optimized |
| 47 | A51 | A | FA2 | FA2 T11 | 0.8775 | 0.0820 | 0.0035 | 1.4461666570627267 | 1.600342990251732 | 1.3334063658895143 | exact base-class TNA template; linkage-optimized |
| 48 | A52 | G | TG | TG T10 | 0.9252 | 0.0700 | 0.0017 | 1.4664422934435717 | 1.609917456809694 | 1.612057389954977 | exact base-class TNA template; linkage-optimized |
| 49 | A53 | A | FA2 | FA2 T16 | 0.7841 | 0.0660 | 0.0175 | 1.4475648517423974 | 1.6001363901337589 | 1.5802179383403363 | exact base-class TNA template; linkage-optimized |
| 50 | A54 | G | TG | TG T14 | 0.9066 | 0.1017 | 0.0021 | 1.4545246646241523 | 1.6010641780220514 | 1.6145152621271197 | exact base-class TNA template; linkage-optimized |
| 51 | A55 | G | TG | TG T4 | 0.7573 | 0.0527 | 0.0037 | 1.451580517918318 | 1.5992335763420187 | 1.5994504626353958 | exact base-class TNA template; linkage-optimized |
| 52 | A56 | U | TU | TFT T9 | 1.0222 | 0.0667 | 0.0045 | 1.4534142561568655 | 1.6070360282240417 | 1.6164795287708598 | exact base-class TNA template; linkage-optimized |
| 53 | A57 | G | TG | TG T8 | 1.0572 | 0.0400 | 0.0060 | 1.4601102698084087 | 1.592505444271619 | 1.619800302768661 | exact base-class TNA template; linkage-optimized |
| 54 | A58 | A | FA2 | FA2 T6 | 0.9776 | 0.0807 | 0.0021 | 1.473466999969791 | 1.6167545253018971 | 1.613089320223588 | exact base-class TNA template; linkage-optimized |
| 55 | A59 | A | FA2 | FA2 T11 | 0.9532 | 0.0743 | 0.0029 | 1.4461666570627363 | 1.6003189313297224 | 1.3333923114253285 | exact base-class TNA template; linkage-optimized |
| 56 | A60 | G | TG | TG T10 | 0.9117 | 0.0705 | 0.0016 | 1.4664422934435488 | 1.6099160919816056 | 1.6120597162182586 | exact base-class TNA template; linkage-optimized |
| 57 | A61 | A | FA2 | FA2 T16 | 0.8231 | 0.0686 | 0.0184 | 1.4475648517423874 | 1.600195979764589 | 1.5802286845663527 | exact base-class TNA template; linkage-optimized |
| 58 | A62 | A | FA2 | FA2 T6 | 0.7602 | 0.2782 | 0.0012 | 1.473466999969808 | 1.616728134796664 | 1.6130812915056876 | exact base-class TNA template; linkage-optimized |
| 59 | A63 | U | TU | TFT T12 | 0.8210 | 0.3052 | 0.0018 | 1.458606869584825 | 1.603934505263367 | 1.6038220366572669 | exact base-class TNA template; linkage-optimized |
| 60 | A64 | A | FA2 | FA2 T11 | 1.0485 | 0.0774 | 0.0024 | 1.4461666570627414 | 1.6002930367975245 | 1.3333775919479292 | exact base-class TNA template; linkage-optimized |
| 61 | A65 | C | TC | TC T7 | 0.7306 | 0.3174 | 0.0022 | 1.4220780569293687 | 1.6101705062239406 | 1.6148776702571488 | exact base-class TNA template; linkage-optimized |
| 62 | A66 | G | TG | TG T14 | 1.0371 | 0.2967 | 0.0052 | 1.4545246646241539 | 1.6011557714529818 | 1.6145919858923177 | exact base-class TNA template; linkage-optimized |
| 63 | A67 | A | FA2 | FA2 T16 | 0.8078 | 0.0675 | 0.0168 | 1.4475648517424073 | 1.6001660277560912 | 1.580213906554939 | exact base-class TNA template; linkage-optimized |
| 64 | A68 | C | TC | TC T13 | 1.0465 | 0.1214 | 0.0021 | 1.4149621903075762 | 1.5889689306711718 | 1.6008347007093662 | exact base-class TNA template; linkage-optimized |
| 65 | A69 | C | TC | TC T15 | 1.0959 | 0.0649 | 0.0027 | 1.4149943462784573 | 1.6025211605578036 | 1.5889856038173396 | exact base-class TNA template; linkage-optimized |
| 66 | A70 | A | FA2 | FA2 T6 | 0.9417 | 0.0832 | 0.0022 | 1.4734669999697945 | 1.6167698669150323 | 1.613093562678464 | exact base-class TNA template; linkage-optimized |
| 67 | A71 | C | TC | TC T7 | 0.8192 | 0.0483 | 0.0026 | 1.4220780569293467 | 1.6101780625264914 | 1.6148798519175258 | exact base-class TNA template; linkage-optimized |
| 68 | A72 | C | TC | TC T13 | 0.9605 | 0.1037 | 0.0028 | 1.4149621903075698 | 1.5890236226632262 | 1.600866653937341 | exact base-class TNA template; linkage-optimized |
| 69 | A73 | U | TU | TFT T5 | 0.8525 | 0.0674 | 0.0030 | 1.458652117538659 | 1.603649518040659 | 1.6097480080001547 | exact base-class TNA template; linkage-optimized |
| 70 | A74 | A | FA2 | FA2 T11 | 0.8936 | 0.0812 | 0.0031 | 1.4461666570627418 | 1.6003351141774187 | 1.3333944120400847 | exact base-class TNA template; linkage-optimized |
| 71 | A75 | G | TG | TG T4 | 0.8056 | 0.0541 | 0.0043 | 1.4515805179183179 | 1.5992464417048033 | 1.5994588558631155 | exact base-class TNA template; linkage-optimized |
| 72 | A76 | G | TG | TG T8 | 1.0895 | 0.0392 | 0.0072 | 1.4601102698084218 | 1.592513480488541 | 1.6197582944640097 | exact base-class TNA template; linkage-optimized |
| 73 | A77 | C | TC | TC T15 | 0.9687 | 0.0490 | 0.0086 | 1.4149943462784447 | 1.6026909049770706 | 1.5891151564038968 | exact base-class TNA template; linkage-optimized |
| 74 | A78 | U | TU | TFT T9 | 1.2477 | 0.0761 | 0.0024 | 1.4534142561568517 | 1.6069726738510735 | 1.6164494820626976 | exact base-class TNA template; linkage-optimized |
| 75 | A79 | C | TC | TC T7 | 0.8645 | 0.0480 | 0.0012 | 1.422078056929353 | 1.610115397382598 | 1.6148553859949322 | exact base-class TNA template; linkage-optimized |
| 76 | A80 | G | TG | TG T10 | 0.9967 | 0.0664 | 0.0021 | 1.4664422934435655 | 1.60992523809357 | 1.612062050585148 | exact base-class TNA template; linkage-optimized |
| 77 | A81 | A | FA2 | FA2 T16 | 1.0007 | 0.0590 | 0.0324 | 1.4475648517423862 | 1.6003002296291464 | 1.5803087455423455 | exact base-class TNA template; linkage-optimized |
| 78 | A82 | A | FA2 | FA2 T6 | 1.1644 | 0.0653 | 0.0085 | 1.4734669999697974 | 1.6170939699628266 | 1.6133907289790583 | exact base-class TNA template; linkage-optimized |
| 79 | A83 | A | FA2 | FA2 T11 | 1.1351 | 0.0919 | 0.0022 | 1.4461666570627252 | 1.6002799123030573 | 1.333369792003152 | exact base-class TNA template; linkage-optimized |
| 80 | A84 | G | TG | TG T14 | 1.3118 | 0.0724 | 0.0081 | 1.4545246646241543 | 1.601178216718559 | 1.6146596753579272 | exact base-class TNA template; linkage-optimized |
| 81 | A85 | A | FA2 | FA2 T16 | 0.8056 | 0.0726 | 0.0162 | 1.4475648517423885 | 1.6001735702932987 | 1.5802111247886899 | exact base-class TNA template; linkage-optimized |
| 82 | A86 | G | TG | TG T4 | 0.8538 | 0.0560 | 0.0035 | 1.451580517918309 | 1.5992184944392966 | 1.5994491071806702 | exact base-class TNA template; linkage-optimized |
| 83 | A87 | C | TC | TC T13 | 0.9627 | 0.1025 | 0.0026 | 1.4149621903075684 | 1.5890131015869828 | 1.6008631573268612 | exact base-class TNA template; linkage-optimized |
| 84 | A88 | C | TC | TC T15 | 1.0595 | 0.0578 | 0.0032 | 1.4149943462784498 | 1.602541323550683 | 1.5890012357383307 | exact base-class TNA template; linkage-optimized |
| 85 | A89 | U | TU | TFT T12 | 0.9231 | 0.0913 | 0.0023 | 1.4586068695848238 | 1.603943538171716 | 1.6038279471243142 | exact base-class TNA template; linkage-optimized |
| 86 | A90 | A | FA2 | FA2 T6 | 1.1500 | 0.0901 | 0.0024 | 1.4734669999697954 | 1.6167347330522042 | 1.6130838873767601 | exact base-class TNA template; linkage-optimized |
| 87 | A91 | A | FA2 | FA2 T11 | 0.8738 | 0.0811 | 0.0038 | 1.4461666570627274 | 1.6003705120167229 | 1.3333672802865986 | exact base-class TNA template; linkage-optimized |
| 88 | A92 | A | FA2 | FA2 T16 | 0.7923 | 0.3223 | 0.0262 | 1.4475648517424051 | 1.6003889085253422 | 1.5803804080152244 | exact base-class TNA template; linkage-optimized |
| 89 | A93 | A | FA2 | FA2 T6 | 0.9378 | 0.0840 | 0.0018 | 1.4734669999697967 | 1.6167447577139107 | 1.613091538072046 | exact base-class TNA template; linkage-optimized |
| 90 | A94 | C | TC | TC T7 | 0.8236 | 0.0489 | 0.0019 | 1.4220780569293643 | 1.610153519270838 | 1.6148643590555625 | exact base-class TNA template; linkage-optimized |
| 91 | A95 | A | FA2 | FA2 T11 | 0.8296 | 0.0748 | 0.0039 | 1.4461666570627218 | 1.6003622961787656 | 1.3334106745676797 | exact base-class TNA template; linkage-optimized |
| 92 | A96 | U | TU | TFT T5 | 1.1933 | 0.0698 | 0.0115 | 1.4586521175386589 | 1.6038222453198556 | 1.609876730792277 | exact base-class TNA template; linkage-optimized |
| 93 | A97 | A | FA2 | FA2 T16 | 0.7984 | 0.0700 | 0.0159 | 1.4475648517424073 | 1.6001727085372668 | 1.5802100137543833 | exact base-class TNA template; linkage-optimized |
| 94 | A98 | C | TC | TC T13 | 1.0210 | 0.1166 | 0.0022 | 1.4149621903075735 | 1.588982401285457 | 1.6008381851457685 | exact base-class TNA template; linkage-optimized |
| 95 | A99 | C | TC | TC T15 | 1.0704 | 0.0584 | 0.0032 | 1.4149943462784538 | 1.602540329046094 | 1.588999436074739 | exact base-class TNA template; linkage-optimized |
| 96 | A100 | U | TU | TFT T9 | 0.7912 | 0.0691 | 0.0030 | 1.4534142561568493 | 1.6070084156839717 | 1.6164661354571466 | exact base-class TNA template; linkage-optimized |
| 97 | A101 | U | TU | TFT T12 | 0.9879 | 0.0950 | 0.0019 | 1.458606869584814 | 1.6039243870437114 | 1.603822451396817 | exact base-class TNA template; linkage-optimized |
| 98 | A102 | U | TU | TFT T5 | 0.9179 | 0.0679 | 0.0028 | 1.4586521175386484 | 1.603635278693616 | 1.6097520471783027 | exact base-class TNA template; linkage-optimized |
| 99 | A103 | C | TC | TC T7 | 0.7794 | 0.3471 | 0.0103 | 1.4220780569293667 | 1.6106515461821895 | 1.615336543350431 | exact base-class TNA template; linkage-optimized |
| 100 | A104 | C | TC | TC T13 | 1.1758 | 0.0890 | 0.0048 | 1.4149621903075722 | 1.589076516743483 | 1.6008936588969331 | exact base-class TNA template; linkage-optimized |
| 101 | A105 | U | TU | TFT T9 | 0.8402 | 0.0711 | 0.0018 | 1.45341425615685 | 1.6069688402551316 | 1.6164418310997086 | exact base-class TNA template; linkage-optimized |
| 102 | A106 | G | TG | TG T8 | 0.7792 | 0.0391 | 0.0033 | 1.46011026980843 | 1.592438214424704 | 1.6197266733578173 | exact base-class TNA template; linkage-optimized |
| 103 | A107 | G | TG | TG T10 | 1.0982 | 0.0635 | 0.0031 | 1.4664422934435724 | 1.6099520895212802 | 1.6120806476162033 | exact base-class TNA template; linkage-optimized |
| 104 | A108 | A | FA2 | FA2 T6 | 1.2397 | 0.0652 | 0.0081 | 1.473466999969804 | 1.616955740111426 | 1.6132462128237406 | exact base-class TNA template; linkage-optimized |
| 105 | A109 | U | TU | TFT T12 | 0.9588 | 0.0887 | 0.0024 | 1.4586068695848189 | 1.603943896510694 | 1.6038315872265785 | exact base-class TNA template; linkage-optimized |
| 106 | A110 | U | TU | TFT T5 | 1.0818 | 0.3689 | 0.0057 | 1.4586521175386455 | 1.60373585546099 | 1.609842577412754 | exact base-class TNA template; linkage-optimized |
| 107 | A111 | C | TC | TC T15 | 1.0361 | 0.0521 | 0.0036 | 1.4149943462784549 | 1.6025512634352082 | 1.589014404653871 | exact base-class TNA template; linkage-optimized |
| 108 | A112 | C | TC | TC T7 | 0.8777 | 0.0503 | 0.0000 | 1.4220780569293765 | 1.610091749396925 | NA | exact base-class TNA template; linkage-optimized |
| 109 | A115 | U | TU | TFT T9 | 0.9232 | 0.0671 | 0.0040 | 1.4534142561568675 | 1.6070389614142577 | 1.6164696833313732 | exact base-class TNA template; linkage-optimized |
| 110 | A116 | G | TG | TG T14 | 1.3086 | 0.0642 | 0.0140 | 1.4545246646241468 | 1.6014163594036777 | 1.614871315505961 | exact base-class TNA template; linkage-optimized |
| 111 | A117 | C | TC | TC T13 | 0.9913 | 0.2719 | 0.0000 | 1.4149621903075635 | 1.5889472233502653 | NA | exact base-class TNA template; linkage-optimized |

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
