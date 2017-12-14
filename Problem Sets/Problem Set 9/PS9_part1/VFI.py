def main(theta, params, z_grid, kgrid, sizek, sizez, pi):

    '''
    This function takes the wage and parameters and runs the value function
    iteration routine to convergence.

    The function returns the value function and loc objects.

    loc object determines the policy function from the kgrid.
    '''

    import numpy as np
    from scipy.stats import norm
    import scipy.integrate as integrate
    import numba
    import time
    import earnings

    # unpack params
    ak, psi, rho, sigma = theta
    mu, sizez, al, delta, betaf = params

    CV = np.zeros((sizez, sizek))  # guess i.e. V0

    # initialize matrix that will hold value for every combo of z, k, k'
    VAL = np.zeros((sizez, sizek, sizek))

    tol = 1e-6  # tolerance
    maxiter = 400  # maximum iterations
    iter = 1  # initialize iter counter
    dist = 5  # initialize dist for use in the VFI

    E = earnings.main(theta, params, kgrid, sizek, z_grid)

    @numba.jit
    def valf_it(VAL, CV, sizez, sizek, E, pi):

        '''
        given the current value function, this function will return
        the VAL matrix cotaining the expected valueVAL
        conditional on z of all possible combinations of z, k, k'
        '''
        CondV = np.dot(pi, CV)

        for q in range(sizez):
            for i in range(sizek):
                for j in range(sizek):
                    VAL[q, i, j] = E[q, i, j] + betaf * CondV[q, j]

        return VAL



    start_time = time.clock()
    while dist > tol and iter < maxiter:
        VAL = valf_it(VAL, CV, sizez, sizek, E, pi)  # gets VAL matrix
        Vnext = VAL.max(axis=2)  # val fn guess for next iteration
        loc = np.argmax(VAL, axis=2)  # stores index of optimal choice
        dist = (np.absolute(Vnext - CV)).max()
        iter += 1
        CV = Vnext

    if iter < maxiter:
        result = 'Successful Convergence'

    else:
        result = 'Max Iterations Reached'

    #time = time.clock() - start_time

    return Vnext, loc
