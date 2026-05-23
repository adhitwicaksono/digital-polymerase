# RNA → GNA Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 007A  
**Method:** Linkage-optimized GNA reconstruction  
**Status:** Experimental candidate, not physically validated  
**GNA chain-continuity status:** `O2G(i)→P(i+1) PASS`, `P(i)→O3G(i) PASS`  
**Base-attachment status:** `PASS`  
**Local GNA scaffold status:** `C1G→C2G PASS`, `C2G→C3G PASS`, `C2G→O2G PASS`, `C3G→O3G PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/8t5o-HH-typeI-111mer-full.pdb`
- GNA template PDB: `/mnt/data/2xc6-GNA-8nt.pdb`
- Output PDB: `/mnt/data/gna_prototype_007A_outputs/converted_gna_8t5o-HH-typeI-111mer-full_auto_007A.pdb`

---

## Source and Template

- Source RNA sequence: `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC`
- GNA template base-class sequence: `CUCUAGAG`
- Source residue count: `111`
- Template residue count: `8`
- Converted residues: `111`

---

## Why GNA Is Difficult

GNA is not a pentose-like local edit. It uses a much smaller glycerol-like scaffold.

The uploaded GNA template uses atoms such as:

```text
C1G
C2G
C3G
O2G
O3G
```

The observed GNA-like linkage pattern is:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

Therefore, this prototype treats GNA as a linkage-remapped and scaffold-optimized reconstruction problem, not as a simple RNA sugar modification.

---

## Method Summary

Prototype 007A performs linkage-optimized GNA reconstruction:

1. parse source RNA and GNA template PDB files
2. infer source base identity
3. select a GNA template residue by base class
4. use source RNA phosphate positions as the global chain guide
5. generate an initial GNA glycerol scaffold from the template
6. locally optimize GNA scaffold distances
7. attach source RNA bases to `C1G`
8. export a GNA-like candidate PDB
9. validate GNA-specific linkages and scaffold geometry

---

## Alignment / Optimization Summary

- Mean initial alignment RMSD: `0.9987 Å`
- Maximum initial alignment RMSD: `1.4842 Å`
- Mean base shift: `0.8870 Å`
- Maximum base shift: `1.6972 Å`
- Mean optimization cost: `0.0454`
- Mean C1G→glycosidic N distance: `1.4677 Å`
- Mean P(i)→O3G(i) distance: `1.5944 Å`
- Mean O2G(i)→P(i+1) distance: `1.5928 Å`

---

## Structural Validation

| Metric | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| GNA O2G(i)→P(i+1) | 109 | 0 | 0 | 1.593 | 1.580 | 1.603 | 1.25–1.95 | PASS |
| GNA P(i)→O3G(i) | 111 | 0 | 0 | 1.594 | 1.587 | 1.608 | 1.25–1.95 | PASS |
| C1G→glycosidic N | 111 | 0 | 0 | 1.468 | 1.442 | 1.516 | 1.25–1.75 | PASS |
| C1G→C2G | 111 | 0 | 0 | 1.524 | 1.516 | 1.534 | 1.30–1.80 | PASS |
| C2G→C3G | 111 | 0 | 0 | 1.525 | 1.518 | 1.533 | 1.30–1.80 | PASS |
| C2G→O2G | 111 | 0 | 0 | 1.424 | 1.409 | 1.442 | 1.20–1.65 | PASS |
| C3G→O3G | 111 | 0 | 0 | 1.423 | 1.402 | 1.439 | 1.20–1.65 | PASS |

---

## Per-Residue Conversion

| # | Source residue | Base | Output residue | Template used | Initial RMSD (Å) | Base shift (Å) | Opt. cost | C1G–N (Å) | P–O3G (Å) | O2G–next P (Å) | Note |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | A5 | G | ZGU | ZGU A6 | 1.4842 | 0.9495 | 0.0420 | 1.449869304454709 | 1.6024655975645448 | 1.5841116863946738 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 2 | A6 | G | ZGU | ZGU A8 | 0.8412 | 0.8892 | 0.0401 | 1.4607077051895154 | 1.5889654898105527 | 1.5904320890891408 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 3 | A7 | U | ZBU | ZTH A2 | 1.1027 | 0.9752 | 0.0449 | 1.4896006176153398 | 1.6055473201887671 | 1.5800317610403734 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 4 | A8 | G | ZGU | ZGU A6 | 0.8148 | 0.9080 | 0.0407 | 1.4498693044547077 | 1.603069094665352 | 1.5844813744621293 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 5 | A9 | C | ZCY | ZCY A1 | 1.0684 | 1.0807 | 0.0625 | 1.483192502677916 | 1.5903905271262653 | 1.5965690452874697 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 6 | A10 | A | ZAD | ZAD A5 | 0.9177 | 0.8148 | 0.0317 | 1.4423723513711666 | 1.5900343510545043 | 1.598585835386746 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 7 | A11 | G | ZGU | ZGU A8 | 0.9942 | 1.6653 | 0.2068 | 1.4607077051895005 | 1.5936706634458244 | 1.5947813514818356 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 8 | A12 | G | ZGU | ZGU A6 | 1.2068 | 1.1667 | 0.0644 | 1.449869304454711 | 1.602845996615699 | 1.5843032651734246 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 9 | A13 | U | ZBU | ZBU A4 | 0.9737 | 0.8227 | 0.0329 | 1.5163353850649206 | 1.5866673722927298 | 1.6022880965400441 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 10 | A14 | A | ZAD | ZAD A7 | 1.1082 | 1.0011 | 0.0468 | 1.4539859008945124 | 1.592214425975096 | 1.59853604891597 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 11 | A15 | C | ZCY | ZCY A3 | 0.9377 | 0.8791 | 0.0383 | 1.4806245303924876 | 1.6008224316438715 | 1.584840137154056 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 12 | A16 | A | ZAD | ZAD A5 | 1.0399 | 0.8156 | 0.0314 | 1.4423723513711542 | 1.5898327795988503 | 1.5987039446563078 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 13 | A17 | U | ZBU | ZTH A2 | 0.9826 | 0.8229 | 0.0324 | 1.4896006176153314 | 1.605590221395412 | 1.5799682530516694 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 14 | A18 | C | ZCY | ZCY A1 | 0.9818 | 0.8439 | 0.0403 | 1.4831925026779336 | 1.5900612313315952 | 1.5963491572744437 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 15 | A19 | C | ZCY | ZCY A3 | 0.9871 | 0.8017 | 0.0311 | 1.4806245303924994 | 1.6006580537584811 | 1.5848924081282387 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 16 | A20 | A | ZAD | ZAD A7 | 1.1993 | 1.3610 | 0.0893 | 1.4539859008945037 | 1.5929437555142971 | 1.5989113483631545 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 17 | A21 | G | ZGU | ZGU A8 | 0.7722 | 0.8789 | 0.0389 | 1.4607077051895103 | 1.5887579658870061 | 1.5903588690707875 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 18 | A22 | C | ZCY | ZCY A1 | 0.8238 | 0.7858 | 0.0315 | 1.4831925026779196 | 1.5904630526876378 | 1.5965477832123462 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 19 | A23 | U | ZBU | ZBU A4 | 0.9185 | 0.8095 | 0.0319 | 1.516335385064925 | 1.5866286255951134 | 1.602287668692264 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 20 | A24 | G | ZGU | ZGU A6 | 1.1773 | 0.9912 | 0.0453 | 1.4498693044547106 | 1.6024692985366666 | 1.5841322574496457 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 21 | A25 | A | ZAD | ZAD A5 | 1.1227 | 0.9793 | 0.0443 | 1.4423723513711648 | 1.5897417647181638 | 1.5987563103277733 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 22 | A26 | U | ZBU | ZTH A2 | 0.7991 | 0.5215 | 0.0138 | 1.4896006176153351 | 1.6055454052244658 | 1.5798575748487098 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 23 | A27 | G | ZGU | ZGU A8 | 0.7049 | 0.9591 | 0.0455 | 1.4607077051895176 | 1.588718633684167 | 1.5903986138569117 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 24 | A28 | A | ZAD | ZAD A7 | 1.2150 | 0.9955 | 0.0472 | 1.4539859008945077 | 1.5924059760637255 | 1.5984160279001172 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 25 | A29 | G | ZGU | ZGU A6 | 0.9457 | 0.8148 | 0.0315 | 1.4498693044547184 | 1.602635550121661 | 1.5840788718912484 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 26 | A30 | U | ZBU | ZBU A4 | 1.0471 | 1.2175 | 0.0732 | 1.5163353850649193 | 1.5872888849187263 | 1.6027500683917493 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 27 | A31 | C | ZCY | ZCY A3 | 1.1141 | 0.9526 | 0.0430 | 1.4806245303924943 | 1.6005016989487764 | 1.5849452837530011 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 28 | A32 | C | ZCY | ZCY A1 | 1.0306 | 1.1257 | 0.0661 | 1.483192502677929 | 1.5905379886513347 | 1.5966990114351536 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 29 | A33 | C | ZCY | ZCY A3 | 1.0576 | 0.8938 | 0.0380 | 1.4806245303925034 | 1.600510905103342 | 1.584923247345115 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 30 | A34 | A | ZAD | ZAD A5 | 1.0274 | 0.7864 | 0.0294 | 1.4423723513711706 | 1.589855279834346 | 1.5986856212559828 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 31 | A35 | A | ZAD | ZAD A7 | 0.8027 | 0.0096 | 0.0008 | 1.4539859008945082 | 1.5922150645790085 | 1.5981325878315975 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 32 | A36 | A | ZAD | ZAD A5 | 0.9881 | 0.4816 | 0.0114 | 1.4423723513711746 | 1.589831973886303 | 1.5985974124945947 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 33 | A37 | U | ZBU | ZTH A2 | 0.9711 | 0.9718 | 0.0456 | 1.4896006176153505 | 1.6058089912119025 | 1.580138067839941 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 34 | A38 | A | ZAD | ZAD A7 | 0.7964 | 0.5276 | 0.0130 | 1.453985900894506 | 1.5922349221790664 | 1.5983447992742579 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 35 | A39 | G | ZGU | ZGU A8 | 1.0650 | 1.6972 | 0.1502 | 1.46070770518951 | 1.5906578896297991 | 1.5918167756488266 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 36 | A40 | G | ZGU | ZGU A6 | 1.0680 | 0.8549 | 0.0345 | 1.4498693044547049 | 1.6025507000863124 | 1.5840773157845034 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 37 | A41 | A | ZAD | ZAD A5 | 1.0075 | 0.7737 | 0.0282 | 1.442372351371169 | 1.589849874278653 | 1.5986683630209724 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 38 | A42 | C | ZCY | ZCY A1 | 1.0675 | 1.1118 | 0.0650 | 1.483192502677922 | 1.5904370341852772 | 1.5965931822380643 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 39 | A43 | A | ZAD | ZAD A7 | 1.0370 | 0.8463 | 0.0344 | 1.4539859008945184 | 1.592396603490605 | 1.5985042938290814 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 40 | A44 | A | ZAD | ZAD A5 | 1.0853 | 0.9068 | 0.0382 | 1.4423723513711688 | 1.589750291633238 | 1.5987282818540782 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 41 | A45 | A | ZAD | ZAD A7 | 1.0794 | 0.9186 | 0.0398 | 1.4539859008945095 | 1.5922375622502452 | 1.598506663049771 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 42 | A46 | A | ZAD | ZAD A5 | 1.0626 | 0.8479 | 0.0337 | 1.4423723513711753 | 1.5897942672913126 | 1.5987081578024882 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 43 | A47 | A | ZAD | ZAD A7 | 1.0714 | 0.8720 | 0.0363 | 1.4539859008945 | 1.5923375018734953 | 1.598499702266506 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 44 | A48 | G | ZGU | ZGU A8 | 0.8001 | 0.8202 | 0.0345 | 1.4607077051895125 | 1.5888998637927578 | 1.5903408073105694 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 45 | A49 | G | ZGU | ZGU A6 | 1.0225 | 0.8514 | 0.0344 | 1.4498693044547086 | 1.6026083892067948 | 1.5840858616759734 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 46 | A50 | G | ZGU | ZGU A8 | 0.7775 | 0.8448 | 0.0362 | 1.460707705189507 | 1.5887803255256912 | 1.5903446557683696 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 47 | A51 | A | ZAD | ZAD A5 | 1.0597 | 0.8173 | 0.0316 | 1.4423723513711773 | 1.589808792488607 | 1.5986974073862132 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 48 | A52 | G | ZGU | ZGU A6 | 1.1293 | 0.8866 | 0.0368 | 1.4498693044547282 | 1.6024857702682982 | 1.5840883001998627 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 49 | A53 | A | ZAD | ZAD A7 | 1.1344 | 1.0230 | 0.0485 | 1.4539859008944982 | 1.5922133684785666 | 1.5985426786303294 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 50 | A54 | G | ZGU | ZGU A8 | 0.6929 | 0.7651 | 0.0298 | 1.4607077051895108 | 1.5887304093993118 | 1.5903145106617886 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 51 | A55 | G | ZGU | ZGU A6 | 0.9087 | 0.7566 | 0.0274 | 1.4498693044547255 | 1.6026469382329713 | 1.5840526813099516 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 52 | A56 | U | ZBU | ZBU A4 | 1.1609 | 1.0063 | 0.0495 | 1.5163353850649441 | 1.5868140641719992 | 1.6023959578750282 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 53 | A57 | G | ZGU | ZGU A8 | 1.0017 | 1.3148 | 0.0872 | 1.4607077051895188 | 1.5896745227811093 | 1.5910545432869474 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 54 | A58 | A | ZAD | ZAD A5 | 1.0846 | 0.8852 | 0.0364 | 1.4423723513711784 | 1.5897421242867822 | 1.598718465858484 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 55 | A59 | A | ZAD | ZAD A7 | 1.0832 | 0.9270 | 0.0403 | 1.4539859008945037 | 1.5922198373874887 | 1.5985060956749775 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 56 | A60 | G | ZGU | ZGU A6 | 1.1097 | 0.8926 | 0.0372 | 1.4498693044547077 | 1.6024707791157988 | 1.5840945581273167 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 57 | A61 | A | ZAD | ZAD A5 | 1.0584 | 0.8303 | 0.0326 | 1.4423723513711864 | 1.5898322841946244 | 1.5987043624958168 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 58 | A62 | A | ZAD | ZAD A7 | 0.8264 | 0.5144 | 0.0126 | 1.4539859008945057 | 1.592282210638121 | 1.5983199778324715 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 59 | A63 | U | ZBU | ZTH A2 | 0.8221 | 0.5681 | 0.0167 | 1.4896006176153405 | 1.605622736780404 | 1.5798862656711345 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 60 | A64 | A | ZAD | ZAD A5 | 1.1252 | 0.9526 | 0.0419 | 1.4423723513711781 | 1.5897420296105835 | 1.5987437887341072 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 61 | A65 | C | ZCY | ZCY A3 | 0.8766 | 0.7355 | 0.0263 | 1.480624530392496 | 1.6006490195055563 | 1.5849041621134918 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 62 | A66 | G | ZGU | ZGU A8 | 0.6976 | 0.6888 | 0.0249 | 1.460707705189506 | 1.5890284200998241 | 1.5904048943625815 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 63 | A67 | A | ZAD | ZAD A7 | 1.0960 | 0.9258 | 0.0403 | 1.4539859008945086 | 1.5922134820561307 | 1.5985054924592144 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 64 | A68 | C | ZCY | ZCY A1 | 0.9888 | 0.8485 | 0.0402 | 1.483192502677933 | 1.5900310020602861 | 1.5963502794086197 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 65 | A69 | C | ZCY | ZCY A3 | 1.0843 | 0.9182 | 0.0400 | 1.4806245303925054 | 1.6005001750135777 | 1.5849331853820994 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 66 | A70 | A | ZAD | ZAD A5 | 1.0657 | 0.8317 | 0.0325 | 1.4423723513711613 | 1.5898024199202674 | 1.598697347254911 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 67 | A71 | C | ZCY | ZCY A1 | 0.9470 | 0.8375 | 0.0403 | 1.483192502677923 | 1.5901564812913118 | 1.5963644217923447 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 68 | A72 | C | ZCY | ZCY A3 | 1.0531 | 0.8785 | 0.0373 | 1.480624530392495 | 1.600674208045069 | 1.5849432361594327 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 69 | A73 | U | ZBU | ZBU A4 | 1.0054 | 0.7949 | 0.0310 | 1.5163353850649235 | 1.5866969210942907 | 1.6022507261063943 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 70 | A74 | A | ZAD | ZAD A7 | 1.0610 | 0.8455 | 0.0340 | 1.4539859008945137 | 1.5922928365042202 | 1.5984732301655844 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 71 | A75 | G | ZGU | ZGU A6 | 0.9418 | 0.8355 | 0.0333 | 1.4498693044547166 | 1.602685730840654 | 1.584099275977451 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 72 | A76 | G | ZGU | ZGU A8 | 1.0619 | 1.3338 | 0.0888 | 1.4607077051895012 | 1.5894486987228467 | 1.5907449543103045 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 73 | A77 | C | ZCY | ZCY A1 | 0.6490 | 0.8930 | 0.0425 | 1.4831925026779345 | 1.590581009037379 | 1.5965759079336777 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 74 | A78 | U | ZBU | ZTH A2 | 1.0766 | 0.4553 | 0.0110 | 1.4896006176153438 | 1.6055506965144022 | 1.5798264636750385 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 75 | A79 | C | ZCY | ZCY A3 | 0.9821 | 0.7486 | 0.0268 | 1.4806245303924899 | 1.6005143568259468 | 1.584857221136837 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 76 | A80 | G | ZGU | ZGU A6 | 1.1972 | 0.9850 | 0.0451 | 1.4498693044547086 | 1.6024719482651968 | 1.5841314146136571 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 77 | A81 | A | ZAD | ZAD A5 | 1.1756 | 1.0876 | 0.0561 | 1.442372351371181 | 1.59005809238755 | 1.5988769355222443 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 78 | A82 | A | ZAD | ZAD A7 | 0.9809 | 1.3613 | 0.1762 | 1.4539859008944969 | 1.5975177318529863 | 1.6033783079754658 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 79 | A83 | A | ZAD | ZAD A5 | 1.1799 | 0.9745 | 0.0440 | 1.4423723513711728 | 1.5897425978637454 | 1.5987529590755698 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 80 | A84 | G | ZGU | ZGU A8 | 0.9262 | 1.0386 | 0.0543 | 1.4607077051895077 | 1.5892777604689636 | 1.5907781759808077 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 81 | A85 | A | ZAD | ZAD A7 | 1.0825 | 0.8732 | 0.0361 | 1.45398590089451 | 1.5922364985733435 | 1.5984849095461666 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 82 | A86 | G | ZGU | ZGU A6 | 1.0764 | 0.8856 | 0.0369 | 1.449869304454718 | 1.602535996087113 | 1.5840943527291307 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 83 | A87 | C | ZCY | ZCY A1 | 0.9090 | 0.8013 | 0.0372 | 1.4831925026779298 | 1.5901551449792832 | 1.5963499954089797 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 84 | A88 | C | ZCY | ZCY A3 | 1.0560 | 0.8859 | 0.0374 | 1.4806245303924983 | 1.6005317145303277 | 1.584919665017135 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 85 | A89 | U | ZBU | ZBU A4 | 0.9638 | 0.8106 | 0.0321 | 1.5163353850649373 | 1.5867217049227205 | 1.6022799380387274 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 86 | A90 | A | ZAD | ZAD A5 | 1.1841 | 0.9862 | 0.0448 | 1.4423723513711597 | 1.5897429093434539 | 1.5987569112563107 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 87 | A91 | A | ZAD | ZAD A7 | 0.8803 | 0.8277 | 0.0330 | 1.4539859008944984 | 1.592531073205208 | 1.5983585886715692 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 88 | A92 | A | ZAD | ZAD A5 | 0.9801 | 0.8888 | 0.0396 | 1.4423723513711657 | 1.5906829744402133 | 1.599309333442854 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 89 | A93 | A | ZAD | ZAD A7 | 1.0523 | 0.8729 | 0.0358 | 1.453985900894501 | 1.5922139871655623 | 1.5984843769283343 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 90 | A94 | C | ZCY | ZCY A1 | 0.9390 | 0.7964 | 0.0368 | 1.4831925026779202 | 1.5900861250879892 | 1.5963303333590972 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 91 | A95 | A | ZAD | ZAD A5 | 1.0154 | 0.7792 | 0.0289 | 1.442372351371174 | 1.5898895705732095 | 1.5986835484782818 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 92 | A96 | U | ZBU | ZTH A2 | 1.1496 | 1.2270 | 0.0727 | 1.4896006176153385 | 1.6060575444702487 | 1.5802521641338334 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 93 | A97 | A | ZAD | ZAD A7 | 1.0685 | 0.8555 | 0.0347 | 1.4539859008945089 | 1.592243432483103 | 1.5984779547544736 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 94 | A98 | C | ZCY | ZCY A3 | 1.0637 | 0.8910 | 0.0379 | 1.480624530392496 | 1.600528503630667 | 1.5849218411441295 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 95 | A99 | C | ZCY | ZCY A1 | 0.9628 | 0.8253 | 0.0387 | 1.4831925026779182 | 1.590064128386888 | 1.5963394153686996 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 96 | A100 | U | ZBU | ZBU A4 | 0.9388 | 0.8424 | 0.0347 | 1.5163353850649222 | 1.5867903019470118 | 1.6023143118027952 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 97 | A101 | U | ZBU | ZTH A2 | 1.0333 | 0.8558 | 0.0348 | 1.489600617615333 | 1.6055528172081985 | 1.5799806690553937 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 98 | A102 | U | ZBU | ZBU A4 | 1.0935 | 0.8948 | 0.0388 | 1.5163353850649404 | 1.5865909641805758 | 1.6023071965478242 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 99 | A103 | C | ZCY | ZCY A3 | 1.0781 | 1.0741 | 0.2141 | 1.480624530392503 | 1.6078062601630385 | 1.5918243626343878 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 100 | A104 | C | ZCY | ZCY A1 | 0.9512 | 1.0812 | 0.0586 | 1.4831925026779156 | 1.5904395258221966 | 1.5965186641382245 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 101 | A105 | U | ZBU | ZTH A2 | 1.0022 | 0.8084 | 0.0312 | 1.4896006176153358 | 1.6055600395315934 | 1.579960276527663 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 102 | A106 | G | ZGU | ZGU A8 | 0.7972 | 0.8705 | 0.0385 | 1.4607077051895148 | 1.5891235355668916 | 1.5904594004778005 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 103 | A107 | G | ZGU | ZGU A6 | 1.1665 | 1.0238 | 0.0490 | 1.4498693044547144 | 1.6026376548401104 | 1.584173129904624 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 104 | A108 | A | ZAD | ZAD A5 | 1.1533 | 1.3370 | 0.0866 | 1.4423723513711715 | 1.5906483076160634 | 1.5993451777025067 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 105 | A109 | U | ZBU | ZBU A4 | 1.0001 | 0.8678 | 0.0367 | 1.516335385064934 | 1.5867043455718728 | 1.6023089489765714 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 106 | A110 | U | ZBU | ZTH A2 | 0.8520 | 0.7168 | 0.0263 | 1.4896006176153407 | 1.60581994906421 | 1.5800444779985436 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 107 | A111 | C | ZCY | ZCY A3 | 1.0355 | 0.8862 | 0.0375 | 1.4806245303924852 | 1.600552696672943 | 1.5849243173315584 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 108 | A112 | C | ZCY | ZCY A1 | 0.0792 | 0.0073 | 0.0010 | 1.4831925026779114 | 1.5900054715216219 | NA | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 109 | A115 | U | ZBU | ZBU A4 | 0.9302 | 0.6556 | 0.0233 | 1.5163353850649133 | 1.586921726632481 | 1.6023082630278014 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 110 | A116 | G | ZGU | ZGU A8 | 0.9488 | 1.3150 | 0.1998 | 1.4607077051895205 | 1.5952048445570244 | 1.5966186453167674 | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |
| 111 | A117 | C | ZCY | ZCY A3 | 1.0697 | 0.0119 | 0.0002 | 1.4806245303925125 | 1.6004979526106817 | NA | exact base-class GNA template; GNA linkage-optimized glycerol scaffold |

---

## Scientific Interpretation

This output should be interpreted as:

> a GNA-like computational candidate generated by linkage-optimized glycerol-scaffold reconstruction.

It should **not** be interpreted as:

> a chemically validated, experimentally confirmed, or MD-ready GNA structure.

---

## Important Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- GNA stereochemistry requires expert inspection.
- Molecular viewers may not render standard nucleic-acid cartoon paths reliably for GNA-like structures.
- The output is a candidate geometry only; biological function, stability, replication, or catalytic activity is not implied.
