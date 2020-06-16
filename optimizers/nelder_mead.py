from __future__ import division
import numpy as np
from copy import copy
import scipy.optimize as sp

class Nelder_Mead_Optimizer():
    def __init__(self, f, x0, n, reps=1, args=()):
        self.args = args
        self.reps = reps
        self.f = f
        self.x0 = x0
        self.nit = n
        self.optimize()

    # This repeats the evaluation with very slightly
    # different values to get more accurate drag number
    def repf(self, pts):
        yaw_weights = np.array([6.641, 6.55, 6.283, 5.863,
                                5.321, 4.697, 4.033, 3.368,
                                2.736, 2.162, 1.661])
        if self.reps == 1:
            obj = np.dot(self.f(pt, *(self.args)), yaw_weights)
        else:
            objs = [[] for _ in range(self.reps)]
            weights = np.ones(self.reps)
            for i in range(self.reps):
                npt = pt + np.random.normal(0, np.mean(pt)/20, pt.shape)
                objs[i] = self.f(npt, *(self.args))
                weights[i] -= (len(objs[i]) - len(set(objs[i])))/len(objs[i])
            obj = np.dot( (np.dot(weights,objs) / np.sum(weights)), yaw_weights )
        return obj

    # Nelder Mead Optimization
    def optimize(self):
        self.opt = sp.minimize(
            self.repf,
            self.x0,
            method="Nelder-Mead",
            options={'maxiter': self.nit}
        )
        self.message = self.opt.message
        self.nit = self.opt.nit
        self.fun = self.opt.fun
        self.x = self.opt.x

# Example
if __name__ == "__main__":
    def rosenbrock(X):
        """
        Good R^2 -> R^1 function for optimization
        http://en.wikipedia.org/wiki/Rosenbrock_function
        """
        x = X[0]
        y = X[1]
        a = 1. - x
        b = y - x*x
        obj = a*a + b*b*100.
        print(obj)
        return obj

    try:
        opt = Nelder_Mead_Optimizer(rosenbrock, np.array([0.,0.]), 100, 3)
        print(opt.message)
        print("Iters: {}".format(opt.nit))
        print("Design:\n{}".format(list(opt.x)))
        print("Objective: {}".format(np.around(opt.fun,decimals=6)))
    except:
        print("sorry ... change line 36 to self.f instead of self.repf")
