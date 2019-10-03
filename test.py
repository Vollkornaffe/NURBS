from ctypes import cdll, cast, POINTER, c_double

lib = cdll.LoadLibrary('./core.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()
    
    def bar(self):
        lib.Foo_bar(self.obj)

    def test(self):
        return cast(lib.Foo_test(self.obj), POINTER(c_double))
