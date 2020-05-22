from __future__ import division
import numpy as np
import math

class Parameters(object):
    '''Parameters defining a PARSEC airfoil'''   
    def __init__(self, x):

        if x.shape != (5,):
            print("5d np array expected")

        front_radius        = x[0]
        x_cross_section     = x[1]
        cross_section_width = x[2]
        sides_curve         = x[3]
        rear_angle          = x[4]

        self.r_le       = front_radius              # Leading edge radius
        self.X_up       = x_cross_section           # Upper crest location X coordinate
        self.Z_up       = cross_section_width       # Upper crest location Z coordinate
        self.Z_XX_up    = -sides_curve              # Upper crest location curvature
        self.X_lo       = x_cross_section           # Lower crest location X coordinate
        self.Z_lo       = -cross_section_width      # Lower crest location Z coordinate
        self.Z_XX_lo    = sides_curve               # Lower crest location curvature
        self.Z_te       = 0 # static                # Trailing edge Z coordinate
        self.dZ_te      = 0 # static                # Trailing edge thickness
        self.alpha_te   = 0 # static                # Trailing edge direction angle
        self.beta_te    = rear_angle #(radians)     # Trailing edge wedge angle
        self.P_mix      = 1.0                       # Blending parameter

class Coefficients(object):
    '''
    Credit for this class goes to
    https://github.com/mbodmer/libairfoil
    This class calculates the equation systems which define the coefficients
    for the polynomials given by the parsec airfoil parameters.
    '''
    def __init__(self, parsec_params):
        self.params = Parameters(parsec_params)
        self._a_up = self._calc_a_up(self.params)
        self._a_lo = self._calc_a_lo(self.params)
    
    def a_up(self):
        '''Returns coefficient vector for upper surface'''
        return self._a_up
    
    def a_lo(self):
        '''Returns coefficient vector for lower surface'''
        return self._a_lo
    
    def _calc_a_up(self, parsec_params):
        Amat = self._prepare_linsys_Amat(parsec_params.X_up)
        Bvec = np.array([parsec_params.Z_te, parsec_params.Z_up,
                            math.tan(parsec_params.alpha_te - parsec_params.beta_te/2),
                            0.0, parsec_params.Z_XX_up, math.sqrt(2*parsec_params.r_le)]) 
        return np.linalg.solve(Amat, Bvec)
    
    def _calc_a_lo(self, parsec_params):
        Amat = self._prepare_linsys_Amat(parsec_params.X_lo)
        Bvec = np.array([parsec_params.Z_te, parsec_params.Z_lo,
                            math.tan(parsec_params.alpha_te + parsec_params.beta_te/2),
                            0.0, parsec_params.Z_XX_lo, -math.sqrt(2*parsec_params.r_le)])
        return np.linalg.solve(Amat, Bvec)
    
    def _prepare_linsys_Amat(self, X):
        return np.array(
            [[1.0,           1.0,          1.0,         1.0,          1.0,          1.0        ],
             [X**0.5,        X**1.5,       X**2.5,      X**3.5,       X**4.5,       X**5.5     ],
             [0.5,           1.5,          2.5,         3.5,          4.5,          5.5        ],
             [0.5*X**-0.5,   1.5*X**0.5,   2.5*X**1.5,  3.5*X**2.5,   4.5*X**3.5,   5.5*X**4.5 ],
             [-0.25*X**-1.5, 0.75*X**-0.5, 3.75*X**0.5, 8.75*X**1.5, 15.75*X**2.5, 24.75*X**3.5],
             [1.0,           0.0,          0.0,         0.0,          0.0,          0.0        ]])

class Airfoil(object):
    '''
    Credit for this class goes to
    https://github.com/mbodmer/libairfoil
    Airfoil defined by PARSEC Parameters
    '''
    def __init__(self, parsec_params):
        self._coeff = Coefficients(parsec_params)
        
    def Z_up(self, X):
        '''Returns Z(X) on upper surface, calculates PARSEC polynomial'''
        a = self._coeff.a_up()
        # print(a)
        return a[0]*X**0.5 + a[1]*X**1.5 + a[2]*X**2.5 + a[3]*X**3.5 + a[4]*X**4.5 + a[5]*X**5.5
        
    
    def Z_lo(self, X):
        '''Returns Z(X) on lower surface, calculates PARSEC polynomial'''
        a = self._coeff.a_lo()
        # print(a)
        return a[0]*X**0.5 + a[1]*X**1.5 + a[2]*X**2.5 + a[3]*X**3.5 + a[4]*X**4.5 + a[5]*X**5.5



if __name__ == "__main__":
    # Whatever you do, DO NOT uncomment
    # and run with python 2
    # Your computer will prob crash
    # I have done this twice lol
    # Python 3 is fine
    # Python 2 does not like matplotlib
    
    # # # import matplotlib.pyplot as plt
    
    # params = Parameters(np.array([0.4, 0.3, 0.3, 2, np.pi/2]))
    # airfoil = Airfoil(params)
    
    # x = np.linspace(0.0, 1.0, 150)
    # foil_up = airfoil.Z_up(x)
    # foil_lo = airfoil.Z_lo(x)
    # topmax = np.max(foil_up)
    
    # foil_up = foil_up * 1/(6*topmax)
    # foil_lo = foil_lo * 1/(6*topmax)
    
    # plt.plot(x, foil_up, 'r--', x,foil_lo, 'b--')
    # plt.xlim(-0.2, 1.2)
    # plt.ylim(-1, 1)
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.grid(True)
    # plt.show()
    pass


