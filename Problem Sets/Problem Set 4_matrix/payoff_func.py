import numpy as np


def payoff_func(df, index, alpha, beta):
        x1, x2, y1, D = ['num_stations_buyer', 'corp_owner_buyer',
                         'population_target', 'distance']

        i = index
        payoff = (df[x1].iloc[i] * df[y1].iloc[i] +
                  alpha * df[x2].iloc[i] *
                  df[y1].iloc[i] + beta * df[D].iloc[i])

        return payoff


def payoff_mat(alpha, beta):
    n = len(actual_2007)
    cf2007 = np.matrix([payoff_func(counter_fact, i, alpha, beta)
                        for i in range(n * (n - 1))])

    cf2007.resize(n, (n - 1))

    m = len(actual_2008)
    cf2008 = np.matrix([payoff_func(counter_fact, i, alpha, beta)
                       for i in range(n * (n - 1), len(counter_fact))])

    cf2008.resize(m, (m - 1))

    act2007 = [payoff_func(actual_2007, i, alpha, beta)
               for i in range(n)]

    act2008 = [payoff_func(actual_2008, i, alpha, beta)
               for i in range(m)]

    return cf2007, cf2008, act2007, act2008
