# Prototype 005A: RNA → XyNA Chain-Preserving Local Sugar Reconstruction

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype:** 005A  
**Conversion:** RNA → XyNA  
**Method:** Chain-preserving local sugar reconstruction  
**Status:** Successful scalable candidate generator; not physically validated

---

## Summary

Prototype 005A is the Digital Polymerase prototype for generating XyNA-like candidate structures from RNA PDB inputs.

XyNA, or xylose-based nucleic acid, is a pentose-based XNA. Because of this, Prototype 005A uses a comparatively conservative strategy:

```text
preserve RNA chain/base framework
+
insert XyNA-like local C2′/O2′ geometry from template
+
validate polymer continuity and local sugar geometry
```

This approach worked from short RNA oligomers up to a 111-mer HH ribozyme-derived RNA input.

---

## Current Script

Recommended path:

```text
src/digital_polymerase/prototypes/rna_to_xyna_fragment_guided.py
```

The script supports:

```text
--mode auto
--mode chain-preserving
--mode full-template
```

In `auto` mode, the script currently defaults to:

```text
chain-preserving mode
```

because XyNA is pentose-based and can be approached as a local sugar-geometry reconstruction problem rather than a full scaffold replacement problem.

---

## Template Used

Primary template:

```text
2n4j_XyNA-8nt.pdb
```

Observed properties:

```text
Length: 8 residues
Base-class sequence: GUGUACAC
Residue names: 8XG, 8XU, 8XA, 8XC
```

Key XyNA/RNA-like atoms:

```text
P
O5'
C5'
C4'
O4'
C1'
C2'
O2'
C3'
O3'
```

The template is used to donate local XyNA-like `C2′/O2′` geometry.

---

## Why XyNA Was Easier Than HNA/CeNA

HNA and CeNA required more aggressive scaffold reconstruction because their backbone/scaffold geometries differ strongly from RNA.

XyNA is closer to RNA-like pentose geometry. Therefore, Prototype 005A can preserve most of the source RNA polymer framework and modify the local sugar geometry.

However, XyNA is still chemically distinct from RNA. The converter therefore does not simply rename residues; it uses template-derived geometry for the local `C2′/O2′` region and explicitly validates the resulting structure.

---

## Method

For each source RNA residue, Prototype 005A:

1. infers the RNA base identity
2. selects an XyNA template residue by base class
3. aligns the template local sugar geometry to the source RNA local frame
4. preserves RNA chain-continuity atoms
5. preserves RNA base atoms
6. inserts XyNA-like `C2′` and `O2′` geometry from the template
7. exports a XyNA-like candidate residue
8. validates chain continuity and local sugar geometry

---

## Preserved RNA Framework

In chain-preserving mode, the converter preserves atoms such as:

```text
P
OP1 / OP2 or O1P / O2P
O5'
C5'
C4'
O4'
C3'
O3'
C1'
```

It also preserves RNA nucleobase atoms.

---

## Inserted XyNA-Like Local Geometry

The converter replaces or inserts local sugar geometry around:

```text
C2'
O2'
```

using the XyNA template.

These atoms are transformed into the source RNA local coordinate frame using anchor atoms such as:

```text
C1'
C3'
C4'
O4'
```

---

## Optional Full-Template Mode

Prototype 005A also contains an optional full-template mode.

This mode:

1. takes the full XyNA scaffold from the template
2. transforms RNA bases onto the XyNA scaffold
3. corrects base attachment when needed
4. exports a short full-template candidate

This was tested as an optional 8-mer comparison, but the main scalable benchmark uses chain-preserving mode.

---

## Example Usage

### Auto mode

```bash
python src/digital_polymerase/prototypes/rna_to_xyna_fragment_guided.py \
  --rna benchmarks/xyna_scaling/inputs/RNA-34mer.pdb \
  --template benchmarks/xyna_scaling/templates/2n4j_XyNA-8nt.pdb \
  --output benchmarks/xyna_scaling/outputs/converted_xyna_RNA-34mer_auto_005A.pdb \
  --report benchmarks/xyna_scaling/reports/conversion_report_RNA-34mer_auto_005A.md \
  --mode auto
```

### Explicit chain-preserving mode

```bash
python src/digital_polymerase/prototypes/rna_to_xyna_fragment_guided.py \
  --rna benchmarks/xyna_scaling/inputs/8t5o-HH-typeI-111mer-full.pdb \
  --template benchmarks/xyna_scaling/templates/2n4j_XyNA-8nt.pdb \
  --output benchmarks/xyna_scaling/outputs/converted_xyna_8t5o-HH-typeI-111mer-full_auto_005A.pdb \
  --report benchmarks/xyna_scaling/reports/conversion_report_8t5o-HH-typeI-111mer-full_auto_005A.md \
  --mode chain-preserving
```

---

## Benchmark Results

Prototype 005A was tested on six RNA inputs.

| Input | Residues | Mode | Chain | Base attach | XyNA sugar | Local/template RMSD mean/max (Å) | C1′→N mean/max (Å) | C2′→O2′ mean/max (Å) |
|---|---:|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0923 / 0.1275 | 1.4768 / 1.4799 | 1.4332 / 1.4343 |
| `RNA-12mer` | 12 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0830 / 0.1275 | 1.4760 / 1.4799 | 1.4330 / 1.4343 |
| `RNA-16mer` | 16 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0864 / 0.1285 | 1.4762 / 1.4799 | 1.4331 / 1.4343 |
| `RNA-22mer` | 22 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0766 / 0.1275 | 1.4742 / 1.4799 | 1.4331 / 1.4343 |
| `RNA-34mer` | 34 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0760 / 0.1275 | 1.4744 / 1.4804 | 1.4330 / 1.4343 |
| `HH-111mer` | 111 | `chain-preserving` | `PASS` | `PASS` | `C2′→O2′ PASS` | 0.0781 / 0.1285 | 1.4745 / 1.4804 | 1.4330 / 1.4343 |

All tested outputs passed the main validation checks.

---

## Validation Metrics

Prototype 005A reports:

- converted residue count
- source sequence
- template sequence
- actual conversion mode
- local template/sugar RMSD
- O3′(i)→P(i+1) chain continuity
- P(i)→O5′ linkage
- C1′→glycosidic-N base attachment
- C1′→C2′ local sugar distance
- C2′→O2′ local sugar distance
- C2′→C3′ local sugar distance
- C1′→O4′ local sugar distance
- C4′→O4′ local sugar distance
- per-residue template usage

---

## Visual Inspection

The following outputs were inspected visually:

```text
converted_xyna_RNA-8mer_auto_005A.pdb
converted_xyna_RNA-34mer_auto_005A.pdb
converted_xyna_8t5o-HH-typeI-111mer-full_auto_005A.pdb
```

Observed:

- continuous backbone/cartoon paths
- coherent base placement
- no obvious residue explosion
- dense but connected atom/stick views
- 111-mer output preserved a global macromolecular architecture

This supports the conclusion that Prototype 005A works as a scalable XyNA-like candidate generator.

---

## Scientific Interpretation

Correct description:

```text
XyNA-like candidate structures generated through chain-preserving local sugar reconstruction.
```

Incorrect descriptions:

```text
validated XyNA structures
experimentally confirmed XyNA ribozymes
MD-ready XyNA polymers
proof of XyNA biological function
```

The outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- XyNA stereochemistry requires expert inspection.
- Chain-preserving mode preserves the original RNA chain path, so large outputs may retain RNA-derived global geometry.
- The 111-mer output is a geometry candidate, not proof that XyNA can adopt or maintain that fold experimentally.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Relationship to Other XNA Prototypes

Current working candidate-generation families:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
XyNA  → Prototype 005A
```

Development pattern learned so far:

```text
chain continuity must be preserved or enforced
local XNA geometry must be template-informed
base attachment and local scaffold geometry must be validated
visual inspection must follow report-level validation
```

---

## Recommended Repository Placement

```text
src/digital_polymerase/prototypes/rna_to_xyna_fragment_guided.py
docs/prototype_005A_rna_to_xyna_fragment_guided.md
benchmarks/xyna_scaling/
```

---

## Current Status

Prototype 005A is a successful scalable XyNA-like candidate generator.

It should remain under:

```text
src/digital_polymerase/prototypes/
```

until the project adds:

- shared core parser/alignment/validation modules
- explicit topology/connectivity support
- stronger stereochemical validation
- force-field or minimization workflows

---

## Final Note

Prototype 005A marks the point where XyNA joined HNA, ANA, FANA, and CeNA as working Digital Polymerase candidate-generation families.

It is still a candidate generator, not a physical validation engine — but it is now robust enough to archive as a major development milestone.
