# Prototype 002A.2 Patch Summary

**Project:** Digital Polymerase  
**Patch:** Prototype 002A.2  
**Mode added:** `ana-chain-preserving`  
**Purpose:** Preserve source RNA polymer-chain continuity while replacing ANA-sensitive local atoms from the ANA fragment template.

---

## What changed

Prototype 002A.1 detected that residue-local RNA → ANA reconstruction produced low local RMSD but failed inter-residue O3′→P continuity.

Prototype 002A.2 adds a new default mode:

```text
ana-chain-preserving
```

In this mode, the converter:

1. preserves the source RNA chain atoms that define polymer continuity
2. preserves RNA base atoms in their source coordinates
3. aligns the ANA fragment template using local anchors
4. replaces ANA-sensitive local atoms, currently `C2′` and `O2′`, using the aligned ANA template
5. validates O3′→P and P→O5′ continuity in the report

This is better suited to ANA than whole-backbone replacement because ANA is close to RNA in overall chain architecture.

---

## Scaling result with default `ana-chain-preserving` mode

| Input | Converted residues | Mean anchor RMSD | Max anchor RMSD | O3′→P failed links | O3′→P status |
|---|---:|---:|---:|---:|---|
| RNA-8mer | 8 | 0.0407 Å | 0.0644 Å | 0 / 7 | PASS |
| RNA-12mer | 12 | 0.0389 Å | 0.0644 Å | 0 / 11 | PASS |
| RNA-16mer | 16 | 0.0392 Å | 0.0644 Å | 0 / 15 | PASS |
| RNA-22mer | 22 | 0.0548 Å | 0.1377 Å | 0 / 21 | PASS |
| RNA-34mer | 34 | 0.0484 Å | 0.1377 Å | 0 / 33 | PASS |
| HH 111mer | 111 | 0.0489 Å | 0.1414 Å | 0 / 109 | PASS |

---

## Important scientific caution

This patch improves chain-continuity behavior, but it does **not** make the output a validated ANA molecule.

The output should still be interpreted as:

> an ANA-like chain-preserving candidate structure.

It should not be interpreted as:

> a chemically validated, force-field-ready, experimentally confirmed ANA polymer.

Remaining requirements include stereochemistry validation, explicit topology/connectivity support, energy minimization, force-field compatibility, and expert chemical inspection.
