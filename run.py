import numpy as np
from xfoil import xfoil
from parameterizations.helpers import fn_2_dat
from parameterizations.parsec import Airfoil
import os


# Perform an objective function
# evaluation at x
def evaluation(x):
    filename = "evaluation.dat"
    airfoil = Airfoil(x)
    # Write points into .dat file
    # for Xfoil to load
    fn_2_dat(filename,
             airfoil.Z_up,
             airfoil.Z_lo)
    # Do an evaluation of the point
    # using Afoil CFD shtuff
    alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr = xfoil.evaluate(filename)
    # Remove the file
    os.remove(filename)
    return CD

# Example
x0 = np.array([0.4, 0.3, 0.3, 2, np.pi/2])
CD = evaluation(x0)
print(CD)

