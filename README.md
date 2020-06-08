# Final Project AA222

Joint work with [Ethan](https://github.com/ezshen)!

Check out our [report](report.pdf)!

Or check out some [plots & exploration](results/plotting.ipynb)!

The main script is [run.py](run.py). Interfacing with XFOIL is done in [xfoil/xfoil.py](xfoil/xfoil.py). If you're not on Mac, please replace `xfoil/xfoil` with an executable or binary containing the [XFOIL software](https://web.mit.edu/drela/Public/web/xfoil/). You can see the airfoil parameterization methods in [parameterizations](parameterizations).

ToDo: currently only runs on python2 because of the xfoil subprocess.subp() call. We will adjust to include python3 support soon.
