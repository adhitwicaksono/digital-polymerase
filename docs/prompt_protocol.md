# Prompt Protocol for Digital Polymerase

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Purpose:** AI-assisted development protocol for nucleic acid → XNA converter prototypes  
**Status:** Living document

---

## Why This Protocol Exists

Digital Polymerase uses AI-assisted reasoning and coding during early prototype development. However, nucleic acid conversion is not a simple text transformation or atom-renaming task.

A request such as:

```text
Convert this RNA structure into HNA.
```

is scientifically underspecified.

For Digital Polymerase, the safer and more useful approach is:

```text
Compare the source and target structures first.
Infer the chemical and geometric transformation logic.
Then generate a constrained prototype.
Visualize, criticize, and iterate.
```

This protocol documents the development pattern used in **Prototype 001: RNA → HNA template-guided reconstruction** and should guide future NA → XNA converter development.

---

## Core Principle

> Compare → infer → implement → visualize → criticize → iterate → generalize.

Digital Polymerase should not begin by assuming that one nucleic acid polymer can be converted into another by direct atom substitution.

Instead, each conversion should begin with structure comparison and end with cautious candidate-model generation.

---

## Recommended Prompting Workflow

### Step 1 — Establish the Scientific Context

Start by grounding the AI model in the correct meaning of XNA.

Example prompt:

```text
What do you know about xeno nucleic acids, especially XNA as alternative genetic polymers rather than Microsoft XNA?
```

Then narrow the discussion:

```text
We are interested in xeno nucleic acids such as HNA, FANA, TNA, CeNA, ANA, GNA, PNA, and related alternative nucleic acid chemistries.
```

Purpose:

- avoid ambiguity around the acronym XNA
- establish the synthetic biology / xenobiology context
- make the AI reason about nucleic acid chemistry, not unrelated software

---

### Step 2 — Provide a Source Structure

Upload or provide the source nucleic acid structure.

Example prompt:

```text
Here is an RNA 8-mer PDB structure.
Before writing any code, analyze the structure residue by residue.

Please identify:
- residue names
- chain ID
- residue numbering
- sequence
- sugar/backbone atoms
- nucleobase atoms
- whether hydrogens are present
- whether the file appears experimental or modeled
```

Purpose:

- force the model to inspect the actual input
- prevent hallucinated assumptions about atom names or residue numbering
- identify whether the input is suitable for conversion

---

### Step 3 — Provide a Target XNA Template

Upload or provide an experimentally derived or curated target XNA structure.

Example prompt:

```text
Here is an HNA 8-mer PDB structure for comparison.
Analyze the target structure and identify what makes it different from RNA.

Please identify:
- target residue names
- target backbone atoms
- target sugar/backbone topology
- base attachment atoms
- template residue numbering
- whether the structure contains HETATM records
- any target-specific atoms such as C6'
```

Purpose:

- make the target polymer concrete
- avoid treating the XNA as a vague symbolic label
- derive conversion logic from real coordinates whenever possible

---

### Step 4 — Ask for Conversion Requirements Before Code

Do not ask for code immediately.

First ask the model to infer what must change.

Example prompt:

```text
Now that you have inspected both the RNA source and HNA target structures,
scrutinize what needs to be converted at the atomic, topological, and geometric levels.

Do not write code yet.

Please identify:
- atoms to keep
- atoms to remove
- atoms to rebuild
- residue renaming rules
- backbone differences
- base-attachment differences
- ring or scaffold differences
- whether direct atom insertion is chemically reasonable
- whether template-guided reconstruction is safer
```

Purpose:

- reveal hidden assumptions
- identify likely failure modes
- separate symbolic conversion from geometric reconstruction

---

### Step 5 — Classify the Conversion Level

Digital Polymerase recognizes several conversion levels.

Before implementing, identify which level the prototype is attempting.

```text
Classify this conversion according to the Digital Polymerase conversion levels:

1. Symbolic conversion
2. Topological conversion
3. Geometric reconstruction
4. Physically refined modeling

Explain what this prototype can and cannot claim.
```

Recommended interpretation for Prototype 001:

```text
RNA → HNA template-guided reconstruction is Level 3: geometric reconstruction.
It is not Level 4 because it does not perform molecular mechanics refinement or MD validation.
```

Purpose:

- prevent overclaiming
- make documentation scientifically defensible
- clarify whether the output is a candidate structure or a validated model

---

### Step 6 — Request a Minimal Prototype

Only after the comparison and conversion logic are clear, request code.

Example prompt:

```text
Write a minimal Python prototype that performs template-guided RNA → HNA reconstruction.

The script should:
- parse RNA and HNA PDB files
- separate backbone atoms from base atoms
- extract the HNA backbone from the template
- preserve the RNA base atoms and sequence order
- align RNA base atoms into the HNA residue frame using local anchor atoms
- use Kabsch alignment for coordinate transformation
- combine HNA backbone atoms with transformed RNA base atoms
- export a candidate HNA-like PDB
- clearly mark the output as computational and unvalidated
```

Recommended constraints:

```text
Do not hardcode input/output paths.
Use command-line arguments.
Do not claim that the structure is physically valid.
Do not silently convert U to T unless the methyl group is modeled or the option is explicitly label-only.
```

Purpose:

- produce a reusable script
- avoid environment-specific paths
- enforce scientific caution

---

### Step 7 — Visualize the Output

The first generated structure should be visualized immediately.

Recommended viewers:

- PyMOL
- ChimeraX
- VMD
- Mol*
- Discovery Studio Visualizer

Example prompt after visualization:

```text
I visualized the output.
The sugar/backbone still looks like RNA.
What went wrong?
```

or:

```text
The backbone looks distorted and sticks close to the bases.
Diagnose the likely source of the geometric failure.
```

Purpose:

- use visualization as a reality check
- expose failures that code alone may not reveal
- force iterative correction

---

### Step 8 — Criticize Failures Scientifically

When the output looks wrong, describe the failure specifically.

Useful failure descriptions:

```text
The sugar backbone still looks pentose-like.
```

```text
The inserted atom does not create a proper target scaffold.
```

```text
The backbone trajectory is distorted.
```

```text
The bases are oriented incorrectly relative to the backbone.
```

```text
The molecular viewer infers impossible bonds.
```

Ask the AI to diagnose, not merely patch.

Example prompt:

```text
Do not just patch the code.
Explain why the previous geometric model failed chemically and structurally.
Then propose a safer reconstruction strategy.
```

Purpose:

- prevent random code mutation
- identify whether the model is using the wrong chemical assumption
- improve the underlying algorithm

---

### Step 9 — Prefer Template-Guided Reconstruction When Needed

If direct geometry fails, shift toward template-guided reconstruction.

Example prompt:

```text
The direct geometric approach is failing.
Use the experimental HNA structure as a backbone template.

Build a template-guided converter that:
- takes the HNA backbone directly from the template
- preserves the RNA base identity
- aligns the RNA bases onto the HNA residue geometry
- transplants the transformed bases onto the HNA backbone
- exports a candidate PDB
```

For Prototype 001, the successful strategy was:

```text
HNA backbone from experimental template
+
RNA base atoms transformed by local Kabsch alignment
=
candidate HNA-like PDB structure
```

Purpose:

- avoid forcing incompatible source geometry into target chemistry
- leverage real target structures
- make conversion more physically plausible at the starting-model level

---

### Step 10 — Add Explicit Scientific Warnings

Every prototype output should include warnings in the documentation and, when possible, inside the PDB `REMARK` lines.

Recommended warning:

```text
This structure is a computational candidate generated by template-guided reconstruction.
It has not been energy-minimized, force-field-validated, or experimentally verified.
```

Recommended README language:

```text
Digital Polymerase does not claim that a converted structure is automatically physically valid,
chemically complete, or biologically functional.
```

Purpose:

- protect the project from overclaiming
- make the tool useful without pretending it is a validated modeling package

---

## General Prompt Template for Future Converters

Use this template for future NA → XNA prototypes.

```text
We are developing a Digital Polymerase converter from [SOURCE_NA] to [TARGET_XNA].

Input:
1. A source PDB structure of [SOURCE_NA]
2. A target/template PDB structure of [TARGET_XNA]
3. Desired rule: preserve [sequence/base identity/base pairing/etc.]

Task:
First, analyze both structures residue-by-residue and atom-by-atom.
Do not write code yet.

Identify:
- source residue names
- target residue names
- source backbone atoms
- target backbone atoms
- source base atoms
- target base attachment atoms
- residue naming conventions
- topology differences
- ring/backbone differences
- atoms to remove, retain, rename, or rebuild
- whether conversion should be symbolic, topological, geometric, or template-guided

Then propose the safest conversion algorithm.

Avoid naive atom insertion unless chemically justified.
Prefer template-guided reconstruction when source and target backbone geometries differ strongly.

After that, write a Python prototype that:
- parses PDB files
- separates backbone and base atoms
- extracts target backbone template
- aligns source bases to target attachment geometry
- transplants transformed bases
- exports a candidate PDB
- reports validation metrics
- marks output as requiring molecular dynamics or structural validation
```

---

## Minimal Code-Generation Prompt

Use this after the structural comparison is complete.

```text
Now write a minimal but GitHub-ready Python prototype.

Requirements:
- no hardcoded local paths
- command-line interface with argparse
- input source PDB argument
- input target template PDB argument
- output PDB argument
- optional Markdown report argument
- clear residue conversion policy
- clear warnings in output PDB REMARK lines
- no claim of physical or biological validity

The script should be readable and modular enough to later refactor into:
- core PDB parser
- atom classifier
- alignment module
- converter module
- validator module
```

---

## Recommended Validation Prompt

Use this after a prototype produces an output structure.

```text
Evaluate the converted structure critically.

Check:
- residue count
- residue naming
- missing atoms
- backbone atom completeness
- base atom completeness
- local alignment quality
- obvious clashes
- suspicious bond lengths
- suspicious base orientations
- whether the structure needs CONECT records
- whether molecular viewers may infer wrong bonds

Do not assume success just because the script runs.
```

---

## Lessons from Prototype 001

The RNA → HNA prototype produced several important lessons:

### 1. Naive atom insertion is unsafe

Simply inserting `C6'` into RNA did not correctly create an HNA-like structure.

### 2. Direct geometric construction can distort the model

Even when a six-membered ring was attempted, the backbone trajectory and base orientation could become unrealistic.

### 3. Source and target base orientation may differ strongly

RNA and HNA can position bases differently relative to the backbone. This makes simple coordinate editing unreliable.

### 4. Experimental XNA templates are valuable

Using an experimental HNA structure as a backbone template gave a much more plausible starting point.

### 5. The correct output is a candidate, not proof

The generated structure is useful for visualization and downstream modeling, but it is not evidence of stability, function, replication, or biological relevance.

---

## Documentation Rule

Every prototype should have:

```text
docs/prototype_XXX_source_to_target.md
examples/source_to_target_shortmer/README.md
```

Each prototype document should include:

- scope
- method overview
- conversion level
- input requirements
- output interpretation
- base policy
- limitations
- validation recommendations
- future improvements

---

## Naming Convention

Recommended prototype naming:

```text
prototype_001_rna_to_hna.md
prototype_002_rna_to_fana.md
prototype_003_rna_to_tna.md
```

Recommended script naming:

```text
rna_to_hna_template_based.py
rna_to_fana_template_based.py
rna_to_tna_template_based.py
```

Recommended example folder naming:

```text
examples/rna_to_hna_8mer/
examples/rna_to_fana_shortmer/
examples/rna_to_tna_shortmer/
```

---

## Development Philosophy

Digital Polymerase should grow from specific, well-documented prototypes toward a generalized conversion engine.

Recommended progression:

1. one carefully documented short-mer prototype
2. shared parsing and alignment utilities
3. additional template-guided converters
4. validation metrics
5. polymer metadata database
6. generalized NA → XNA reconstruction engine
7. downstream MD / force-field workflow compatibility

The project should prioritize scientific honesty over dramatic claims.

---

## Final Reminder

Do not prompt the AI with:

```text
Convert this RNA into HNA.
```

Prompt it with:

```text
Analyze the source RNA and target HNA structures.
Infer the atomic, topological, and geometric differences.
Then design the safest template-guided reconstruction workflow.
Generate a candidate model and clearly mark it as requiring validation.
```

That is the Digital Polymerase way.
