
# Part 1: No Transfers
'''transfers = "F"

B = np.array((300, -2))

result_NM_NT = opt.minimize(score_func, B,
                            args=(transfers), method='Nelder-Mead')

bounds = [(0, 400), (-5, 5)]

result_DE_NT = differential_evolution(score_func, bounds, args=(transfers))

print(result_NM_NT)

print(result_DE_NT)
'''
# Part 2 : Transfers
transfers = "T"

bounds = [(-400, 0), (-10, 10), (-500, -100), (-10000, -500)]

result_DE_T = differential_evolution(score_func, bounds, args=(transfers))

print(result_DE_T)

end = time.time()

print(end - start)
