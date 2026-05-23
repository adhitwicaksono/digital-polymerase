# Benchmark 005: HNA Template Regression Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 005  
**Prototype tested:** Prototype 001B — RNA → HNA full-template-guided reconstruction  
**Status:** Successful short-mer regression benchmark  
**Current scope:** 8-mer only  
**Planned continuation:** Add long-input / 111-mer HNA scaling notes after Prototype 001C testing

---

## Executive Summary

Benchmark 005 revisits HNA, the first successful Digital Polymerase RNA → XNA proof-of-concept.

The early HNA prototype successfully produced an HNA-like 8-mer candidate, but it came from the first one-off code generation stage. After the ANA and FANA development arcs established stronger validation practices, the HNA workflow was refactored as Prototype 001B.

Prototype 001B performs **full-template-guided RNA → HNA reconstruction**.

The current benchmark uses:

```text
RNA-8mer.pdb
481d-HNA8nt.pdb
```

and produces:

```text
converted_hna_RNA-8mer_001B.pdb
conversion_report_RNA-8mer_001B.md
```

The current visual inspection shows a coherent short HNA-like candidate.

---

## Why This Benchmark Matters

HNA is more structurally divergent from RNA than ANA or FANA.

For ANA and FANA, chain-preserving strategies worked well because the overall nucleic-acid chain framework remains relatively close to RNA-like geometry.

For HNA, the scaffold is more different. Therefore, Prototype 001B does not preserve the RNA chain framework directly. Instead, it uses the HNA template as a full scaffold donor.

The key benchmark question is:

> Can the refactored HNA converter reproduce a visually coherent short-mer HNA candidate while reporting validation metrics more honestly than the original prototype?

Current answer:

```text
Yes, for the 8-mer full-template case.
```

---

## Files and Roles

### Current input

```text
RNA-8mer.pdb
```

Source RNA used for the current regression test.

### Main HNA template

```text
481d-HNA8nt.pdb
```

Full 8-mer HNA template used as the scaffold donor.

### Additional HNA fragment

```text
481d_HNA_4nt.pdb
```

Shorter HNA fragment. Useful for future HNA fragment-guided reconstruction, but not the primary template for Prototype 001B.

### Historical files

```text
5 - converted_HNA_template_based.pdb
5 - rna_to_hna_template_based.py
```

Archived early-stage HNA prototype files.

These are important historically, but they should not be treated as final stable converter outputs.

---

## Current Result

| Metric | Value |
|---|---|
| Source RNA sequence | `CUAGGCUC` |
| HNA template base-class sequence | `GUGUACAC` |
| Converted residues | 8 |
| Mean anchor RMSD | 0.2454 Å |
| Maximum anchor RMSD | 0.2642 Å |
| Mean C1′→glycosidic N distance | 1.3368 Å |
| Maximum C1′→glycosidic N distance | 1.3593 Å |
| Chain-continuity status | `PASS` |
| Base-attachment status | `PASS` |

---

## Current Method

Prototype 001B uses a full-template-guided strategy:

```text
RNA 8-mer
+
HNA 8-mer template
→
HNA-like 8-mer candidate
```

For each residue, the converter:

1. selects the corresponding HNA template residue
2. extracts HNA backbone/scaffold atoms
3. aligns RNA local sugar anchors to the HNA template frame
4. transforms RNA nucleobase atoms into the HNA template frame
5. combines HNA scaffold + transformed RNA base
6. writes the output PDB
7. validates chain continuity and base attachment

---

## Current Visual Inspection

The current 8-mer output was visually inspected.

Observed:

- continuous curved backbone in cartoon representation
- coherent nucleobase placement
- no obvious residue explosion
- no visible fragment scattering
- atomic/stick view appears globally reasonable for a computational candidate

This supports the conclusion:

```text
Prototype 001B is visually successful for the 8-mer full-template case.
```

---

## Important Boundary

Prototype 001B is not a general long-RNA → HNA converter.

The converter intentionally rejects cases where the RNA input has more residues than the HNA template.

For example:

```text
RNA-12mer.pdb + 481d-HNA8nt.pdb
```

is rejected because the HNA template has only 8 residues.

This is correct behavior because silently recycling the HNA template could produce misleading outputs.

---

## Why We Do Not Force 12-mer Yet

For HNA, forcing a short template onto longer RNA inputs is risky because:

- HNA scaffold geometry differs more strongly from RNA
- chain continuity may become difficult to preserve
- cyclic template reuse may generate artificial periodic geometry
- long folded RNA requires segment-aware reconstruction
- the current method is designed for full-template reconstruction only

Therefore, HNA scaling should be handled as a separate prototype:

```text
Prototype 001C
```

---

## Planned Prototype 001C

Planned goal:

```text
RNA → HNA fragment-guided / segment-guided reconstruction
```

Candidate strategy:

1. use 4-mer and 8-mer HNA templates as local or segment templates
2. reconstruct longer RNA inputs in overlapping HNA windows
3. preserve or enforce O3′→P chain continuity
4. validate P→O5′ and C1′→glycosidic base attachment
5. start with 12-mer and 16-mer before progressing to 22-mer, 34-mer, and 111-mer

The 111-mer test should not be attempted as the first HNA scaling step.

---

## Relationship to Earlier Work

Current HNA arc:

```text
Prototype 001: early RNA → HNA 8-mer proof of concept
Benchmark 002: HH ribozyme RNA → HNA failure / stress-test
Prototype 001B: refactored RNA → HNA 8-mer full-template regression
Planned Prototype 001C: HNA fragment/segment-guided scaling
```

Relationship to later XNAs:

```text
ANA 002A.1 taught chain-continuity validation
ANA 002A.2 taught chain-preserving reconstruction
FANA 003A applied chain-preserving logic successfully
HNA 001B now revisits the original HNA success with better reporting
```

---

## Scientific Interpretation

Correct description:

```text
HNA-like short-mer candidate generated by full-template-guided reconstruction.
```

Incorrect descriptions:

```text
validated HNA molecule
experimentally confirmed HNA polymer
functional HNA ribozyme
MD-ready HNA structure
```

The current output is a computational candidate.

---

## Known Limitations

- Current benchmark is only 8-mer.
- No long-input HNA conversion yet.
- Not energy-minimized.
- No force-field parameters are generated.
- No topology files are generated.
- No explicit `CONECT` records are written.
- HNA ring/scaffold stereochemistry requires expert review.
- Biological function is not implied.
- Molecular viewers may infer nonstandard bonds differently.

---

## Recommended Next Actions

1. Commit the current HNA 001B benchmark folder.
2. Keep the old HNA script/output under `historical/`.
3. Do not force 12-mer conversion with Prototype 001B.
4. Build Prototype 001C for fragment/segment-guided HNA scaling.
5. Update this benchmark after 001C reaches 111-mer testing.
6. Add final prototype documentation after the 111-mer HNA scaling result is evaluated.

---

## Temporary Documentation Note

The full HNA prototype documentation should be treated as evolving.

Recommended placeholder:

```text
docs/prototype_001B_rna_to_hna_template_guided.md
```

Then later add:

```text
docs/prototype_001C_rna_to_hna_fragment_or_segment_guided.md
```

after testing to 111-mer is completed.

---

## Recommended Commit Message

```bash
git add benchmarks/hna_template_regression/
git commit -m "Add HNA template regression benchmark"
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** not yet  
**Use for MD as-is:** no  
**Use as short-mer regression benchmark:** yes  
**Proceed to HNA scaling:** yes, but through Prototype 001C, not Prototype 001B
