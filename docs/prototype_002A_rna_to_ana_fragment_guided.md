# Prototype 002A: RNA → ANA Fragment-Guided / Chain-Preserving Reconstruction

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype family:** 002A  
**Conversion:** RNA → ANA  
**Method:** Fragment-guided reconstruction, later patched into chain-preserving reconstruction  
**Current recommended version:** Prototype 002A.2  
**Status:** Experimental candidate generator; not physically validated

---

## Summary

Prototype 002A is the Digital Polymerase prototype family for generating ANA-like candidate structures from RNA PDB inputs.

ANA, or arabino nucleic acid, is chemically close to RNA, but it cannot be modeled responsibly by simply renaming RNA residues or performing blind atom replacement. Early Digital Polymerase attempts showed that residue-local replacement can generate plausible local geometry while breaking polymer-chain continuity.

The ANA prototype therefore evolved through three stages:

```text
Prototype 002A   → residue-local fragment-guided RNA → ANA reconstruction
Prototype 002A.1 → chain-continuity validation patch
Prototype 002A.2 → chain-preserving ANA reconstruction
```

The currently recommended version is:

```text
Prototype 002A.2
```

because it preserves RNA polymer-chain continuity while introducing ANA-like local sugar/backbone geometry.

---

## Why This Prototype Exists

The ANA converter was developed after the first RNA → HNA work showed that short-mer template-guided reconstruction could work, but larger RNA structures and incomplete XNA templates required a more flexible strategy.

For ANA, only a 4-mer ANA fragment was initially available:

```text
1ho6_ANApart.pdb
```

This meant that the converter could not perform full-template reconstruction for longer RNA inputs.

Instead, the ANA prototype tested whether a shorter XNA template could be used as a **local geometry donor**.

This produced a crucial Digital Polymerase lesson:

```text
local geometry placement is not enough
polymer-chain continuity must be validated explicitly
```

---

## Input Requirements

### Source RNA PDB

Recommended source RNA input should contain:

- standard RNA residues: `A`, `U`, `G`, `C`
- PDB coordinate records
- reasonably complete sugar/phosphate atoms
- expected chain atoms such as:

```text
P
OP1 / OP2 or O1P / O2P
O5'
C5'
C4'
O4'
C3'
O3'
C2'
O2'
C1'
```

The benchmark dataset used RNA fragments extracted from an HH-type I ribozyme.

### ANA Template PDB

Initial ANA template:

```text
1ho6_ANApart.pdb
```

Observed template characteristics:

```text
Length: 4 residues
Residue names: GAO, UAR, CAR, CAR
Available base classes: G-like, U-like, C-like
A-like template: absent
```

Because an A-like ANA residue was absent, A residues used a purine fallback template.

---

## Prototype 002A: Residue-Local Fragment-Guided Reconstruction

### Method

The original ANA converter attempted residue-local reconstruction.

For each RNA residue:

1. infer the RNA base identity
2. select a local ANA template residue
3. align the ANA template residue onto the RNA residue frame using Kabsch alignment
4. transform ANA backbone atoms into the RNA local frame
5. preserve RNA nucleobase atoms
6. export an ANA-like candidate residue

### Template selection policy

| RNA base | Output residue | ANA template donor | Note |
|---|---|---|---|
| `A` | `AAR` | `GAO` | purine fallback |
| `U` | `UAR` | `UAR` | exact base-class template |
| `G` | `GAO` | `GAO` | exact base-class template |
| `C` | `CAR` | `CAR` | exact base-class template |

### Main limitation

The method transformed residues independently.

This caused the output to preserve local ANA-like geometry but break inter-residue polymer-chain continuity.

---

## Prototype 002A.1: Chain-Continuity Validation Patch

Prototype 002A.1 did not attempt to fix geometry. It added explicit validation.

The patch added report-level checks for:

```text
O3′(i) → P(i+1)
P(i) → O5′(i)
```

This revealed that the original residue-local approach failed to preserve polymer-chain continuity.

Example outcome from the ANA scaling benchmark:

```text
source RNA O3′→P: PASS
converted ANA-like output O3′→P: FAIL
```

This was a productive failure because it made the next requirement explicit:

```text
Digital Polymerase needs chain-aware or chain-preserving reconstruction.
```

---

## Prototype 002A.2: Chain-Preserving ANA Reconstruction

Prototype 002A.2 is the currently recommended ANA prototype.

### Core idea

Instead of replacing the entire ANA-like backbone residue-by-residue, the converter preserves the RNA chain framework and introduces ANA-like local geometry more conservatively.

The design rule became:

```text
preserve chain continuity first
introduce XNA-local geometry second
validate explicitly
```

### What is preserved

Prototype 002A.2 preserves source RNA chain-continuity atoms, including:

```text
P
phosphate oxygens
O5'
C5'
C4'
O4'
C3'
O3'
C1'
```

It also preserves RNA nucleobase atoms.

### What is introduced or modified

The prototype introduces ANA-like local sugar/backbone geometry from the ANA fragment template, especially around the local sugar configuration.

The exact local atom policy may evolve as more ANA templates become available.

---

## Conversion Level

Digital Polymerase recognizes four conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Local atom and residue identity transformation.

3. **Geometric candidate reconstruction**  
   Coordinate-level candidate generation using templates and transformations.

4. **Physically refined modeling**  
   Energy minimization, molecular dynamics, force-field validation, and expert inspection.

Prototype 002A.2 operates at:

```text
Level 3: geometric candidate reconstruction
```

It does **not** perform:

```text
Level 4: physically refined modeling
```

---

## Benchmark Dataset

The ANA prototype was tested on RNA fragments extracted from an HH-type I ribozyme.

| Input | Length | Sequence |
|---|---:|---|
| `RNA-8mer.pdb` | 8 nt | `CUAGGCUC` |
| `RNA-12mer.pdb` | 12 nt | `CUAGGCUCGAAA` |
| `RNA-16mer.pdb` | 16 nt | `ACCACCUAGGCUCGAA` |
| `RNA-22mer.pdb` | 22 nt | `AUACGACCACCUAGGCUCGAAA` |
| `RNA-34mer.pdb` | 34 nt | `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC` |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 nt | full reduced HH ribozyme RNA |

---

## Benchmark Progression

### Prototype 002A result

The converter generated ANA-like candidate outputs across all tested sizes, but inter-residue chain continuity was not enforced.

### Patch 002A.1 result

Chain-continuity validation showed that many or nearly all O3′→P links failed in the converted outputs.

This confirmed:

```text
local residue reconstruction ≠ valid polymer reconstruction
```

### Patch 002A.2 result

After switching to chain-preserving reconstruction, visual inspection in PyMOL showed coherent continuous ANA-like chains for:

```text
8-mer
34-mer
111-mer
```

The output looked visually coherent rather than fragmented into residue-local debris.

---

## Example Usage

Recommended current script path:

```text
src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py
```

Example command:

```bash
python src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py \
  --rna benchmarks/ana_fragment_scaling/inputs/RNA-8mer.pdb \
  --template benchmarks/ana_fragment_scaling/templates/1ho6_ANApart.pdb \
  --output benchmarks/ana_fragment_scaling/outputs/converted_ana_RNA-8mer_002A2.pdb \
  --report benchmarks/ana_fragment_scaling/reports/conversion_report_RNA-8mer_002A2.md
```

For the 111-mer benchmark:

```bash
python src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py \
  --rna benchmarks/ana_fragment_scaling/inputs/8t5o-HH-typeI-111mer-full.pdb \
  --template benchmarks/ana_fragment_scaling/templates/1ho6_ANApart.pdb \
  --output benchmarks/ana_fragment_scaling/outputs/converted_ana_8t5o-HH-typeI-111mer-full_002A2.pdb \
  --report benchmarks/ana_fragment_scaling/reports/conversion_report_8t5o-HH-typeI-111mer-full_002A2.md
```

---

## Validation Metrics

The ANA prototype reports or should report:

- converted residue count
- source sequence
- template residue usage
- local anchor RMSD
- O3′(i)→P(i+1) chain continuity
- P(i)→O5′ intra-residue linkage
- residue completeness
- missing atoms
- scientific warnings and limitations

The most important validation lesson from ANA is:

```text
low local RMSD alone is not enough
```

---

## Visual Inspection

Prototype 002A.2 outputs were visually inspected in PyMOL.

Observed visual behavior:

- 8-mer: coherent curved chain
- 34-mer: continuous folded chain-like structure
- 111-mer: globally coherent ribozyme-scale structure

This visual coherence is encouraging, but it does not replace physical validation.

---

## Scientific Interpretation

Correct description:

```text
ANA-like candidate structures generated through chain-preserving fragment-guided reconstruction.
```

Incorrect descriptions:

```text
validated ANA molecules
experimentally confirmed ANA ribozymes
MD-ready ANA structures
proof of ANA biological function
```

The generated structures are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No molecular dynamics validation.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- Residue names are provisional.
- A-like ANA geometry is absent in the original 4-mer template.
- A residues use a purine fallback donor.
- RNA bases are preserved.
- ANA stereochemistry and sugar geometry require expert inspection.
- Biological function is not implied.
- Molecular viewers may infer nonstandard bonds differently.

---

## Recommended Downstream Checks

Before scientific interpretation, perform:

1. visual inspection in PyMOL, ChimeraX, Discovery Studio, VMD, or Mol*
2. residue completeness checks
3. bond length and angle checks
4. stereochemical inspection of ANA-like sugar geometry
5. clash detection
6. topology/parameter compatibility checks
7. energy minimization
8. restrained relaxation if force-field support is available
9. molecular dynamics only after topology validation

---

## Relationship to Other Prototypes

Prototype 002A sits between the early HNA proof of concept and the later FANA converter.

```text
Prototype 001: RNA → HNA template-guided reconstruction
Benchmark 002: HH ribozyme RNA → HNA scaling failure
Prototype 002A: RNA → ANA fragment-guided reconstruction
Patch 002A.1: ANA chain-continuity validation
Patch 002A.2: ANA chain-preserving reconstruction
Prototype 003A: RNA → FANA chain-preserving reconstruction
```

The ANA arc created the central rule used by later converters:

```text
Do not sacrifice chain continuity for local XNA geometry.
```

---

## Suggested Repository Placement

```text
src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py
docs/prototype_002A_rna_to_ana_fragment_guided.md
benchmarks/ana_fragment_scaling/
```

---

## Current Status

Prototype 002A.2 is a visually coherent experimental candidate generator.

It should remain under:

```text
src/digital_polymerase/prototypes/
```

until the project adds:

- shared core parser/alignment/validation modules
- topology/connectivity handling
- force-field or minimization workflows
- stronger structural chemistry validation

---

## Final Note

Prototype 002A is one of the most important Digital Polymerase development arcs because it converted a failure into a design principle.

It taught the project that:

```text
a converter is not successful just because it writes a PDB
a converter must preserve polymer logic and report its own limitations
```
