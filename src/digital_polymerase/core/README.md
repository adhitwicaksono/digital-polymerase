# Digital Polymerase Core

Reusable engine components shared by Digital Polymerase prototype and stable converter scripts.

| Module | Purpose |
|---|---|
| `atoms.py` | `Atom` dataclass, element inference, atom cloning |
| `residues.py` | Base identity, glycosidic atom, sequence extraction, base/backbone splitting |
| `pdb_io.py` | Simple PDB parser and writer |
| `geometry.py` | Kabsch alignment, RMSD, distance, angle, dihedral, coordinate transforms |
| `templates.py` | Template indexing and base-class donor selection |
| `registry.py` | XNA target grammar and validation defaults |
| `validation.py` | Chain/linkage/base-attachment/local geometry validation |
| `reporting.py` | Markdown and JSON report helpers |
| `errors.py` | Custom exceptions |

The core is not a converter by itself. It provides reusable parts. Converters should define the strategy: chain-preserving, template-guided, linkage-remapped, template-primary, sequence-primary, or hybrid-guided.
