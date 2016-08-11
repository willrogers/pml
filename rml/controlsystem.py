'''
Abstract class used as template to define control systems.
'''

class ControlSystem(object):
    def __init__(self):
        raise NotImplementedError()

    def get(self, pv):
        raise NotImplementedError()
