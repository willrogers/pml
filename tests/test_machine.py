import rml.machines


def test_machine_load_elements():
    pv_names = rml.machines.get_elements(machine='SRI21', elemType='BPM')
    assert pv_names
