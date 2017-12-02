import numpy as np
from scipy.stats import norm
import scipy.integrate as integrate
import numba
import time

import kgrid
import zgrid
import earnings
import VFI
import dist

# initialize parameters
ak = .297  # capital share of output
al = .650  # labor share of output
delta = .154  # Depreciation
psi = 1.080  # Coeff on quadratic adj costs
wage = .7  # wage rate
r = .040  # Int rate
betaf = 1 / (1 + r)  # discount factor
sigma = .213  # Std. Deviation of z shock
mu = 0  # mean of z AR1
rho = .7605  # Persistance of z shock
sizez = 9  # size of z grid


params = (ak, al, delta, psi, wage, r, betaf, sigma, mu, rho, sizez)

kgrid, sizek = kgrid.main(params)

z_grid, pi, expz = zgrid.main(params)

E, E_expz = earnings.main(params, z_grid, expz, kgrid, sizek, sizez)

Vnew, loc, result, time = VFI.main(params, z_grid, expz,
                                   kgrid, sizek, sizez, E, E_expz)

print('VFI', result, 'after', time, 'seconds')


Gamma = dist.main(kgrid, sizez, sizek, pi, loc)

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
#plt.xlim([0, 210])
