# FANA External-Parameter Gate

Digital Polymerase v0.1.2 adds the boundary between the FANA Level 4 geometry
handoff and a controlled Amber minimization attempt. The gate validates a
candidate-bound external-parameter manifest and can prepare Amber input files.
It never runs Amber and never treats a structurally valid manifest as proof that
the parameters are scientifically correct.

The repository does not ship FANA force-field parameters. Parameter artifacts
must come from an independently reviewed external workflow.

## Workflow

Start with a FANA candidate whose v0.1.1 readiness manifest reports both
`PARAMETERIZATION_REQUIRED` and a passing geometry gate.

Create a candidate-specific manifest template:

```bash
digital-polymerase-fana-parameters init \
  --candidate candidate_fana.pdb \
  --readiness fana_readiness.json \
  --output fana_parameters.json
```

The generated template is intentionally blocked. Complete it only after the
parameterization artifacts and review evidence exist. Store every referenced
artifact at a relative path beneath the directory containing
`fana_parameters.json`.

Run the preflight and bundle preparer:

```bash
digital-polymerase-fana-parameters prepare \
  --candidate candidate_fana.pdb \
  --readiness fana_readiness.json \
  --parameters fana_parameters.json \
  --output-dir fana_amber_bundle
```

The command returns exit code 1 when blocked. Once a completed manifest passes,
it reports `PREPARED_NOT_EXECUTED` and writes reviewable inputs to
`fana_amber_bundle/`. Add `--strict` in automation when a blocker should raise a
validation error. Use `--overwrite` only after inspecting the destination.

## Required manifest evidence

| Area | Required declaration |
|---|---|
| Candidate identity | Exact SHA-256 hashes of the candidate PDB and Level 4 readiness manifest |
| Parent force field | Name, version, and LEaP source file |
| Parameter generator | Tool name, version, command provenance, and base-specific fragments; modXNA routes must declare `A5L` as the FANA sugar/linker fragment |
| Residue mappings | One unique 1–3 character Amber residue name for every observed internal chemistry and exact input atom-name inventories |
| Termini | Explicit 5′ and 3′ chemistry, residue-library names, and reviewed source-atom removals for every chain segment |
| Artifacts | Relative paths, roles, and exact SHA-256 hashes for at least one `frcmod` and one residue-library artifact |
| Coverage | Explicit confirmation of atom names, atom types, charges, bonds, angles, dihedrals, impropers, and nonbonded terms |
| Charges | Charge method, quantum method, integer expected total charge, and validation confirmation |
| Review | Approved status, named reviewer, ISO review date, and at least one evidence reference |
| Protocol | Solvent, ion, buffer, cutoff, and bounded two-stage minimization settings |

Artifact hashes are recalculated. Paths that escape the manifest directory,
unsafe LEaP filenames, missing residue names, unresolved terminal states, and
incomplete declarations block bundle generation.

The v0.1.4 manifest contract accepts an additive `remove_atoms` list on each terminal
declaration. The only supported normalization is removal of `P`, `OP1`, and
`OP2` from the first source residue when using a neutral 5′-OH library; the
3′ declaration cannot remove source atoms. Every named atom must exist at the
declared terminus. The preparer applies the operation before writing
`candidate_amber_names.pdb`, and the post-run audit uses the same normalized
comparison inventory.

## Prepared bundle

A passing preflight writes:

- a candidate PDB renamed to the approved internal and terminal Amber residue
  names, with approved terminal atom normalization applied;
- copies of the hash-validated parameter files;
- `tleap.in` for loading parameters, checking the unit, solvating with OPC,
  neutralizing, and writing topology/coordinates;
- restrained-solvent and unrestrained minimization control files;
- a deliberately non-executable `run_minimization.sh` review artifact;
- snapshots of both input manifests; and
- JSON and Markdown preflight reports with `executed: false`.

No `tleap`, `sander`, or `ambpdb` process is launched. Their absence is reported
as a warning because preparation remains portable without AmberTools.

For the candidate-bound 8-mer campaign initializer and the post-minimization
structural audit, continue with
[`fana_controlled_minimization.md`](fana_controlled_minimization.md).

## Scientific boundary

The gate verifies consistency and provenance claims. It cannot establish that
atom types, charges, equilibrium values, force constants, torsions, terminal
chemistry, or the selected parent force field accurately model FANA. A named
expert must review those choices and their evidence.

After preparation, run LEaP manually in a reviewed AmberTools environment.
Reject unknown atoms, missing atom types or parameters, duplicate/conflicting
parameters, and unexplained charge differences. Before any dynamics, inspect
minimization energies and gradients, structural drift, covalent geometry, C2′
stereochemistry, and sugar pucker.

## Primary references

- Love O. et al. *modXNA: A Modular Approach to Parametrization of Modified
  Nucleic Acids for Use with Amber Force Fields.* J. Chem. Theory Comput. 2024.
  https://doi.org/10.1021/acs.jctc.4c01164
- Galindo-Murillo R. et al. *Parameterizing modified nucleic acids for molecular
  simulations in the AMBER MD software environment.* Living J. Comput. Mol.
  Sci. 2025. https://doi.org/10.33011/livecoms.6.1.4545
- modXNA fragment catalog: https://modxna.chpc.utah.edu/catalog/
- modXNA LEaP handoff tutorial:
  https://modxna.chpc.utah.edu/generate-a-phosphothioate-backbone-residue/
- Amber file formats: https://ambermd.org/FileFormats.php
- Experimental FANA/RNA hybrid template 2KP4:
  https://www.rcsb.org/structure/2KP4
