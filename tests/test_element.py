import rml.element


def test_create_element():
    e = rml.element.Element('BPM', 6.0)
    assert e.element_type == 'BPM'
    assert e.s == 6.0
