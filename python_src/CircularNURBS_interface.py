from ctypes import cdll, c_double, c_void_p, c_size_t, POINTER, c_int

lib = cdll.LoadLibrary('libCircularNURBS.so')

lib.SC_construct.argtypes = [c_size_t, c_size_t, c_size_t]
lib.SC_construct.restype = c_void_p

lib.SC_get_intervals.argtypes = [c_void_p]
lib.SC_get_intervals.restype = POINTER(c_double)

lib.SC_get_control.argtypes = [c_void_p]
lib.SC_get_control.restype = POINTER(c_double)

lib.SC_get_samples.argtypes = [c_void_p]
lib.SC_get_samples.restype = POINTER(c_double)

class SimpleCircle(object):
    def __init__(self, degree, numControl, numSamples):
        self.obj = lib.SC_construct(degree, numControl, numSamples)

    def intervals(self):
        return lib.SC_get_intervals(self.obj)

    def control(self):
        return lib.SC_get_control(self.obj)

    def samples(self):
        return lib.SC_get_samples(self.obj)
