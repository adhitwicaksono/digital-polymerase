# FANA Controlled-Minimization Campaign

Digital Polymerase v0.1.3 adds reproducible campaign initialization and a
post-run audit for the first controlled FANA minimization. It still does not
ship force-field parameters or execute Amber.

Digital Polymerase v0.1.4 adds an explicit terminal atom-normalization contract.
An approved neutral 5′-OH template may remove the source candidate's terminal
`P`, `OP1`, and `OP2` atoms before LEaP. The same declaration is honored by
bundle preparation and the post-minimization structural audit; hand-editing the
prepared candidate is neither required nor allowed by the reproducible route.

## Current status

The software path is ready, but the physical campaign remains
`EXTERNAL_PARAMETERS_REQUIRED`. Closing the milestone requires genuine external
parameters, family-consistent fragment choices, resolved terminal chemistry,
Amber execution, and expert review.

## Initialize the campaign

Use the canonical RNA 8-mer as the first target:

```bash
digital-polymerase-fana-campaign init \
  --rna benchmarks/ana_fragment_scaling/inputs/RNA-8mer.pdb \
  --template benchmarks/fana_fragment_scaling/templates/2KP4_FANA_10mer.pdb \
  --output-dir fana_8mer_campaign
```

The command copies both inputs and regenerates the candidate, conversion
metrics, Level 4 readiness handoff, unresolved parameter manifest, explicit
connectivity PDB, campaign metadata, and review instructions. It does not
create parameter artifacts.

## Fragment decision boundary

The modXNA catalog identifies `A5L` as the 2′FANA sugar/linker built C2′-endo.
It does not uniquely determine the remaining parameterization:

| Choice | Catalog candidates | Why unresolved |
|---|---|---|
| Backbone | `DPO` or `RPO` | `DPO` declares OL15/21 atom types; `RPO` declares OL3 atom types. |
| A base | `DAA` or `RAA` | Must match the selected force-field family. |
| C base | `DCC` or `RCC` | Must match the selected force-field family. |
| G base | `DGG` or `RGG` | Must match the selected force-field family. |
| U base | catalog exposes `RUU` | Compatibility must be reviewed; thymine must not be silently substituted. |
| Termini | `--5cap` / `--3cap` libraries | The chemistry, residue names, and any source-atom normalization must be declared and reviewed. |

The generated `modxna_fragment_decisions.tsv` leaves those choices explicitly
unresolved. A reviewer must document one compatible route before running
modXNA.

modXNA input uses one line per residue chemistry:

```text
<backbone fragment> A5L <base fragment>
```

The tool requires AmberTools and current CPPTRAJ. It generates a random
three-character residue name; that name must match the PDB and parameter
manifest mapping.

For the controlled `CUAGGCUC` campaign, the reviewed neutral 5′-OH route uses a
`CF5` library generated from `5PO A5L RCC --5cap`. Its terminal declaration must
include `"remove_atoms": ["P", "OP1", "OP2"]`. The 3′-OH `CF3` library uses
`RPO A5L RCC --3cap` and declares an empty removal list. Digital Polymerase
rejects other terminal atom removals.

## Parameter preparation

Place reviewed `.lib`/`.off` and `frcmod` artifacts under the campaign's
`parameters/` directory. Complete `fana_parameters.json` and run:

```bash
digital-polymerase-fana-parameters prepare \
  --candidate candidate/candidate_fana.pdb \
  --readiness fana_readiness.json \
  --parameters fana_parameters.json \
  --output-dir minimization \
  --strict
```

Only `PREPARED_NOT_EXECUTED` may proceed. LEaP output must then be reviewed for
unknown atoms, missing or conflicting parameters, and charge inconsistencies
before manually starting minimization.

## Post-run audit

After an externally executed two-stage minimization:

```bash
digital-polymerase-fana-campaign audit \
  --candidate candidate/candidate_fana.pdb \
  --minimized minimization/fana_minimized.pdb \
  --template inputs/2KP4_FANA_template.pdb \
  --parameters fana_parameters.json \
  --preflight minimization/parameter_preflight.json \
  --stage1 minimization/minimize_stage1.out \
  --stage2 minimization/minimize_stage2.out \
  --output-dir post_minimization \
  --strict
```

The audit:

1. verifies candidate, approved-manifest, and passing-preflight identity;
2. identifies FANA residues by the approved internal and terminal names while
   excluding solvent and ions;
3. restores the original FANA residue identities and residue numbering;
4. requires every comparison atom to remain present after applying the same
   approved terminal normalization used during preparation;
5. parses finite `FINAL RESULTS` rows from both Amber stages and blocks NaN,
   fatal, explicit error, or abnormal-termination markers;
6. computes aligned heavy-atom RMSD and maximum displacement;
7. reruns covalent-distance, C2′/F2′ stereochemistry, and template-relative
   sugar-pucker checks; and
8. records hashes for all primary inputs and Amber outputs.

The strongest automatic status is
`STRUCTURAL_PASS_EXPERT_REVIEW_REQUIRED`. The default 2 Å RMSD ceiling is a
campaign safeguard, not a universal validity criterion. Final energy,
gradients, restraints, parameter provenance, and intended use still require a
named expert decision. Dynamics remain out of scope.

## Primary references

- modXNA paper: https://doi.org/10.1021/acs.jctc.4c01164
- modified-nucleotide parameterization tutorial:
  https://doi.org/10.33011/livecoms.6.1.4545
- modXNA catalog: https://modxna.chpc.utah.edu/catalog/
- modXNA generation tutorial:
  https://modxna.chpc.utah.edu/generate-a-phosphothioate-backbone-residue/
- AmberTools: https://ambermd.org/AmberTools.php
- experimental FANA/RNA hybrid 2KP4:
  https://www.rcsb.org/structure/2KP4
