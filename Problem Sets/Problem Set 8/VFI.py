def main(params, z_grid, expz, kgrid, sizek, sizez, E, E_expz):

    import numpy as np
    from scipy.stats import norm
    import scipy.integrate as integrate
    import numba
    import time

    ak, al, delta, psi, wage, r, betaf, sigma, mu, rho, sizez = params

    CV = [np.zeros(sizek) for el in range(sizez)]
    Vnext = [np.zeros(sizek) for el in range(sizez)]
    Vnew = [np.zeros(sizek) for el in range(sizez)]
    VAL = [np.zeros((sizek, sizek)) for el in range(sizez)]
    loc = [np.zeros(sizek) for i in range(sizez)]
    tol = 5e-5
    maxiter = 300
    iter = 1
    dist = 1

    @numba.jit
    def valf_it(CV):
        for q in range(len(z_grid)):
            for i in range(len(kgrid)):
                for j in range(len(kgrid)):
                    VAL[q][i,j] = E[q][i,j] +  betaf * CV[q][j]

        return VAL

    #@numba.jit
    def NewV(VAL):
        for q in range(len(VAL)):
            Vnew[q] = VAL[q].max(axis = 1)
            loc[q] = np.argmax(VAL[q], axis = 1)

        return Vnew, loc

    @numba.jit
    def nextV(CV, E_expz, loc):
        for q in range(len(z_grid)):
            for i in range(len(loc[q])):
                l = int(loc[q][i])
                Vnext[q][i] = E_expz[q][i, l]+ betaf * CV[q][l]

        return Vnext


    start_time = time.clock()
    while dist > tol and iter < maxiter:
        VAL = valf_it(CV)
        Vnew, loc = NewV(VAL)
        dist = np.absolute((Vnew[0] - CV[0]).max())
        iter += 1
        Vnext = nextV(CV, E_expz, loc)
        CV = Vnext
        print(iter, dist)

    if iter < maxiter:
        result = 'Successful Convergence'

    else:
        result = 'Max Iterations Reached'

    time = time.clock() - start_time

    return Vnew, loc, result, time
