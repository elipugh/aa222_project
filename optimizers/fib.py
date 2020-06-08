from __future__ import division
import numpy as np
from copy import copy

class Fib_Optimizer():
    def __init__(self, f, x0, n, a, b, reps=4, args=()):
        self.args = args
        self.reps = reps
        self.f = f
        self.x0 = x0
        self.n = n
        self.a = np.array([a])
        self.b = np.array([b])
        self.bounds = (a,b)
        self.optimize()
        self.message = "Eli wrote this so there's no fancy optimizer status, lol"

    # This repeats the evaluation with very slightly
    # different values to get more accurate drag number
    def repf(self, pt):
        yaw_weights = np.array([6.641, 6.55, 6.283, 5.863, 5.321, 4.697,
                                4.033, 3.368, 2.736, 2.162, 1.661])
        if self.reps == 1:
            return self.f(pt, *(self.args))
        objs = [[] for _ in range(self.reps)]
        weights = np.ones(self.reps)
        for i, npt in enumerate(np.linspace(0.99*pt, 1.01*pt, self.reps)):
            objs[i] = self.f(npt, *(self.args))
            weights[i] -= (len(objs[i]) - len(set(objs[i])))/len(objs[i])
        return np.dot( (np.dot(weights,objs) / np.sum(weights)), yaw_weights )

    # Fibonacci Search Optimization
    # see slides 10-19:
    #   https://www.cs.ccu.edu.tw/~wtchu/courses/2014s_OPT/Lectures/
    #   Chapter%207%20One-Dimensional%20Search%20Methods.pdf
    def optimize(self):
        x0, n, a, b = self.x0, self.n, self.a, self.b
        eps = 0.01
        phi = (1+np.sqrt(5))/2
        s = (1-np.sqrt(5))/(1+np.sqrt(5))
        p = 1 / (phi*(1-s**(n+1))/(1-s**n))
        d = p*b + (1-p)*a
        yd = self.repf(d)
        for i in range(n-1):
            if i == n-2:
                c = eps*a + (1-eps)*d
            else:
                c = p*a + (1-p)*b
            yc = self.repf(c)
            if yc < yd:
                b, d, yd = d, c, yc
            else:
                a, b = b, c
            a_r, b_r = np.around([a,b],decimals=3)
            print("\nInterval: [{},{}]\n".format(a_r[0], b_r[0]))
            p = 1 / (phi**(1-s**(n-i))/(1-s**(n-i-1)))

        self.bounds = ((a, b) if a < b else (b,a))
        self.x = np.array([np.mean(self.bounds)])
        self.fun = self.repf(self.x)
        self.nit = n

# Example
if __name__ == "__main__":
    f = lambda x : x**2 - 0.8*x + 0.56
    opt = Fib_Optimizer(f, np.array([0.6]), 8, 0.2, 1)
    print(opt.bounds)    # -5.999543942488367
    print(opt.fun)  # 0.002399843156309108