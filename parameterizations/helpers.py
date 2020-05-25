from __future__ import division
import numpy as np

def fn_2_dat(filename, upper, lower):
    # get a grid of points approximating
    # the upper and lower edge of the foil
    x = np.linspace(0.0, 1.0, 150)
    foil_up = upper(x)
    foil_lo = lower(x)
    topmax = np.max(foil_up)

    # to appease UCI regulation
    # 3 to 1 ratio max
    # (we automatically take max
    # ratio at each design)
    foil_up = foil_up * 1/(6*topmax)
    foil_lo = foil_lo * 1/(6*topmax)

    # Write to a .dat file for Xfoil.
    # defines curve starting at far
    # rear of the foil (x=1) and then
    # moves counterclockwise up around
    # to the front of the airfoil at
    # x=0, then down and back to the
    # rear tip (right)
    with open(filename, "w") as f:
        f.write("Custom_Airfoil\n")
        for i in range(len(x)-1,-1,-1):
            f.write("{:.5f}  {:.5f}\n".format(x[i],foil_up[i]))
        for i in range(len(x)):
            f.write("{:.5f} {:.5f}\n".format(x[i],foil_lo[i]))
