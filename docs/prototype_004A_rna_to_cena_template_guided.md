# Prototype 004A: RNA → CeNA Template-Guided / Chain-Preserving Reconstruction

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype:** 004A  
**Conversion:** RNA → CeNA  
**Method:** Full-template and chain-preserving CeNA-like scaffold reconstruction  
**Status:** Successful scalable candidate generator; not physically validated

---

## Summary

Prototype 004A is the Digital Polymerase prototype for generating CeNA-like candidate structures from RNA PDB inputs.

CeNA, or cyclohexenyl nucleic acid, uses a noncanonical scaffold that differs from canonical RNA. Prototype 004A therefore follows a mature Digital Polymerase strategy developed through the HNA, ANA, and FANA prototype arcs:

```text
preserve polymer-chain logic
insert target-specific XNA scaffold geometry
transform and preserve sequence/base identity
validate explicitly
inspect visually
```

The current prototype supports both short full-template conversion and longer chain-preserving conversion.

---

## Current Script

Recommended path:

```text
src/digital_polymerase/prototypes/rna_to_cena_template_guided.py
```

The script supports:

```text
--mode auto
--mode full-template
--mode chain-preserving
```

In `auto` mode:

```text
source RNA length <= CeNA template length → full-template mode
source RNA length > CeNA template length  → chain-preserving mode
```

---

## Template Used

Primary template:

```text
2H0N_CeNA_8mer_clean_ss.pdb
```

Observed properties:

```text
Length: 8 residues
Base-class sequence: GUGUACAC
Residue names: XGL, XTL, XAL, XCL
```

Key CeNA scaffold atoms:

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

Prototype 004A uses these atoms to define and validate local CeNA-like scaffold geometry.

---

## Why CeNA Needed Its Own Prototype

CeNA is not simply RNA with one atom renamed.

The CeNA scaffold contains a cyclohexenyl-like architecture, and the uploaded template includes local scaffold atoms such as:

```text
C6'
C7'
```

These require target-specific validation checks beyond the generic RNA-like sugar checks used for simpler nucleic acid analogs.

Prototype 004A therefore adds CeNA-specific scaffold validation:

```text
C4′ → C6′
C6′ → C7′
C7′ → C1′
```

---

## Method Modes

### Full-template mode

Used when a full-length CeNA template is available.

For the 8-mer benchmark:

```text
RNA-8mer.pdb
+
2H0N_CeNA_8mer_clean_ss.pdb
→
CeNA-like 8-mer candidate
```

In this mode:

1. the CeNA scaffold is taken directly from the template
2. RNA bases are transformed into the CeNA local frame
3. C1′→glycosidic-N distance is corrected using template-derived geometry
4. the output is validated and written as PDB

### Chain-preserving mode

Used when the RNA input is longer than the CeNA template.

For 12-mer through 111-mer inputs:

```text
RNA chain atoms preserved
+
CeNA local scaffold atoms inserted
+
RNA bases transformed onto CeNA-like local scaffold
```

In this mode:

1. RNA chain-continuity atoms are preserved
2. RNA O4′ is not preserved as a core scaffold atom
3. CeNA local scaffold atoms are transformed from the template into the RNA local frame
4. RNA bases are transformed onto the inserted CeNA-like local scaffold
5. base attachment is corrected
6. output geometry is validated

---

## Preserved RNA Chain Atoms

In chain-preserving mode, the converter preserves atoms such as:

```text
P
OP1 / OP2 or O1P / O2P
O5'
C5'
C4'
C3'
O3'
```

These atoms preserve the original RNA polymer path and prevent long-chain fragmentation.

---

## Introduced CeNA-Like Local Scaffold Atoms

The converter introduces local CeNA scaffold atoms from the template, including:

```text
C1'
C2'
C6'
C7'
```

These are inserted into the source RNA local frame using coordinate alignment.

---

## Base Transplant and Correction

RNA nucleobases are transformed onto the CeNA-like local scaffold.

Prototype 004A also corrects C1′→glycosidic-N distance using a template-derived target distance. This keeps base attachment within the expected local range while preserving the transformed base orientation as much as possible.

---

## Example Usage

### Auto mode

```bash
python src/digital_polymerase/prototypes/rna_to_cena_template_guided.py   --rna benchmarks/cena_scaling/inputs/RNA-34mer.pdb   --template benchmarks/cena_scaling/templates/2H0N_CeNA_8mer_clean_ss.pdb   --output benchmarks/cena_scaling/outputs/converted_cena_RNA-34mer_auto_004A.pdb   --report benchmarks/cena_scaling/reports/conversion_report_RNA-34mer_auto_004A.md   --mode auto
```

### Explicit chain-preserving mode

```bash
python src/digital_polymerase/prototypes/rna_to_cena_template_guided.py   --rna benchmarks/cena_scaling/inputs/8t5o-HH-typeI-111mer-full.pdb   --template benchmarks/cena_scaling/templates/2H0N_CeNA_8mer_clean_ss.pdb   --output benchmarks/cena_scaling/outputs/converted_cena_8t5o-HH-typeI-111mer-full_auto_004A.pdb   --report benchmarks/cena_scaling/reports/conversion_report_8t5o-HH-typeI-111mer-full_auto_004A.md   --mode chain-preserving
```

---

## Benchmark Results

Prototype 004A was tested on six RNA inputs.

| Input | Residues | Mode | Chain | Base attach | CeNA scaffold | Template/local RMSD mean/max (Å) | Base RMSD mean/max (Å) | C1′→N mean/max (Å) |
|---|---:|---|---|---|---|---:|---:|---:|
| `RNA-8mer` | 8 | `full-template` | `PASS` | `PASS` | `C4′→C6′ PASS` | 0.5160 / 0.5421 | NA | 1.4865 / 1.4965 |
| `RNA-12mer` | 12 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8029 / 0.9289 | 0.4679 / 0.7588 | 1.4938 / 1.4996 |
| `RNA-16mer` | 16 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8256 / 0.9389 | 0.5180 / 0.7531 | 1.4932 / 1.4996 |
| `RNA-22mer` | 22 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8373 / 0.9435 | 0.5788 / 0.7589 | 1.4928 / 1.4996 |
| `RNA-34mer` | 34 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.8255 / 0.9435 | 0.5651 / 0.7666 | 1.4932 / 1.4996 |
| `HH-111mer` | 111 | `chain-preserving` | `PASS` | `PASS` | `C4′→C6′ FAIL` | 0.7988 / 0.9389 | 0.5186 / 0.7666 | 1.4931 / 1.4996 |

All tested outputs passed the main validation checks.

---

## Validation Metrics

Prototype 004A reports:

- converted residue count
- source sequence
- template sequence
- actual conversion mode
- local template/scaffold RMSD
- base-transplant RMSD
- O3′(i)→P(i+1) chain continuity
- P(i)→O5′ linkage
- C1′→glycosidic-N base attachment
- C1′→C2′ local scaffold distance
- C2′→C3′ local scaffold distance
- C3′→C4′ local scaffold distance
- C4′→C5′ local scaffold distance
- C4′→C6′ CeNA scaffold distance
- C6′→C7′ CeNA scaffold distance
- C7′→C1′ CeNA scaffold distance
- per-residue template usage

---

## Visual Inspection

The following outputs were inspected visually:

```text
converted_cena_RNA-8mer_auto_004A.pdb
converted_cena_RNA-34mer_auto_004A.pdb
converted_cena_8t5o-HH-typeI-111mer-full_auto_004A.pdb
```

Observed:

- continuous backbone/cartoon paths
- coherent longer-chain structures
- no obvious residue explosion
- dense but connected atom/stick views
- 111-mer output preserved a global macromolecular architecture

This supports the conclusion that Prototype 004A works as a scalable CeNA-like candidate generator.

---

## Scientific Interpretation

Correct description:

```text
CeNA-like candidate structures generated through template-guided and chain-preserving local scaffold reconstruction.
```

Incorrect descriptions:

```text
validated CeNA structures
experimentally confirmed CeNA ribozymes
MD-ready CeNA polymers
proof of CeNA biological function
```

The outputs are computational candidates only.

---

## Known Limitations

- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- CeNA stereochemistry requires expert inspection.
- `XUL` is a provisional residue label when RNA `U` is preserved.
- Chain-preserving mode preserves the original RNA chain path, so large outputs may retain RNA-derived global geometry.
- The 111-mer output is a geometry candidate, not proof that CeNA can adopt or maintain that fold experimentally.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Relationship to Other XNA Prototypes

Current working candidate-generation families:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
```

Development pattern learned so far:

```text
local XNA geometry alone is not enough
polymer-chain continuity must be preserved or enforced
base attachment must be validated
target-specific scaffold geometry must be checked
visual inspection must follow report-level validation
```

---

## Recommended Repository Placement

```text
src/digital_polymerase/prototypes/rna_to_cena_template_guided.py
docs/prototype_004A_rna_to_cena_template_guided.md
benchmarks/cena_scaling/
```

---

## Current Status

Prototype 004A is a successful scalable CeNA-like candidate generator.

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

Prototype 004A marks the point where CeNA joined HNA, ANA, and FANA as working Digital Polymerase candidate-generation families.

It is still a candidate generator, not a physical validation engine — but it is now robust enough to archive as a major development milestone.
