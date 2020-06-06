from __future__ import division
import numpy as np
import math

from parameterizations.naca import Airfoil as NacaAirfoil
from parameterizations.parsec import Airfoil as ParsecAirfoil

class Airfoil(object):
    def __init__(self, params):
        self.naca_params = params[0:1]
        self.parsec_params = params[1:7]
        self.mix = params[7]
        self.naca = NacaAirfoil(self.naca_params)
        self.parsec = ParsecAirfoil(self.parsec_params)

    def Z_up(self, X):
        naca_coords = self.naca.Z_up(X)
        parsec_coords = self.parsec.Z_up(X)
        naca_coords = naca_coords * 1/(6*np.max(naca_coords))
        parsec_coords = parsec_coords * 1/(6*np.max(parsec_coords))

        foil = self.mix * naca_coords + (1-self.mix) * parsec_coords
        # foil[-1] = 0
        return foil

    def Z_lo(self, X):
        return -self.Z_up(X)