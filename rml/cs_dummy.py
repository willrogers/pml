'''
Class to implement a dummy control system to use on git.
It is needed to make tests dependendant on a specific control system pass.
'''
from rml.cs import ControlSystem


class CsDummy(ControlSystem):

    def __init__(self):
        self.storage = dict()

    def get(self, pv):
        if pv in self.storage:
            return self.storage[pv]
        else:
            return 4.0

    def put(self, pv, value):
        self.storage[pv] = value
