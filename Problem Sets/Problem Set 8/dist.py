def main(kgrid, sizez, sizek, pi, loc):
    '''
    This function takes k and z grids and transition matrix along with policy
    function from VFI to determine the stationary distribution for a given
    partial equilibrium

    '''

    import numpy as np

    # finding stationary distribution as in class Credit: J Debacker

    Gamma = np.ones((sizez, sizek)) * (1 / (sizek * sizez))
    Gamma = np.ones((sizez, sizek)) * (1 / (sizek * sizez))
    SDtol = 1e-12
    SDdist = 7
    SDiter = 0
    SDmaxiter = 1000
    while SDdist > SDtol and SDmaxiter > SDiter:
        HGamma = np.zeros((sizez, sizek))
        for i in range(sizez):  # z
            for j in range(sizek):  # k
                for m in range(sizez):  # z'
                    HGamma[m, loc[i, j]] = \
                        HGamma[m, loc[i, j]] + pi[i, m] * Gamma[i, j]
        SDdist = (np.absolute(HGamma - Gamma)).max()
        Gamma = HGamma
        SDiter += 1

    if SDiter < SDmaxiter:
        print('Stationary distribution converged after this many iterations: ',
              SDiter)
    else:
        print('Stationary distribution did not converge')

    return Gamma
