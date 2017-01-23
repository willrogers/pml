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


class Physics(object):
    def __init__(self, length):
        self.length = length

    def get_length(self, field, handle):
        raise NotImplementedError('''This method should be overwritten
                                     in children classes!''')

    def set_length(self, field, unit):
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
    def __init__(self, length, x=0, y=0):
        super(Bpm10, self).__init__(length)
        self.x = x
        self.y = y


class Source(Physics):
    pass


class Rf(Physics):
    def __init__(self, length, voltage=0, frequency=0, harmonic_no=0, time_lag=0):
        super(Rf, self).__init__(length)
        self.voltage = voltage
        self.frequency = frequency
        self.harmonic_no = harmonic_no
        self.time_lag = time_lag

    def get_voltage(self):
        return self.voltage

    def set_voltage(self, value):
        self.voltage = value

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, value):
        self.frequency = value

    def get_harmonic_no(self):
        return self.harmonic_no

    def set_harmonic_no(self, value):
        self.harmonic_no = value

    def get_time_lag(self):
        return self.time_lag

    def set_time_lag(self, value):
        self.time_lag = value


class Ap(Physics):
    def __init__(self, length):
        super(Ap, self).__init__(length)
        self.limits = [0] * 4


class Drift(Physics):
    pass


class Bpm(Physics):
    def __init__(self, length, x=None, y=None):
        super(Bpm, self).__init__(length)
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# Magnets
class Magnet(Physics):
    # Should create subclasses of each magnet that inherit MagnetPhysics
    # Quad, dipole, corrector, sext
    def __init__(self, length, poly_a=0, poly_b=0, r1=0, r2=0, t1=0, t2=0):
        super(Magnet, self).__init__(length)
        self.poly_a = [0 for _ in range(4)]
        self.poly_b = [0 for _ in range(4)]
        self.r1 = [[0 for _ in range(6)] for _ in range(6)]
        self.r2 = [[0 for _ in range(6)] for _ in range(6)]
        self.t1 = [0 for _ in range(6)]
        self.t2 = [0 for _ in range(6)]


    def get_poly_a(self, value):
        self.poly_a = value

    def set_poly_a(self, value):
        self.poly_a = value

    def get_poly_b(self):
        return self.poly_b

    def set_poly_b(self, value):
        self.poly_b = value

    def get_r1(self):
        return self.r1

    def set_r1(self, value):
        self.r1 = value

    def get_r2(self):
        return self.r2

    def set_r2(self, value):
        self.r2 = value

    def get_t1(self):
        return self.t1

    def set_t1(self, value):
        self.t1 = value

    def get_t2(self):
        return self.t2

    def set_t2(self, value):
        self.t2 = value


class Aperture(Physics):
    def __init__(self, limits):
        assert len(limits) == 4
        self.limits = limits

    def get_limits(self):
        return self.limits

    def set_limits(self, value):
        self.limits = value

class Bend(Magnet):
    pass


class Quad(Magnet):
    def __init__(self, length):
        super(Quad, self).__init__(length)


class Sext(Magnet):
    pass


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


class Marker(Physics):
    def __init__(self):
        pass


class Monitor(Physics):
    def __init__(self):
        pass


class RF(Physics):
    def __init__(self, voltage, frequency, harmonic_number, time_lag=0):
        self.voltage = voltage
        self.frequency = frequency
        self.harmonic_number = harmonic_number
        self.time_lag = time_lag

    def get_voltage(self):
        return self.voltage

    def set_voltage(self, value):
        self.voltage = value

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, value):
        self.frequency = value

    def get_harmonic_number(self):
        return self.harmonic_number

    def set_harmonic_number(self, value):
        self.harmonic_number = value

    def get_time_lag(self):
        return self.time_lag

    def set_time_lag(self, value):
        self.time_lag = value


class Dipole(Magnet):
    def __init__(self, bending_angle, entrance_angle, exit_angle,
                 full_gap, fringe_int1, fringe_int2):
        self.bending_angle = bending_angle
        self.entrance_angle = entrance_angle
        self.exit_angle = exit_angle
        self.full_gap = full_gap
        self.fringe_int1 = fringe_int1
        self.fringe_int2 = fringe_int2

    def get_bending_angle(self):
        return self.bending_angle

    def set_bending_angle(self, value):
        self.bending_angle = value

    def get_entrance_angle(self):
        return self.entrance_angle

    def set_entrance_angle(self, value):
        self.entrance_angle = value

    def get_exit_angle(self):
        return self.exit_angle

    def set_exit_angle(self, value):
        self.exit_angle = value

    def get_full_gap(self):
        return self.full_gap

    def set_full_gap(self, value):
        self.full_gap = value

    def get_fringe_int1(self):
        return self.fringe_int1

    def set_fringe_int1(self, value):
        self.fringe_int1 = value

    def get_fringe_int2(self):
        return self.fringe_int2

    def set_fringe_int2(self, value):
        self.fringe_int2 = value

