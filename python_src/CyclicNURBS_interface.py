import CyclicNURBS_path

from ctypes import cdll, c_double, c_void_p, c_size_t, POINTER, c_int

lib = cdll.LoadLibrary(CyclicNURBS_path.binary_path)
#os.path.abspath(os.path.basename(sys.argv[0]))

lib.CC_construct.argtypes = [c_size_t, c_size_t, c_size_t]
lib.CC_construct.restype = c_void_p

lib.CS_construct.argtypes = [c_size_t, c_size_t, c_size_t, c_size_t, c_size_t, c_size_t]
lib.CS_construct.restype = c_void_p

lib.CC_get_intervals.argtypes = [c_void_p]
lib.CC_get_intervals.restype = POINTER(c_double)

lib.CS_get_u_intervals.argtypes = [c_void_p]
lib.CS_get_u_intervals.restype = POINTER(c_double)

lib.CS_get_v_intervals.argtypes = [c_void_p]
lib.CS_get_v_intervals.restype = POINTER(c_double)

lib.CC_get_control.argtypes = [c_void_p]
lib.CC_get_control.restype = POINTER(c_double)

lib.CS_get_n_control.argtypes = [c_void_p, c_size_t]
lib.CS_get_n_control.restype = POINTER(c_double)

lib.CC_get_samples.argtypes = [c_void_p]
lib.CC_get_samples.restype = POINTER(c_double)

lib.CS_get_samples.argtypes = [c_void_p]
lib.CS_get_samples.restype = POINTER(c_double)

class CyclicCurve:
    def __init__(self, curveData):
        self.obj = lib.CC_construct(curveData.degree, curveData.numControl, curveData.numSamples)

    def intervals(self):
        return lib.CC_get_intervals(self.obj)

    def control(self):
        return lib.CC_get_control(self.obj)

    def samples(self):
        return lib.CC_get_samples(self.obj)

class CyclicSurface:
    def __init__(self, surfaceData):
        self.obj = lib.CS_construct(surfaceData.u_degree, surfaceData.v_degree, surfaceData.u_numControl, surfaceData.v_numControl, surfaceData.u_numSamples, surfaceData.v_numSamples)

    def u_intervals(self):
        return lib.CS_get_u_intervals(self.obj)
    def v_intervals(self):
        return lib.CS_get_v_intervals(self.obj)

    def control(self, n):
        return lib.CS_get_n_control(self.obj, n)

    def samples(self):
        return lib.CS_get_samples(self.obj)
