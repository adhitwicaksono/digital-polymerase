<p align="center">
  <img src="assets/digital_polymerase_banner__v2.png" alt="Digital Polymerase banner" width="100%">
</p>

# Digital Polymerase

**Digital Polymerase** is an early-stage dry-lab software project for exploring computational conversion and reconstruction between canonical nucleic acids (**DNA** and **RNA**) and xeno/synthetic nucleic acids (**XNA**) such as **HNA, ANA, FANA, CeNA, XyNA, TNA, GNA, PNA**, and future targets such as **morpholino nucleic acids** when suitable structural templates become available.

The project focuses on **structure-guided nucleic acid transformation**, especially using **PDB structures as input and output**. Rather than treating conversion as a simple atom-replacement problem, Digital Polymerase develops template-guided, chain-aware, linkage-aware, scaffold-aware, and polymer-aware approaches for rebuilding nucleic acid candidate structures across different backbone chemistries.

All generated structures should be interpreted as **computational candidate models**, not experimentally validated molecules. They require downstream structural validation such as geometry inspection, stereochemical review, energy minimization, molecular dynamics simulation, force-field/topology assessment, and expert chemical evaluation.

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
   Rebuilding a candidate 3D structure using structural templates, local alignment, chain-preserving transformations, linkage remapping, scaffold tiling, or coordinate reconstruction.

4. **Physically refined modeling**  
   Evaluating and refining the candidate structure through molecular mechanics, energy minimization, molecular dynamics, force-field/topology preparation, and other validation workflows.

The current focus is on **Level 3: geometric candidate reconstruction**.

A key lesson from the early prototypes is:

> A converter is not successful just because it writes a PDB. It must preserve polymer logic, validate its own geometry, and report its limitations.

A second major lesson from the PNA prototypes is:

> Not every XNA should be treated as “RNA with a modified sugar.” Some XNAs require chemistry-first scaffold strategies rather than fold-preserving conversion.

---

## Goals

- Convert nucleic acid structures between **DNA, RNA, and XNA types**
- Support **PDB-based structural transformation**
- Develop a modular framework for **polymer-aware parsing, alignment, rebuilding, validation, and export**
- Preserve sequence information while allowing backbone chemistry to change
- Distinguish **local residue geometry** from **whole-polymer chain continuity**
- Distinguish **fold-preserving conversion** from **sequence-carrier generation**
- Facilitate future modeling of **alternative nucleic acid worlds**
- Serve as a computational support layer for **xenobiology, synthetic biology, computational structural biology, nucleic acid engineering, and origins-of-life research**

---

## Current Working Prototype Families

Digital Polymerase currently contains multiple RNA → XNA candidate-generation prototype families. These are **prototype candidate generators**, not stable production converters.

| Prototype | Conversion | Main method | Current status |
|---|---|---|---|
| `001B` | RNA → HNA | Full-template-guided short-mer reconstruction | Successful 8-mer candidate |
| `001C.1` | RNA → HNA | Chain-preserving scalable HNA-like reconstruction with base-attachment correction | Successful scaling to 111 nt |
| `002A.2` | RNA → ANA | Chain-preserving fragment-guided reconstruction | Successful candidate generation up to 111 nt |
| `003A` | RNA → FANA | Chain-preserving reconstruction with FANA C2′/F2′ local geometry | Successful candidate generation up to 111 nt |
| `004A` | RNA → CeNA | Template-guided cyclohexenyl-scaffold reconstruction | Successful candidate generation up to 111 nt |
| `005A` | RNA → XyNA | Pentose-like template-guided reconstruction | Successful candidate generation up to 111 nt |
| `006B.4` | RNA → TNA | Linkage-remapped threose-scaffold reconstruction | Successful candidate generation up to 111 nt |
| `007A` | RNA → GNA | Linkage-optimized glycerol-scaffold reconstruction | Successful first-pass candidate generation up to 111 nt |
| `008B` | RNA → PNA | Template-primary PNA scaffold-first base replacement | Successful sequence-preserving PNA candidate generation |
| `008C` | Sequence/RNA/FASTA → PNA | Sequence-primary PNA generator | Useful sequence-carrier generator; not fold-preserving |
| `008D` | RNA → PNA | RNA-informed hybrid-guided PNA reconstruction | Boundary/partial result; fold-preserving PNA remains unsolved |

---

## Conversion Strategy Classes

The prototypes have revealed that Digital Polymerase needs multiple conversion paradigms rather than one universal algorithm.

| Strategy class | Description | Example prototypes |
|---|---|---|
| **Full-template-guided reconstruction** | Use a target XNA template as the primary scaffold and transplant sequence/base identity | `001B` |
| **Chain-preserving reconstruction** | Preserve RNA chain continuity first, then introduce target local scaffold geometry | `001C.1`, `002A.2`, `003A` |
| **Linkage-remapped reconstruction** | Replace canonical RNA linkage assumptions with target-XNA-specific linkage grammar | `006B.4`, `007A` |
| **Template-primary scaffold-first reconstruction** | Preserve/tile target scaffold first, then map base identity | `008B` |
| **Sequence-primary generation** | Generate a target XNA sequence carrier from sequence, FASTA, or RNA-derived sequence | `008C` |
| **Hybrid-guided boundary testing** | Combine RNA spatial information with target-XNA local chemistry under movement limits | `008D` |

This distinction is one of the main conceptual outputs of the project so far.

---

## Prototype 001B/001C.1: RNA → HNA

The HNA family began as the first RNA → XNA proof of concept, then evolved into a refactored and scalable prototype family.

### Prototype 001B — full-template HNA reconstruction

Prototype 001B is used when a full-length HNA template is available.

Example:

```text
RNA-8mer.pdb + 481d-HNA8nt.pdb → HNA-like 8-mer candidate
```

The method:

1. uses the HNA template as the backbone/scaffold donor
2. aligns RNA base atoms into the HNA local frame
3. transplants RNA bases onto the HNA scaffold
4. validates chain continuity and base attachment

### Prototype 001C.1 — scalable chain-preserving HNA reconstruction

Prototype 001C.1 extends HNA reconstruction to RNA inputs longer than the available HNA template.

Example benchmarked inputs:

```text
RNA-12mer
RNA-16mer
RNA-22mer
RNA-34mer
HH-type I ribozyme-derived 111-mer
```

The method:

1. preserves RNA chain-continuity atoms
2. inserts local HNA scaffold atoms such as `O4′`, `C6′`, `C1′`, and `C2′`
3. transforms RNA bases onto the new HNA-like local scaffold
4. corrects C1′→glycosidic-N distance using the selected HNA template
5. validates O3′→P, C1′→N, C1′→C6′, and C6′→O4′ distances

Current benchmark result:

```text
HNA-like candidate generation scales from 8 nt to 111 nt.
```

---

## Prototype 002A.2: RNA → ANA

The ANA prototype began as a residue-local fragment-guided converter using a 4-mer ANA template.

Initial ANA reconstruction showed a critical failure mode:

```text
low local RMSD ≠ valid polymer chain
```

Patch 002A.1 added explicit chain-continuity validation and revealed that residue-local conversion broke many O3′→P links.

Patch 002A.2 introduced a chain-preserving strategy:

```text
preserve chain continuity first
introduce ANA-like local geometry second
validate explicitly
```

Current status:

```text
RNA → ANA chain-preserving candidate generation works visually and computationally up to the 111-mer benchmark.
```

---

## Prototype 003A: RNA → FANA

Prototype 003A applies the chain-preserving design principle from the beginning.

For FANA, the converter:

1. preserves RNA polymer-chain atoms
2. removes RNA O2′
3. introduces FANA-like C2′ and F2′ local geometry from a FANA template
4. preserves RNA bases
5. validates O3′→P, P→O5′, C1′→C2′, C2′→C3′, and C2′→F2′ geometry

Current status:

```text
RNA → FANA candidate generation works from 8 nt to 111 nt, with C2′→F2′ distances around the expected template-derived range.
```

---

## Prototype 004A: RNA → CeNA

Prototype 004A explores RNA → CeNA candidate generation.

CeNA uses a cyclohexenyl-like scaffold, so it is not merely a small local sugar edit. The converter treats CeNA as a template-guided scaffold reconstruction problem.

Current status:

```text
RNA → CeNA candidate generation works from 8 nt to 111 nt as a first-pass computational model.
```

---

## Prototype 005A: RNA → XyNA

Prototype 005A explores RNA → XyNA candidate generation.

XyNA is closer to canonical pentose-like logic than PNA or GNA, making it more amenable to template-guided candidate reconstruction.

Current status:

```text
RNA → XyNA candidate generation works from 8 nt to 111 nt.
```

---

## Prototype 006B.4: RNA → TNA

TNA required a more careful linkage-remapping strategy because it uses a threose-like scaffold.

The key lesson from TNA:

```text
TNA cannot be treated as RNA with a cosmetic sugar replacement.
Target-specific linkage grammar matters.
```

Current status:

```text
RNA → TNA candidate generation works from 8 nt to 111 nt using linkage-remapped reconstruction.
```

---

## Prototype 007A: RNA → GNA

GNA uses a compact glycerol-like scaffold.

The observed GNA-like linkage pattern is:

```text
P(i)    → O3G(i)
O2G(i) → P(i+1)
```

Prototype 007A treats GNA as a linkage-optimized glycerol-scaffold reconstruction problem rather than a chain-preserving RNA sugar-edit problem.

Current status:

```text
RNA → GNA candidate generation works as a successful first-pass prototype from 8 nt to 111 nt.
```

Known caveat:

```text
GNA outputs are compact/crowded and require explicit base-orientation, carbonyl/base-atom, stereochemical, and force-field validation.
```

---

## Prototype 008B/008C/008D: RNA/Sequence → PNA

PNA became the strongest boundary case in Digital Polymerase because it is not a sugar-phosphate-like XNA.

PNA uses a pseudopeptide backbone with nucleobases attached as side-chain-like groups. Therefore, PNA cannot be treated as just another RNA-like scaffold.

### Prototype 008A.1 — failed RNA-fold-forced attempt

The first PNA attempt tried:

```text
RNA fold → force PNA backbone onto it
```

The result was a tangled 8-mer and was archived as a failure benchmark.

### Prototype 008B — successful template-primary PNA converter

Prototype 008B reversed the logic:

```text
PNA scaffold first
RNA sequence/base identity second
```

This produced clean sequence-preserving PNA-like candidates.

Current status:

```text
008B is the best current practical PNA converter.
```

Important limitation:

```text
008B does not preserve RNA tertiary fold.
```

### Prototype 008C — sequence-primary PNA generator

Prototype 008C generalizes PNA generation to:

```bash
--rna input.pdb
--fasta input.fasta
--sequence CUAGGCUC
```

Current status:

```text
008C is useful for sequence-to-PNA candidate generation, but it is not a fold-preserving converter.
```

### Prototype 008D — hybrid RNA-informed boundary test

Prototype 008D attempted:

```text
RNA base-frame guidance
+
PNA local scaffold
+
bounded C′(i)→N1′(i+1) smoothing
```

Current status:

```text
008D is an important partial/negative result. It partially preserves local organization but does not solve reliable RNA-fold-preserving PNA reconstruction.
```

Main PNA conclusion:

```text
PNA is tameable as a sequence-carrier scaffold,
but not yet tameable as an RNA-fold-preserving analog under the current prototype framework.
```

---

## Benchmarks

Digital Polymerase keeps both successful and failed benchmarks. Failure cases are intentionally preserved because they define the next algorithmic boundary.

| Benchmark | Focus | Result |
|---|---|---|
| `Benchmark 002` | HH ribozyme RNA → HNA early scaling failure | Productive failure; short-mer logic did not generalize directly |
| `Benchmark 003` | ANA fragment-guided scaling | Revealed chain-continuity failure, then led to 002A.2 chain-preserving ANA |
| `Benchmark 004` | FANA chain-preserving scaling | Successful candidate generation from 8 nt to 111 nt |
| `Benchmark 005` | HNA template regression | Successful HNA 8-mer full-template regression |
| `Benchmark 006` | HNA scaling | Successful HNA-like candidate generation from 8 nt to 111 nt using 001C.1 |
| `Benchmark 007` | HNA documentation/prototype consolidation | Prototype documentation and scaling interpretation |
| `Benchmark 008` | CeNA candidate scaling | Successful first-pass candidate generation from 8 nt to 111 nt |
| `Benchmark 009` | XyNA candidate scaling | Successful candidate generation from 8 nt to 111 nt |
| `Benchmark 010` | GNA scaling | Successful first-pass glycerol-scaffold reconstruction up to 111 nt |
| `Benchmark 011` | PNA failed RNA-fold-forced attempt | Productive failure; direct forcing caused tangling |
| `Benchmark 012` | PNA template-primary scaling | Successful sequence-preserving PNA scaffold generation |
| `Benchmark 013` | PNA sequence-primary regression/limitation | Useful generator; not fold-preserving |
| `Benchmark 014` | PNA hybrid-guided boundary test | Partial/negative boundary result |

Recommended benchmark folders:

```text
benchmarks/
├── hh_ribozyme_8t5o/
├── ana_fragment_scaling/
├── fana_fragment_scaling/
├── hna_template_regression/
├── hna_scaling/
├── cena_scaling/
├── xyna_scaling/
├── tna_scaling/
├── gna_scaling/
└── pna_scaling/
```

---

## Suggested Repository Structure

```text
digital-polymerase/
├── README.md
├── LICENSE
├── requirements.txt
├── assets/
│   └── digital_polymerase_banner__v2.png
│
├── src/
│   └── digital_polymerase/
│       ├── core/
│       │   └── README.md
│       ├── converters/
│       │   └── README.md
│       └── prototypes/
│           ├── rna_to_hna_template_guided.py
│           ├── rna_to_hna_chain_preserving.py
│           ├── rna_to_ana_fragment_guided.py
│           ├── rna_to_fana_fragment_guided.py
│           ├── rna_to_cena_template_guided.py
│           ├── rna_to_xyna_template_guided.py
│           ├── rna_to_tna_linkage_remapped.py
│           ├── rna_to_gna_linkage_optimized.py
│           ├── rna_to_pna_template_primary.py
│           ├── pna_sequence_primary_generator.py
│           └── rna_to_pna_hybrid_guided.py
│
├── docs/
│   ├── prompt_protocol.md
│   ├── prototype_001B_rna_to_hna_template_guided.md
│   ├── prototype_001C_rna_to_hna_chain_preserving.md
│   ├── prototype_002A_rna_to_ana_fragment_guided.md
│   ├── prototype_003A_rna_to_fana_fragment_guided.md
│   ├── prototype_004A_rna_to_cena_template_guided.md
│   ├── prototype_005A_rna_to_xyna_template_guided.md
│   ├── prototype_006B_rna_to_tna_linkage_remapped.md
│   ├── prototype_007A_rna_to_gna_linkage_optimized.md
│   ├── prototype_008B_rna_to_pna_template_primary.md
│   ├── prototype_008D_rna_to_pna_hybrid_guided_plan.md
│   └── pna_arc_summary_008A1_to_008D.md
│
├── examples/
│   ├── rna_to_hna_8mer/
│   ├── rna_to_pna_8mer/
│   └── sequence_to_pna/
│
└── benchmarks/
    ├── hh_ribozyme_8t5o/
    ├── ana_fragment_scaling/
    ├── fana_fragment_scaling/
    ├── hna_template_regression/
    ├── hna_scaling/
    ├── cena_scaling/
    ├── xyna_scaling/
    ├── tna_scaling/
    ├── gna_scaling/
    └── pna_scaling/
```

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

Digital Polymerase is inspired by this tradition of programmatic nucleic acid construction, but aims to focus specifically on template-guided and chain-aware NA→XNA reconstruction.

---

## Planned Features

### Core features

- Parse nucleic acid structures from **PDB**
- Detect and classify nucleic acid residue types
- Separate backbone atoms from base atoms
- Perform local coordinate alignment
- Validate polymer-chain continuity
- Validate target-specific linkage patterns
- Validate local scaffold geometry
- Audit expected base atoms and carbonyl/oxygen atoms
- Export reconstructed structures as **PDB**
- Generate Markdown reports describing method, validation, and limitations

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
- CeNA
- XyNA
- TNA
- GNA
- PNA
- LNA/BNA
- morpholino nucleic acid / PMO, when suitable templates are available

### Structural rebuilding

- Template-guided nucleic acid reconstruction
- Chain-preserving reconstruction
- Fragment-guided reconstruction
- Segment-guided reconstruction
- Linkage-remapped reconstruction
- Scaffold-first template-primary reconstruction
- Sequence-primary target-polymer generation
- Preservation of sequence order and approximate base arrangement
- Backbone/scaffold-template transplantation
- Local base alignment
- Candidate PDB generation

### Downstream compatibility

Future versions may support integration with:

- molecular dynamics workflows
- energy minimization pipelines
- force-field parameterization tools
- external nucleic acid/XNA modeling tools
- topology/connectivity generation
- explicit `CONECT` output
- residue naming and parameterization dictionaries

---

## Important Note

Digital Polymerase does **not** claim that a converted structure is automatically physically valid, chemically complete, or biologically functional.

A converted model should be interpreted as a **computationally generated candidate structure**, which may require:

- geometry refinement
- bond and angle validation
- stereochemical inspection
- energy minimization
- molecular dynamics simulation
- force-field and topology assessment
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

Near-term development priorities include:

1. Refactor shared parser, residue, alignment, validation, and report logic into `core/`
2. Standardize prototype CLI behavior and report format
3. Preserve prototype scripts under `prototypes/` until they pass stronger validation
4. Add topology/connectivity support, including possible `CONECT` output
5. Add stronger stereochemistry, chirality, torsion, and clash validation
6. Add expected-base-atom and carbonyl/base-oxygen audits
7. Add residue naming dictionaries for target XNAs
8. Explore compatibility with minimization and force-field parameter workflows
9. Develop a generalized NA → XNA conversion framework
10. Build a template registry for XNA structural donors
11. Revisit morpholino NA / PMO when better structural templates are available

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

---

## Milestones

### 2026 — Short-oligomer and scalable RNA → XNA converter prototypes

The first development milestone is to create and validate prototype converters for nucleic acid-to-XNA candidate reconstruction using RNA input structures.

Achieved targets include:

- RNA → HNA full-template-guided reconstruction
- RNA → HNA scalable chain-preserving reconstruction
- RNA → ANA chain-preserving fragment-guided reconstruction
- RNA → FANA chain-preserving reconstruction
- RNA → CeNA candidate reconstruction
- RNA → XyNA candidate reconstruction
- RNA → TNA linkage-remapped reconstruction
- RNA → GNA linkage-optimized reconstruction
- RNA/sequence → PNA template-primary and sequence-primary candidate generation
- PNA boundary testing for RNA-informed hybrid conversion
- Scaling tests from 8-mer inputs to an HH-type I ribozyme-derived 111-mer input
- Markdown reports with chain-continuity, target-linkage, base-attachment, and local scaffold validation
- Visual inspection using PyMOL and Discovery Studio

The 2026 goal is not to claim full physical or biological validity, but to establish a working computational foundation for **nucleic-acid-to-XNA candidate reconstruction** and to clearly map where current geometry-transfer logic succeeds or fails.

---

## Current Status

This project is in early active development.

The current prototype families have demonstrated candidate-generation workflows for:

```text
RNA → HNA
RNA → ANA
RNA → FANA
RNA → CeNA
RNA → XyNA
RNA → TNA
RNA → GNA
RNA/sequence → PNA
```

Most sugar/phosphate-like XNA outputs are visually coherent and pass current internal geometry checks up to the 111-mer benchmark, but they remain **computational candidates**.

PNA is treated separately because it is a pseudopeptide nucleic acid. Current PNA support is strongest for **template-primary scaffold-first sequence-carrier generation**, while reliable **RNA-fold-preserving PNA reconstruction** remains unsolved under the current prototype framework.

The next major development stage is modularization, stronger chemical validation, topology/connectivity support, force-field/minimization compatibility, and careful separation between fold-preserving conversion and sequence-carrier generation.

---

## License

This project is released under the **MIT License**.

---

## Acknowledgment of AI-Assisted Development

This project uses AI-assisted coding and reasoning workflows during early prototyping, including iterative comparison between source and target nucleic acid structures, prototype generation, code review, benchmark interpretation, and documentation drafting.

All generated code and structural outputs should be critically reviewed, tested, and scientifically validated before use in research conclusions.

---

## Author

Developed by **Adhityo Wicaksono**  
in collaboration with **Prof. Dr. rer. nat. Arli Aditya Parikesit**  
as part of an ongoing computational exploration of nucleic acid diversity, xenobiology, and the dry-lab side of the **XNA World Project**.

---

## References

[1] Rihon, J., Mattelaer, C.-A., Montalvão, R. W., Froeyen, M., Pinheiro, V. B., & Lescrinier, E. (2024). Structural insights into the morpholino nucleic acid/RNA duplex using the new XNA builder Ducque in a molecular modeling pipeline. *Nucleic Acids Research*, 52(6), 2836–2847. https://doi.org/10.1093/nar/gkae135

[2] Alenaizan, A., Barnett, J. L., Hud, N. V., Sherrill, C. D., & Petrov, A. S. (2021). The proto-Nucleic Acid Builder: a software tool for constructing nucleic acid analogs. *Nucleic Acids Research*, 49(1), 79–89. https://doi.org/10.1093/nar/gkaa1159

[3] Love, O., Galindo-Murillo, R., Roe, D. R., Dans, P. D., Cheatham, T. E. III, & Bergonzo, C. (2024). modXNA: A modular approach to parametrization of modified nucleic acids for use with Amber force fields. *Journal of Chemical Theory and Computation*, 20(21), 9354–9363. https://doi.org/10.1021/acs.jctc.4c01164

[4] Lu, X.-J., & Olson, W. K. (2003). 3DNA: a software package for the analysis, rebuilding and visualization of three-dimensional DNA and RNA structures. *Nucleic Acids Research*, 31(17), 5108–5121. https://doi.org/10.1093/nar/gkg680

[5] Lu, X.-J., Bussemaker, H. J., & Olson, W. K. (2015). DSSR: an integrated software tool for dissecting the spatial structure of RNA. *Nucleic Acids Research*, 43(21), e142. https://doi.org/10.1093/nar/gkv716

[6] Macke, T. J., & Case, D. A. (1998). Modeling unusual nucleic acid structures. In N. B. Leontis & J. SantaLucia Jr. (Eds.), *Molecular Modeling of Nucleic Acids* (ACS Symposium Series, Vol. 682, pp. 379–393). American Chemical Society. https://doi.org/10.1021/bk-1998-0682.ch024
