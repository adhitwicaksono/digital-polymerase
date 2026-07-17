import numpy as np
from digital_polymerase.core.atoms import Atom
from digital_polymerase.core.geometry import kabsch, apply_transform
from digital_polymerase.core.residues import base_of, glycosidic_atom
from digital_polymerase.core.registry import get_target_spec
from digital_polymerase.core.validation import validate_required_atoms
from digital_polymerase.core.validation import validate_intra_residue_distance


def test_atom_basic():
    atom = Atom("HETATM", "C1'", "A", "A", 1, "", np.array([1.0, 2.0, 3.0]))
    assert atom.element == "C"
    assert atom.residue_key == ("A", 1, "")


def test_base_helpers():
    assert base_of("APN") == "A"
    assert base_of("TPN") == "U"
    assert glycosidic_atom("A") == "N9"
    assert glycosidic_atom("U") == "N1"


def test_kabsch_identity_translation():
    mobile = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    target = mobile + np.array([1.0, 2.0, 3.0])
    r, t, fit = kabsch(mobile, target)
    assert fit < 1e-8
    assert np.allclose(apply_transform(mobile, r, t), target)


def test_registry_pna():
    spec = get_target_spec("PNA")
    assert "C8'" in spec["backbone_atoms"]
    assert spec["base_attachment_atom"] == "C8'"


def test_required_atoms_validation():
    res = {
        ("A", 1, ""): {
            "C1'": Atom("HETATM", "C1'", "A", "A", 1, "", np.array([0.0, 0.0, 0.0])),
            "N9": Atom("HETATM", "N9", "A", "A", 1, "", np.array([1.4, 0.0, 0.0])),
        }
    }
    assert validate_required_atoms(res, ["C1'", "N9"])["status"] == "PASS"


def test_missing_distance_data_does_not_pass():
    res = {
        ("A", 1, ""): {
            "C1'": Atom("HETATM", "C1'", "A", "A", 1, "", np.array([0.0, 0.0, 0.0]))
        }
    }
    result = validate_intra_residue_distance(res, "C1'", "N9", 1.2, 1.8)
    assert result.measured == 0
    assert result.missing == 1
    assert result.status == "NO_DATA"
