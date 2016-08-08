import rml.lattice

def test_create_lattice():
    l = rml.lattice.Lattice()
    assert(len(l)) == 0

def test_non_negative_lattice():
    l = rml.lattice.Lattice()
    assert(len(l)) >= 0
