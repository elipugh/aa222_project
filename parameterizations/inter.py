from __future__ import division
import numpy as np
import math
from scipy.interpolate import interp1d

class Airfoil(object):
    def __init__(self, params):
        params = np.array(params)
        assert params.size % 2 == 0
        xs = np.linspace(0,np.pi/2,1+params.size//2)
        xs = np.array([(0.5*(1.0-np.cos(x))) for x in xs])
        self.x = np.hstack([xs,[1-e for e in xs[::-1][1:]]])
        self.y = np.zeros(params.size+1)
        for i in range(1,self.y.size):
            self.y[i] = self.y[i-1] + params[i-1]
        self.f = interp1d(self.x, self.y, kind=1)

    def Z_up(self, X):
        return self.f(X)

    def Z_lo(self, X):
        return -self.Z_up(X)