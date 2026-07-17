# FANA Level 4 Physical-Readiness Gate

Digital Polymerase separates geometric reconstruction from physical modeling.
The stable RNA-to-FANA converter produces a Level 3 coordinate candidate. The
FANA physical-readiness gate is the first Level 4 bridge: it makes topology and
parameterization gaps explicit before anyone attempts minimization or molecular
dynamics.

## What the gate does

For a FANA-only candidate PDB, the gate:

1. constructs an explicit covalent graph for the phosphate, sugar, F2′
   substituent, glycosidic attachment, nucleobases, and consecutive
   phosphodiester linkages;
2. checks every modeled covalent distance against a deliberately broad
   chemistry-aware interval;
3. compares the sign of the C2′/F2′ stereochemical volume with fluorinated
   residues in the supplied experimental template;
4. fits the five endocyclic sugar torsions to a pseudorotation phase and
   amplitude, then compares each residue with the nearest same-base template
   reference;
5. identifies consecutive chain segments and records both terminal states as
   unresolved;
6. optionally writes a PDB containing explicit `CONECT` records; and
7. writes a Markdown report plus a versioned JSON handoff manifest.

The pseudorotation phase is used only as a template-relative metric under the
same fitting convention. The gate does not independently assign north, south,
east, or west labels from its phase value.

## Status semantics

| Status | Meaning |
|---|---|
| `GEOMETRY_GATE_FAILED` | At least one required atom, covalent distance, C2′ stereochemical sign, or template-relative sugar-pucker check failed. |
| `PARAMETERIZATION_REQUIRED` | The modeled geometry passed, but the structure is not MD-ready because physical parameters remain unresolved. |

There is intentionally no `MD_READY` result. Digital Polymerase cannot make
that claim from coordinates alone.

## Run from the command line

First generate a FANA candidate:

```bash
digital-polymerase-fana \
  --rna input_rna.pdb \
  --template benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb \
  --output candidate_fana.pdb \
  --report conversion_report.md \
  --metrics conversion_metrics.json \
  --strict
```

Then run the physical-readiness gate:

```bash
digital-polymerase-fana-readiness \
  --candidate candidate_fana.pdb \
  --template benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb \
  --report fana_readiness.md \
  --manifest fana_readiness.json \
  --conect-output candidate_fana_conect.pdb \
  --strict
```

`--strict` raises only when the geometry gate fails. A successful invocation
still reports `PARAMETERIZATION_REQUIRED`.

## Python API

```python
from digital_polymerase.physical import audit_fana_physical_readiness

result = audit_fana_physical_readiness(
    "candidate_fana.pdb",
    "2KP4_FANA_10mer.pdb",
    "fana_readiness.md",
    "fana_readiness.json",
    conect_pdb="candidate_fana_conect.pdb",
    strict=True,
)

assert result.geometry_ok
assert result.status == "PARAMETERIZATION_REQUIRED"
```

## Why parameterization remains blocked

The gate records these unresolved requirements:

- complete hydrogen placement and protonation states;
- force-field atom types;
- partial atomic charges;
- bonded and nonbonded parameters with versions and provenance;
- 5′ and 3′ terminal protonation or capping states; and
- mapping from PDB residue names to validated force-field residue templates.

The emitted `CONECT` records describe connectivity only. They do not encode
bond order, equilibrium values, force constants, charges, or nonbonded terms.

## Amber/modXNA handoff

The modXNA catalog identifies fragment `A5L` as a 2′FANA sugar/linker built in a
C2′-endo conformer. The manifest records that catalog match as a suggested
parameterization route. It does not automatically select backbone/base modules
or claim that `A5L` alone parameterizes a FANA polymer.

An external parameterization workflow must select and validate:

1. the Amber-family parent force field and exact version;
2. backbone and base modules compatible with the FANA sugar/linker;
3. internal and terminal residue forms;
4. atom-name and residue-name mappings;
5. charges, atom types, and all missing parameters; and
6. minimization and MD protocols with appropriate controls.

Digital Polymerase v0.1.2 turns those requirements into a candidate-bound,
hash-validated manifest contract and can prepare an unexecuted Amber input
bundle after the contract passes. See
[`fana_external_parameter_gate.md`](fana_external_parameter_gate.md). The
external gate does not provide parameters or replace scientific review.

## Primary references

- Love O. et al. *modXNA: A Modular Approach to Parametrization of Modified
  Nucleic Acids for Use with Amber Force Fields.* J. Chem. Theory Comput. 2024.
  https://doi.org/10.1021/acs.jctc.4c01164
- Galindo-Murillo R. et al. *Parameterizing modified nucleic acids for molecular
  simulations in the AMBER MD software environment.* Living J. Comput. Mol.
  Sci. 2025. https://doi.org/10.33011/livecoms.6.1.4545
- modXNA fragment catalog: https://modxna.chpc.utah.edu/catalog/
- Experimental FANA/RNA hybrid template 2KP4:
  https://www.rcsb.org/structure/2KP4

These references establish the parameterization route and experimental
template context. Digital Polymerase does not redistribute or silently embed
their force-field parameters.
