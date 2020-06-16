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

from optimizers.fib import Fib_Optimizer


# Perform an objective function
# evaluation at x
def evaluation(x, parameterization, avg=True, ticks=None, iters=3000):
    # Angles are of wind on airfoil
    angles = [i for i in range(11)]

    # Weights how much we care abt each yaw angle
    # These are given by:
    #   from scipy.stats import norm
    #   rv = norm(loc=0, scale=6)
    #   weights = np.array([rv.cdf(i+.5)-rv.cdf(i-.5) for i in range(11)])
    #   weights *= 100
    # This is because experienced yaw is roughly gaussian
    # with mean 0 and variance 6-7ish probably
    weights = np.array([6.641, 6.55, 6.283, 5.863, 5.321, 4.697,
                        4.033, 3.368, 2.736, 2.162, 1.661])
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
        # Probably should not be none!
        if ticks is None:
            ticks = np.linspace(0,1,x.size+1)

        params = np.zeros((2,len(ticks)))
        params[0] = ticks
        params[1,:-1] = x
        airfoil = InterAirfoil(params)
    # Write points into .dat file
    # for Xfoil to load
    fn_2_dat(filename,
             airfoil.Z_up,
             airfoil.Z_lo)

    # Do an evaluation of the point
    # using Afoil CFD shtuff
    metrics = xfoil.evaluate(filename, angles, visc, iters=iters)

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
    print("\tObjective : {}\n".format(np.around(np.array(obj).dot(weights), decimals=4)))

    if avg:
        return np.array(obj).dot(weights)
    else:
        return obj


# Change this to change type of airfoil
parameterization="Interpolate"
# Initial point
x0 = None
# Evaluation Args
args = None
# Opt Iterations
n = None

# Note that these initializations are roughly optimal,
# so you're unlikely to see much improvement
# The exception is NACA, where Fib Search Opt is used
# Nelder Mead works for NACA too, but Fib Search is nice
if x0 is None:
    if parameterization == "PARSEC":
        x0 = np.array([0.3997, 0.2453, 0.3009, 2.3359, 0.618, 0.7968])
    if parameterization == "NACA":
        x0 = [0.34,0.50]
        a, b = x0[0], x0[1]
    if parameterization == "Mixed":
        x0 = np.array([0.4388, 0.4285, 0.2319, 0.2924, 2.2184, 0.6653, 0.4959, 0.3065])
    if parameterization == "Interpolate":
        x0 = [0.0372, 0.0374, 0.0204, 0.0301, 0.0367, 0.0206, 0.0114, 0.0038,
              0.003, 0.0001, -0.001, -0.0021, -0.0031, -0.003, -0.003]

if args is None:
    if parameterization == "PARSEC":
        args = (parameterization,True,None)
    if parameterization == "NACA":
        args = (parameterization,False)
    if parameterization == "Mixed":
        args = (parameterization,True,None)
    if parameterization == "Interpolate":
        ticks = np.linspace(0,np.pi/2,10)
        ticks = np.array([(0.5*(1.0-np.cos(x))) for x in ticks])
        ticks = np.hstack([ticks, np.linspace(0.5,1,7)[1:]])
        args = (parameterization,True,ticks)

print("\n\n PARAMETERIZATION\n==================\n\n{}\n".format(parameterization))
print(" INITIALIZATION\n================\n\n{}\n".format(x0))

if parameterization == "NACA":
    if a is None or b is None:
        a, b = 0.34, 0.50
    if n is None:
        n = 30
    opt = Fib_Optimizer(evaluation, x0, n, a, b, args=args)
else:
    if n is None:
        n = 200
    opt = sp.minimize(evaluation, x0, args=args, method="Nelder-Mead", options={'maxiter': n})

print("\n\n")
if parameterization != "NACA":
    print(opt.message)
print("Iters: {}".format(opt.nit))
print("Design:\n{}".format(list(np.around(opt.x,decimals=4))))
print("Objective: {}".formay(np.around(opt.fun,decimals=6)))


