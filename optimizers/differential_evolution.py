from __future__ import division
import numpy as np
from copy import copy
import scipy.optimize as sp

class Differential_Evolution_Optimizer():
    def __init__(self, f, bounds, n, reps=1, args=(), popsize=5):
        self.args = args
        self.reps = reps
        self.f = f
        self.bounds = bounds
        self.nit = n
        self.popsize = popsize
        self.optimize()

    # This repeats the evaluation with very slightly
    # different values to get more accurate drag number
    def repf(self, pts):
        yaw_weights = np.array([6.641, 6.55, 6.283, 5.863,
                                5.321, 4.697, 4.033, 3.368,
                                2.736, 2.162, 1.661])
        if self.reps == 1:
            obj = np.dot(self.f(pts, *(self.args)), yaw_weights)
        else:
            objs = [[] for _ in range(self.reps)]
            weights = np.ones(self.reps)
            for i in range(self.reps):
                npt = pts + np.random.normal(0, np.mean(pt)/20, pt.shape)
                objs[i] = self.f(npt, *(self.args))
                weights[i] -= (len(objs[i]) - len(set(objs[i])))/len(objs[i])
            obj = np.dot( (np.dot(weights,objs) / np.sum(weights)), yaw_weights )
        print("\tRegularized : {}\n".format(obj + np.linalg.norm(pts)*20))
        return obj + np.linalg.norm(pts)*20

    # Nelder Mead Optimization
    def optimize(self):
        self.opt = sp.differential_evolution(
            self.repf,
            self.bounds,
            strategy="best1bin",
            maxiter=self.nit,
            popsize=self.popsize
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
        opt = Differential_Evolution_Optimizer(rosenbrock, [(-1,2),(-1,2)], n=5, reps=1, popsize=5)
        print(opt.message)
        print("Iters: {}".format(opt.nit))
        print("Design:\n{}".format(list(opt.x)))
        print("Objective: {}".format(opt.fun))
    except:
        print("sorry ... change line 37 to self.f instead of self.repf")