import scipy.optimize as opt

from scipy.optimize import differential_evolution


def score_func(B):

    alpha, beta = B

    cf2007, cf2008, act2007, act2008 = payoff_mat(alpha, beta)

    '''
    score = 0

    for m in [[act2007, cf2007], [act2008, cf2008]]:
        n = len(m[0])
        for i in range(n):
            for j in range(n):
                if j > i:
                    if (m[0][i] + m[0][j] >= m[1][j, i] + m[1][i, (j - 1)]):
                        score = score + 1

    return score * -1
    '''

    score = [1 for m in [[act2007, cf2007], [act2008, cf2008]]
             for i in range(len(m[0]))
             for j in range(len(m[0]))
             if j > i if m[0][i] + m[0][j] >= m[1][j, i] + m[1][i, (j - 1)]]
    return sum(score) * -1


B = np.array((300, -2))

result_NM = opt.minimize(score_func, B, method='Nelder-Mead')

bounds = [(0, 400), (-5, 5)]

result_DE = differential_evolution(score_func, bounds)

print(result_NM)

print(result_DE)

end = time.time()

print(end - start)
