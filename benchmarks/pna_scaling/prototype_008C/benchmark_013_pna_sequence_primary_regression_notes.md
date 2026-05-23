# Benchmark 013: PNA Sequence-Primary Regression Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 013  
**Prototype tested:** Prototype 008C — Sequence/RNA/FASTA → PNA sequence-primary generator  
**Status:** Useful generator, but not a structural-conversion solution  
**Primary result:** Prototype 008C generates clean sequence-primary PNA strands, but scaling beyond short motifs reveals that it behaves as a sequence-carrier generator rather than an RNA-structure-preserving converter.

---

## Summary

Benchmark 013 documents the observed limitation of Prototype 008C.

Prototype 008C extended the successful Prototype 008B strategy by allowing PNA generation from:

```text
--rna input.pdb
--fasta input.fasta
--sequence CUAGGCUC
```

This made PNA generation more reusable because it no longer depended strictly on RNA PDB input. However, visual inspection showed that the output behavior changes in an important way:

```text
008B: template-primary PNA reconstruction from RNA-derived sequence
008C: sequence-primary PNA generator
```

Prototype 008C is therefore useful, but it is not a replacement for structure-informed PNA reconstruction.

---

## Context

Earlier PNA milestones:

```text
Benchmark 011 → Prototype 008A.1 failure
Benchmark 012 → Prototype 008B success
Benchmark 013 → Prototype 008C regression/limitation characterization
```

Prototype 008A.1 failed because it tried to force a PNA pseudopeptide backbone directly onto the RNA fold.

Prototype 008B succeeded because it reversed the logic:

```text
PNA scaffold first
RNA sequence/base identity second
```

Prototype 008C extended this idea into a general sequence-primary generator.

---

## Prototype 008C Purpose

Prototype 008C answers this question:

```text
Can we generate a PNA-like strand carrying a requested nucleotide sequence?
```

It does **not** answer this question:

```text
Can we generate a PNA-like structural analog of a folded RNA molecule?
```

This distinction is crucial.

---

## Input Types Supported by Prototype 008C

Prototype 008C supports:

```bash
--rna input.pdb
--fasta input.fasta
--sequence CUAGGCUC
```

This is valuable because PNA is often better treated as a sequence carrier than as an RNA-fold-preserving analog.

---

## Visual Inspection Notes

### 8-mer

Observed behavior:

```text
clean enough
interpretable
PNA-like scaffold visible
bases attached
```

Interpretation:

```text
008C works well for short sequence-primary PNA generation.
```

### 34-mer

Observed behavior:

```text
elongated repeated motif
snake-like sequence carrier
less structurally informative
not an RNA-fold analog
```

Interpretation:

```text
008C scales as a PNA sequence generator, but global structure is template-tiling-driven.
```

### 111-mer

Expected/observed behavior:

```text
long sequence-carrier strand
not an HH ribozyme fold
not a tertiary-structure analog
```

Interpretation:

```text
008C should not be used to claim PNA reconstruction of complex RNA folds.
```

---

## Regression Character

The word "regression" here does not mean that Prototype 008C is useless.

It means:

```text
008C improved input flexibility,
but reduced structural-conversion relevance.
```

Compared with 008B:

```text
008B is better for documenting RNA-input-derived PNA candidate generation.
008C is better for direct sequence-to-PNA generation.
```

They should coexist.

---

## Why This Happens

PNA is chemically different from sugar-phosphate XNAs.

Most previous Digital Polymerase targets still had nucleic-acid-like scaffold logic:

```text
HNA
ANA
FANA
CeNA
XyNA
TNA
GNA
```

PNA instead uses:

```text
pseudopeptide backbone
neutral scaffold
nucleobases as side-chain-like groups
```

Because of this, long PNA structures cannot be assumed to preserve RNA tertiary geometry.

Sequence-primary tiling can create visually coherent chains, but it does not encode:

```text
RNA fold
RNA base-pairing geometry
RNA tertiary constraints
RNA local backbone topology
```

---

## Scientific Interpretation

Correct description:

```text
Prototype 008C is a sequence-primary PNA candidate generator.
```

Incorrect descriptions:

```text
Prototype 008C is an RNA-fold-preserving PNA converter.
Prototype 008C creates PNA hammerhead ribozyme structural analogs.
Prototype 008C produces physically validated PNA structures.
```

The correct scope is sequence-carrier generation.

---

## Relationship to Prototype 008B

Keep both prototypes:

```text
Prototype 008B → RNA PDB-derived PNA template-primary candidate generation
Prototype 008C → raw sequence / FASTA / RNA PDB sequence-to-PNA generation
```

Do not let 008C replace 008B.

008B is still the better milestone for the first successful PNA prototype because it emerged directly from the failed RNA-to-PNA conversion attempt and produced a clean 8-mer, 34-mer, and 111-mer sequence-carrier output.

008C is a convenience/generalization layer.

---

## Current Status

**Keep Prototype 008C:** yes  
**Promote as stable sequence generator:** not yet  
**Use as RNA-fold converter:** no  
**Use as sequence-to-PNA candidate generator:** yes  
**Use for MD as-is:** no  
**Use as evidence of solved PNA structural conversion:** no

---

## Recommended Next Step

The next meaningful PNA prototype should not merely extend 008C.

It should attempt a new hybrid strategy:

```text
Prototype 008D — RNA-informed PNA hybrid-guided builder
```

This would combine:

```text
RNA global spatial information
PNA local chemistry
chain-continuity optimization
base-orientation guidance
clash/crowding checks
```

Prototype 008D should be treated as a separate research attempt, not a simple patch of 008C.

---

## Stop Condition Reminder

If Prototype 008D also fails to produce a clean and interpretable 8-mer and 34-mer after a small number of rational attempts, PNA should be paused.

PNA does not need to be fully solved tonight to be scientifically valuable. The current PNA documentation already contains:

```text
one failed RNA-fold-forcing strategy
one successful template-primary strategy
one sequence-primary generator with clear limitations
one proposed hybrid path
```

That is already a strong methodological story.
