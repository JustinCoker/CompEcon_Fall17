def main(w0, eq_params, sizek, kgrid, z_grid, pi):

    '''
    This function takes wage and eqiulibrium values as arguments and calls
    value function and stationary distribution iteration until convergence.

    The function returns the market clearing distance which illustrates the
    difference between aggregate labor supply and labor demand.
    '''

    import numpy as np

    import earnings  # import the earnings module
    import VFI  # import the VFI (value function iteration) module
    import dist  # import the dist (stationary distribution) module

    # unpack params
    ak, al, delta, psi, r, betaf, sigma, mu, rho, sizez, h = eq_params

    # wage = initial guess (w0)
    wage = w0

    # calls the earnings module, which returns the grid of per period earnings
    E = earnings.main(wage, eq_params, z_grid, kgrid, sizek)

    # calls the VFI module, which returns the firm decision rule objects
    Vnext, loc, result, time, iter = VFI.main(wage, eq_params, z_grid, kgrid, sizek, E, pi)

    # prints VFI, dist iteration for diagnostics
    print('VFI', result, 'after', iter, 'iterations', 'in', time, 'seconds')

    # calls the dist module which returns the stationary distribution for a
    # given partial equilibrium
    Gamma = dist.main(kgrid, sizez, sizek, pi, loc)

    # the policy function for a given partial equilibrium
    kopt = kgrid[loc]  # finds optimal K after VFI Convergence

    # the optimal net investment for an individual firm in partial eq
    iopt = kopt - (1 - delta) * kgrid  # net investment given k

    # calculates labor demand for an individual firm
    ld = np.zeros((sizez, sizek))  # per firm labor demand
    for q in range(sizez):
        for j in range(sizek):
            ld[q, j] = (((al / wage) ** (1 / (1 - al))) *
                        ((kgrid[j] ** ak) ** (1 / (1 - al))) *
                        (z_grid[q] ** (1 / (1 - al))))

    # calculates value of adjustment cost function
    adj_cost = psi / 2 * np.multiply((iopt)**2, 1 / kgrid)  # adj cost given k

    # per firm output given the optimal labor demand and current value of k
    y = (np.multiply(np.multiply((ld) ** al,
                                 kgrid ** ak), np.transpose([z_grid])))

    ####################################################################
    # Steady State Aggregates:

    LD = np.multiply(ld, Gamma).sum()  # Aggregate labor Demand

    I = np.multiply(iopt, Gamma).sum()  # Aggregate Investment

    ADJ_cost = np.multiply(adj_cost, Gamma).sum()  # Aggregate Adj costs

    Y_agg = np.multiply(y, Gamma).sum()  # Aggregate Output

    C_agg = Y_agg - I - ADJ_cost  # Aggregate consumption

    LS = h * (1 / (wage * C_agg))  # Aggregate Labor supply

    Clearing_Dist = abs(LS - LD)  # distance between supply and demand

    print('LD-LS', Clearing_Dist)

    return Clearing_Dist
