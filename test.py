from ctypes import cdll, c_double, c_void_p, c_size_t, POINTER

lib = cdll.LoadLibrary('./core.so')

lib.SC_construct.argtypes = []
lib.SC_construct.restype = c_void_p
lib.SC_get_control.argtypes = [c_void_p, c_size_t]
lib.SC_get_control.restype = POINTER(c_double)

class SimpleCircle(object):
    def __init__(self):
        self.obj = lib.SC_construct()

    def control(self, n):
        return lib.SC_get_control(self.obj, n)

SC = SimpleCircle()
asdf = SC.control(3)

for i in range(0, 3*3):
    print(asdf[i])
