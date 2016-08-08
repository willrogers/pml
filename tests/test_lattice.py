import rml.lattice

def test_create_lattice():
    l = rml.lattice.Lattice()
    assert(len(l)) == 0

