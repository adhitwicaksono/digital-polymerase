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

## Related Tools and Inspirations

Digital Polymerase is inspired by existing nucleic acid and XNA modeling tools, but it is not intended to duplicate them.

At present, there is no widely established one-click tool that takes an arbitrary DNA/RNA PDB structure and directly converts it into a chemically validated XNA PDB structure. Existing tools instead focus on related tasks such as building XNA duplexes, modeling nucleic acid analogs, analyzing or rebuilding nucleic acid structures, or preparing modified nucleotides for molecular dynamics.

Relevant inspirations include:

### Ducque

**Ducque** is an open-source XNA builder designed for constructing nucleic acid analog duplexes with customizable chemistry. It has been demonstrated in a molecular modeling pipeline for morpholino nucleic acid/RNA duplexes and is especially relevant to XNA-native structure generation [1].

Digital Polymerase is inspired by Ducque’s XNA-native philosophy, especially its focus on customizable nucleic acid analog chemistry.

### proto-Nucleic Acid Builder (pNAB)

**pNAB** is an open-source tool for modeling nucleic acid analogs with alternative backbones and nucleobases. It performs conformational searches to generate candidate structures and was developed to support exploration of XNAs and possible pre-RNA genetic polymers [2].

Digital Polymerase is inspired by pNAB’s general framework for exploring alternative nucleic acid architectures.

### modXNA

**modXNA** is a modular tool for deriving and building modified nucleotides for use with Amber force fields. It is especially relevant for molecular dynamics simulations of noncanonical or modified nucleic acid systems [3].

Digital Polymerase is not currently a force-field parameterization tool, but future workflows may benefit from compatibility with parameterization approaches such as modXNA.

### 3DNA / X3DNA-DSSR

**3DNA** provides tools for the analysis, reconstruction, and visualization of three-dimensional DNA and RNA structures from coordinate files [4]. **DSSR** extends this structural-analysis tradition by dissecting and annotating RNA tertiary structures, including canonical and noncanonical base pairs [5].

Digital Polymerase is inspired by the nucleic-acid structural analysis and rebuilding tradition represented by these tools, while extending the question toward XNA-aware reconstruction.

### NAB / AmberTools

**NAB** is a nucleic acid modeling language originally developed for building unusual nucleic acid structures using rigid-body transformations, distance geometry, and molecular mechanics refinement [6].

Digital Polymerase is inspired by this tradition of programmatic nucleic acid construction, but aims to focus specifically on template-guided NA→XNA reconstruction.

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
```

---

## Relationship to the XNA World Project

Digital Polymerase is envisioned as one component of the broader XNA World Project.

The XNA World Project aims to explore how alternative nucleic acid chemistries may approach life-relevant functional thresholds, including:

- information storage
- molecular recognition
- templated copying
- structural folding
- catalytic potential
- evolvability
- system integration

Digital Polymerase contributes to this vision by providing computational tools for structure conversion, reconstruction, and scenario modeling.

--

## Current Status

This project is in early development.

The first prototype has demonstrated that RNA → HNA conversion is more realistically approached through template-guided reconstruction rather than direct atom insertion or simple geometric editing.

Further development will focus on improving generality, validation, documentation, and modularity.

--

## License

This project is released under the **MIT License**.

--

## Acknowledgment of AI-Assisted Development

This project uses AI-assisted coding and reasoning workflows during early prototyping, including iterative comparison between source and target nucleic acid structures, prototype generation, code review, and documentation drafting.

All generated code and structural outputs should be critically reviewed, tested, and scientifically validated before use in research conclusions.

--

## Author
Developed by **Adhityo Wicaksono, Arli Aditya Parikesit**
as part of an ongoing computational exploration of nucleic acid diversity, xenobiology, and the dry-lab side of the **XNA World Project**.

--

## References

[1] Rihon, J., Mattelaer, C.-A., Montalvão, R. W., Froeyen, M., Pinheiro, V. B., & Lescrinier, E. (2024). Structural insights into the morpholino nucleic acid/RNA duplex using the new XNA builder Ducque in a molecular modeling pipeline. *Nucleic Acids Research*, 52(6), 2836–2847. https://doi.org/10.1093/nar/gkae135

[2] Alenaizan, A., Barnett, J. L., Hud, N. V., Sherrill, C. D., & Petrov, A. S. (2021). The proto-Nucleic Acid Builder: a software tool for constructing nucleic acid analogs. *Nucleic Acids Research*, 49(1), 79–89. https://doi.org/10.1093/nar/gkaa1159

[3] Love, O., Galindo-Murillo, R., Roe, D. R., Dans, P. D., Cheatham, T. E. III, & Bergonzo, C. (2024). modXNA: A modular approach to parametrization of modified nucleic acids for use with Amber force fields. *Journal of Chemical Theory and Computation*, 20(21), 9354–9363. https://doi.org/10.1021/acs.jctc.4c01164

[4] Lu, X.-J., & Olson, W. K. (2003). 3DNA: a software package for the analysis, rebuilding and visualization of three-dimensional nucleic acid structures. *Nucleic Acids Research*, 31(17), 5108–5121. https://doi.org/10.1093/nar/gkg680

[5] Lu, X.-J., Bussemaker, H. J., & Olson, W. K. (2015). DSSR: an integrated software tool for dissecting the spatial structure of RNA. *Nucleic Acids Research*, 43(21), e142. https://doi.org/10.1093/nar/gkv716

[6] Macke, T. J., & Case, D. A. (1998). Modeling unusual nucleic acid structures. In N. B. Leontis & J. SantaLucia Jr. (Eds.), *Molecular Modeling of Nucleic Acids* (ACS Symposium Series, Vol. 682, pp. 379–393). American Chemical Society. https://doi.org/10.1021/bk-1998-0682.ch024
