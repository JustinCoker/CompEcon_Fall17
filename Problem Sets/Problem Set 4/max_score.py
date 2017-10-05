import numpy as np

i1 = np.array([i for i in range(len(actual_2007)) for j in range(len(actual_2007)-1)])

i2 = np.array([j for i in range(len(actual_2007))
                 for j in range(len(actual_2007)-1)])


arrays = [i1, i2]
