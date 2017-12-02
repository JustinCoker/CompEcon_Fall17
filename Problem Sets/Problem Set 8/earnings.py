def main(params, z_grid, expz, kgrid, sizek, sizez):

    import numpy as np
    from scipy.stats import norm
    import scipy.integrate as integrate
    import numba
    import time

    ak, al, delta, psi, wage, r, betaf, sigma, mu, rho, sizez = params

    def firmprofit(z, k):
        p = ((1-al)*(al/wage)**(al/(1-al))*
            z**(1/(1-al))*
            k**(ak/(1-al)))

        return p

    def adjcost(k, k1):
        c = (psi/2) * ((k1 - (1-delta) * k) / k) ** 2 * k

        return c

    def earnings(z, k, k1):
        p = firmprofit(z, k)
        c = adjcost(k, k1)
        e = p - (k1 - (1-delta)*k) - c

        return e


    # initialize earnings matrix for each possible z
    E = [np.zeros((sizek, sizek)) for i in range(sizez)]

    E_expz = [np.zeros((sizek, sizek)) for i in range(sizez)]

    # creates "per period earnings" matrix for all possible values of z and k, k'
    for z in range(len(z_grid)):
        for k in range(len(kgrid)):
            for k1 in range(len(kgrid)):
                E[z][k, k1] = earnings(z_grid[z], kgrid[k], kgrid[k1])
                E_expz[z][k, k1] = earnings(expz[z], kgrid[k], kgrid[k1])

    return E, E_expz
