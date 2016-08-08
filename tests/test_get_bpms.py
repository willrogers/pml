import pytest
import rml


@pytest.mark.xfail
def test_get_bpms():
    rml.initialise('VMX')
    bpms = rml.get_elements('BPM')
    assert len(bpms) == 173
