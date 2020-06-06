import os

design_points = []
objectives = []
i = 0
with open("results3.txt", "r") as f:
    for l in f:
        if l is not None:
            l = l.replace(",", " ")
            l = l.replace("[", " ")
            l = l.replace("]", " ")
            l = l.replace(":", " ")
            r = l.split()
            if r[0] == "Design":
                dp = [float(x) for x in r[1:]]
                design_points += [dp]
            if r[0] == "Objective":
                objectives += [float(r[1])]

with open("objectives3.txt", "w") as f:
    for i, o in enumerate(objectives):
        if i >= 200:
            break
        f.write("{},\n".format(o))

with open("design_points3.txt", "w") as f:
    for i, p in enumerate(design_points):
        if i >= 200:
            break
        f.write("{},\n".format(p))

