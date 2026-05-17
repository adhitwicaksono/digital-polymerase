# Prototype 001: RNA → HNA Template-Guided Reconstruction

**Status:** Experimental proof-of-concept  
**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Current scope:** Short-oligomer candidate-structure generation

---

## Summary

Prototype 001 explores a template-guided method for converting a short RNA structure into an HNA-like candidate structure.

The prototype was developed from an 8-mer RNA input structure and an experimental 8-mer HNA template structure. Instead of attempting direct atom insertion or simple sugar editing, the current approach uses the HNA structure as a geometric backbone template and transplants the RNA nucleobases onto that backbone after local coordinate alignment.

This prototype demonstrates one of the central principles of **Digital Polymerase**:

> Compare source and target structures first, infer the transformation logic, then reconstruct candidate models using polymer-aware rules.

The output should be treated as a **computational candidate model**, not as a chemically validated or experimentally confirmed HNA molecule.

---

## Why Template-Guided Reconstruction?

Early RNA → HNA conversion attempts revealed that direct geometric editing is not sufficient.

Naive strategies such as simply inserting a `C6'` atom into an RNA ribose framework can preserve the appearance of a pentose-like sugar or distort the backbone. HNA has a different backbone geometry and different base-backbone orientation compared with RNA. Because of this, local atom editing can create visually and chemically implausible structures.

The successful prototype therefore uses a different strategy:

- take the backbone geometry from an experimental HNA structure
- preserve the source RNA sequence and nucleobases
- align RNA base atoms to the HNA template residue geometry
- transplant the transformed bases onto the HNA backbone
- export a candidate HNA-like PDB structure

This is a **template-guided reconstruction** approach, not a one-to-one atom substitution.

---

## Conversion Level

Digital Polymerase recognizes several levels of nucleic acid conversion:

1. **Symbolic conversion**  
   Sequence or residue-label rewriting.

2. **Topological conversion**  
   Reassignment of residue type, backbone atoms, linkage pattern, and polymer architecture.

3. **Geometric reconstruction**  
   Generation of a candidate 3D structure using templates, coordinate alignment, or rebuilding rules.

4. **Physically refined modeling**  
   Energy minimization, molecular dynamics, force-field validation, and expert chemical inspection.

Prototype 001 operates mainly at **Level 3: geometric reconstruction**.

It does not perform molecular mechanics refinement or force-field validation.

---

## Method Overview

The current RNA → HNA prototype follows this workflow:

1. Parse the input RNA PDB structure.
2. Parse the experimental HNA template PDB structure.
3. Separate each residue into:
   - backbone atoms
   - nucleobase atoms
4. Extract the HNA backbone from each template residue.
5. Use local anchor atoms to align the RNA residue geometry onto the HNA residue geometry.
6. Transform the RNA base coordinates using Kabsch alignment.
7. Combine the HNA backbone with the transformed RNA base atoms.
8. Rename residues according to the selected base policy.
9. Export the reconstructed candidate model as a PDB file.
10. Optionally write a Markdown conversion report.

---

## Alignment Strategy

The prototype uses local residue-level alignment.

Default alignment anchors:

```text
C1'
C2'
C4'
```

These atoms are used to calculate an optimal rigid-body transformation between the source RNA residue and the target HNA template residue.

The transformed coordinates are then applied to the RNA base atoms, placing them into the HNA-like geometric frame.

This allows the method to preserve the source base identity while adapting the residue to the target backbone template.

---

## Base Policy

The default base policy is:

```text
preserve
```

Under this policy, RNA base chemistry is preserved:

```text
A → 6HA
U → 6HU
G → 6HG
C → 6HC
```

This avoids falsely implying that uracil has been chemically converted into thymine.

An optional label-level policy may be used:

```text
rna-to-dna-label
```

Under this policy:

```text
U → 6HT
```

However, this is only a residue-label conversion unless the thymine methyl group is explicitly modeled. For chemically cautious use, the recommended default is `preserve`.

---

## Example Usage

From the repository root:

```bash
python src/digital_polymerase/prototypes/rna_to_hna_template_based.py \
  --rna examples/rna_to_hna_8mer/input_rna_8mer.pdb \
  --template data/templates/hna_8mer.pdb \
  --output examples/rna_to_hna_8mer/converted_hna_candidate.pdb \
  --base-policy preserve \
  --report examples/rna_to_hna_8mer/conversion_report.md
```

Example with label-level uracil-to-thymine conversion:

```bash
python src/digital_polymerase/prototypes/rna_to_hna_template_based.py \
  --rna examples/rna_to_hna_8mer/input_rna_8mer.pdb \
  --template data/templates/hna_8mer.pdb \
  --output examples/rna_to_hna_8mer/converted_hna_candidate_u_to_t_label.pdb \
  --base-policy rna-to-dna-label \
  --report examples/rna_to_hna_8mer/conversion_report_u_to_t_label.md
```

---

## Expected Input

### RNA input

A PDB file containing a short RNA structure.

Recommended for Prototype 001:

- single chain
- short oligomer
- standard RNA residue names (`A`, `U`, `G`, `C`)
- reasonably complete base and sugar atoms
- no complex modified residues

### HNA template

A PDB file containing an HNA structure with comparable residue count or suitable template residues.

Recommended:

- experimentally derived or carefully curated HNA structure
- residue names such as `6HA`, `6HT`, `6HG`, `6HC`, or related HNA naming
- complete HNA backbone atoms
- consistent residue order

---

## Expected Output

The output is a candidate HNA-like PDB structure.

The output PDB includes `REMARK` lines describing that the structure is:

- template-guided
- computationally generated
- not energy-minimized
- not experimentally validated
- intended for downstream inspection and refinement

The output should be inspected before any scientific interpretation.

---

## Current Strengths

Prototype 001 successfully demonstrates:

- PDB parsing for short nucleic acid structures
- residue-level backbone/base separation
- use of an HNA backbone as a structural template
- local alignment using anchor atoms
- RNA base transplantation onto HNA geometry
- preservation of source sequence order
- candidate PDB export
- optional reporting

Most importantly, it demonstrates that **template-guided reconstruction is more plausible than naive atom insertion** for RNA → HNA conversion.

---

## Known Limitations

This prototype is experimental and has several limitations.

### Structural limitations

- The output is not energy-minimized.
- Bond lengths, bond angles, torsions, and stereochemistry are not fully validated.
- Inter-residue connectivity may not be explicitly encoded with `CONECT` records.
- Molecular viewers may infer bonds differently for nonstandard residues.
- Base placement depends strongly on template quality.

### Parser limitations

- The prototype is designed for simple PDB files.
- Complex multi-chain structures may require additional handling.
- Insertion codes, alternate locations, missing atoms, and nonstandard residue naming may require improvements.

### Chemical limitations

- The method does not automatically create or remove atoms needed for true base chemistry conversion.
- The default `preserve` policy retains RNA base chemistry.
- The `rna-to-dna-label` policy should be interpreted cautiously because label conversion does not equal chemical conversion.
- Force-field parameters are not generated.

### Biological limitations

- The generated structure is not evidence that the molecule is synthesizable.
- The generated structure is not evidence of stability, replication, catalysis, or biological function.
- Molecular dynamics and expert chemical evaluation are required before stronger claims can be made.

---

## Recommended Validation Steps

Before using any generated structure in a research workflow, perform:

1. Visual inspection in PyMOL, ChimeraX, VMD, or another molecular viewer.
2. Residue completeness checks.
3. Bond-length and bond-angle sanity checks.
4. Clash detection.
5. Comparison with the original HNA template.
6. Energy minimization using a suitable force field.
7. Molecular dynamics simulation if appropriate.
8. Expert review of backbone chemistry and stereochemistry.

---

## Development Notes

Prototype 001 emerged from an iterative AI-assisted development workflow:

1. Analyze XNA conceptually.
2. Upload and inspect a source RNA PDB.
3. Upload and inspect a target HNA PDB.
4. Identify atomic and topological differences.
5. Attempt direct conversion.
6. Visualize failure.
7. Revise the chemical model.
8. Attempt geometric reconstruction.
9. Visualize additional failure.
10. Shift to template-guided reconstruction.
11. Preserve sequence while transplanting bases onto the target backbone.
12. Mark output as a candidate structure requiring validation.

This workflow is now part of the Digital Polymerase development philosophy:

> Compare → infer → implement → visualize → criticize → iterate → generalize.

---

## Suggested Next Improvements

Short-term improvements:

- Add residue-level RMSD reporting.
- Improve base/backbone atom classification.
- Add missing-atom checks.
- Add chain-aware and insertion-code-aware parsing.
- Write explicit validation summaries.
- Add small test cases.
- Add `CONECT` record support for nonstandard residues.
- Add unit tests for Kabsch alignment and PDB parsing.

Medium-term improvements:

- Refactor shared utilities into `digital_polymerase.core`.
- Move conversion-specific logic into `digital_polymerase.converters`.
- Define polymer metadata in `polymer_db`.
- Add additional RNA → XNA prototypes.
- Create benchmark examples for FANA, TNA, CeNA, ANA, and GNA where suitable templates exist.

Long-term improvements:

- Generalize the template-guided reconstruction engine.
- Support XNA → XNA conversion.
- Integrate with molecular mechanics or MD preparation workflows.
- Explore compatibility with external XNA modeling and force-field tools.
- Develop life-threshold scenario modeling under the XNA World Project.

---

## Scientific Caution

Digital Polymerase is a dry-lab exploratory toolkit.

Prototype 001 should not be interpreted as a validated HNA modeling package. It is a proof-of-concept for generating candidate structures that may be useful for visualization, hypothesis generation, and downstream modeling.

Any structure produced by this prototype should be clearly described as:

> a template-guided computational candidate requiring further validation.

---

## Repository Placement

Suggested location:

```text
docs/prototype_001_rna_to_hna.md
```

Related files:

```text
src/digital_polymerase/prototypes/rna_to_hna_template_based.py
examples/rna_to_hna_8mer/README.md
data/templates/hna_8mer.pdb
```
