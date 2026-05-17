# Digital Polymerase

**Digital Polymerase** is a tool-building project aimed at converting nucleic acids into other nucleic acid types, including canonical nucleic acids (**DNA** and **RNA**) and xeno/synthetic nucleic acids (**XNA**) such as **HNA, ANA, FANA, TNA, GNA, CeNA**, and others.

The project is designed to use **PDB structures as both input and output**, enabling structure-guided transformation of one nucleic acid polymer type into another. Because such conversions are computational reconstructions rather than experimental validation, all generated structures should still be evaluated through **molecular dynamics simulations** and other downstream structural validation workflows.

---

## Vision

Digital Polymerase is part of a broader dry-lab effort to explore the **computational world of alternative genetic polymers**.

While wet-lab xenobiology studies whether XNA molecules can be synthesized, replicated, or made functional, Digital Polymerase focuses on the **in silico side**: building tools that help researchers model, transform, and compare nucleic acid systems across natural and synthetic chemistries.

---

## Goals

- Convert nucleic acid structures between **DNA, RNA, and XNA types**
- Support **PDB-based structural transformation**
- Provide a modular framework for **polymer-aware parsing and rebuilding**
- Facilitate future modeling of **alternative nucleic acid worlds**
- Serve as a computational support layer for **xenobiology and synthetic biology**

---

## Planned Features

### Core features
- Parse nucleic acid structures from **PDB**
- Detect and classify polymer type
- Convert canonical nucleic acids:
  - DNA → RNA
  - RNA → DNA

### Extended XNA conversion
- DNA/RNA → XNA
- XNA → DNA/RNA
- XNA → XNA

### Structural rebuilding
- Template-guided nucleic acid reconstruction
- Preservation of sequence order and approximate base arrangement
- Export of converted structures as **PDB**

### Downstream compatibility
- Support for future integration with:
  - molecular dynamics workflows
  - force-field parameter pipelines
  - external nucleic acid/XNA modeling tools

---

## Important Note

Digital Polymerase does **not** claim that a converted structure is automatically physically valid or biologically functional.

A converted model should be interpreted as a **computationally generated candidate structure**, which may require:

- geometry refinement
- energy minimization
- molecular dynamics simulation
- expert chemical inspection

---

## Scope

This repository is intended as a **dry-lab computational tool**, not as a substitute for experimental validation.

Its long-term purpose is to help researchers explore possible structural scenarios in which functional XNA molecules may exist, interact, or be compared with canonical nucleic acids.

---

## Long-Term Context

Digital Polymerase is envisioned as one component of the broader **XNA World Project**, a computational framework for exploring alternative nucleic acid chemistries and their potential relevance to the functional thresholds of life.

In that broader vision, Digital Polymerase serves as the **conversion and reconstruction engine**.

---

## Current Status

This project is in its early development stage.

Initial development priorities include:

1. defining polymer representations
2. designing conversion logic
3. implementing PDB parsing
4. building a minimal canonical NA → NA conversion workflow
5. extending support toward XNA-aware reconstruction

---

## License

This project is released under the **MIT License**.

---

## Author

Developed by **Adhityo Wicaksono, Arli Aditya Parikesit**  
as part of an ongoing computational exploration of nucleic acid diversity, xenobiology, and the dry-lab side of the **XNA World Project**.
