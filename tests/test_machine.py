import rml.machines


def test_machine_load_elements():
    lattice = rml.machines.get_elements(machine='SRI21', elem_type='BPM')
    assert len(lattice) == 173
    for element in lattice.get_elements():
        assert isinstance(element.get_pv_name('readback', 'x'), str)
        assert isinstance(element.get_pv_name('readback', 'y'), str)
