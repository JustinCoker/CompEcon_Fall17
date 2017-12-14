def main(params):

    '''
    Calculates and returns the grid of k values
    '''
    import numpy as np
    from scipy.stats import norm
    import scipy.integrate as integrate
    import numba
    import time

    mu, sizez, al, delta, betaf = params
    # creating kgrid as done in class. Credit: J Debacker
    dens = 5
    # put in bounds here for the capital stock space
    kstar = 10 # after increasing kstar repeatedly, this gives
	       # the smallest grid space where the stationary
	       # distribution doesn't have a mass at the tail.


    kbar = 2*kstar
    lb_k = 0.05
    ub_k = kbar
    krat = np.log(lb_k / ub_k)
    numb = np.ceil(krat / np.log(1 - delta))
    K = np.zeros(int(numb * dens))

    for j in range(int(numb * dens)):
        K[j] = ub_k * (1 - delta) ** (j / dens)
    kgrid = K[::-1]
    sizek = kgrid.shape[0]

    return kgrid, sizek
