'''
This script calls the optimization routines in order to estimate the desired
coefficients.

In Part 1, we have no transfers so transfers = "F". In Part 2, we add transfers
in order to indentify target specific characteristics, so transfers = "T"
'''


# Part 1: No Transfers
transfers = "F"

B = np.array((300, -2))  # initial guess for Nelder-Mead

# Nelder-Mead method

result_NM_NT = opt.minimize(score_func, B,
                            args=(transfers), method='Nelder-Mead')


bounds = [(0, 400), (-5, 5)]  #Bounds for differential_evolution

# differential_evolution method

result_DE_NT = differential_evolution(score_func, bounds, args=(transfers))

print(result_NM_NT)

print(result_DE_NT)

# Part 2 : Transfers
transfers = "T"  # So that our function use correct specification

# bounds for the differential_evolution method

bounds = [(-1000, 1000), (0, 1000), (-1000, 0), (-1000, 0)]

#differential_evolution method

result_DE_T = differential_evolution(score_func, bounds, args=(transfers))

print(result_DE_T)

end = time.time()

print(end - start)
