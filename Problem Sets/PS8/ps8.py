import numpy as np
from scipy.stats import norm
import scipy.integrate as integrate
import numba
import time
import scipy.optimize as opt


import kgrid
import zgrid
import earnings
import VFI
import dist
import equil

# initialize parameters
ak = .297  # capital share of output
al = .650  # labor share of output
delta = .154  # Depreciation
psi = 1.080  # Coeff on quadratic adj costs
wage = .7  # wage rate
r = .040  # Int rate
betaf = 1 / (1 + r)  # discount factor
sigma = .213  # Std. Deviation of z shockkgrid
mu = 0  # mean of z AR1
rho = .7605  # Persistance of z shock
sizez = 9  # size of z grid
h = 6.616

params = (ak, al, delta, psi, wage, r, betaf, sigma, mu, rho, sizez)

kgrid, sizek = kgrid.main(params)

z_grid, pi = zgrid.main(params)

eq_params = (ak, al, delta, psi, r, betaf, sigma, mu, rho, sizez, h)

wage_initial = .89
OPTWAGE = opt.minimize(equil.main, wage_initial,
                          (eq_params, sizek, kgrid, z_grid, pi),
                          method='Nelder-Mead', tol = 1e-5,
                          options={'maxiter': 5000})
'''
## plot the SD

# import packages
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# Plot the stationary distribution over k
fig, ax = plt.subplots()
ax.plot(kgrid, Gamma.sum(axis=0))
plt.xlabel('Size of Capital Stock')
plt.ylabel('Density')
plt.title('Stationary Distribution over Capital')
plt.show()

'''
