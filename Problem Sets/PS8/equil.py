def main(w0, eq_params, sizek, kgrid, z_grid, pi):

    import numpy as np

    import zgrid
    import earnings
    import VFI
    import dist

    ak, al, delta, psi, r, betaf, sigma, mu, rho, sizez, h = eq_params

    wage = w0

    E = earnings.main(wage, eq_params, z_grid, kgrid, sizek)

    Vnext, loc, result, time, iter = VFI.main(wage, eq_params, z_grid, kgrid, sizek, E, pi)

    #print('VFI', result, 'after', iter, 'iterations', 'in', time, 'seconds')

    Gamma = dist.main(kgrid, sizez, sizek, pi, loc)



    kopt = kgrid[loc]  # finds optimal K after VFI Convergence

    iopt = kopt - (1 - delta) * kgrid  # net investment given k

    ld = np.zeros((sizez, sizek))  # per firm labor demand
    for q in range(sizez):
        for j in range(sizek):
            ld[q, j] = (((al / wage) ** (1 / (1 - al))) *
                        ((kgrid[j] ** ak) ** (1 / (1 - al))) *
                        (z_grid[q] ** (1 / (1 - al))))

    adj_cost = psi / 2 * np.multiply((iopt)**2, 1 / kgrid)  # adj cost given k

    y = (np.multiply(np.multiply((ld) ** al,
                                 kgrid ** ak), np.transpose([z_grid])))

    LD = np.multiply(ld, Gamma).sum()  # Aggregate labor Demand

    I = np.multiply(iopt, Gamma).sum()  # Aggregate Investment

    ADJ_cost = np.multiply(adj_cost, Gamma).sum()  # Aggregate Adj costs

    Y_agg = np.multiply(y, Gamma).sum()  # Aggregate Output

    C_agg = Y_agg - I - ADJ_cost  # Aggregate consumption

    LS = h * (1 / (wage * C_agg))

    Clearing_Dist = abs(LS - LD)

    print('LD-LS', Clearing_Dist)

    return Clearing_Dist
