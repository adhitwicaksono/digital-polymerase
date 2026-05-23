# Benchmark 007: CeNA Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 007  
**Prototype tested:** Prototype 004A — RNA → CeNA template-guided / chain-preserving reconstruction  
**Status:** Successful candidate-generation benchmark; not physically validated  
**Primary result:** CeNA-like candidate generation scales from 8 nt to 111 nt.

---

## Summary

Benchmark 007 documents the first RNA → CeNA scaling benchmark in Digital Polymerase.

CeNA, or cyclohexenyl nucleic acid, uses a backbone/scaffold architecture that differs from canonical RNA. For this reason, Prototype 004A follows the design lessons learned from HNA, ANA, and FANA:

```text
preserve polymer-chain logic
introduce XNA-specific local scaffold geometry
validate explicitly
inspect visually
```

The benchmark tested six RNA inputs:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer HH ribozyme-derived RNA
```

The CeNA template used was:

```text
2H0N_CeNA_8mer_clean_ss.pdb
```

All tested outputs passed the current core validation checks, including polymer-chain continuity, base attachment, and CeNA local scaffold distances.

Visual inspection in PyMOL and Discovery Studio showed coherent continuous structures for the 8-mer, 34-mer, and 111-mer outputs.

---

## Why CeNA Was Tested After HNA/ANA/FANA

The working converter families before this benchmark were:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
```

CeNA was selected next because it is more structurally distinct than ANA/FANA, but still shares enough nucleic-acid-like coordinate logic to be a reasonable next target before moving to more difficult targets such as TNA, GNA, or PNA.

The CeNA benchmark therefore tests whether the mature Digital Polymerase pattern can generalize to a cyclohexenyl-like XNA scaffold.

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── cena_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 2H0N_CeNA_8mer_clean_ss.pdb
    ├── outputs/
    │   ├── converted_cena_RNA-8mer_auto_004A.pdb
    │   ├── converted_cena_RNA-12mer_auto_004A.pdb
    │   ├── converted_cena_RNA-16mer_auto_004A.pdb
    │   ├── converted_cena_RNA-22mer_auto_004A.pdb
    │   ├── converted_cena_RNA-34mer_auto_004A.pdb
    │   └── converted_cena_8t5o-HH-typeI-111mer-full_auto_004A.pdb
    ├── reports/
    │   ├── conversion_report_RNA-8mer_auto_004A.md
    │   ├── conversion_report_RNA-12mer_auto_004A.md
    │   ├── conversion_report_RNA-16mer_auto_004A.md
    │   ├── conversion_report_RNA-22mer_auto_004A.md
    │   ├── conversion_report_RNA-34mer_auto_004A.md
    │   └── conversion_report_8t5o-HH-typeI-111mer-full_auto_004A.md
    ├── visual_inspection/
    │   ├── pymol/
    │   └── discovery_studio/
    └── benchmark_007_cena_scaling_notes.md
```

---

## Input RNA Dataset

| File | Length | Residue range | Sequence |
|---|---:|---|---|
| `RNA-8mer.pdb` | 8 nt | A:72–79 | `CUAGGCUC` |
| `RNA-12mer.pdb` | 12 nt | A:72–83 | `CUAGGCUCGAAA` |
| `RNA-16mer.pdb` | 16 nt | A:67–82 | `ACCACCUAGGCUCGAA` |
| `RNA-22mer.pdb` | 22 nt | A:62–83 | `AUACGACCACCUAGGCUCGAAA` |
| `RNA-34mer.pdb` | 34 nt | A:54–87 | `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC` |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 nt | A:5–117, with source numbering gap | `GGUGCAGGUACAUCCAGCUGAUGAGUCCCAAAUAGGACAAAAAGGGAGAGGUGAAGAAUACGACCACCUAGGCUCGAAAGAGCCUAAAACAUACCUUUCCUGGAUUCCUGC` |

---

## CeNA Template

Primary template:

```text
2H0N_CeNA_8mer_clean_ss.pdb
```

Template properties observed during inspection:

```text
Length: 8 residues
Base-class sequence: GUGUACAC
Observed CeNA residue names: XGL, XTL, XAL, XCL
```

Important CeNA scaffold atoms observed:

```text
C1'
C2'
C3'
C4'
C5'
C6'
C7'
O3'
O5'
P
```

CeNA-specific local scaffold distances validated in this benchmark include:

```text
C4′ → C6′
C6′ → C7′
C7′ → C1′
```

---

## Prototype 004A Method Modes

### Full-template mode

Used when the CeNA template length is equal to or greater than the RNA input length.

For the 8-mer:

```text
RNA-8mer + CeNA-8mer template → full-template mode
```

The CeNA scaffold is taken directly from the template, and RNA bases are transformed into the CeNA local frames.

### Chain-preserving mode

Used when the source RNA is longer than the CeNA template.

For 12-mer and above:

```text
RNA chain atoms preserved
+
CeNA local scaffold atoms inserted from template
+
RNA bases transformed onto CeNA-like local scaffold
```

This mode preserves the original RNA polymer path while introducing local CeNA-like scaffold geometry.

---

## Conversion Logic

For each source RNA residue, Prototype 004A:

1. infers RNA base identity
2. selects an appropriate CeNA template residue by base class
3. preserves or transfers polymer-chain geometry depending on mode
4. inserts CeNA local scaffold atoms such as `C1′`, `C2′`, `C6′`, and `C7′`
5. transforms RNA base atoms onto the CeNA-like local scaffold
6. corrects C1′→glycosidic-N distance using template-derived geometry
7. exports an output PDB
8. writes a Markdown validation report

---

## Scaling Results

| Input | Residues | Mode | Chain | Base attach | CeNA scaffold | Template/local RMSD mean/max (Å) | Base RMSD mean/max (Å) | C1′→N mean/max (Å) |
|---|---:|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `full-template` | `PASS` | `PASS` | `C4′→C6′ PASS` | 0.5160 / 0.5421 | NA | 1.4865 / 1.4965 |
| `RNA-12mer` | 12 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8029 / 0.9289 | 0.4679 / 0.7588 | 1.4938 / 1.4996 |
| `RNA-16mer` | 16 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8256 / 0.9389 | 0.5180 / 0.7531 | 1.4932 / 1.4996 |
| `RNA-22mer` | 22 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8373 / 0.9435 | 0.5788 / 0.7589 | 1.4928 / 1.4996 |
| `RNA-34mer` | 34 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8255 / 0.9435 | 0.5651 / 0.7666 | 1.4932 / 1.4996 |
| `HH-111mer` | 111 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.7988 / 0.9389 | 0.5186 / 0.7666 | 1.4931 / 1.4996 |

Interpretation:

- The 8-mer used full-template mode.
- 12-mer through 111-mer used chain-preserving mode.
- All tested outputs passed O3′→P chain-continuity validation.
- All tested outputs passed C1′→glycosidic-N validation.
- All tested outputs passed the current CeNA local scaffold checks.
- Visual inspection showed coherent continuous structures.

---

## Visual Inspection

Visual inspection was performed in PyMOL and Discovery Studio.

### 8-mer

- short-mer candidate appears coherent
- one cartoon end looks visually dramatic, but stick view supports structural continuity
- no obvious residue explosion

### 34-mer

- convincing longer CeNA-like chain
- continuous backbone/cartoon path
- stick view remains connected and interpretable

### 111-mer HH ribozyme-derived RNA

- globally coherent macromolecular candidate
- dense but connected atom/stick view
- no obvious large-scale fragmentation
- global fold-like topology remains recognizable

Visual inspection supports the benchmark conclusion:

```text
Prototype 004A produces visually coherent CeNA-like candidate structures up to 111 nt.
```

---

## Scientific Interpretation

Correct description:

```text
CeNA-like computational candidate structures generated by full-template and chain-preserving reconstruction.
```

Incorrect descriptions:

```text
validated CeNA molecules
experimentally confirmed CeNA ribozymes
MD-ready CeNA structures
proof of CeNA biological function
```

These outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No molecular dynamics validation.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- `XUL` residue labels are provisional when RNA `U` is preserved.
- Chain-preserving mode preserves the RNA chain path and inserts CeNA-like local scaffold geometry; it is not de novo CeNA folding.
- CeNA stereochemistry requires expert inspection.
- Large 111-mer output should be treated as a geometry candidate, not a validated CeNA ribozyme.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Development Classification

Digital Polymerase conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Local atom/residue identity transformation.

3. **Geometric candidate reconstruction**  
   Coordinate-level candidate generation using templates and coordinate transformations.

4. **Physically refined modeling**  
   Energy minimization, MD, force-field validation, and expert inspection.

Prototype 004A reaches:

```text
Level 3: geometric candidate reconstruction
```

It does not reach:

```text
Level 4: physically refined modeling
```

---

## Relationship to Other XNA Families

Current working candidate-generation families:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
```

Development pattern reinforced by CeNA:

```text
template availability matters
chain continuity must be preserved or explicitly reconstructed
base attachment must be validated
local XNA scaffold geometry must be checked
visual inspection remains essential
```

---

## Recommended Repository Status

Keep the current script under:

```text
src/digital_polymerase/prototypes/rna_to_cena_template_guided.py
```

Do not yet promote it into:

```text
src/digital_polymerase/converters/
```

until the project adds:

- shared core modules
- explicit topology/connectivity support
- stronger stereochemistry validation
- force-field/minimization compatibility
- cross-XNA shared conversion framework

---

## Recommended Commit Message

```bash
git add src/digital_polymerase/prototypes/rna_to_cena_template_guided.py
git add benchmarks/cena_scaling/
git add docs/prototype_004A_rna_to_cena_template_guided.md
git commit -m "Add RNA-to-CeNA prototype and scaling benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as CeNA scaling benchmark:** yes  
**Proceed to next XNA target:** yes, after documentation and repo cleanup

Benchmark 007 marks the point where CeNA joins HNA, ANA, and FANA as a working Digital Polymerase candidate-generation family.
