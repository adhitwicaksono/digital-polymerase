# Digital Polymerase Core

This directory is reserved for reusable **core utilities** shared across Digital Polymerase prototypes, converters, examples, and benchmarks.

The purpose of `core/` is to prevent each RNA → XNA prototype from becoming an isolated one-off script.

---

## Purpose

The `core/` module will eventually provide shared functionality for:

- PDB parsing
- residue handling
- atom classification
- base/backbone separation
- coordinate alignment
- Kabsch transformation
- PDB writing
- validation reporting
- chain-continuity checking
- polymer metadata handling

These utilities should be used by both:

```text
src/digital_polymerase/prototypes/
src/digital_polymerase/converters/
```

---

## Why Core Exists

Early Digital Polymerase prototypes showed that many tasks are repeated across converters.

For example, both RNA → HNA and RNA → ANA require:

```text
parse PDB
identify residues
split backbone and base atoms
choose alignment anchors
perform Kabsch alignment
transform coordinates
write output PDB
write report
warn about limitations
```

Without a shared `core/`, each converter would duplicate this logic and become harder to test.

---

## Planned Modules

A possible future structure:

```text
core/
├── README.md
├── pdb_parser.py
├── residue.py
├── atom_classifier.py
├── alignment.py
├── geometry.py
├── pdb_writer.py
├── validators.py
├── reports.py
└── exceptions.py
```

---

## Module Responsibilities

### `pdb_parser.py`

Parse PDB coordinate files into structured Python objects.

Expected responsibilities:

- read `ATOM` and `HETATM` records
- preserve chain ID
- preserve residue number
- preserve insertion code if present
- preserve atom name
- preserve residue name
- preserve coordinates
- preserve element, occupancy, and B-factor where available

Future residue keys should ideally use:

```python
(chain_id, residue_number, insertion_code)
```

rather than only residue number.

---

### `residue.py`

Represent residues in a consistent internal format.

Expected responsibilities:

- store residue metadata
- access atom coordinates
- retrieve residue base identity
- update residue names
- copy or transform residue atoms
- preserve source-to-output mapping

---

### `atom_classifier.py`

Classify atoms into functional groups.

Expected categories:

```text
backbone atoms
sugar/scaffold atoms
phosphate atoms
nucleobase atoms
hydrogen atoms
unknown atoms
```

This module should avoid overly broad substring matching when possible.

---

### `alignment.py`

Coordinate-alignment utilities.

Expected responsibilities:

- implement Kabsch alignment
- compute rotation and translation
- transform atom coordinates
- calculate local alignment RMSD
- handle degenerate or missing anchor atoms

This module should be reusable across template-guided and fragment-guided converters.

---

### `geometry.py`

Geometry utilities.

Expected responsibilities:

- calculate distances
- calculate angles
- calculate dihedrals
- estimate RMSD
- check steric proximity
- compare local coordinate frames

---

### `pdb_writer.py`

Write candidate structures to PDB format.

Expected responsibilities:

- write `ATOM` or `HETATM` records
- preserve or renumber atom IDs
- write project-specific `REMARK` lines
- optionally write `CONECT` records in future versions
- keep output formatting compatible with molecular viewers

---

### `validators.py`

Structural validation utilities.

Minimum planned checks:

- residue count
- missing atoms
- base atom completeness
- backbone atom completeness
- local anchor RMSD
- inter-residue `O3′(i) → P(i+1)` distance
- `P(i) → O5′(i)` distance
- suspicious clashes
- unusually short or long distances
- chain breaks

The ANA scaling benchmark showed that this module is essential.

---

### `reports.py`

Generate Markdown conversion reports.

Expected report sections:

- project/prototype metadata
- input files
- source sequence
- template index
- method summary
- settings
- alignment summary
- per-residue conversion table
- chain-continuity validation
- scientific interpretation
- limitations
- recommended next steps

---

### `exceptions.py`

Custom error classes for clearer failure handling.

Possible errors:

```text
MissingAtomError
ResidueMappingError
TemplateCoverageError
AlignmentError
ChainContinuityError
UnsupportedPolymerError
```

---

## Current Development Priorities

The first `core/` utilities should be extracted from existing prototype scripts in this order:

1. `alignment.py`  
   Kabsch alignment and RMSD calculation

2. `pdb_parser.py`  
   Chain-aware PDB parsing

3. `atom_classifier.py`  
   Safer backbone/base atom classification

4. `pdb_writer.py`  
   Output PDB writer with warning `REMARK` lines

5. `validators.py`  
   Residue completeness and O3′–P chain-continuity checks

6. `reports.py`  
   Standardized Markdown report generation

---

## Core Design Principles

### 1. Be explicit

Do not hide chemistry behind vague labels.

A converter should say whether it performs:

```text
symbolic conversion
topological conversion
geometric reconstruction
physically refined modeling
```

### 2. Preserve metadata

Keep source residue IDs, chain IDs, and mapping information whenever possible.

### 3. Validate before trusting

A script that writes a PDB has not necessarily produced a valid molecule.

### 4. Separate local and chain-level metrics

Local anchor RMSD is not enough.

Reports should distinguish:

```text
local residue geometry
inter-residue chain continuity
global structural preservation
```

### 5. Make failures useful

Digital Polymerase benchmarks should archive failure cases because they define the next algorithmic boundary.

---

## Relationship to Benchmarks

Core validation utilities should be tested against existing benchmarks:

```text
Benchmark 002: HH ribozyme RNA → HNA failure benchmark
Benchmark 003: ANA fragment-guided scaling benchmark
```

Benchmark 003 especially requires `validators.py` because it revealed that low local RMSD can coexist with broken O3′–P chain continuity.

---

## Relationship to Polymer Metadata

Eventually, `core/` should interact with a polymer metadata system, for example:

```text
src/digital_polymerase/polymer_db/
```

Possible metadata:

```text
polymer name
residue naming conventions
expected backbone atoms
expected base atoms
linkage atoms
anchor atoms
template residue names
base fallback rules
```

This will help avoid hardcoding residue policies inside converter scripts.

---

## Suggested Future Layout with Polymer DB

```text
src/digital_polymerase/
├── core/
│   ├── pdb_parser.py
│   ├── atom_classifier.py
│   ├── alignment.py
│   ├── validators.py
│   └── reports.py
├── polymer_db/
│   ├── polymers.yaml
│   ├── residue_names.yaml
│   └── anchor_atoms.yaml
├── prototypes/
└── converters/
```

---

## Testing Goals

Core functions should eventually have unit tests under:

```text
tests/
```

Suggested tests:

```text
test_pdb_parser.py
test_atom_classifier.py
test_alignment.py
test_validators.py
test_reports.py
```

Minimum expected tests:

- Kabsch alignment returns low RMSD for known transformed point sets
- parser preserves chain and residue numbering
- atom classifier separates base and backbone atoms correctly
- chain-continuity validator detects broken O3′–P links
- report writer creates valid Markdown output

---

## Current Status

This directory is currently a placeholder for the shared engine of Digital Polymerase.

The immediate next patch should prioritize:

```text
chain-continuity validation
```

because Benchmark 003 showed that residue-local reconstruction can produce low local RMSD while failing polymer-chain continuity.

---

## Development Reminder

`core/` should not contain project-specific one-off logic.

If a function only works for one prototype, it belongs in:

```text
prototypes/
```

If a function can support multiple converters or benchmarks, it belongs in:

```text
core/
```

Digital Polymerase should grow from prototypes into a reusable framework.
