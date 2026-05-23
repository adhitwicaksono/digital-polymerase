# Prototype 008D Plan: RNA-Informed PNA Hybrid-Guided Builder

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Prototype:** 008D  
**Conversion:** RNA → PNA  
**Proposed method:** RNA-informed, PNA-chemistry-aware hybrid reconstruction  
**Status:** Design plan only; not yet implemented  
**Goal:** Attempt a better compromise between RNA structural guidance and PNA scaffold realism.

---

## Why Prototype 008D Is Needed

PNA has shown three distinct behaviors in Digital Polymerase:

```text
Prototype 008A.1 → RNA-fold-forced PNA reconstruction failed
Prototype 008B   → template-primary PNA generation succeeded
Prototype 008C   → sequence-primary PNA generation works but does not preserve RNA fold
```

This means a fourth strategy is needed if the project wants to attempt an actual structure-informed RNA → PNA conversion.

Prototype 008D should not force PNA onto the RNA fold too aggressively, but it also should not ignore RNA structure completely.

The intended compromise is:

```text
RNA-informed global path
+
PNA-compatible local scaffold
+
controlled chain-continuity optimization
```

---

## Core Concept

Prototype 008D should treat the input RNA as a **coarse spatial guide**, not as a geometry that must be copied atom-for-atom.

The RNA provides:

```text
residue order
base identity
base centroid
local chain tangent
local base orientation
approximate global fold/topology
```

The PNA template provides:

```text
pseudopeptide backbone geometry
C8′→base attachment geometry
C′(i)→N1′(i+1) linkage grammar
base donor atoms
local residue chemistry
```

The output should be a PNA-like candidate that is:

```text
less tangled than 008A.1
more RNA-informed than 008C
more structurally honest than direct RNA-fold forcing
```

---

## Proposed Method

### Step 1 — Extract RNA residue frames

For each RNA residue, compute:

```text
base identity
base centroid
glycosidic atom position
C1′ position
local chain tangent
base-plane normal
neighbor residue vectors
```

Possible RNA frame anchors:

```text
C1′
glycosidic N: N9 for A/G, N1 for C/U
base ring atoms
base centroid
previous/next C1′ or P positions
```

---

### Step 2 — Select PNA residue template

For each RNA base:

```text
A → APN donor
G → GPN donor
C → CPN donor
U → TPN/UPN donor with thymine methyl removed if necessary
```

The scaffold should use PNA backbone atoms:

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

---

### Step 3 — Place PNA monomers using RNA-informed local frames

Each PNA monomer should be initially placed so that:

```text
PNA base roughly matches RNA base orientation
PNA C8′ attaches near RNA glycosidic-base region
PNA residue order follows RNA residue order
```

Unlike 008A.1, this should **not** aggressively force the entire PNA backbone onto RNA sugar positions.

Suggested anchor priority:

```text
base ring alignment > base centroid > local tangent > sugar/backbone mimicry
```

This is because PNA is a base-displaying pseudopeptide scaffold, not a sugar-phosphate backbone.

---

### Step 4 — Chain-continuity optimization

After initial monomer placement, optimize:

```text
C′(i) → N1′(i+1)
C8′ → glycosidic N
internal PNA backbone distances
base-plane orientation
```

Unlike 008A.1, avoid suffix-wide aggressive correction.

Instead use local smoothing:

```text
small local rigid-body adjustments
limited neighbor-aware optimization
maximum movement threshold
clash penalty
base-orientation penalty
```

---

### Step 5 — Clash and crowding audit

PNA is flexible and can collapse easily.

Prototype 008D should include simple diagnostics:

```text
minimum heavy-atom distance
number of severe clashes
base-base overlap warning
backbone-backbone overlap warning
large displacement warning
```

Do not attempt full energy minimization yet.

The goal is a **geometry sanity audit**, not physical validation.

---

### Step 6 — Output report

The report should include:

```text
converted residue count
source sequence
template sequence
C8′→glycosidic N distances
C′(i)→N1′(i+1) distances
internal PNA backbone distances
base-plane deviation score
clash count
mean displacement from RNA guide
visual inspection recommendation
success/failure classification
```

---

## Proposed Success Criteria

Prototype 008D should be judged in tiers.

### Tier 1 — 8-mer

Minimum requirements:

```text
not tangled
bases attached
C8′→glycosidic N passes
C′(i)→N1′(i+1) mostly passes
no severe collapse
visual inspection acceptable
```

If 8-mer fails badly, stop and do not scale.

### Tier 2 — 34-mer

Minimum requirements:

```text
chain remains coherent
no catastrophic collapse
base placement remains interpretable
clash count manageable
global shape not absurdly over-compressed
```

If 34-mer fails badly, do not proceed to 111-mer.

### Tier 3 — 111-mer

Minimum requirements:

```text
global chain coherence
no molecular confetti
no severe global knotting
honest report that RNA fold is only partially/weakly guided
```

For 111-mer, success should not require perfect HH ribozyme fold preservation.

---

## Proposed Failure Criteria

Prototype 008D should be classified as failed if:

```text
8-mer is visibly tangled
bases detach or overlap severely
C8′→glycosidic N fails broadly
C′(i)→N1′(i+1) fails broadly
chain continuity only passes by causing visual collapse
output is worse than 008B
```

If the 8-mer fails after two or three rational algorithmic attempts, PNA structure-informed conversion should be paused.

---

## Recommended Implementation Strategy

Do not jump directly into a full large script.

Recommended staged implementation:

```text
008D.0 → frame extraction from RNA residues
008D.1 → place one PNA monomer per RNA residue using base-frame alignment
008D.2 → local pairwise C′→N1′ correction only
008D.3 → add clash/crowding audit
008D.4 → test 8-mer
008D.5 → test 34-mer only if 8-mer passes
008D.6 → test 111-mer only if 34-mer passes
```

This avoids repeating the 008A.1 mistake.

---

## What Not To Do

Avoid:

```text
forcing PNA backbone onto RNA sugar-phosphate coordinates
global suffix correction without movement limits
claiming RNA fold preservation too early
scaling to 111-mer before 8-mer and 34-mer pass
judging success only by distance metrics
```

Distance metrics are necessary but not sufficient.

Visual/global sanity matters for PNA.

---

## Relationship to Other PNA Prototypes

```text
008A.1 → failed RNA-fold-forced attempt
008B   → successful template-primary PNA base-replacement converter
008C   → sequence-primary PNA generator
008D   → proposed RNA-informed hybrid-guided builder
```

008D should not replace 008B or 008C.

Instead:

```text
008B = best current PNA benchmark success
008C = useful sequence generator
008D = experimental attempt to recover structure guidance
```

---

## Stop/Pause Rule

The project should stop or pause PNA prototyping if:

```text
008D cannot beat 008B visually for 8-mer and 34-mer
after two or three rational algorithmic attempts.
```

At that point, the honest conclusion should be:

```text
Digital Polymerase can generate clean PNA sequence-carrier candidates,
but structure-informed RNA-to-PNA conversion requires more advanced modeling,
possibly including force fields, conformational sampling, or dedicated PNA structural templates.
```

That is not a failure of the project. It is a scientifically useful boundary.

---

## Current Recommendation

Proceed to Prototype 008D only if the goal is to test the boundary.

If time, energy, or clarity becomes limited, freeze PNA at:

```text
Benchmark 011: failed RNA-fold-forced PNA attempt
Benchmark 012: successful template-primary PNA scaling
Benchmark 013: sequence-primary generator limitation
Prototype 008D: documented future plan
```

This is already a strong and honest PNA chapter.
