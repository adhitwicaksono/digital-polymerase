# Digital Polymerase

**Digital Polymerase** is an early-stage dry-lab software project for exploring computational conversion and reconstruction between canonical nucleic acids (**DNA** and **RNA**) and xeno/synthetic nucleic acids (**XNA**) such as **HNA, ANA, FANA, TNA, GNA, CeNA**, and others.

The project focuses on **structure-guided nucleic acid transformation**, especially using **PDB structures as input and output**. Rather than treating conversion as a simple atom replacement problem, Digital Polymerase aims to develop template-guided and polymer-aware approaches for rebuilding nucleic acid structures across different backbone chemistries.

All generated structures should be interpreted as **computational candidate models**, not experimentally validated molecules. They require downstream structural validation such as geometry inspection, energy minimization, molecular dynamics simulation, and expert chemical evaluation.

---

## Vision

Digital Polymerase is part of the broader **XNA World Project**, a dry-lab framework for exploring alternative genetic polymers and their relevance to the functional thresholds of life.

Wet-lab xenobiology investigates whether XNA molecules can be synthesized, copied, evolved, and made functional. Digital Polymerase focuses on the complementary **in silico side**: building tools that help researchers model, transform, compare, and stress-test nucleic acid systems across natural and synthetic chemistries.

In this broader vision, Digital Polymerase serves as the **conversion and reconstruction engine**.

---

## Project Philosophy

Digital Polymerase does not assume that nucleic acid conversion is a one-step operation.

A conversion may occur at different levels:

1. **Symbolic conversion**  
   Rewriting a sequence or residue representation from one nucleic acid type to another.

2. **Topological conversion**  
   Reassigning residue identity, backbone atoms, linkage patterns, and polymer architecture.

3. **Geometric reconstruction**  
   Rebuilding a candidate 3D structure using structural templates, local alignment, or coordinate transformation.

4. **Physically refined modeling**  
   Evaluating and refining the candidate structure through molecular mechanics, energy minimization, molecular dynamics, and other validation workflows.

The current focus is on **template-guided geometric reconstruction**.

---

## Goals

- Convert nucleic acid structures between **DNA, RNA, and XNA types**
- Support **PDB-based structural transformation**
- Develop a modular framework for **polymer-aware parsing, alignment, rebuilding, and export**
- Preserve sequence information while allowing backbone chemistry to change
- Facilitate future modeling of **alternative nucleic acid worlds**
- Serve as a computational support layer for **xenobiology, synthetic biology, and origins-of-life research**

---

## Current Prototype

### Prototype 001: RNA → HNA template-guided reconstruction

The first working prototype explores conversion from an RNA 8-mer into an HNA-like candidate structure.

The successful strategy is **not naive atom insertion**. Instead, it uses a template-guided reconstruction workflow:

1. Parse the input RNA PDB structure
2. Parse an experimental HNA template PDB structure
3. Extract the HNA backbone geometry
4. Preserve the RNA base identities and sequence order
5. Align RNA base atoms onto the HNA template using local anchor atoms and Kabsch alignment
6. Transplant the transformed bases onto the HNA backbone
7. Export a candidate HNA PDB structure

This prototype demonstrates the project’s core principle:

> Compare source and target structures first, infer the transformation logic, then reconstruct candidate models using polymer-aware rules.

---

## Planned Features

### Core features

- Parse nucleic acid structures from **PDB**
- Detect and classify nucleic acid residue types
- Separate backbone atoms from base atoms
- Perform local coordinate alignment
- Export reconstructed structures as **PDB**

### Canonical nucleic acid conversion

- DNA → RNA
- RNA → DNA

### Extended XNA conversion

- DNA/RNA → XNA
- XNA → DNA/RNA
- XNA → XNA

Candidate XNA targets include:

- HNA
- ANA
- FANA
- TNA
- GNA
- CeNA
- LNA
- PNA

### Structural rebuilding

- Template-guided nucleic acid reconstruction
- Preservation of sequence order and approximate base arrangement
- Backbone-template transplantation
- Local base alignment
- Candidate PDB generation

### Downstream compatibility

Future versions may support integration with:

- molecular dynamics workflows
- energy minimization pipelines
- force-field parameterization tools
- external nucleic acid/XNA modeling tools

---

## Important Note

Digital Polymerase does **not** claim that a converted structure is automatically physically valid, chemically complete, or biologically functional.

A converted model should be interpreted as a **computationally generated candidate structure**, which may require:

- geometry refinement
- bond and angle validation
- stereochemical inspection
- energy minimization
- molecular dynamics simulation
- expert chemical evaluation
- comparison with experimental XNA structures

---

## Scope

This repository is intended as a **dry-lab computational tool**, not as a replacement for experimental validation.

Its long-term purpose is to help researchers explore possible structural scenarios in which functional XNA molecules may exist, interact, or be compared with canonical nucleic acids.

Digital Polymerase is especially intended for exploratory work in:

- xenobiology
- synthetic biology
- computational structural biology
- nucleic acid engineering
- alternative genetic polymers
- origins-of-life and astrobiology-inspired molecular systems

---

## Development Roadmap

Initial development priorities include:

1. Define polymer representations and residue naming conventions
2. Improve PDB parsing for canonical and noncanonical nucleic acids
3. Formalize backbone/base atom classification
4. Refactor the RNA → HNA prototype into reusable modules
5. Add validation metrics for reconstructed structures
6. Expand template-guided reconstruction to additional XNA types
7. Develop a generalized NA → XNA conversion framework

---

## Suggested Repository Structure

```text
digital-polymerase/
├── README.md
├── LICENSE
├── requirements.txt
├── src/
│   └── digital_polymerase/
│       ├── core/
│       ├── converters/
│       ├── polymer_db/
│       └── prototypes/
├── data/
│   └── templates/
├── examples/
├── docs/
└── tests/
