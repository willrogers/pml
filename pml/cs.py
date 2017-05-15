"""
Template module to define control systems.
"""


class ControlSystem(object):
    """ Define a control system to be used with a device

    It uses channel access to comunicate over the network with
    the hardware.
    """
    def __init__(self):
        raise NotImplementedError()

    def get(self, pv):
        raise NotImplementedError()

    def put(self, pv, value):
        raise NotImplementedError()


class NullControlSystem(ControlSystem):

    def __init__(self):
        pass

    def get(self, pv):
        pass

    def put(self, pv, value):
        pass
