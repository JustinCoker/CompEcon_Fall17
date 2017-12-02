def main(w, params, z_grid, kgrid, sizek):

    import numpy as np
    from scipy.stats import norm
    import scipy.integrate as integrate
    import numba
    import time

    wage = w

    ak, al, delta, psi, r, betaf, sigma, mu, rho, sizez, h = params

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
    E = np.zeros((sizez, sizek, sizek))


    # creates "per period earnings" matrix for all possible values of z and k, k'
    
    for z in range(sizez):
        for k in range(sizek):
            for k1 in range(sizek):
                E[z, k, k1] = earnings(z_grid[z], kgrid[k], kgrid[k1])

    return E
