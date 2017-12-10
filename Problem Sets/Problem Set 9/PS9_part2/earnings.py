def main(theta, params, kgrid, sizek, z_grid):
    import numba

    '''
    This function takes wage, parameters and returns the per period profit
    for matrix (profit for each combination of z, k, k')
    '''
    import numpy as np
    from scipy.stats import norm
    import scipy.integrate as integrate
    import numba
    import time

    # unpack params
    ak, psi, rho, sigma, theta0 = theta
    mu, sizez, al, delta, betaf = params

    # returns the firm operating profit for a given z and k
    @numba.jit
    def firmprofit(z, k):
        p = (z*k**ak)

        return p

    # returns the adjustment costs for a given k and k'
    @numba.jit
    def adjcost(k, k1):
        c = (psi/2) * ((k1 - (1 - delta) * k) / k) ** 2 * k

        return c

    # returns the per period earnings for a given z, k, k'
    @numba.jit
    def earnings(z, k, k1):
        p = firmprofit(z, k)  # Operating profit
        c = adjcost(k, k1)  # adjustment costs
        e = p - (k1 - (1-delta)*k) - c - theta0 # op - net investment - adj costs

        return e


    # initialize earnings matrix for each possible z
    E = np.zeros((sizez, sizek, sizek))


    # creates "per period earnings" matrix for all possible values of z and k, k'
    @numba.jit
    def Epp():
        for z in range(sizez):
            for k in range(sizek):
                for k1 in range(sizek):
                    E[z, k, k1] = earnings(z_grid[z], kgrid[k], kgrid[k1])
        return E

    E = Epp()

    return E
