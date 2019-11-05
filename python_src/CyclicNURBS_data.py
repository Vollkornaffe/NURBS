class CurveData:
    def __init__(self, degree = 3, numControl = 4, numSamples = 100):
        self.degree = degree
        self.numControl = numControl
        self.numSamples = numSamples

class SurfaceData:
    def __init__(self, u_degree = 3, v_degree = 3, u_numControl = 4, v_numControl = 4, u_numSamples = 100, v_numSamples = 100):
        self.u_degree = u_degree
        self.v_degree = v_degree
        self.u_numControl = u_numControl
        self.v_numControl = v_numControl
        self.u_numSamples = u_numSamples
        self.v_numSamples = v_numSamples