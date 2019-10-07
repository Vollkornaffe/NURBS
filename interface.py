from ctypes import cdll, c_double, c_void_p, c_size_t, POINTER

lib = cdll.LoadLibrary('/home/lars/src/NURBS/core.so')

lib.SC_construct.argtypes = []
lib.SC_construct.restype = c_void_p

lib.SC_set_degree.argtypes = [c_void_p, c_size_t]
lib.SC_set_degree.restype = None

lib.SC_get_control.argtypes = [c_void_p, c_size_t]
lib.SC_get_control.restype = POINTER(c_double)

lib.SC_get_samples.argtypes = [c_void_p, c_size_t]
lib.SC_get_samples.restype = POINTER(c_double)

class SimpleCircle(object):
    def __init__(self):
        self.obj = lib.SC_construct()

    def degree(self, n):
        lib.SC_set_degree(self.obj, n)

    def control(self, n):
        return lib.SC_get_control(self.obj, n)

    def samples(self, n):
        return lib.SC_get_samples(self.obj, n)
