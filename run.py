import numpy as np
import scipy.optimize as sp
from xfoil import xfoil
import os
import random

from parameterizations.helpers import fn_2_dat
from parameterizations.naca import Airfoil as NacaAirfoil
from parameterizations.parsec import Airfoil as ParsecAirfoil
from parameterizations.naca_parsec_mix import Airfoil as MixAirfoil
from parameterizations.inter import Airfoil as InterAirfoil


# Perform an objective function
# evaluation at x
def evaluation(x, parameterization="Mixed"):
    # These are hyperparams of the evaluation
    # Angles are of wind on airfoil
    # angles = [0, 4, 10, 20, 30, 40]
    angles = [0, 0.5, 2, 4, 8, 12]
    # Weights how much we care abt each angle
    weights = np.ones(len(angles))
    # Viscuous?
    visc = True
    filename = "evaluation{}.dat".format(random.randrange(10**20)%(10**15))

    if parameterization == "Mixed":
        airfoil = MixAirfoil(x)
    if parameterization == "PARSEC":
        airfoil = ParsecAirfoil(x)
    if parameterization == "NACA":
        airfoil = NacaAirfoil(x)
    if parameterization == "Interpolate":
        airfoil = InterAirfoil(x)
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


# Change this to change type of airfoil
parameterization="Interpolate"


if parameterization == "PARSEC":
    x0 = np.array([0.4, 0.26, 0.26, 2.2, np.pi/5, 0.5])
if parameterization == "NACA":
    x0 = np.array([0.4])
if parameterization == "Mixed":
    x0 = np.array([0.45, 0.41, 0.25, 0.28, 2.25, 0.65, .5, 0.3])
if parameterization == "Interpolate":
    x0 = np.array([[0.0354, 0.0332, 0.0295, 0.0245, 0.0188, 0.013,
                    0.0077, 0.0033, 0.0, -0.0022, -0.0035, -0.0041,
                    -0.0039, -0.0033, -0.0022, 0.0]])


opt = sp.minimize(evaluation, x0, args=(parameterization,), method="Nelder-Mead", options={'maxiter': 200})
# opt = sp.minimize(evaluation, x0, args=(parameterization,), options={'maxiter': 1000})

print "\n\n"
print(opt.message)
print(opt.nit)
print(list(np.around(opt.x,decimals=4)))
print(np.around(opt.fun,decimals=6))


