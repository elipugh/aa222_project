from __future__ import division
import numpy as np
import math

class Airfoil(object):
    def __init__(self, params):
        self.truncation = params[0]
        self.thickness = 1

    def Z_up(self, X):
        X = X * self.truncation
        t = self.thickness
        foil = 5*t * (.2969*np.sqrt(X) - .1260*X - .3516*X**2 + .2843*X**3 - .102*X**4)
        # foil[-1] = 0
        return foil

    def Z_lo(self, X):
        X = X * self.truncation
        t = self.thickness
        foil = -5*t * (.2969*np.sqrt(X) - .1260*X - .3516*X**2 + .2843*X**3 - .102*X**4)
        # foil[-1] = 0
        return foil