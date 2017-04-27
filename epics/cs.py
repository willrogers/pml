'''
Class to implement an EpicsControlSystem object which is used to
get real-time data from the synchrotron.
'''

from pml.cs import ControlSystem
from cothread.catools import caget, caput


class EpicsControlSystem(ControlSystem):

    def __init__(self):
        pass

    def get(self, pv):
        return caget(pv)

    def put(self, pv, value):
        caput(pv, value)
