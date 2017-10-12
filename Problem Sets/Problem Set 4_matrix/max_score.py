import scipy.optimize as opt

from scipy.optimize import differential_evolution


def score_func(B, transfers):
    '''
    This function defines the maximum score of the model specification

    input:
        B: coefficients of the model to be estimated, these will ultimately be
           passed to payoff_mat() and subsequently payoff_func() for
           caclulation of the payoff matrices.

        transfers: "T" or "F" depending on the specification
    '''

    
    if transfers == "F":
        alpha, beta = B

        cf2007, cf2008, act2007, act2008 = payoff_mat(transfers, alpha, beta)

        score = [1 for m in [[act2007, cf2007], [act2008, cf2008]]
                 for i in range(len(m[0]))
                 for j in range(len(m[0]))
                 if j > i if m[0][i] + m[0][j] >=
                 m[1][j, i] + m[1][i, (j - 1)]]

    if transfers == "T":
        delta, alpha, gamma, beta = B

        cf2007, cf2008, act2007, act2008 = payoff_mat(transfers, delta,
                                                      alpha, gamma, beta)

        price_2007 = actual_2007['price'].tolist()

        price_2008 = actual_2008['price'].tolist()

        score = [1 for m in [[act2007, cf2007, price_2007],
                             [act2008, cf2008, price_2008]]
                 for i in range(len(m[0]))
                 for j in range(len(m[0]))
                 if j > i if (m[0][i] - m[1][j, i] >= m[2][i] - m[2][j]) &
                 (m[0][j] - m[1][i, (j - 1)] >= m[2][j] - m[2][i])]

    return sum(score) * -1
