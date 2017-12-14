def main(theta, params, kgrid, pi, Vnext, loc, T, N, z_grid):
    import numpy as np
    import numba
    import zgrid
    import zshocks

    ak, psi, rho, sigma = theta

    mu, sizez, al, delta, betaf = params

    def zdraws():
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

    @numba.jit()
    def V_sim():
        V_sim = np.zeros((N, T))
        for i in range(N):
            for j in range(T):
                V_sim[i, j] = Vnext[zshocks[i, j]][kloc_sim[i, j]]

        return V_sim


    @numba.jit()
    def pi_sim():
        pi_sim = np.zeros((N, T))
        for i in range(N):
            for j in range(T):
                pi_sim[i, j] = z_grid[zshocks[i, j]] * kgrid[kloc_sim[i, j]] ** ak

        return pi_sim

    I_sim = I_sim()

    V_sim = V_sim()

    pi_sim = pi_sim()

    return k_sim[:, -50:], I_sim[:, -50:], V_sim[:, -50:], pi_sim[:, -50:]
