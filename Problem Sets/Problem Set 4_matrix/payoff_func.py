'''
This script defines the payoff functions and matrices
'''

import numpy as np


def payoff_func(df, index, transfers, *args):
    '''
    This function calculates the integer value of the payoff function given
    the specification.

    input:
        df: a dataframe containing data relevant to our payoff function

        index: The row value of df that we wish to apply our payoff function to

        transfer: T or F depending on the form of our payoff function

        args: parameters of the model to be estimates

    output:
        payoff: integer value of the payoff function appied to a row of df.

    '''
    if transfers == "F":

            alpha, beta = args[0]

            x1, x2, y1, D = ['num_stations_buyer', 'corp_owner_buyer',
                             'population_target', 'distance']

            i = index
            payoff = (df[x1].iloc[i] * df[y1].iloc[i] +
                      alpha * df[x2].iloc[i] *
                      df[y1].iloc[i] + beta * df[D].iloc[i])

    if transfers == "T":
            delta, alpha, gamma, beta = args[0]

            x1, x2, y1, H, D = ['num_stations_buyer', 'corp_owner_buyer',
                                'population_target', 'hhi_target', 'distance']

            i = index

            payoff = (delta * df[x1].iloc[i] * df[y1].iloc[i] +
                      alpha * df[x2].iloc[i] * df[y1].iloc[i] +
                      gamma * df[H].iloc[i] + beta * df[D].iloc[i])

    return payoff


def payoff_mat(transfers, *args):
    '''
    This function creates the payoff matrices defined in the write up. The
    elements of this matrix are payoff values of the respective buyer, target
    matches.

    input:
        transfers: "T" or "F" depending on the specification

        args: coefficients of the model to be estimated. These are ultimately
              passed to payoff_func() to calculate payoff values

    '''
    n = len(actual_2007)
    cf2007 = np.matrix([payoff_func(counter_fact, i, transfers, args)
                        for i in range(n * (n - 1))])

    cf2007.resize(n, (n - 1))

    m = len(actual_2008)
    cf2008 = np.matrix([payoff_func(counter_fact, i, transfers, args)
                        for i in range(n * (n - 1), len(counter_fact))])

    cf2008.resize(m, (m - 1))

    act2007 = [payoff_func(actual_2007, i, transfers, args)
               for i in range(n)]

    act2008 = [payoff_func(actual_2008, i, transfers, args)
               for i in range(m)]

    return cf2007, cf2008, act2007, act2008
