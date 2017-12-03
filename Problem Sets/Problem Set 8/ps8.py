import numpy as np
from scipy.stats import norm
import scipy.integrate as integrate
import numba
import time
import scipy.optimize as opt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import kgrid
import zgrid
import earnings
import VFI
import dist
import equil
import solu

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

# parameters that occur in any state of the model (Gen or Partial equilibrium)
params = (ak, al, delta, psi, wage, r, betaf, sigma, mu, rho, sizez)

# calls the kgrid function to return the grid of k values and size of kgrid
kgrid, sizek = kgrid.main(params)

# calls the z_grid function to caluclate the zgrid given sizez
z_grid, pi = zgrid.main(params)

# free parameters in the Gen eq (not including wage since it is endog.)
eq_params = (ak, al, delta, psi, r, betaf, sigma, mu, rho, sizez, h)

wage_initial = .89  # initialize a wage guess.

# cal the optimizer routine of the equil function which determines equlibrium
# for a given wage and param values
OPTWAGE = opt.minimize(equil.main, wage_initial,
                       (eq_params, sizek, kgrid, z_grid, pi),
                       method='Nelder-Mead', tol=1e-5,
                       options={'maxiter': 5000})

print('The Equilibrium Wage is:', OPTWAGE.x[0])

wstar = OPTWAGE.x[0]

# Calculates partial equilibrium values at the equilibrium wage.
(kopt, Gamma, iopt, ld, adj_cost, y,
 LD, I, ADJ_cost, Y_agg, C_agg, LS) = solu.main(wstar, eq_params, sizek, kgrid,
                                                z_grid, pi)


# Plot the stationary distribution over k
fig, ax = plt.subplots()
ax.plot(kgrid, Gamma.sum(axis=0))
plt.xlabel('Size of Capital Stock')
plt.ylabel('Density')
plt.title('Stationary Distribution over Capital')
plt.show()


# plot the policy functions

plt.plot(kgrid, kgrid)
for i in range(9):
    plt.plot(kgrid, kopt[i], label = 'z' + str(i))
plt.plot(kgrid, kgrid, color = 'k', markersize =25, label='45 degree')
plt.legend()
plt.show()
