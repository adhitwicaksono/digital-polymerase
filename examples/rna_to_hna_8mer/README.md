# Example: RNA 8-mer → HNA Candidate Structure

This example demonstrates **Prototype 001** of Digital Polymerase: a template-guided reconstruction workflow for converting a short RNA oligomer into an HNA-like candidate structure.

The goal is to test whether an RNA input structure can be transformed into an HNA candidate model by using an experimental HNA structure as a backbone template.

---

## Overview

This example uses:

1. an input RNA 8-mer PDB structure
2. an HNA 8-mer template PDB structure
3. the Prototype 001 RNA → HNA converter

The converter does **not** simply insert atoms into RNA. Instead, it performs a template-guided reconstruction:

1. parse the RNA input PDB
2. parse the HNA template PDB
3. extract the HNA backbone geometry
4. preserve the RNA sequence and nucleobase atoms
5. align RNA bases onto the HNA residue geometry
6. transplant transformed bases onto the HNA backbone
7. export a candidate HNA-like PDB structure

---

## Files

Recommended example directory structure:

```text
examples/rna_to_hna_8mer/
├── README.md
├── input_rna_8mer.pdb
├── hna_8mer_template.pdb
├── converted_hna_candidate.pdb
└── conversion_report.md
