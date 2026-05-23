# RNA → ANA Fragment-Guided Conversion Report

**Project:** Digital Polymerase  
**Prototype:** 002A.1  
**Method:** Fragment-guided RNA → ANA candidate reconstruction with chain-preserving mode and chain-continuity validation  
**Status:** Experimental candidate, not physically validated  
**Chain-continuity status:** `PASS`

---

## Inputs

- Source RNA PDB: `/mnt/data/RNA-8mer.pdb`
- ANA fragment template PDB: `/mnt/data/1ho6_ANApart.pdb`
- Output PDB: `/mnt/data/ana_patch_002A2_outputs/converted_ana_RNA-8mer_002A2.pdb`

---

## Source Sequence

```text
CUAGGCUC
```

---

## Template Index

The ANA template is shorter than the RNA input, so template residues are used as local geometry donors.

- `C` → `CAR` at chain `A`, residue `11`
- `G` → `GAO` at chain `A`, residue `9`
- `U` → `UAR` at chain `A`, residue `10`

---

## Method Summary

This prototype uses a local ANA fragment as a residue-level backbone geometry donor.

For each RNA residue:

1. determine source RNA base identity
2. select the best available ANA template residue
3. align ANA template anchor atoms onto RNA anchor atoms using Kabsch alignment
4. reconstruct the candidate residue according to the selected mode
5. preserve RNA nucleobase atoms in their original coordinates
6. export an ANA-like candidate residue
7. validate inter-residue chain continuity in the generated output

This is **not** a full-template reconstruction because the ANA template contains only 4 residues.

Patch 002A.2 adds `ana-chain-preserving` mode. In this mode, the source RNA chain atoms are preserved to maintain polymer continuity, while ANA-sensitive local atoms such as C2′/O2′ are taken from the aligned ANA template. This improves chain-continuity behavior but still does **not** create an experimentally validated ANA structure.

---

## Settings

- Conversion mode: `ana-chain-preserving`
- Anchor atoms: `C1', C3', C4', O4'`
- Pin C1' after alignment: `True`
- Residue naming policy: `template-observed`
- Skip residue-numbering gaps in inter-residue validation: `True`

---

## Alignment Summary

- Converted residues: `8`
- Mean anchor RMSD: `0.0407 Å`
- Maximum anchor RMSD: `0.0644 Å`

Important:

> Anchor RMSD measures local residue-frame alignment only. It does not prove polymer-chain continuity.

---

## Chain-Continuity Validation

The patch evaluates whether the generated output preserves basic covalent-distance plausibility.

| Metric | Structure | Measured | Missing | Failed | Mean (Å) | Min (Å) | Max (Å) | Expected range (Å) | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| O3'(i)→P(i+1) | source | 7 | 0 | 0 | 1.606 | 1.604 | 1.609 | 1.40–1.80 | PASS |
| O3'(i)→P(i+1) | output | 7 | 0 | 0 | 1.606 | 1.604 | 1.609 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | source | 8 | 0 | 0 | 1.591 | 1.590 | 1.595 | 1.40–1.80 | PASS |
| P(i)→O5'(i) | output | 8 | 0 | 0 | 1.591 | 1.590 | 1.595 | 1.40–1.80 | PASS |

### Worst output O3′–P links

No failed links detected.

---

## Per-Residue Conversion

| # | Source residue | Source base | Output residue | Template used | Anchor RMSD (Å) | Note |
|---:|---|---|---|---|---:|---|
| 1 | A72 | C | CAR | CAR A11 | 0.0394 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 2 | A73 | U | UAR | UAR A10 | 0.0326 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 3 | A74 | A | AAR | GAO A9 | 0.0287 | purine fallback: A uses G-like ANA backbone template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 4 | A75 | G | GAO | GAO A9 | 0.0265 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 5 | A76 | G | GAO | GAO A9 | 0.0369 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 6 | A77 | C | CAR | CAR A11 | 0.0448 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 7 | A78 | U | UAR | UAR A10 | 0.0644 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |
| 8 | A79 | C | CAR | CAR A11 | 0.0524 | exact base-class template; ANA chain-preserving mode: source chain atoms preserved, C2'/O2' template-derived |

---

## Scientific Interpretation

This output should be interpreted as:

> an ANA-like candidate structure generated using fragment-guided local backbone reconstruction.

It should **not** be interpreted as:

> a chemically validated or experimentally confirmed ANA structure.

If chain-continuity status is `FAIL`, the structure should also **not** be interpreted as a continuous ANA polymer.

---

## Important Limitations

- The ANA template contains only a 4-mer fragment.
- A-like ANA geometry is absent in the uploaded template; A residues may use a purine fallback template.
- RNA nucleobase atoms are preserved, but backbone geometry is template-derived.
- Patch 002A.2 reports chain-continuity problems but does not correct them.
- The output is not energy-minimized.
- No force-field parameters are generated.
- Connectivity is not explicitly written with `CONECT` records.
- Molecular viewers may infer nonstandard residue bonds differently.
- Residue names are provisional and may need adjustment for downstream tools.
- Biological function, stability, replication, or catalytic activity is not implied.

---

## Recommended Next Steps

1. Visually inspect the output in PyMOL, ChimeraX, VMD, or Mol*.
2. Check residue completeness and atom naming.
3. Inspect base-backbone attachment geometry.
4. Check bond lengths, angles, torsions, and clashes.
5. Review the O3′–P chain-continuity table.
6. Compare local ANA backbone geometry with the original 4-mer ANA template.
7. Add explicit connectivity records or topology files in future versions.
8. Implement fragment-chain reconstruction or chain-aware coordinate correction.
9. Perform energy minimization with appropriate force-field support.

---

## Development Note

This patch marks a transition from:

```text
low local RMSD = looks promising
```

to:

```text
low local RMSD + chain-continuity validation = more honest structural assessment
```

The next Digital Polymerase requirement is chemically rigorous ANA stereochemistry validation, explicit connectivity/topology support, and eventually energy minimization.
