import rml.machines


def test_machine_load_elements():
    lattice = rml.machines.get_elements(machine='SRI21', elemType='BPM')
    assert len(lattice) == 173
