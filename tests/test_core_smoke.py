import numpy as np
from digital_polymerase.core.atoms import Atom
from digital_polymerase.core.geometry import distance, kabsch, apply_transform
from digital_polymerase.core.residues import base_of, glycosidic_atom
from digital_polymerase.core.registry import get_target_spec
from digital_polymerase.core.validation import validate_required_atoms

def test_atom_basic():
    atom = Atom("HETATM", "C1'", "A", "A", 1, "", np.array([1.0,2.0,3.0]))
    assert atom.element == "C"
    assert atom.residue_key == ("A", 1, "")

def test_base_helpers():
    assert base_of("APN") == "A"
    assert base_of("TPN") == "U"
    assert glycosidic_atom("A") == "N9"
    assert glycosidic_atom("U") == "N1"

def test_kabsch_identity_translation():
    mobile = np.array([[0.,0.,0.],[1.,0.,0.],[0.,1.,0.]])
    target = mobile + np.array([1.,2.,3.])
    r,t,fit = kabsch(mobile, target)
    assert fit < 1e-8
    assert np.allclose(apply_transform(mobile, r, t), target)

def test_registry_pna():
    spec = get_target_spec("PNA")
    assert "C8'" in spec["backbone_atoms"]
    assert spec["base_attachment_atom"] == "C8'"

def test_required_atoms_validation():
    res = {("A",1,""): {"C1'": Atom("HETATM","C1'","A","A",1,"",np.array([0.,0.,0.])), "N9": Atom("HETATM","N9","A","A",1,"",np.array([1.4,0.,0.]))}}
    assert validate_required_atoms(res, ["C1'", "N9"])["status"] == "PASS"
