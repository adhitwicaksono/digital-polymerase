# Benchmark 002: HH Ribozyme RNA → HNA Conversion Failure Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 002  
**Input case:** HH-type I ribozyme RNA structure  
**Conversion attempt:** RNA → HNA  
**Status:** Failure benchmark / stress-test case  
**Recommended interpretation:** Not a validated converter output

---

## Summary

Benchmark 002 tests whether the early RNA → HNA conversion logic from **Prototype 001** can scale from a short 8-mer RNA example to a larger folded RNA structure.

The input structure is an HH-type I ribozyme RNA PDB structure. The goal was to test whether Digital Polymerase could generate an HNA-like candidate structure while preserving the global folded architecture of a larger RNA.

The result was informative but not successful.

This benchmark shows that:

> A short-template RNA → HNA reconstruction strategy does not generalize directly to large folded RNA structures.

It also shows that local sugar-ring editing can preserve the global RNA fold visually, but this produces a **pseudo-HNA-like perturbation**, not a chemically validated HNA structure.

---

## Files Involved

Recommended benchmark folder:

```text
benchmarks/hh_ribozyme_8t5o/
├── README.md
├── input/
│   └── 8t5o-HH-typeI.pdb
├── failed_outputs/
│   ├── 8t5o_converted_HNA.pdb
│   └── 8t5o_HNA_structure_preserved.pdb
├── scripts_archive/
│   └── rna_to_hna_structure_preserving.py
└── notes/
    └── benchmark_002_hh_ribozyme_failure_notes.md
```

### Input

```text
6 - 8t5o-HH-typeI.pdb
```

Large folded RNA input structure used as the stress-test case.

### Failed / experimental outputs

```text
7 - 8t5o_converted_HNA.pdb
```

Attempted HNA conversion output generated after applying earlier RNA → HNA logic to a larger RNA structure.

```text
8 - 8t5o_HNA_structure_preserved.pdb
```

Structure-preserving pseudo-HNA output generated using local in-place sugar modification.

### Script

```text
8 - rna_to_hna_structure_preserving.py
```

Experimental structure-preserving RNA → HNA script.

---

## Background

Prototype 001 showed that a short RNA 8-mer can be converted into an HNA-like candidate structure using a template-guided strategy:

1. use an experimental HNA 8-mer as a backbone template
2. preserve RNA nucleobase identity
3. align RNA bases to HNA residue geometry
4. transplant the transformed bases onto the HNA backbone
5. export a candidate HNA-like PDB structure

This worked as a **short-oligomer proof-of-concept**.

Benchmark 002 asked whether the same conceptual direction could be extended to a larger folded RNA, specifically an HH-type I ribozyme.

---

## Main Question

Can a larger folded RNA structure be converted into an HNA-like structure while preserving its global fold?

More specifically:

- Can short-template HNA geometry be generalized to a large RNA?
- Can local sugar-ring modification preserve ribozyme-like tertiary structure?
- Can the output be interpreted as a meaningful HNA candidate?
- What failure modes appear when moving from short oligomers to folded RNAs?

---

## Attempt 1: Scaling the Short-Template Logic

### Method

The first direction attempted to extend the earlier short-mer RNA → HNA logic to the larger HH ribozyme input.

Conceptually, this was based on the successful Prototype 001 idea:

```text
HNA backbone template
+
RNA nucleobases
+
local alignment / transplantation
=
candidate HNA-like structure
```

### Why It Failed

The earlier 8-mer approach depends on having a comparable HNA template with residue-by-residue geometry that can meaningfully guide reconstruction.

For a larger folded ribozyme, an 8-mer HNA template is insufficient because:

- the target RNA has a complex folded tertiary structure
- there is no equivalent full-length HNA ribozyme template
- short local backbone geometry cannot automatically preserve long-range RNA folding
- residue-by-residue transplantation does not solve global topology
- local success does not guarantee global structural coherence

### Lesson

Short-template reconstruction is useful for controlled short oligomers, but it does not directly scale to large folded RNAs.

Digital Polymerase should treat this as a **template coverage problem**:

> Template-guided reconstruction requires compatible target-template coverage.

For large RNAs, this may require:

- segment-wise reconstruction
- longer XNA template libraries
- fragment-based assembly
- constrained optimization
- molecular mechanics refinement
- explicit tertiary-structure preservation rules

---

## Attempt 2: Structure-Preserving Local Sugar Modification

### Method

The second direction attempted to preserve the global RNA structure by modifying each residue locally.

The script strategy was:

```text
Keep C1' fixed
Keep C3', C4', C5' mostly fixed
Insert C6'
Adjust O4'
Minimally adjust C2'
Preserve base positions and approximate backbone trajectory
```

The purpose was to avoid destroying the larger ribozyme fold.

### What Worked

This strategy was useful as a stress-test because it attempted to preserve:

- global RNA fold
- base positions
- stacking arrangement
- C1' base-attachment positions
- approximate backbone trajectory

This may be useful for generating a **local perturbation model**.

### Why It Is Not a Successful HNA Conversion

Despite preserving the apparent global fold, this output should not be treated as a validated HNA model.

Problems include:

1. **It is an in-place local edit, not true template-guided HNA reconstruction.**  
   The method modifies RNA residues locally rather than rebuilding them from a complete HNA backbone template.

2. **RNA-like features may remain.**  
   Some RNA atoms and local geometries can remain embedded in the output.

3. **The residue labels may overclaim chemistry.**  
   The script maps RNA `U` to HNA `T`, but label conversion does not automatically add the thymine methyl group.

4. **The output is not energy-minimized.**  
   Local atom placement may introduce unrealistic bond lengths, angles, torsions, or clashes.

5. **The output is not force-field validated.**  
   No AMBER, GROMACS, or other molecular mechanics parameterization is performed.

6. **Connectivity may be viewer-dependent.**  
   Without explicit connectivity records or validated residue templates, molecular viewers may infer bonds incorrectly.

7. **Biological function is not implied.**  
   The output does not indicate ribozyme activity, folding stability, replication, catalysis, or experimental feasibility.

### Better Interpretation

This output should be described as:

> a fold-preserving pseudo-HNA local perturbation model

Not:

> a successfully converted HNA ribozyme

---

## Conversion-Level Classification

Digital Polymerase recognizes several conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Reassignment of residue identity, atom naming, backbone topology, and linkage patterns.

3. **Geometric reconstruction**  
   Candidate 3D structure generation using templates, coordinate transformation, or local rebuilding.

4. **Physically refined modeling**  
   Energy minimization, molecular dynamics, force-field validation, and expert chemical inspection.

Benchmark 002 reaches only an unstable boundary between:

```text
Level 2: topological/local editing
```

and

```text
Level 3: geometric pseudo-reconstruction
```

It does **not** reach:

```text
Level 4: physically refined modeling
```

Therefore, the output should not be treated as a validated HNA structure.

---

## Key Failure Modes

### 1. Template Scaling Failure

A short HNA template cannot automatically provide valid geometry for a large folded RNA.

The 8-mer case is a controlled toy model. The HH ribozyme is a real folded RNA architecture.

### 2. Local Chemistry vs Global Structure Conflict

Changing sugar/backbone chemistry changes local geometry.

But preserving a ribozyme fold requires maintaining:

- base stacking
- tertiary contacts
- backbone path
- catalytic-site geometry
- local torsion compatibility
- long-range spatial constraints

A local edit can preserve the fold visually while still producing chemically questionable residues.

### 3. Residue Label vs Actual Chemistry

Changing residue labels from:

```text
U → 6HT
```

does not chemically convert uracil into thymine unless the methyl group and geometry are explicitly modeled.

For chemically cautious workflows, the safer default should be:

```text
U → 6HU
```

unless the script performs true uracil-to-thymine chemistry.

### 4. Lack of Connectivity Control

Nonstandard XNA residues may require explicit bond definitions.

Without proper connectivity:

- viewers may infer impossible bonds
- rings may be misread
- sugar/backbone topology may be displayed incorrectly
- downstream MD preparation may fail

### 5. No Physical Relaxation

Large structure conversion likely requires:

- constrained minimization
- molecular dynamics relaxation
- steric clash removal
- torsion correction
- force-field parameterization

Without these steps, large converted structures remain speculative.

---

## Scientific Conclusion

Benchmark 002 is a **productive failure**.

It shows that Digital Polymerase cannot simply scale an 8-mer RNA → HNA conversion into a folded ribozyme.

The benchmark clarifies that large structured RNA → XNA conversion needs a different strategy from short-mer conversion.

The correct conclusion is:

> Short-mer template-guided reconstruction is promising, but large folded RNA conversion requires segment-wise, constraint-aware, and validation-heavy methods.

---

## Recommended Repository Status

Do **not** add the file 8 structure-preserving script as a production converter.

Recommended status:

```text
experimental / archived / benchmark failure
```

Recommended placement:

```text
benchmarks/hh_ribozyme_8t5o/scripts_archive/rna_to_hna_structure_preserving.py
```

Recommended output placement:

```text
benchmarks/hh_ribozyme_8t5o/failed_outputs/
```

Do not place this script yet in:

```text
src/digital_polymerase/converters/
```

because it is not a validated general RNA → HNA converter.

---

## Recommended Next Strategies

### Strategy 1: Segment-Wise Template-Guided Reconstruction

Instead of converting the whole ribozyme at once, split the RNA into local windows:

```text
4-mer
6-mer
8-mer
10-mer
```

For each segment:

1. identify local RNA geometry
2. match to an HNA template fragment
3. reconstruct locally
4. stitch fragments with constraints
5. minimize the full structure

This may be more realistic than global one-shot conversion.

---

### Strategy 2: XNA Fragment Library

Build a small library of experimentally derived or curated HNA backbone fragments:

```text
HNA dinucleotide
HNA trinucleotide
HNA tetranucleotide
HNA 8-mer
```

Then use fragment matching to reconstruct local regions.

Possible matching criteria:

- base step geometry
- C1'–C1' distance
- phosphate spacing
- local backbone direction
- base-plane orientation
- torsion compatibility

---

### Strategy 3: Preserve Base Frame, Rebuild Backbone

For functional RNAs, base placement may be more important than preserving every original sugar atom.

A future method could:

1. preserve nucleobase planes and stacking
2. preserve key base-pairing or catalytic contacts
3. discard RNA sugar coordinates
4. rebuild the HNA backbone around the preserved base frame
5. apply constrained minimization

This may be more realistic than editing RNA sugar rings in place.

---

### Strategy 4: Constraint-Aware Optimization

Large RNA → XNA conversion should eventually include optimization constraints such as:

- keep base-pair hydrogen-bond distances near original values
- preserve selected catalytic residues
- preserve Mg²⁺-binding geometry if relevant
- minimize backbone strain
- avoid steric clashes
- maintain chain continuity

This may require integration with molecular mechanics tools.

---

### Strategy 5: Use Benchmark 002 as a Regression Test

Benchmark 002 should remain in the repository as a known difficult case.

A future converter should be tested against it with clear metrics:

- residue count preserved
- sequence preserved
- base frames preserved
- sugar/backbone topology valid
- no obvious clashes
- no impossible bonds
- reasonable local geometry
- successful energy minimization
- stable short MD relaxation

This benchmark should become a stress-test case for future versions.

---

## What This Benchmark Teaches Digital Polymerase

This benchmark adds an important rule:

> Short-mer success does not imply folded-RNA success.

Digital Polymerase should therefore support at least two development modes:

### Mode 1: Short-Oligomer Template Reconstruction

For controlled small systems such as:

```text
8-mer RNA → HNA
short RNA duplex → XNA duplex candidate
small single-stranded oligomer → XNA candidate
```

### Mode 2: Large Folded-RNA Stress Testing

For larger systems such as:

```text
hammerhead ribozyme
aptamers
riboswitch fragments
ribozymes
structured RNA domains
```

Mode 2 requires more constraints, more validation, and much more caution.

---

## Recommended Language for README or Roadmap

Add this idea to the roadmap:

```text
Benchmark 002 showed that RNA → HNA conversion does not scale trivially from short oligomers to folded RNAs. Future versions will distinguish short-mer template-guided reconstruction from larger structure-preserving or segment-wise reconstruction workflows.
```

---

## Recommended Commit Message

```bash
git add benchmarks/hh_ribozyme_8t5o/
git commit -m "Add HH ribozyme RNA-to-HNA failure benchmark"
```

---

## Final Note

Benchmark 002 should be treated as a success of the development process, not of the converter.

It did not produce a validated HNA ribozyme.

It produced something more valuable for this stage:

> a clear failure mode that defines the next algorithmic boundary for Digital Polymerase.
