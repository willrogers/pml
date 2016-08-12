'''
Class to implement a dummy control system to use on git.
It is needed to make tests dependendant on a specific control system pass.
'''

from rml.controlsystem import ControlSystem


class DummyControlSystem(ControlSystem):

    def __init__(self):
        pass

    def get(self, pv):
        return 4.0
