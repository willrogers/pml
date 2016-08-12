'''
Class to implement an EpicsControlSystem object which is used to
get real-time data from the synchrotron.
'''

from rml.controlsystem import ControlSystem
from cothread.catools import caget


class EpicsControlSystem(ControlSystem):

    def __init__(self):
        pass

    def get(self, pv):
        return caget(pv)
