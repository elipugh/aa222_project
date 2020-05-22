import subprocess as subp
import numpy as np
import os
import re
import time


# Evaluate the different characteristics
# of an airfoil
# Hyperparams I chose ... maybe changed later:
#   - Reynolds number set to 38k
#   - Mach number set to 0.03
#   - Max 10k iterations
#   - Visuous flow
#   - Evals at 0, 0.5, 2, 4, 8, 12 degrees
def evaluate(filename):
    curdir = os.path.dirname(os.path.realpath(__file__))
    xf = Xfoil()
    # Normalize foil
    xf.cmd("NORM\n")
    # Load foil
    xf.cmd('LOAD {}\n'.format(filename))
    # Disable graphing
    xf.cmd("PLOP\nG\n\n")
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
    # Viscous mode
    xf.cmd("v\n")
    # Allow more iterations
    xf.cmd("ITER 10000\n")
    # Get started with an eval
    xf.cmd("ALFA 0\n")
    # Set recording to file sf.txt
    xf.cmd("PACC\nsf.txt\n\n")
    # Run evals for 0deg to 12deg
    xf.cmd("ALFA 0\n")
    xf.cmd("ALFA 0.5\n")
    xf.cmd("ALFA 2\n")
    xf.cmd("ALFA 4\n")
    xf.cmd("ALFA 8\n")
    xf.cmd("ALFA 12\n")
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
    Top_Xtr = []
    Bot_Xtr = []
    # open log savefile and read
    # results into arrays to return
    with open("sf.txt", "r") as f:
        for _ in range(12):
            f.next()
        for line in f:
            if line is None:
                break
            a = line.split()
            alpha   += [a[0]]
            CL      += [a[1]]
            CD      += [a[2]]
            CDp     += [a[3]]
            CM      += [a[4]]
            Top_Xtr += [a[5]]
            Bot_Xtr += [a[6]]
    # Remove savefile
    os.remove("sf.txt")
    # Return results
    return alpha, CL, CD, CDp, CM, Top_Xtr, Bot_Xtr


class Xfoil():
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.xfsubprocess = subp.Popen(os.path.join(path, 'xfoil'), stdin=subp.PIPE, stdout=open(os.devnull, 'w'))
        self._stdin = self.xfsubprocess.stdin
    def cmd(self, cmd):
        self.xfinst.stdin.write(cmd)
    def wait_to_finish(self):
        self.xfinst.wait()

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