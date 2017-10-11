import scipy.optimize as opt

from scipy.optimize import differential_evolution

counter_fact_2007 = (
    counter_fact[counter_fact['year'] == 2007].reset_index(drop=True))

counter_fact_2008 = (
    counter_fact[counter_fact['year'] == 2008].reset_index(drop=True))


def score_func(B):
    alpha, beta = B

    dfs = [actual_2007, counter_fact_2007, actual_2008, counter_fact_2008]

    for el in dfs:
        payoff_func(el, alpha, beta)

    '''score = [1 for m in [dfs[0:2], dfs[2:]]
             for i in range(len(m[0]))
             for j in range(len(m[0]))
             if j > i if m[0]['payoff'].iloc[i] + m[0]['payoff'].iloc[j] >=
             int(m[1]['payoff'].iloc[
                 m[1].loc[(m[1]['buyer_id'] == j + 1) &
                          (m[1]['target_id'] == i + 1)].index].values) +
             int(m[1]['payoff'].iloc[
                 m[1].loc[(m[1]['buyer_id'] == i + 1) &
                          (m[1]['target_id'] == j + 1)].index].values)]'''
    score = 0
    for m in [dfs[0:2], dfs[2:]]:
        for i in range(len(m[0])):
            for j in range(len(m[0])):
                if j > i:
                    if (m[0]['payoff'].iloc[i] + m[0]['payoff'].iloc[j] >=
                    int(m[1]['payoff'].iloc[
                        m[1].loc[(m[1]['buyer_id'] == j + 1) &
                                 (m[1]['target_id'] == i + 1)].index].values) +
                    int(m[1]['payoff'].iloc[
                        m[1].loc[(m[1]['buyer_id'] == i + 1) &
                                 (m[1]['target_id'] == j + 1)].index].values)):
                        score = score + 1

    return score * -1


bounds = [(-500, 500), (-100, 100)]

result = differential_evolution(score_func, bounds)

'''
B = (100, -100)

result = opt.minimize(score_func, B, method='Nelder-Mead')
'''

print(result)

end = time.time()

print(end - start)
