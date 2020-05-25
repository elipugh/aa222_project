import subprocess as subp
import numpy as np
import os
import sys
import re
import time
import random
import sys


# Evaluate the different characteristics
# of an airfoil
# Hyperparams I chose ... maybe changed later:
#   - Reynolds number set to 38k
#   - Mach number set to 0.03
#   - Max 10k iterations
#   - Visuous flow
#   - Evals at each degree in angles
def evaluate(filename, angles, viscous):
    curdir = os.path.dirname(os.path.realpath(__file__))
    xf = Xfoil()
    # Normalize foil
    xf.cmd("NORM\n")
    # Load foil
    xf.cmd('LOAD {}\n'.format(filename))
    # Disable graphing
    xf.cmd("PLOP\nG F\n\n")
    # Set options for panels
    xf.cmd("PPAR\n")
    xf.cmd("N 240\n")
    xf.cmd("T 1\n\n\n")
    xf.cmd("PANE\n")
    # Operation mode
    xf.cmd("OPER\n")
    # Set Reynolds #
    xf.cmd("Re 38000\n")
    # Set Mach
    xf.cmd("Mach 0.03\n")
    if viscous:
        # Viscous mode
        xf.cmd("v\n")
    # Allow more iterations
    xf.cmd("ITER 10000\n")
    # Get started with an eval
    xf.cmd("ALFA 0\n")
    # Set recording to file sf.txt
    savefile = "sf{}.txt".format(random.randrange(10**20)%(10**15))
    xf.cmd("PACC\n{}\n\n".format(savefile))
    # Run evals for 0deg to 12deg
    for a in angles:
        xf.cmd("ALFA {}\n".format(a))
    # End recording
    xf.cmd("PACC\n\n\nQUIT\n")
    # Don't try to read results before
    # Xfoil finished simulations
    xf.wait_to_finish()

    alpha = []
    CL = []
    CD = []
    CDp = []
    CM = []

    try:
        # open log savefile and read
        # results into arrays to return
        with open(savefile, "r") as f:
            for _ in range(12):
                f.next()
            for line in f:
                if line is not None:
                    r = line.replace("-", " -").split()
                    alpha   += [float(r[0])]
                    CL      += [float(r[1])]
                    CD      += [float(r[2])]
                    CDp     += [float(r[3])]
                    CM      += [float(r[4])]
    except:
        print(sys.exc_info())
        # probably worst case,
        # nothing converged,
        # hence no savefile?
        print("Uh oh. Delete savefile then retry")
        return None

    dnc = []
    for i,a in enumerate(angles):
        if a not in alpha:
            dnc += [i]

    if len(dnc)>0:
        print "Angles did not converge:\n\t", np.array(angles)[dnc]

    # Worst case scenario, nothing converges
    if len(dnc) == len(angles):
        return None

    worsts = [0, 0, 0, 0]
    for i in range(len(alpha)):
        if CL[i] > worsts[0]:
            worsts[0] = CL[i]
        if CD[i] > worsts[1]:
            worsts[1] = CD[i]
        if CDp[i] > worsts[2]:
            worsts[2] = CDp[i]
        if CM[i] > worsts[3]:
            worsts[3] = CM[i]

    for i in dnc:
        alpha.insert(i, angles[i])
        CL.insert(i, worsts[0])
        CD.insert(i, worsts[1])
        CDp.insert(i, worsts[2])
        CM.insert(i, worsts[3])

    try:
        # Remove savefile
        os.remove(savefile)
    except:
        # probably worst case,
        # nothing converged,
        # hence no savefile?
        print("fail rm {}".format(savefile))
        pass

    # Return results
    return alpha, CL, CD, CDp, CM


class Xfoil():
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.xfsubprocess = subp.Popen(os.path.join(path, 'xfoil'), stdin=subp.PIPE, stdout=open(os.devnull, 'w'))
        self._stdin = self.xfsubprocess.stdin
    def cmd(self, cmd):
        self.xfsubprocess.stdin.write(cmd)
    def wait_to_finish(self):
        self.xfsubprocess.wait()

# Example
if __name__ == "__main__":
    alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr = evaluate("/users/EliPugh/custom4.txt")
    print("alpha    :", alpha)
    print("CL       :", CL)
    print("CD       :", CD)
    print("CDp      :", CDp)
    print("CM       :", CM)
    print("Top_Xtr  :", Top_Xtr)

    print("Bot_Xtr  :", Bot_Xtr)