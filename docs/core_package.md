# Digital Polymerase Core Package

This package contains the first reusable `core/` modules for Digital Polymerase.

## Install locally

```bash
pip install -e .
```

## Run smoke tests

```bash
pytest
```

## Current scope

This is not yet the stable converter layer. It is the shared engine:

```text
atoms
residues
PDB I/O
geometry
templates
registry
validation
reporting
errors
```

Next recommended step:

```text
Refactor RNA → FANA prototype as the first stable converter candidate using this core.
```
