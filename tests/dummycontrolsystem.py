'''
Class to implement a dummy control system to use on git.
It is needed to make tests dependendant on a specific control system pass.
'''


class DummyControlSystem():

    def __init__(self):
        pass

    def get(self, pv):
        return 4.0

    def put(self, pv, value):
        pass
