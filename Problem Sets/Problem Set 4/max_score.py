import scipy.optimize as opt

from scipy.optimize import differential_evolution


def score_func(B):
    #score = 0

    alpha, beta = B

    cf2007, cf2008, act2007, act2008 = payoff_mat(alpha, beta)

    '''for m in [[act2007, cf2007], [act2008, cf2008]]:
        n = len(m[0])
        for i in range(n):
            for j in range(n):
                if j > i:
                    if (m[0][i] + m[0][j] >= m[1][j, i] + m[1][i, (j - 1)]):
                        score = score + 1'''

    score = [1 for m in [[act2007, cf2007], [act2008, cf2008]]
             for i in range(len(m[0]))
             for j in range(len(m[0]))
             if j > i if m[0][i] + m[0][j] >= m[1][j, i] + m[1][i, (j - 1)]]
    return sum(score) * -1


# score = score_func()
'''
B = np.array((.5, .5))

coefs = opt.minimize(score_func, B, method='Nelder-Mead',
                     tol=1e-10, options={'maxiter': 5000})

coefs = opt.minimize.differential_evolution()
'''

bounds = [(-100000, 100000), (-100000, 100000)]

result = differential_evolution(score_func, bounds)

print(result)

end = time.time()

print(end - start)
