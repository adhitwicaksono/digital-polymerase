# Benchmark 011: PNA Failure Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 011  
**Prototype tested:** Prototype 008A.1 — RNA → PNA chimaera-guided pseudopeptide-backbone reconstruction  
**Status:** Failed / rough first-pass attempt  
**Primary result:** The converter produced connected PNA-like candidate structures, but the 8-mer visual inspection showed severe tangling/collapse. Prototype 008A.1 should not be archived as a successful PNA converter.

---

## Summary

Benchmark 011 documents the first RNA → PNA attempt in Digital Polymerase.

PNA, or peptide nucleic acid, is fundamentally different from the previous XNA targets. It is not a sugar-modified nucleic acid. Instead, PNA replaces the sugar-phosphate backbone with a pseudopeptide backbone, while nucleobases are attached as side-chain-like groups.

Earlier successful Digital Polymerase candidate-generation families include:

```text
HNA   → Prototype 001B/001C.1
ANA   → Prototype 002A.2
FANA  → Prototype 003A
CeNA  → Prototype 004A
XyNA  → Prototype 005A
TNA   → Prototype 006B.4
GNA   → Prototype 007A
```

PNA is different enough that the RNA-to-XNA strategies used previously did not transfer cleanly.

Prototype 008A.1 attempted to generate PNA-like structures from RNA inputs using a chimaera-guided pseudopeptide-backbone reconstruction strategy. Although the output was not molecular confetti and likely retained some topological connectivity, the 8-mer visual inspection showed severe tangling. Because the 8-mer is the simplest benchmark case, this is enough to classify the attempt as a failed or rough prototype.

---

## Why This Benchmark Exists

Failure documentation is useful because PNA revealed a limitation of the current Digital Polymerase strategy.

For HNA, ANA, FANA, CeNA, XyNA, TNA, and GNA, the general strategy was:

```text
RNA structure
→ target XNA scaffold reconstruction
→ local template-guided geometry correction
→ output candidate
```

For PNA, this became problematic because PNA does not preserve the sugar-phosphate logic of RNA.

The failure of Prototype 008A.1 shows that:

```text
PNA should not be forced directly onto an RNA fold using aggressive linkage correction.
```

Instead, future PNA conversion should likely start from a PNA scaffold and transplant or mutate bases according to the RNA sequence.

---

## PNA Template

The template used for Prototype 008A.1 was:

```text
3mbs_PNA-1mer-8.pdb
```

Observed PNA-like residues included:

```text
APN
TPN
GPN
CPN
```

Important PNA scaffold atoms observed in the template:

```text
C8'
C7'
O7'
N4'
C3'
C2'
N1'
C5'
C'
O1'
```

Observed PNA-like base attachment:

```text
C8′ → glycosidic N
```

Observed PNA-like polymer linkage:

```text
C′(i) → N1′(i+1)
```

---

## Prototype 008A.1 Strategy

Prototype 008A.1 used a chimaera-guided strategy:

1. infer source RNA base identity
2. select a PNA template residue by base class
3. place the PNA pseudopeptide scaffold using neighboring RNA `C1′` positions as guide points
4. enforce PNA `C′(i)→N1′(i+1)` continuity using suffix-linkage correction
5. attach the source RNA base to PNA `C8′`
6. export a PNA-like candidate PDB
7. validate PNA-specific backbone and base-attachment geometry

The intention was to preserve some relationship to the original RNA fold while converting the backbone into a PNA-like pseudopeptide chain.

---

## Test Inputs

Prototype 008A.1 was generated for the usual Digital Polymerase scaling inputs:

```text
RNA-8mer.pdb
RNA-12mer.pdb
RNA-16mer.pdb
RNA-22mer.pdb
RNA-34mer.pdb
8t5o-HH-typeI-111mer-full.pdb
```

However, the benchmark was stopped at visual inspection of the 8-mer because the simplest output was already too tangled to trust.

---

## Visual Inspection Result

The first inspected output was:

```text
converted_pna_RNA-8mer_auto_008A1.pdb
```

Visual result:

```text
Severely tangled / collapsed.
```

The output was not completely fragmented and did not look like random molecular confetti, but it appeared over-knotted and geometrically unsafe.

Current visual classification:

```text
PNA 8-mer visual status: FAIL / rough chimaera capture
Topological status: probably connected
Chemical-geometry status: too tangled to trust
```

This is especially important because the 8-mer should be the easiest benchmark. If the 8-mer is visually tangled, then larger outputs such as 34-mer and 111-mer should not be interpreted as successful even if report-level distance checks appear acceptable.

---

## Likely Failure Mode

The most likely failure mode is that Prototype 008A.1 optimized for linkage-level metrics while sacrificing global visual and geometric sanity.

The converter attempted to satisfy:

```text
C′(i) → N1′(i+1)
```

using suffix-linkage correction.

This likely caused downstream residues to shift too aggressively, pulling the pseudopeptide backbone into a collapsed or over-knotted shape.

In short:

```text
The metric may pass,
but the molecule looks cursed.
```

This is not a safe success criterion.

---

## Why Report-Level Validation Was Not Enough

For previous XNA families, report-level validation worked reasonably well because the target structures still resembled nucleic-acid-like polymers or could be interpreted through target-specific linkage checks.

For PNA, distance validation alone is insufficient.

A PNA-like output must satisfy:

```text
local pseudopeptide geometry
base attachment geometry
chain continuity
global scaffold sanity
base orientation
lack of severe collapse
```

Prototype 008A.1 may satisfy some local constraints but fails visual/global sanity at the 8-mer level.

---

## Scientific Interpretation

Correct description:

```text
Prototype 008A.1 is a failed or rough first attempt at RNA-to-PNA candidate generation.
```

Incorrect descriptions:

```text
validated PNA converter
successful PNA scaling benchmark
MD-ready PNA output
physically reliable PNA reconstruction
```

The output should not be used as a successful PNA benchmark.

---

## Current Status

**Keep as historical failure note:** yes  
**Promote as successful converter:** no  
**Use for MD as-is:** no  
**Use as benchmark success:** no  
**Use to guide next prototype:** yes

Prototype 008A.1 should remain documented as a failure/learning step.

Recommended file placement:

```text
benchmarks/pna_scaling/benchmark_011_pna_failure_notes.md
```

---

## Recommended Next Strategy: Prototype 008B

The next PNA strategy should avoid forcing a PNA backbone directly onto the RNA fold.

Instead of:

```text
RNA fold → force PNA backbone onto it
```

try:

```text
PNA scaffold → mutate/transplant bases according to RNA sequence
```

Recommended Prototype 008B direction:

1. use the PNA template as the primary scaffold
2. preserve the template PNA pseudopeptide backbone
3. replace or transplant bases to match the RNA sequence
4. validate `C8′→glycosidic N`
5. validate `C′(i)→N1′(i+1)`
6. inspect the 8-mer visually first
7. only after a clean 8-mer, attempt tiling/scaling to longer inputs

This means PNA should be handled more like:

```text
template-primary base replacement
```

rather than:

```text
RNA-primary scaffold conversion
```

---

## Proposed Prototype 008B Goals

Prototype 008B should aim for:

```text
clean PNA 8-mer first
```

before any scaling attempt.

Minimum success criteria:

```text
8-mer not tangled
bases attached
pseudopeptide backbone coherent
C′(i)→N1′(i+1) reasonable
C8′→glycosidic N reasonable
carbonyl/base atoms present
visual inspection acceptable in stick view
```

Only after that should the project attempt:

```text
34-mer PNA candidate
111-mer PNA candidate
```

---

## Lessons Learned

PNA teaches a new Digital Polymerase rule:

```text
Some XNAs are not converted from RNA geometry.
Some XNAs require template-first reconstruction.
```

For PNA, the sugar-phosphate-to-pseudopeptide jump is too large for the current RNA-primary conversion strategy.

The chimaera is not defeated yet, but Benchmark 011 identifies the failure mode and gives a clearer path toward Prototype 008B.
