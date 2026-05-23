# PNA Arc Summary: Prototype 008A.1 → 008D

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Topic:** PNA conversion strategy arc  
**Status:** PNA final-boss chapter summarized  
**Core conclusion:** PNA is not untameable, but it is not tameable by the same fold-preserving geometry-transfer logic used for sugar/phosphate-like XNAs.

---

## Executive Summary

PNA became the “final boss” of the current Digital Polymerase ssXNA campaign because it is chemically distinct from the previous targets.

The project successfully generated working or partially working candidate-generation strategies for:

```text
HNA
ANA
FANA
CeNA
XyNA
TNA
GNA
```

PNA was different.

Unlike these XNAs, PNA does not preserve a sugar-phosphate-like backbone. It uses a pseudopeptide backbone with nucleobases attached as side-chain-like groups.

This forced a shift in conversion philosophy.

---

## The PNA Prototypes

### Prototype 008A.1 — Failed RNA-Fold-Forced Attempt

Strategy:

```text
RNA fold → force PNA pseudopeptide backbone onto it
```

Result:

```text
failed / tangled / over-collapsed
```

The 8-mer output was already too tangled to trust.

Lesson:

```text
Directly forcing PNA onto RNA geometry is too aggressive.
```

This became:

```text
Benchmark 011: PNA Failure Notes
```

---

### Prototype 008B — Successful Template-Primary PNA Converter

Strategy:

```text
PNA scaffold first
RNA sequence/base identity second
```

Result:

```text
successful scaffold-first sequence-preserving PNA candidate generation
```

Visual inspection:

```text
8-mer  → clean
34-mer → elongated, coherent PNA-like strand
111-mer → long clean sequence-carrier strand
```

Important limitation:

```text
Does not preserve RNA tertiary fold.
```

Lesson:

```text
PNA conversion works when PNA is allowed to remain PNA.
```

This became:

```text
Benchmark 012: PNA Template-Primary Scaling
```

---

### Prototype 008C — Sequence-Primary PNA Generator

Strategy:

```text
sequence / FASTA / RNA-derived sequence → PNA scaffold generator
```

Result:

```text
useful sequence-carrier generator
```

Supported input modes:

```bash
--rna input.pdb
--fasta input.fasta
--sequence CUAGGCUC
```

Observed behavior:

```text
good for short sequence-primary generation
less meaningful as structural conversion at longer length
```

Lesson:

```text
008C is useful, but it is not a fold-preserving converter.
```

This became:

```text
Benchmark 013: PNA Sequence-Primary Regression Notes
```

---

### Prototype 008D — RNA-Informed Hybrid Boundary Test

Strategy:

```text
RNA base-frame guidance
+
PNA local scaffold
+
bounded C′(i)→N1′(i+1) smoothing
+
movement caps
```

Result:

```text
partial/negative boundary result
```

Visual inspection:

```text
8-mer  → partial rescue but not clean
34-mer → local clusters, loss of global coherence
111-mer → semi-collapsed domains, no stable RNA-like fold preservation
```

Lesson:

```text
PNA can be locally RNA-informed, but reliable global RNA-fold-preserving reconstruction remains unsolved.
```

This became:

```text
Benchmark 014: PNA Hybrid-Guided Boundary Notes
```

---

## Main Methodological Lesson

The PNA arc revealed that Digital Polymerase needs multiple conversion paradigms.

For many sugar/phosphate-like XNAs:

```text
RNA geometry → XNA-like geometry
```

can be a useful approximation.

For PNA:

```text
RNA sequence → PNA sequence carrier
```

is currently more reliable.

The important distinction:

```text
PNA sequence-preserving generation: feasible
PNA RNA-fold-preserving reconstruction: not solved
```

---

## Comparison to Earlier XNA Families

| XNA | Conversion behavior | Current interpretation |
|---|---|---|
| HNA | Template-guided / fold-derived candidate | Working prototype |
| ANA | Fragment/template-guided candidate | Working prototype |
| FANA | Chain-preserving candidate | Working prototype |
| CeNA | Template-guided candidate | Working prototype |
| XyNA | Pentose-like candidate | Working prototype |
| TNA | Linkage-remapped candidate | Working prototype |
| GNA | Glycerol-scaffold linkage-optimized candidate | Working prototype |
| PNA | Requires multiple paradigms | Final-boss boundary case |

---

## Is PNA “Untameable”?

No.

PNA is not untameable.

A better conclusion is:

```text
PNA is tameable as a sequence-carrier scaffold,
but not yet tameable as an RNA-fold-preserving analog under this prototype framework.
```

The current PNA work does not resemble a total defeat. It resembles a mapped frontier.

The project learned:

```text
what fails
what works
what generalizes
where the boundary lies
```

That is a scientific win.

---

## Best Current PNA Status

Recommended practical status:

```text
008B = best current PNA converter
008C = useful sequence generator
008D = boundary/negative result
```

Recommended user-facing claim:

```text
Digital Polymerase currently supports PNA-like sequence-carrier candidate generation through a template-primary scaffold-first strategy.
```

Avoid claiming:

```text
Digital Polymerase can reliably convert folded RNA structures into folded PNA analogs.
```

---

## Why Stop Here?

The current stop condition is satisfied:

```text
008A.1 failed by collapse
008B succeeded by abandoning fold preservation
008C works as sequence generation but not structural conversion
008D partially rescues local geometry but fails global fold preservation
```

Continuing with small patches is likely to produce diminishing returns unless the project introduces new modeling machinery, such as:

```text
PNA-specific force fields
conformational sampling
explicit topology generation
better PNA structural templates
energy minimization
template libraries for PNA single-strand or duplex conformations
```

Therefore, the responsible move is:

```text
pause PNA fold-preserving conversion
document the boundary
move forward with the broader XNA framework
```

---

## Recommended Repository Files

```text
benchmarks/pna_scaling/benchmark_011_pna_failure_notes.md
benchmarks/pna_scaling/benchmark_012_pna_template_primary_scaling_notes.md
benchmarks/pna_scaling/benchmark_013_pna_sequence_primary_regression_notes.md
benchmarks/pna_scaling/benchmark_014_pna_hybrid_guided_boundary_notes.md

docs/prototype_008B_rna_to_pna_template_primary.md
docs/prototype_008D_rna_to_pna_hybrid_guided_plan.md
docs/pna_arc_summary_008A1_to_008D.md
```

---

## Final Conclusion

PNA was not fully conquered in the same way as the earlier XNAs.

But it was not a failure.

The PNA chapter produced:

```text
a failed direct strategy
a successful scaffold-first strategy
a useful sequence-primary generator
a hybrid boundary test
a clear stop rule
a stronger conceptual framework for Digital Polymerase
```

That is enough to close the current PNA arc with scientific honesty.

The chimaera is not “untameable.”

It simply refuses to be tamed as RNA.
