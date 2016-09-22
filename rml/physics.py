'''
List of available physics objects:
RF
AP
DRIFT
BPM
BEND
QUAD
SEXT
DIPOLE
HSTR
VSTR
HCHICA
VTRIM
HTRIM
MPW12
MPW15
BPM10
source
'''
from rml.device import Device


class Physics(object):
    def __init__(self, length):
        self.length = length

    def get_value(self, field, handle):
        raise NotImplementedError('''This method should be overwritten
                                     in children classes!''')

    def put_value(self, field, unit):
        raise NotImplementedError('''This method should be overwritten
                                     in children classes!''')


class Hchica(Physics):
    pass


class Vtrim(Physics):
    pass


class Htrim(Physics):
    pass


class Mpw12(Physics):
    pass


class Mpw10(Physics):
    pass


class Mpw15(Physics):
    pass


class Bpm10(Physics):
    pass


class Source(Physics):
    pass


class Rf(Physics):
    def __init__(self, length, voltage=0, frequency=0, harmonic_no=0):
        super(Rf, self).__init__(length)
        self.voltage = voltage
        self.frequency = frequency
        self.harmonic_no = harmonic_no
        self.time_lag = 0


class Ap(Physics):
    def __init__(self, length):
        super(Ap, self).__init__(length)
        self.limits = [0] * 4


class Drift(Physics):
    pass


class Bpm(Physics):
    def get_x(self):
        pass

    def get_y(self):
        pass


# Magnets
class Magnet(Physics):
    # Should create subclasses of each magnet that inherit MagnetPhysics
    # Quad, dipole, corrector, sext
    def __init__(self, length, poly_a=0, poly_b=0):
        super(Magnet, self).__init__(length)
        self.poly_a = poly_a
        self.poly_b = poly_b
        self.r1 = [[0 for x in range(6)] for y in range(6)]
        self.r2 = [[0 for x in range(6)] for y in range(6)]
        self.t1 = [0 for x in range(6)]
        self.t2 = [0 for x in range(6)]

    def put_b2(self, value, unit):
        pass

    def get_b2(self, value, unit):
        pass


class Bend(Magnet):
    pass


class Quad(Magnet):
    def put_b1(self):
        pass

    def get_b1(self):
        pass


class Sext(Magnet):
    def put_b2(self):
        pass

    def get_b2(self):
        pass


class Dipole(Magnet):
    def __init__(self, length, entrance_angle, bending_angle, exit_angle,
                 full_gap):
        super(Dipole, self).__init__(length)
        self.entrance_angle = entrance_angle
        self.bending_angle = bending_angle
        self.exit_angle = exit_angle
        self.full_gap = full_gap
        self.fringe_int1 = 0
        self.fringe_int2 = 0


# Correctors
class Corrector(Magnet):
    def put_b0(self):
        pass

    def get_b0(self):
        pass


class Hstr(Corrector):
    pass


class Vstr(Corrector):
    pass
