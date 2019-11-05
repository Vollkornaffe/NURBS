import CyclicNURBS_path

from ctypes import cdll, c_double, c_void_p, c_size_t, POINTER, c_int

lib = cdll.LoadLibrary(CyclicNURBS_path.binary_path)
#os.path.abspath(os.path.basename(sys.argv[0]))

lib.CC_construct.argtypes = [c_size_t, c_size_t, c_size_t]
lib.CC_construct.restype = c_void_p

lib.CC_get_intervals.argtypes = [c_void_p]
lib.CC_get_intervals.restype = POINTER(c_double)

lib.CC_get_control.argtypes = [c_void_p]
lib.CC_get_control.restype = POINTER(c_double)

lib.CC_get_samples.argtypes = [c_void_p]
lib.CC_get_samples.restype = POINTER(c_double)

class CircularCurve:
    def __init__(self, degree, numControl, numSamples):
        self.obj = lib.CC_construct(degree, numControl, numSamples)

    def intervals(self):
        return lib.CC_get_intervals(self.obj)

    def control(self):
        return lib.CC_get_control(self.obj)

    def samples(self):
        return lib.CC_get_samples(self.obj)