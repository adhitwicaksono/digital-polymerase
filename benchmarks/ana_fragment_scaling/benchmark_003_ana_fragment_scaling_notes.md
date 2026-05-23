# Benchmark 003: ANA Fragment-Guided Scaling Notes

**Project:** Digital Polymerase  
**Broader context:** XNA World Project  
**Benchmark:** 003  
**Prototype tested:** Prototype 002A — RNA → ANA fragment-guided reconstruction  
**Status:** Productive partial success / failure benchmark  
**Core finding:** Local residue alignment scales, but polymer-chain continuity is not enforced.

---

## Executive Summary

Benchmark 003 was designed to test whether the RNA → ANA fragment-guided converter can scale beyond the first 8-mer example.

The test used six RNA structures extracted from the same HH-type I ribozyme:

```text
8-mer
12-mer
16-mer
22-mer
34-mer
111-mer full structure
```

All were converted using the same 4-mer ANA template fragment.

The converter successfully processed all input sizes and generated reports for all outputs. Local anchor RMSD values remained stable at approximately 0.20 Å across all tested lengths.

However, follow-up structural evaluation revealed that the converted structures do **not** preserve valid inter-residue O3′–P chain continuity. Therefore, the benchmark should be interpreted as a **residue-local transformation success** but a **polymer-chain reconstruction failure**.

This is useful because it defines the next necessary Digital Polymerase module: **chain-continuity validation and chain-aware reconstruction**.

---

## Why This Benchmark Matters

Prototype 001, RNA → HNA, showed that full-template reconstruction can work for a short 8-mer when a comparable HNA template is available.

Prototype 002A asked a harder and more realistic question:

> What happens when the target XNA template is shorter than the RNA input?

For ANA, only a 4-mer template fragment was available. This forced the converter to use the ANA template as a local geometry donor rather than as a full-length residue-by-residue template.

This is an important real-world scenario because many XNA systems may not have full-length structural templates matching the source nucleic acid.

---

## Benchmark Design

### Inputs

The RNA inputs were reduced from a single HH-type I ribozyme source structure.

| Input | Length | Sequence |
|---|---:|---|
| `RNA-8mer.pdb` | 8 nt | `CUAGGCUC` |
| `RNA-12mer.pdb` | 12 nt | `CUAGGCUCGAAA` |
| `RNA-16mer.pdb` | 16 nt | `ACCACCUAGGCUCGAA` |
| `RNA-22mer.pdb` | 22 nt | `AUACGACCACCUAGGCUCGAAA` |
| `RNA-34mer.pdb` | 34 nt | `GGUGAAGAAUACGACCACCUAGGCUCGAAAGAGC` |
| `8t5o-HH-typeI-111mer-full.pdb` | 111 nt | full reduced HH ribozyme RNA |

### Target template

The ANA template was:

```text
1ho6_ANApart.pdb
```

It contains four ANA residues:

```text
GAO
UAR
CAR
CAR
```

The template includes G-like, U-like, and C-like ANA residue geometries, but lacks an A-like ANA residue.

---

## Method Tested

The tested method was **residue-local fragment-guided reconstruction**.

For each RNA residue:

1. identify the RNA base
2. choose an ANA template residue
3. align ANA template anchor atoms to RNA anchor atoms
4. transform the ANA backbone into the RNA residue frame
5. preserve the RNA base atoms
6. combine transformed ANA backbone with preserved RNA base
7. export an ANA-like candidate residue

The anchor atoms were:

```text
C1'
C2'
C3'
C4'
O4'
```

The converter pinned `C1'` after alignment to preserve base attachment geometry.

---

## What Worked

### 1. All input lengths were processed

The converter processed all tested RNA lengths:

```text
8 nt
12 nt
16 nt
22 nt
34 nt
111 nt
```

This shows that the parser and conversion loop can scale beyond the initial 8-mer case.

### 2. Local anchor RMSD remained stable

The mean anchor RMSD remained around 0.20 Å:

| Input | Mean anchor RMSD | Max anchor RMSD |
|---|---:|---:|
| 8-mer | 0.2036 Å | 0.2161 Å |
| 12-mer | 0.2048 Å | 0.2161 Å |
| 16-mer | 0.2046 Å | 0.2161 Å |
| 22-mer | 0.1962 Å | 0.2161 Å |
| 34-mer | 0.1989 Å | 0.2161 Å |
| 111-mer | 0.1961 Å | 0.2161 Å |

This suggests that local residue-level Kabsch alignment is numerically stable.

### 3. Sequence and residue count were preserved

The output reports preserved the number of residues and source sequence for each input.

### 4. The benchmark exposed a real algorithmic boundary

The benchmark clearly shows that local residue-level success does not imply whole-polymer success.

That is a valuable discovery for Digital Polymerase.

---

## What Failed

### Main failure: inter-residue chain continuity

The current converter transforms each residue locally and independently.

This means it does not enforce the covalent connection between:

```text
O3′ of residue i
P of residue i+1
```

In RNA, this distance is normally around:

```text
~1.6 Å
```

But in the converted ANA-like outputs, the distances were often far outside this range.

| Output | Mean O3′–P | Min O3′–P | Max O3′–P | Failed links |
|---|---:|---:|---:|---:|
| `converted_ana_8mer.pdb` | 3.203 Å | 0.935 Å | 5.303 Å | 7 / 7 |
| `converted_ana_12mer.pdb` | 2.793 Å | 0.847 Å | 5.303 Å | 11 / 11 |
| `converted_ana_16mer.pdb` | 2.965 Å | 0.847 Å | 5.303 Å | 15 / 15 |
| `converted_ana_22mer.pdb` | 2.635 Å | 0.847 Å | 5.303 Å | 19 / 21 |
| `converted_ana_34mer.pdb` | 2.968 Å | 0.847 Å | 6.350 Å | 31 / 33 |
| `converted_ana_HH_111mer.pdb` | 3.045 Å | 0.847 Å | 6.350 Å | 103 / 109 |

This is the strongest evidence that the current output is not a valid continuous ANA polymer.

---

## Why the Local RMSD Was Misleading

The converter reports local alignment RMSD using anchor atoms within each residue.

This tells us whether a local ANA template can be placed into the RNA residue frame.

It does **not** tell us whether the final residues are connected correctly as a polymer chain.

Therefore:

```text
low local RMSD ≠ valid polymer chain
```

This is the central lesson of Benchmark 003.

---

## Classification of the Output

The current outputs should be classified as:

```text
residue-local ANA-like candidate models
```

They should not be classified as:

```text
validated ANA polymers
MD-ready ANA structures
chemically confirmed ANA ribozymes
```

A better description is:

> ANA-like structures generated through residue-local fragment-guided backbone replacement, with preserved RNA bases and unvalidated inter-residue connectivity.

---

## Conversion-Level Classification

Digital Polymerase recognizes four conversion levels:

1. **Symbolic conversion**  
   Sequence or residue-name rewriting.

2. **Topological conversion**  
   Residue identity, atom naming, and local backbone topology assignment.

3. **Geometric reconstruction**  
   Candidate 3D coordinate generation using templates or coordinate transformations.

4. **Physically refined modeling**  
   Energy minimization, MD, force-field validation, and expert chemical inspection.

Benchmark 003 sits between:

```text
Level 2: topological/local residue transformation
```

and

```text
Level 3: local geometric reconstruction
```

It does not reach:

```text
Level 4: physically refined modeling
```

and it does not yet achieve chain-aware Level 3 reconstruction.

---

## Why This Should Be Archived Before Patching

This benchmark should be committed before modifying the converter because it documents a clean baseline.

It shows exactly what the current method can and cannot do:

| Capability | Status |
|---|---|
| Parse multiple RNA input sizes | Pass |
| Convert residue count consistently | Pass |
| Preserve source sequence | Pass |
| Use ANA 4-mer as local geometry donor | Pass |
| Maintain low local anchor RMSD | Pass |
| Preserve inter-residue O3′–P continuity | Fail |
| Produce MD-ready ANA polymer | Fail |
| Support biological interpretation | Fail |

This baseline will be useful for regression testing after patching the converter.

---

## Recommended Repository Status

Recommended label:

```text
Benchmark 003: partial success / chain-continuity failure benchmark
```

Recommended placement:

```text
benchmarks/ana_fragment_scaling/
```

The generated structures should be kept as benchmark outputs, not promoted as validated examples.

The script should remain:

```text
src/digital_polymerase/prototypes/rna_to_ana_fragment_guided.py
```

until chain-continuity validation and reconstruction are improved.

---

## Recommended Next Patch

Before progressing to FANA, patch ANA with chain-continuity reporting.

### Patch 002A.1: add chain-continuity validation

Add report metrics for:

```text
O3′(i) → P(i+1)
P(i) → O5′(i)
C1′ to base attachment sanity
missing atoms
residue completeness
```

Minimum report table:

```text
Inter-residue O3′–P continuity:
expected range: 1.4–1.8 Å
mean:
min:
max:
failed links:
```

This patch does not need to fix the geometry yet. It only needs to make the failure visible in every report.

---

## Recommended Next Algorithmic Upgrade

After validation is added, move toward fragment-chain reconstruction.

### Patch 002A.2: fragment-chain reconstruction

Instead of transforming residues independently, use connected ANA fragments.

Possible approach:

```text
RNA residues 1–4  ← ANA 4-mer template
RNA residues 2–5  ← ANA 4-mer template
RNA residues 3–6  ← ANA 4-mer template
...
```

Then use overlapping windows to choose or average coordinates while preserving chain continuity.

This may help the converter move from:

```text
residue-local reconstruction
```

to:

```text
fragment-chain reconstruction
```

---

## Why Not Progress to FANA Immediately?

FANA may be a promising next XNA target, but the current ANA benchmark revealed a core engine problem.

If FANA is built using the same residue-local method, it may also produce:

```text
low local RMSD
+
broken inter-residue polymer continuity
```

Therefore, ANA should be patched first.

Recommended order:

```text
1. Commit/archive Benchmark 003
2. Patch ANA report with chain-continuity validation
3. Patch ANA reconstruction strategy if possible
4. Only then proceed to FANA
```

---

## Key Takeaway

Benchmark 003 teaches:

> Local geometry placement is not enough. Digital Polymerase must become chain-aware.

This is the next development boundary.

The current ANA converter is not wrong to keep. It is valuable because it reveals the exact next problem that must be solved.

---

## Suggested README Addition

Add this to the project README or roadmap:

```text
Benchmark 003 showed that RNA → ANA fragment-guided reconstruction scales computationally from 8 nt to 111 nt, but residue-local conversion does not preserve inter-residue O3′–P chain continuity. Future versions will add chain-continuity validation and fragment-chain reconstruction before expanding to additional XNA targets.
```

---

## Suggested Commit Message

```bash
git add benchmarks/ana_fragment_scaling/
git commit -m "Add ANA fragment-guided scaling benchmark"
```

---

## Final Status

**Keep:** yes  
**Patch before FANA:** yes  
**Use for publication-level claims:** no  
**Use as software-development benchmark:** yes

This benchmark is not a failure of the project.

It is a successful discovery of the next algorithmic requirement.
