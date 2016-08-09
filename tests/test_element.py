import rml.element


def test_create_element():
    e = rml.element.Element('BPM', 6.0)
    assert e.get_type() == 'BPM'
    assert e.get_length() == 6.0


def test_add_element_to_family():
    e = rml.element.Element('dummy', 0.0)
    e.add_to_family('fam')
    assert 'fam' in e.get_families()
