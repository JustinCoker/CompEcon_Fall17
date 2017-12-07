

import numpy as np
import time
import numba

import zgrid
import kgrid
import zshocks
#import earnings
import VFI
start  = time.clock()

# params
sigma = 0.213  # struct param to be estimated
mu = 0  # fixed param
rho = 0.7605  # struct param to be estimated
sizez = 9  # fixed param
ak = .297  # struct param to be estimated
al = .650  # fixed
delta = 0.15  # fixed
betaf = .95  # fixed
psi = 1.080  # struct param to be estimated

theta = np.array([ak, psi, rho, sigma])

params = (mu, sizez, al, delta, betaf)

kgrid, sizek = kgrid.main(params)

z_grid, pi = zgrid.main(sigma, mu, rho, sizez)

# E = earnings.main(theta, params, kgrid, sizek, z_grid)

Vnext, loc = VFI.main(theta, params, z_grid, kgrid, sizek, sizez, pi)

T = 1050  # number of years simulated
N = 1000  # number of firms simulated


def zdraws():
    z_grid, pi = zgrid.main(sigma, mu, rho, sizez)

    z_shocks = np.zeros((N, T))
    for i in range(N):
        z_shocks[i] = zshocks.sim_markov(z_grid, pi, T)

    return z_shocks.astype(dtype=np.int)

zshocks = zdraws()

@numba.jit
def kloc_sim():
    kloc_sim = np.zeros((N, T), dtype = np.int)
    for i in range(N):
        for j in range(T-1):
            kloc_sim[i, j+1] = loc[zshocks[i, j]][kloc_sim[i, j]]
    return kloc_sim


kloc_sim = kloc_sim()
k_sim = kgrid[kloc_sim]

@numba.jit()
def I_sim():
    I_sim = np.zeros((N, T))
    for i in range(N):
        for j in range(T-1):
            I_sim[i, j + 1] = k_sim[i, j+1] - k_sim[i, j] * (1-delta)
    return I_sim


I_sim = I_sim()
end = time.clock()

print("time: ", end-start)
