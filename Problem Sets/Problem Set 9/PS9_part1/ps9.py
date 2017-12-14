import numpy as np
import scipy.optimize as opt
from scipy.misc import derivative
import time

start = time.clock()

def sim_moments(theta):

    import numpy as np
    import time
    import numba

    import zgrid
    import kgrid
    import zshocks
    import simul
    import VFI



    # params
    #sigma = 0.213  # struct param to be estimated
    mu = 0  # fixed param
    #rho = 0.7605  # struct param to be estimated
    sizez = 9  # fixed param
    #ak = .297  # struct param to be estimated
    al = .650  # fixed
    delta = 0.15  # fixed
    betaf = .95  # fixed
    #psi = 1.080  # struct param to be estimated

    params = (mu, sizez, al, delta, betaf)

    T = 250  # number of years simulated
    N = 1000  # number of firms simulated

    kgrid, sizek = kgrid.main(params)

    z_grid, pi = zgrid.main(sigma, mu, rho, sizez)

    # E = earnings.main(theta, params, kgrid, sizek, z_grid)

    Vnext, loc = VFI.main(theta, params, z_grid, kgrid, sizek, sizez, pi)

    k_sim, I_sim, V_sim, prof_sim = simul.main(theta, params, kgrid, pi,
                                             Vnext, loc, T, N, z_grid)

    def moments(k_sim, I_sim, V_sim, prof_sim):

        IoverK = (I_sim/k_sim).reshape((N*50, 1))
        avgQ = (V_sim/k_sim).reshape((N*50, 1))
        PIoverK = (prof_sim/k_sim).reshape((N*50, 1))

        y = np.matrix(IoverK)
        X = np.matrix(np.concatenate((np.ones((N*50, 1)), avgQ, PIoverK), axis = 1))

        a0, a1, a2 = np.linalg.inv(X.T * X) * X.T * y  # reg coeffs

        ik = IoverK.reshape((1, N*50))  # I over K reshaped for corrcoef()
        sc_ik = np.corrcoef(ik[0][1:], ik[0][:50000-1])[0,1]  # sc_
        sd_piK = np.std(PIoverK)
        qbar = V_sim.sum() / k_sim.sum()

        U_sim = np.array((a1[0, 0], a2[0, 0], sc_ik, sd_piK, qbar))

        return U_sim


    U_sim = moments(k_sim, I_sim, V_sim, prof_sim)

    return U_sim

sigma = 0.857
rho = 0.111
ak = .699
psi = .1647

theta = np.array([ak, psi, rho, sigma])

def dist(theta):
    U_sim = sim_moments(theta)
    U_data = np.array((.03, .24, .4, .25, 3.0))

    dist = np.matrix((U_data - U_sim)) * np.eye(5) * np.matrix((U_data - U_sim)).T

    return dist[0, 0]


#distance = dist(theta)

bounds = [(0, 1), (0, .5), (0, .4), (0, 1.5)]

result = opt.minimize(dist, theta, method='nelder-mead', options={'maxiter': 100})

# Get SE's of parameter estimates

x0 = result['x']

dtheta = derivative(sim_moments, x0)

std_err = dtheta.T * np.eye(5) * dtheta

end = time.clock()

print("time: ", end-start)
