# Benchmark 012: PNA Template-Primary Scaling

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 012  
**Prototype tested:** Prototype 008B — RNA → PNA template-primary base replacement  
**Status:** Successful template-primary candidate-generation benchmark; not physically validated  
**Primary result:** PNA-like candidate generation scales cleanly from 8 nt to 111 nt when treated as a scaffold-first, sequence-preserving problem rather than an RNA-fold-preserving conversion.

---

## Summary

Benchmark 012 documents the successful second RNA → PNA strategy in Digital Polymerase.

PNA, or peptide nucleic acid, is not a sugar-phosphate XNA. It replaces the sugar-phosphate backbone with a pseudopeptide backbone. Because of this, Prototype 008A.1 failed when it attempted to force PNA geometry onto the original RNA fold.

Prototype 008B reverses the logic:

```text
PNA scaffold first
RNA sequence/base identity second
```

The goal is no longer to preserve the RNA tertiary fold. Instead, Prototype 008B asks a narrower and more honest question:

```text
Can we generate a clean PNA-like molecule carrying the same base sequence?
```

The answer from Benchmark 012 is yes.

The benchmark tested six RNA inputs:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer HH ribozyme-derived RNA
```

All tested outputs passed the current report-level validation checks. Visual inspection showed that the 8-mer, 34-mer, and 111-mer are clean, elongated, PNA-like structures rather than tangled collapsed structures.

---

## Relation to Benchmark 011

Benchmark 011 documented the failure of Prototype 008A.1.

Prototype 008A.1 attempted:

```text
RNA fold → force PNA backbone onto it
```

This produced a tangled 8-mer and was classified as a failed/rough first attempt.

Prototype 008B instead uses:

```text
PNA scaffold → replace bases by RNA sequence
```

This produced a much cleaner 8-mer and scaled to 34-mer and 111-mer outputs without catastrophic collapse.

This makes Benchmark 012 a direct response to Benchmark 011.

---

## Why PNA Is Different

Earlier working Digital Polymerase families include:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
XyNA  → Prototype 005A
TNA   → Prototype 006B.4
GNA   → Prototype 007A
```

Most of these can be understood as modified nucleic-acid scaffolds.

PNA is different because:

```text
RNA/DNA/XNA-like systems: sugar/scaffold + phosphate-like chain
PNA: pseudopeptide backbone + nucleobase side chains
```

This changes the conversion philosophy.

For many XNAs:

```text
RNA 3D fold → XNA-like fold candidate
```

For PNA:

```text
RNA sequence → PNA sequence carrier
```

This distinction is essential.

---

## Folder Layout

Recommended repository placement:

```text
benchmarks/
└── pna_scaling/
    ├── README.md
    ├── inputs/
    │   ├── RNA-8mer.pdb
    │   ├── RNA-12mer.pdb
    │   ├── RNA-16mer.pdb
    │   ├── RNA-22mer.pdb
    │   ├── RNA-34mer.pdb
    │   └── 8t5o-HH-typeI-111mer-full.pdb
    ├── templates/
    │   └── 3mbs_PNA-1mer-8.pdb
    ├── outputs/
    │   ├── converted_pna_RNA-8mer_template_primary_008B.pdb
    │   ├── converted_pna_RNA-12mer_template_primary_008B.pdb
    │   ├── converted_pna_RNA-16mer_template_primary_008B.pdb
    │   ├── converted_pna_RNA-22mer_template_primary_008B.pdb
    │   ├── converted_pna_RNA-34mer_template_primary_008B.pdb
    │   └── converted_pna_8t5o-HH-typeI-111mer-full_template_primary_008B.pdb
    ├── reports/
    │   ├── conversion_report_RNA-8mer_template_primary_008B.md
    │   ├── conversion_report_RNA-12mer_template_primary_008B.md
    │   ├── conversion_report_RNA-16mer_template_primary_008B.md
    │   ├── conversion_report_RNA-22mer_template_primary_008B.md
    │   ├── conversion_report_RNA-34mer_template_primary_008B.md
    │   └── conversion_report_8t5o-HH-typeI-111mer-full_template_primary_008B.md
    ├── visual_inspection/
    │   ├── pymol/
    │   └── discovery_studio/
    ├── benchmark_011_pna_failure_notes.md
    └── benchmark_012_pna_template_primary_scaling_notes.md
```

---

## Input RNA Dataset

| File | Length | Residue range | Sequence |
|---|---:|---|---|
| `RNA-8mer.pdb` | TBD nt | A:72–79 | `TBD` |
| `RNA-12mer.pdb` | TBD nt | A:72–83 | `TBD` |
| `RNA-16mer.pdb` | TBD nt | A:67–82 | `TBD` |
| `RNA-22mer.pdb` | TBD nt | A:62–83 | `TBD` |
| `RNA-34mer.pdb` | TBD nt | A:54–87 | `TBD` |
| `8t5o-HH-typeI-111mer-full.pdb` | TBD nt | A:5–117, with source numbering gap | `TBD` |

---

## PNA Template

Primary template:

```text
3mbs_PNA-1mer-8.pdb
```

Observed PNA-like residues include:

```text
APN
TPN
GPN
CPN
```

Important PNA scaffold atoms:

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

Observed PNA-like linkage:

```text
C′(i) → N1′(i+1)
```

Observed base attachment:

```text
C8′ → glycosidic N
```

---

## Prototype 008B Method

Prototype 008B performs **template-primary PNA base replacement**.

For each source RNA residue, the converter:

1. reads the RNA base sequence from the source PDB
2. preserves or tiles the PNA template scaffold
3. selects a PNA base donor by target RNA base identity
4. transforms the donor base onto the scaffold residue
5. removes thymine `C5M` when using a T-like donor for RNA U
6. exports a PNA-like candidate PDB
7. validates PNA backbone geometry
8. validates `C8′→glycosidic N`
9. audits expected base oxygens

This method intentionally does **not** preserve the source RNA 3D fold.

---

## Scaling Results

| Input | Residues | C′→N1′ next | C8′→gly N | Backbone C8′→C7′ | C7′→N4′ | C′→O1′ | Base oxygen audit | Mean C8′→N / C′→N1′ next (Å) | Missing base oxygens |
|---|---:|---|---|---|---|---|---|---:|---:|
| `RNA-8mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-12mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-16mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-22mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `RNA-34mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |
| `HH-111mer` | TBD | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | TBD / TBD | TBD |

Interpretation:

- All tested inputs were converted using template-primary PNA scaffold reconstruction.
- All outputs passed PNA `C′(i)→N1′(i+1)` validation.
- All outputs passed `C8′→glycosidic N` base-attachment validation.
- All outputs passed the backbone checks reported here.
- The expected base-oxygen audit passed.
- Visual inspection supports that the 8-mer, 34-mer, and 111-mer are clean sequence-preserving PNA-like candidates.

---

## Visual Inspection

### 8-mer

The 8-mer output was the decisive test because Prototype 008A.1 failed at this size.

Prototype 008B produced a clean and coherent 8-mer:

```text
converted_pna_RNA-8mer_template_primary_008B.pdb
```

Observed:

- no severe tangling
- no collapsed knot-like structure
- bases attached clearly
- pseudopeptide backbone visible
- much cleaner than Prototype 008A.1

### 34-mer

The 34-mer output formed an elongated, PNA-like chain:

```text
converted_pna_RNA-34mer_template_primary_008B.pdb
```

Observed:

- continuous chain
- not catastrophically tangled
- scalable elongated geometry
- bases distributed along the scaffold

### 111-mer HH ribozyme-derived RNA

The 111-mer output formed a long, clean, sequence-preserving PNA strand:

```text
converted_pna_8t5o-HH-typeI-111mer-full_template_primary_008B.pdb
```

Observed:

- extended PNA-like molecular serpent
- no collapse
- no obvious fragmentation
- not an HH ribozyme fold, by design

---

## Interpretation of the 111-mer

The 111-mer output should not be interpreted as a PNA version of the hammerhead ribozyme fold.

Correct interpretation:

```text
A PNA-like sequence carrier generated from the HH-ribozyme-derived RNA sequence.
```

Incorrect interpretation:

```text
A PNA hammerhead ribozyme structural analog.
```

This matters because Prototype 008B is a sequence-preserving scaffold generator, not a fold-preserving converter.

---

## Scientific Interpretation

Correct description:

```text
PNA-like computational candidate structures generated by template-primary base replacement.
```

Incorrect descriptions:

```text
validated PNA molecules
experimentally confirmed PNA ribozymes
MD-ready PNA structures
proof of PNA biological function
RNA-fold-preserving PNA analogs
```

These outputs are computational candidates only.

---

## Known Limitations

- Does not preserve RNA 3D fold.
- Not energy-minimized.
- No molecular dynamics validation.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- PNA stereochemistry requires expert inspection.
- Large outputs are tiled/scaffold-primary candidates, not folded biological models.
- Molecular viewers may not recognize the output as a canonical nucleic-acid polymer.
- Biological function, stability, binding, or catalytic activity is not implied.

---

## Development Classification

Digital Polymerase conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Local atom/residue identity transformation.

3. **Geometric candidate reconstruction**  
   Coordinate-level candidate generation using templates, coordinate transformations, tiling, and validation.

4. **Physically refined modeling**  
   Energy minimization, MD, force-field validation, and expert inspection.

Prototype 008B reaches:

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
XyNA  → Prototype 005A
TNA   → Prototype 006B.4
GNA   → Prototype 007A
PNA   → Prototype 008B
```

PNA adds a new conversion paradigm:

```text
template-primary scaffold-first sequence remapping
```

This should be explicitly described in the main project README.

---

## Recommended Repository Status

Keep the current script under:

```text
src/digital_polymerase/prototypes/rna_to_pna_template_primary.py
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
- explicit PNA parameterization guidance
- template-tiling controls and sequence-length warnings

---

## Recommended Commit Message

```bash
git add src/digital_polymerase/prototypes/rna_to_pna_template_primary.py
git add benchmarks/pna_scaling/
git add docs/prototype_008B_rna_to_pna_template_primary.md
git commit -m "Add template-primary RNA-to-PNA prototype and scaling benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as PNA scaling benchmark:** yes  
**Claim RNA fold preservation:** no  
**Claim sequence-preserving PNA candidate generation:** yes

Benchmark 012 marks the point where PNA joins the Digital Polymerase working prototype roster through a new template-primary strategy.
