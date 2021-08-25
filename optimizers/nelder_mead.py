from __future__ import division
import numpy as np
from copy import copy
import scipy.optimize as sp

# This is just my wrapper for Nelder Mead, but you could
# easily change this wrapper class do do LBFGS or something
# similar
class Nelder_Mead_Optimizer():
    def __init__(self, f, x0, n):
        # Function to optimize
        self.f = f
        # Initial starting point
        self.x0 = x0
        # Number of iterations
        self.nit = n

    # This performs Nelder Mead Optimization
    def optimize(self):
        self.opt = sp.minimize(
            self.f,
            self.x0,
            method="Nelder-Mead",
            options={'maxiter': self.nit}
        )
        # Set the output of the optimizer
        self.message = self.opt.message
        # Number of iterations to convergence
        self.nit = self.opt.nit
        # Value of the optimal solution
        self.fun = self.opt.fun
        # Optimal solution
        self.x = self.opt.x

        
# Example
if __name__ == "__main__":
    # Example of an arbitrary black-box function:
    # Here's where you would put your software shtuff.
    # Anything that takes in vector, outputs score
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

    # Choose initial design. Nelder Mead will have easier
    # time optimizing if the initial design point is decent
    x0 = np.array([0.,0.])
    # Make an optimizer with an initial point, max 100 iterations
    opt = Nelder_Mead_Optimizer(rosenbrock, x0, 100)
    # Do the optimization
    opt.optimize()
    # Get optimization output and print it for user
    print(opt.message)
    print("Iters: {}".format(opt.nit))
    print("Design:\n{}".format(list(opt.x)))
    print("Objective: {}".format(np.around(opt.fun,decimals=6)))
