import numpy as np
import scipy.optimize as sp
from xfoil import xfoil
from parameterizations.helpers import fn_2_dat
# from parameterizations.parsec import Airfoil
from parameterizations.truncated_parsec import Airfoil
import os
import random


# Perform an objective function
# evaluation at x
def evaluation(x):
    # These are hyperparams of the evaluation
    # Angles are of wind on airfoil
    # angles = [0, 4, 10, 20, 30, 40]
    angles = [0, 0.5, 2, 4, 8, 12]
    # Weights how much we care abt each angle
    weights = np.ones(len(angles))
    # Viscuous?
    visc = True

    filename = "evaluation{}.dat".format(random.randrange(10**20)%(10**15))
    airfoil = Airfoil(x)
    # Write points into .dat file
    # for Xfoil to load
    fn_2_dat(filename,
             airfoil.Z_up,
             airfoil.Z_lo)

    # Do an evaluation of the point
    # using Afoil CFD shtuff
    metrics = xfoil.evaluate(filename, angles, visc)

    if metrics is None:
        # uh oh, nothing converged,
        # probably very bad design?
        alpha, CL, CD, CDp, CM = [[np.inf]*len(angles) for _ in range(5)]
    else:
        alpha, CL, CD, CDp, CM = metrics

    # Remove the file
    os.remove(filename)

    obj = CD
    if not visc:
        obj = np.abs(CDp)

    print("Eval:")
    print("\tDesign    : {}".format(list(np.around(x, decimals=3))))
    print("\tDrags     : {}".format(obj))
    print("\tObjective : {}".format(np.around(np.array(obj).dot(weights), decimals=4)))

    return np.array(obj).dot(weights)




# Example
# x0 = np.array([0.4, 0.26, 0.26, 2, np.pi/5, 0.8])
x0 = np.array([0.4, 0.26, 0.26, 2.2, np.pi/5, 0.9])

opt = sp.minimize(evaluation, x0, method="Nelder-Mead", options={'maxiter': 100})

print "\n\n"
print(opt.message)
print(opt.nit)
print(list(np.around(opt.x,decimals=4)))
print(np.around(opt.fun,decimals=6))


