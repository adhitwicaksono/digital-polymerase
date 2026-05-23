# Benchmark 014: PNA Hybrid-Guided Boundary Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 014  
**Prototype tested:** Prototype 008D — RNA-informed PNA hybrid-guided builder  
**Status:** Important partial/negative result  
**Primary result:** Prototype 008D partially rescues local RNA-informed PNA placement but does not solve reliable RNA-fold-preserving PNA reconstruction at larger scale.

---

## Summary

Benchmark 014 documents the result of the Prototype 008D boundary test.

Prototype 008D was designed after three earlier PNA stages:

```text
008A.1 → failed RNA-fold-forced PNA attempt
008B   → successful template-primary PNA scaffold-first conversion
008C   → sequence-primary PNA generator with clear limitations
```

Prototype 008D attempted a hybrid compromise:

```text
RNA base-frame guidance
+
PNA local pseudopeptide scaffold
+
bounded C′(i)→N1′(i+1) smoothing
+
movement caps to prevent collapse
```

The purpose was to test whether PNA could be guided by RNA structure without collapsing into the tangled geometry observed in 008A.1.

The result is scientifically useful but not a full success.

---

## Core Finding

Prototype 008D shows that:

```text
RNA-informed PNA placement can work locally,
but reliable RNA-fold-preserving PNA reconstruction is not solved.
```

The output is not molecular confetti, and it does not fail as catastrophically as 008A.1. However, it also does not produce a clean PNA structural analog of the RNA input.

This places Prototype 008D in the category:

```text
partial rescue / boundary test / negative result
```

rather than:

```text
successful fold-preserving PNA converter
```

---

## Visual Inspection Summary

### 8-mer

Observed:

```text
not totally collapsed
bases present
some local organization visible
geometry still too separated/broken to call clean
```

Interpretation:

```text
Partial local rescue, not clean success.
```

The 8-mer is useful because it shows that 008D is less catastrophic than 008A.1. However, it is not as clean or conceptually robust as 008B.

---

### 34-mer

Observed:

```text
several local clusters
partial organization in pieces
loss of global coherence
not a clean continuous RNA-informed PNA analog
```

Interpretation:

```text
Hybrid guidance becomes unstable at medium scale.
```

This is the decisive warning sign. If the 34-mer cannot maintain coherent global architecture, the method should not be claimed as a solved structural converter.

---

### 111-mer HH ribozyme-derived RNA

Observed:

```text
distributed semi-collapsed domains
local organization
no clean RNA-like global fold preservation
not a clean elongated template-primary PNA strand either
```

Interpretation:

```text
008D defines the boundary between local guidance and global fold failure.
```

The 111-mer output is scientifically valuable as a boundary case, but it is not a PNA hammerhead ribozyme structural analog.

---

## Comparison with Earlier PNA Prototypes

| Prototype | Strategy | Result | Interpretation |
|---|---|---|---|
| 008A.1 | Force PNA backbone onto RNA fold | Failed/tangled | Too aggressive |
| 008B | PNA scaffold first, replace bases by RNA sequence | Successful | Best current practical PNA converter |
| 008C | Sequence/FASTA/RNA sequence to PNA | Useful but limited | Sequence carrier, not fold-preserving |
| 008D | RNA base-frame guidance + bounded smoothing | Partial/negative | Boundary test; fold preservation remains unstable |

---

## Why 008D Did Not Fully Solve PNA

PNA is not merely a sugar-modified nucleic acid.

Most previous Digital Polymerase XNA targets retain some nucleic-acid-like scaffold logic:

```text
HNA
ANA
FANA
CeNA
XyNA
TNA
GNA
```

PNA is different:

```text
PNA uses a pseudopeptide backbone.
PNA lacks the sugar-phosphate geometry that RNA fold motifs depend on.
PNA has different flexibility, spacing, and torsional behavior.
```

Therefore, RNA tertiary geometry does not transfer cleanly into PNA using only coordinate transformation and local distance correction.

Prototype 008D confirms this limitation.

---

## What 008D Proves

Prototype 008D proves that:

```text
bounded hybrid guidance can avoid the worst catastrophic collapse,
but it cannot currently preserve RNA fold architecture across larger RNAs.
```

This is valuable because it prevents overclaiming.

It also clarifies the current methodological boundary:

```text
Digital Polymerase can generate PNA sequence carriers.
Digital Polymerase cannot yet reliably generate RNA-fold-preserving PNA analogs.
```

---

## What 008D Does Not Prove

Prototype 008D does **not** prove that:

```text
PNA cannot form structured molecules.
PNA cannot bind nucleic acids.
PNA is impossible to model.
RNA-like PNA analogs are impossible.
```

It only shows that:

```text
this current prototype framework is insufficient for reliable RNA-fold-informed PNA reconstruction.
```

This is an important distinction.

---

## Scientific Interpretation

Correct description:

```text
Prototype 008D is an RNA-informed PNA boundary-test that partially preserves local organization but does not solve global fold-preserving PNA reconstruction.
```

Incorrect descriptions:

```text
Prototype 008D is a successful PNA hammerhead-ribozyme converter.
Prototype 008D proves PNA is untameable.
Prototype 008D is useless because it did not fully pass.
Prototype 008D produces physically validated PNA structures.
```

The correct interpretation is methodological boundary mapping.

---

## Recommended Repository Status

Keep Prototype 008D as:

```text
src/digital_polymerase/prototypes/rna_to_pna_hybrid_guided.py
```

Recommended benchmark path:

```text
benchmarks/pna_scaling/benchmark_014_pna_hybrid_guided_boundary_notes.md
```

Recommended report interpretation:

```text
partial/negative result
```

Do not promote Prototype 008D to stable converter.

---

## Recommended Stop Rule

The current PNA prototype line should pause here if the goal is RNA-fold-preserving conversion.

The stop condition is satisfied because:

```text
8-mer is not cleanly stable
34-mer loses global coherence
111-mer does not preserve meaningful fold architecture
```

Further progress likely requires a different level of modeling, such as:

```text
PNA-specific force fields
conformational sampling
better PNA structural templates
explicit topology files
energy minimization
PNA duplex/single-strand structural priors
```

---

## Final Status

**Keep:** yes  
**Promote to stable converter:** no  
**Use for MD as-is:** no  
**Use as successful fold-preserving benchmark:** no  
**Use as boundary evidence:** yes  
**Continue brute-force patching tonight:** no  

Prototype 008D is the right place to pause the current PNA attack line and declare the boundary.
