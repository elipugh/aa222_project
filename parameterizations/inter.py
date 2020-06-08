from __future__ import division
import numpy as np
import math
from scipy.interpolate import interp1d

class Airfoil(object):
    def __init__(self, params):
        params = np.array(params)        
        self.x = params[0]
        self.y = np.zeros(params.shape[1])
        for i in range(1,self.y.size):
            self.y[i] = self.y[i-1] + params[1][i-1]
        self.f = interp1d(self.x, self.y, kind=1)

    def Z_up(self, X):
        return self.f(X)

    def Z_lo(self, X):
        return -self.Z_up(X)